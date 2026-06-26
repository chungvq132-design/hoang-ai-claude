import Link from 'next/link'

export default function StoreLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-3 flex items-center justify-between">
          <Link href="/store" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-green-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">+</span>
            </div>
            <span className="font-semibold text-slate-800">Nhà Thuốc Online</span>
          </Link>
          <div className="flex items-center gap-4">
            <Link href="/store/cart" className="text-slate-600 hover:text-slate-900 text-sm flex items-center gap-1">
              🛒 Giỏ hàng
            </Link>
            <Link href="/store/orders" className="text-slate-600 hover:text-slate-900 text-sm">
              Đơn hàng
            </Link>
          </div>
        </div>
      </header>
      <main>{children}</main>
      <footer className="bg-white border-t border-slate-200 mt-12 py-6">
        <div className="max-w-4xl mx-auto px-4 text-center text-sm text-slate-500">
          <p>Nhà Thuốc — Chuyên cung cấp thuốc và sản phẩm sức khỏe chất lượng</p>
          <p className="mt-1">Hotline: 0xxx xxx xxx · Giờ mở cửa: 7:00 - 22:00</p>
        </div>
      </footer>
    </div>
  )
}
