import { db } from '@/db'
import { orders, orderItems, products } from '@/db/schema'
import { eq, desc } from 'drizzle-orm'
import { formatVND } from '@/lib/currency'
import Link from 'next/link'

async function getOrders() {
  return db.select().from(orders).orderBy(desc(orders.createdAt)).limit(50)
}

const statusLabel: Record<string, { label: string; color: string }> = {
  PENDING: { label: 'Chờ xác nhận', color: 'bg-yellow-100 text-yellow-700' },
  CONFIRMED: { label: 'Đã xác nhận', color: 'bg-blue-100 text-blue-700' },
  PREPARING: { label: 'Đang chuẩn bị', color: 'bg-purple-100 text-purple-700' },
  READY: { label: 'Sẵn sàng', color: 'bg-green-100 text-green-700' },
  DELIVERED: { label: 'Đã giao', color: 'bg-slate-100 text-slate-600' },
  CANCELLED: { label: 'Đã hủy', color: 'bg-red-100 text-red-600' },
}

export default async function OrdersPage() {
  const orderList = await getOrders()

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-900">Đơn hàng online</h1>
        <p className="text-sm text-slate-500 mt-0.5">{orderList.length} đơn gần nhất</p>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Mã đơn</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Khách hàng</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Hình thức</th>
              <th className="text-right px-4 py-3 font-medium text-slate-600">Tổng tiền</th>
              <th className="text-center px-4 py-3 font-medium text-slate-600">Trạng thái</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Thời gian</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {orderList.map((o) => {
              const s = statusLabel[o.status] ?? { label: o.status, color: 'bg-slate-100 text-slate-600' }
              return (
                <tr key={o.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-mono text-xs text-slate-600">#{o.id}</td>
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-800">{o.guestName ?? 'Khách'}</div>
                    <div className="text-xs text-slate-400">{o.guestPhone}</div>
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    {o.fulfillment === 'PICKUP' ? '🏪 Lấy tại quầy' : '🚚 Giao hàng'}
                  </td>
                  <td className="px-4 py-3 text-right font-medium text-slate-800">
                    {formatVND(o.total)}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${s.color}`}>{s.label}</span>
                  </td>
                  <td className="px-4 py-3 text-xs text-slate-500">
                    {new Date(o.createdAt).toLocaleString('vi-VN')}
                  </td>
                  <td className="px-4 py-3">
                    <Link href={`/orders/${o.id}`} className="text-xs text-green-600 hover:underline">
                      Chi tiết
                    </Link>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {orderList.length === 0 && (
          <div className="text-center py-12 text-slate-400">
            <p className="text-3xl mb-2">🚚</p>
            <p className="text-sm">Chưa có đơn hàng online nào</p>
          </div>
        )}
      </div>
    </div>
  )
}
