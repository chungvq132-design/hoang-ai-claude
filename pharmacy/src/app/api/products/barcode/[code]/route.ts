import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/db'
import { products, batches } from '@/db/schema'
import { eq, sql } from 'drizzle-orm'

export async function GET(
  _req: NextRequest,
  { params }: { params: Promise<{ code: string }> }
) {
  const { code } = await params

  const [product] = await db
    .select({
      id: products.id,
      name: products.name,
      barcode: products.barcode,
      unit: products.unit,
      retailPrice: products.retailPrice,
      vatRate: products.vatRate,
      requiresPrescription: products.requiresPrescription,
      stock: sql<number>`coalesce(sum(${batches.quantityRemaining}), 0)`,
    })
    .from(products)
    .leftJoin(batches, eq(batches.productId, products.id))
    .where(eq(products.barcode, code))
    .groupBy(products.id)
    .limit(1)

  if (!product) return NextResponse.json({ error: 'Not found' }, { status: 404 })
  return NextResponse.json(product)
}
