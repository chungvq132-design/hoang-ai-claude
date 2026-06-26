'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { signOut } from 'next-auth/react'

const navItems = [
  { href: '/dashboard', label: 'Tổng quan', icon: '📊' },
  { href: '/pos', label: 'Bán hàng (POS)', icon: '🛒' },
  { href: '/inventory', label: 'Kho thuốc', icon: '📦' },
  { href: '/prescriptions', label: 'Toa thuốc', icon: '📋' },
  { href: '/customers', label: 'Khách hàng', icon: '👤' },
  { href: '/orders', label: 'Đơn online', icon: '🚚' },
]

export default function Sidebar() {
  const pathname = usePathname()

  return (
    <aside className="w-56 bg-white border-r border-slate-200 flex flex-col min-h-screen">
      <div className="p-4 border-b border-slate-100">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">+</span>
          </div>
          <span className="font-semibold text-slate-800 text-sm">Nhà Thuốc</span>
        </div>
      </div>

      <nav className="flex-1 p-3 space-y-0.5">
        {navItems.map((item) => {
          const active = pathname === item.href || pathname.startsWith(item.href + '/')
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm transition-colors ${
                active
                  ? 'bg-green-50 text-green-700 font-medium'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
              }`}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          )
        })}
      </nav>

      <div className="p-3 border-t border-slate-100">
        <Link
          href="/store"
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-50 mb-1"
        >
          <span className="text-base">🏪</span>
          Xem cửa hàng
        </Link>
        <button
          onClick={() => signOut({ callbackUrl: '/login' })}
          className="flex items-center gap-2.5 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-red-50 hover:text-red-600 w-full transition-colors"
        >
          <span className="text-base">🚪</span>
          Đăng xuất
        </button>
      </div>
    </aside>
  )
}
