'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { formatVND } from '@/lib/currency'

type Product = {
  id: number
  name: string
  barcode: string | null
  unit: string
  retailPrice: number
  vatRate: number
  requiresPrescription: boolean
  stock: number
}

type CartItem = {
  product: Product
  quantity: number
  unitPrice: number
}

export default function POSPage() {
  const [search, setSearch] = useState('')
  const [searchResults, setSearchResults] = useState<Product[]>([])
  const [cart, setCart] = useState<CartItem[]>([])
  const [paymentMethod, setPaymentMethod] = useState<'CASH' | 'BANK_TRANSFER' | 'MOMO' | 'ZALOPAY'>('CASH')
  const [amountTendered, setAmountTendered] = useState('')
  const [loading, setLoading] = useState(false)
  const [successMessage, setSuccessMessage] = useState('')
  const searchRef = useRef<HTMLInputElement>(null)
  const barcodeBuffer = useRef('')
  const barcodeTimer = useRef<ReturnType<typeof setTimeout> | null>(null)

  // USB barcode scanner: rapid keystrokes ending in Enter
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (document.activeElement === searchRef.current) return

      if (e.key === 'Enter' && barcodeBuffer.current.length > 4) {
        const barcode = barcodeBuffer.current
        barcodeBuffer.current = ''
        lookupBarcode(barcode)
      } else if (e.key.length === 1) {
        barcodeBuffer.current += e.key
        if (barcodeTimer.current) clearTimeout(barcodeTimer.current)
        barcodeTimer.current = setTimeout(() => {
          barcodeBuffer.current = ''
        }, 150)
      }
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [])

  async function lookupBarcode(barcode: string) {
    const res = await fetch(`/api/products/barcode/${barcode}`)
    if (res.ok) {
      const product = await res.json()
      addToCart(product)
    }
  }

  useEffect(() => {
    const timer = setTimeout(async () => {
      if (search.trim().length < 2) { setSearchResults([]); return }
      const res = await fetch(`/api/products?q=${encodeURIComponent(search)}&limit=8`)
      if (res.ok) setSearchResults(await res.json())
    }, 200)
    return () => clearTimeout(timer)
  }, [search])

  function addToCart(product: Product) {
    setCart((prev) => {
      const existing = prev.find((i) => i.product.id === product.id)
      if (existing) {
        return prev.map((i) =>
          i.product.id === product.id ? { ...i, quantity: i.quantity + 1 } : i
        )
      }
      return [...prev, { product, quantity: 1, unitPrice: product.retailPrice }]
    })
    setSearch('')
    setSearchResults([])
  }

  function updateQty(productId: number, qty: number) {
    if (qty <= 0) {
      setCart((prev) => prev.filter((i) => i.product.id !== productId))
    } else {
      setCart((prev) => prev.map((i) => (i.product.id === productId ? { ...i, quantity: qty } : i)))
    }
  }

  const subtotal = cart.reduce((sum, i) => sum + i.quantity * i.unitPrice, 0)
  const vatAmount = Math.round(
    cart.reduce((sum, i) => sum + i.quantity * i.unitPrice * (i.product.vatRate / 100), 0)
  )
  const total = subtotal + vatAmount
  const tendered = parseInt(amountTendered.replace(/\D/g, '')) || 0
  const change = Math.max(0, tendered - total)

  async function handleCheckout() {
    if (cart.length === 0) return
    setLoading(true)

    const res = await fetch('/api/pos/sales', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: cart.map((i) => ({ productId: i.product.id, quantity: i.quantity, unitPrice: i.unitPrice })),
        subtotal,
        vatAmount,
        total,
        paymentMethod,
        amountTendered: paymentMethod === 'CASH' ? tendered : total,
        change: paymentMethod === 'CASH' ? change : 0,
      }),
    })

    if (res.ok) {
      const sale = await res.json()
      setCart([])
      setAmountTendered('')
      setSuccessMessage(`✅ Hóa đơn ${sale.invoiceNumber} — ${formatVND(total)}`)
      setTimeout(() => setSuccessMessage(''), 4000)
    }
    setLoading(false)
  }

  return (
    <div className="flex h-screen overflow-hidden">
      {/* Left: Product Search */}
      <div className="flex-1 flex flex-col border-r border-slate-200 bg-white">
        <div className="p-4 border-b border-slate-200">
          <h2 className="font-semibold text-slate-800 mb-3">Bán hàng tại quầy</h2>
          <input
            ref={searchRef}
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="🔍 Tìm tên sản phẩm... (hoặc dùng máy scan barcode)"
            className="w-full border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
          />
        </div>

        {successMessage && (
          <div className="mx-4 mt-3 p-3 bg-green-50 border border-green-200 rounded-lg text-sm text-green-700">
            {successMessage}
          </div>
        )}

        <div className="flex-1 overflow-y-auto p-4">
          {searchResults.length > 0 ? (
            <div className="space-y-1">
              {searchResults.map((p) => (
                <button
                  key={p.id}
                  onClick={() => addToCart(p)}
                  className="w-full flex items-center justify-between p-3 rounded-lg border border-slate-100 hover:border-green-200 hover:bg-green-50 text-left transition-colors"
                >
                  <div>
                    <div className="font-medium text-slate-800 text-sm">{p.name}</div>
                    <div className="text-xs text-slate-400">{p.unit} · Tồn: {p.stock}</div>
                    {p.requiresPrescription && (
                      <span className="text-xs bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded">Kê đơn</span>
                    )}
                  </div>
                  <div className="text-right ml-4">
                    <div className="font-semibold text-green-700 text-sm">{formatVND(p.retailPrice)}</div>
                    <div className="text-xs text-slate-400">/{p.unit}</div>
                  </div>
                </button>
              ))}
            </div>
          ) : (
            <div className="text-center text-slate-400 mt-12">
              <p className="text-4xl mb-3">🛒</p>
              <p className="text-sm">Gõ tên thuốc hoặc scan barcode để thêm vào giỏ</p>
            </div>
          )}
        </div>
      </div>

      {/* Right: Cart */}
      <div className="w-80 flex flex-col bg-slate-50">
        <div className="p-4 border-b border-slate-200 bg-white">
          <h2 className="font-semibold text-slate-800">Giỏ hàng</h2>
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {cart.length === 0 ? (
            <div className="text-center text-slate-400 mt-8 text-sm">Chưa có sản phẩm</div>
          ) : (
            cart.map((item) => (
              <div key={item.product.id} className="bg-white rounded-lg p-3 border border-slate-200">
                <div className="font-medium text-sm text-slate-800 mb-1 leading-tight">{item.product.name}</div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => updateQty(item.product.id, item.quantity - 1)}
                      className="w-6 h-6 rounded border border-slate-200 text-slate-600 hover:bg-slate-100 text-xs"
                    >
                      −
                    </button>
                    <span className="w-8 text-center text-sm font-medium">{item.quantity}</span>
                    <button
                      onClick={() => updateQty(item.product.id, item.quantity + 1)}
                      className="w-6 h-6 rounded border border-slate-200 text-slate-600 hover:bg-slate-100 text-xs"
                    >
                      +
                    </button>
                  </div>
                  <div className="text-sm font-semibold text-slate-800">
                    {formatVND(item.quantity * item.unitPrice)}
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        <div className="p-4 bg-white border-t border-slate-200 space-y-3">
          <div className="space-y-1 text-sm">
            <div className="flex justify-between text-slate-600">
              <span>Tạm tính</span>
              <span>{formatVND(subtotal)}</span>
            </div>
            <div className="flex justify-between text-slate-600">
              <span>VAT (8%)</span>
              <span>{formatVND(vatAmount)}</span>
            </div>
            <div className="flex justify-between font-semibold text-slate-900 text-base border-t border-slate-100 pt-1">
              <span>Tổng cộng</span>
              <span className="text-green-700">{formatVND(total)}</span>
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-600 mb-1">Thanh toán</label>
            <div className="grid grid-cols-2 gap-1">
              {(['CASH', 'BANK_TRANSFER', 'MOMO', 'ZALOPAY'] as const).map((m) => (
                <button
                  key={m}
                  onClick={() => setPaymentMethod(m)}
                  className={`text-xs py-1.5 px-2 rounded-lg border transition-colors ${
                    paymentMethod === m
                      ? 'bg-green-600 text-white border-green-600'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  {{ CASH: 'Tiền mặt', BANK_TRANSFER: 'Chuyển khoản', MOMO: 'MoMo', ZALOPAY: 'ZaloPay' }[m]}
                </button>
              ))}
            </div>
          </div>

          {paymentMethod === 'CASH' && (
            <div>
              <label className="block text-xs font-medium text-slate-600 mb-1">Tiền khách đưa</label>
              <input
                type="number"
                value={amountTendered}
                onChange={(e) => setAmountTendered(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                placeholder="0"
              />
              {tendered > 0 && (
                <p className="text-xs text-green-700 mt-1">
                  Tiền thối: <strong>{formatVND(change)}</strong>
                </p>
              )}
            </div>
          )}

          <button
            onClick={handleCheckout}
            disabled={cart.length === 0 || loading}
            className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-xl transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {loading ? 'Đang xử lý...' : `Thanh toán ${cart.length > 0 ? formatVND(total) : ''}`}
          </button>
        </div>
      </div>
    </div>
  )
}
