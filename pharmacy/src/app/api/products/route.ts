import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/db'
import { products, batches, categories } from '@/db/schema'
import { eq, ilike, or, sql } from 'drizzle-orm'

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url)
  const q = searchParams.get('q') || ''
  const limit = parseInt(searchParams.get('limit') || '20')
  const onlineOnly = searchParams.get('online') === '1'

  const rows = await db
    .select({
      id: products.id,
      name: products.name,
      barcode: products.barcode,
      unit: products.unit,
      retailPrice: products.retailPrice,
      vatRate: products.vatRate,
      requiresPrescription: products.requiresPrescription,
      availableOnline: products.availableOnline,
      imageUrl: products.imageUrl,
      description: products.description,
      reorderPoint: products.reorderPoint,
      stock: sql<number>`coalesce(sum(${batches.quantityRemaining}), 0)`,
    })
    .from(products)
    .leftJoin(batches, eq(batches.productId, products.id))
    .where(
      q
        ? or(ilike(products.name, `%${q}%`), ilike(products.barcode, `%${q}%`))
        : onlineOnly
        ? eq(products.availableOnline, true)
        : eq(products.active, true)
    )
    .groupBy(products.id)
    .orderBy(products.name)
    .limit(limit)

  return NextResponse.json(rows)
}

export async function POST(req: NextRequest) {
  const body = await req.json()

  const slug = body.name
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, '')
    .replace(/\s+/g, '-')
    + '-' + Date.now()

  const [product] = await db
    .insert(products)
    .values({
      name: body.name,
      slug,
      barcode: body.barcode || null,
      registrationNumber: body.registrationNumber || null,
      unit: body.unit,
      retailPrice: Number(body.retailPrice),
      vatRate: Number(body.vatRate ?? 8),
      requiresPrescription: Boolean(body.requiresPrescription),
      availableOnline: body.availableOnline !== false,
      reorderPoint: Number(body.reorderPoint ?? 10),
      description: body.description || null,
    })
    .returning()

  return NextResponse.json(product, { status: 201 })
}
