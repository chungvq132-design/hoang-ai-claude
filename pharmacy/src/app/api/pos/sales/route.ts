import { NextRequest, NextResponse } from 'next/server'
import { getServerSession } from 'next-auth'
import { authOptions } from '@/lib/auth'
import { db } from '@/db'
import { sales, saleItems, batches } from '@/db/schema'
import { eq, asc, desc } from 'drizzle-orm'

export async function POST(req: NextRequest) {
  const session = await getServerSession(authOptions)
  if (!session?.user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const body = await req.json()
  const { items, subtotal, vatAmount, total, paymentMethod, amountTendered, change } = body

  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '')
  const count = await db.$count(sales)
  const invoiceNumber = `PH-${today}-${String(count + 1).padStart(4, '0')}`

  const sale = await db.transaction(async (tx) => {
    const [newSale] = await tx
      .insert(sales)
      .values({
        invoiceNumber,
        userId: (session.user as { id: string }).id,
        subtotal: Number(subtotal),
        vatAmount: Number(vatAmount),
        total: Number(total),
        paymentMethod: paymentMethod ?? 'CASH',
        amountTendered: Number(amountTendered ?? total),
        change: Number(change ?? 0),
      })
      .returning()

    for (const item of items as { productId: number; quantity: number; unitPrice: number; vatRate?: number }[]) {
      // FEFO: pick oldest non-expired batch first
      const [batch] = await tx
        .select()
        .from(batches)
        .where(eq(batches.productId, item.productId))
        .orderBy(asc(batches.expiryDate))
        .limit(1)

      await tx.insert(saleItems).values({
        saleId: newSale.id,
        productId: item.productId,
        batchId: batch?.id ?? null,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        vatRate: item.vatRate ?? 8,
      })

      if (batch) {
        await tx
          .update(batches)
          .set({ quantityRemaining: Math.max(0, batch.quantityRemaining - item.quantity) })
          .where(eq(batches.id, batch.id))
      }
    }

    return newSale
  })

  return NextResponse.json(sale, { status: 201 })
}

export async function GET() {
  const session = await getServerSession(authOptions)
  if (!session?.user) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })

  const recentSales = await db.select().from(sales).orderBy(desc(sales.createdAt)).limit(50)
  return NextResponse.json(recentSales)
}
