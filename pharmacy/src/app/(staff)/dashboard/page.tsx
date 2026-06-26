import { db } from '@/db'
import { sales, orders, batches, inventoryAlerts } from '@/db/schema'
import { and, eq, gte, sql, lt, ne } from 'drizzle-orm'
import { formatVND } from '@/lib/currency'

async function getDashboardStats() {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const [todaySales] = await db
    .select({ total: sql<number>`coalesce(sum(${sales.total}), 0)`, count: sql<number>`count(*)` })
    .from(sales)
    .where(gte(sales.createdAt, today))

  const [pendingOrders] = await db
    .select({ count: sql<number>`count(*)` })
    .from(orders)
    .where(eq(orders.status, 'PENDING'))

  const [activeAlerts] = await db
    .select({ count: sql<number>`count(*)` })
    .from(inventoryAlerts)
    .where(sql`${inventoryAlerts.resolvedAt} is null`)

  return {
    todayRevenue: Number(todaySales?.total ?? 0),
    todaySalesCount: Number(todaySales?.count ?? 0),
    pendingOrdersCount: Number(pendingOrders?.count ?? 0),
    activeAlertsCount: Number(activeAlerts?.count ?? 0),
  }
}

export default async function DashboardPage() {
  const stats = await getDashboardStats()

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-xl font-semibold text-slate-900">Tổng quan hôm nay</h1>
        <p className="text-sm text-slate-500 mt-0.5">
          {new Date().toLocaleDateString('vi-VN', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
      </div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          label="Doanh thu hôm nay"
          value={formatVND(stats.todayRevenue)}
          sub={`${stats.todaySalesCount} giao dịch`}
          color="green"
          icon="💰"
        />
        <StatCard
          label="Đơn online chờ"
          value={stats.pendingOrdersCount.toString()}
          sub="Cần xác nhận"
          color={stats.pendingOrdersCount > 0 ? 'orange' : 'slate'}
          icon="🚚"
          href="/orders"
        />
        <StatCard
          label="Cảnh báo kho"
          value={stats.activeAlertsCount.toString()}
          sub="Hết hàng / Hết hạn"
          color={stats.activeAlertsCount > 0 ? 'red' : 'slate'}
          icon="⚠️"
          href="/inventory"
        />
        <StatCard
          label="Bán hàng nhanh"
          value="POS →"
          sub="Mở quầy bán"
          color="blue"
          icon="🛒"
          href="/pos"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <QuickActions />
      </div>
    </div>
  )
}

function StatCard({
  label, value, sub, color, icon, href,
}: {
  label: string
  value: string
  sub: string
  color: 'green' | 'orange' | 'red' | 'blue' | 'slate'
  icon: string
  href?: string
}) {
  const colorMap = {
    green: 'bg-green-50 border-green-100',
    orange: 'bg-orange-50 border-orange-100',
    red: 'bg-red-50 border-red-100',
    blue: 'bg-blue-50 border-blue-100',
    slate: 'bg-white border-slate-200',
  }
  const valueColorMap = {
    green: 'text-green-700',
    orange: 'text-orange-700',
    red: 'text-red-700',
    blue: 'text-blue-700',
    slate: 'text-slate-700',
  }

  const content = (
    <div className={`p-4 rounded-xl border ${colorMap[color]} ${href ? 'hover:shadow-sm transition-shadow cursor-pointer' : ''}`}>
      <div className="flex items-start justify-between mb-2">
        <span className="text-lg">{icon}</span>
      </div>
      <div className={`text-xl font-semibold ${valueColorMap[color]}`}>{value}</div>
      <div className="text-xs text-slate-500 mt-0.5">{label}</div>
      <div className="text-xs text-slate-400 mt-0.5">{sub}</div>
    </div>
  )

  if (href) {
    return <a href={href}>{content}</a>
  }
  return content
}

function QuickActions() {
  const actions = [
    { href: '/pos', label: 'Bán hàng tại quầy', desc: 'Mở giao diện POS', icon: '🛒' },
    { href: '/inventory/products/new', label: 'Thêm sản phẩm', desc: 'Nhập sản phẩm mới vào kho', icon: '📦' },
    { href: '/prescriptions/new', label: 'Nhập toa thuốc', desc: 'Tạo toa thuốc mới', icon: '📋' },
    { href: '/orders', label: 'Xử lý đơn online', desc: 'Xem đơn hàng chờ xác nhận', icon: '🚚' },
    { href: '/store', label: 'Xem cửa hàng online', desc: 'Giao diện khách hàng', icon: '🏪' },
    { href: '/inventory', label: 'Kiểm tra tồn kho', desc: 'Xem hàng sắp hết hoặc hết hạn', icon: '⚠️' },
  ]

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-4 col-span-full">
      <h2 className="text-sm font-semibold text-slate-700 mb-3">Thao tác nhanh</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
        {actions.map((a) => (
          <a
            key={a.href}
            href={a.href}
            className="flex items-center gap-2.5 p-3 rounded-lg border border-slate-100 hover:bg-slate-50 hover:border-slate-200 transition-colors"
          >
            <span className="text-xl">{a.icon}</span>
            <div>
              <div className="text-sm font-medium text-slate-800">{a.label}</div>
              <div className="text-xs text-slate-400">{a.desc}</div>
            </div>
          </a>
        ))}
      </div>
    </div>
  )
}
