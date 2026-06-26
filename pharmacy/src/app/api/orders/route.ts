import { NextRequest, NextResponse } from 'next/server'
import { db } from '@/db'
import { orders, orderItems } from '@/db/schema'
import { desc } from 'drizzle-orm'

export async function GET() {
  const orderList = await db.select().from(orders).orderBy(desc(orders.createdAt)).limit(50)
  return NextResponse.json(orderList)
}

export async function POST(req: NextRequest) {
  const body = await req.json()
  const { items, guestName, guestPhone, fulfillment, deliveryAddress, paymentMethod, notes } = body

  const subtotal = items.reduce(
    (sum: number, item: { unitPrice: number; quantity: number }) => sum + item.unitPrice * item.quantity,
    0
  )
  const vatAmount = Math.round(subtotal * 0.08)
  const total = subtotal + vatAmount

  const order = await db.transaction(async (tx) => {
    const [newOrder] = await tx
      .insert(orders)
      .values({
        guestName,
        guestPhone,
        fulfillment: fulfillment ?? 'PICKUP',
        deliveryAddress: deliveryAddress ?? null,
        subtotal,
        vatAmount,
        total,
        paymentMethod: paymentMethod ?? 'CASH',
        notes: notes ?? null,
      })
      .returning()

    await tx.insert(orderItems).values(
      items.map((item: { productId: number; quantity: number; unitPrice: number }) => ({
        orderId: newOrder.id,
        productId: item.productId,
        quantity: item.quantity,
        unitPrice: item.unitPrice,
        vatRate: 8,
      }))
    )

    return newOrder
  })

  return NextResponse.json(order, { status: 201 })
}
