'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function NewProductPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault()
    setLoading(true)
    setError('')

    const form = new FormData(e.currentTarget)
    const data = {
      name: form.get('name'),
      barcode: form.get('barcode') || null,
      registrationNumber: form.get('registrationNumber') || null,
      unit: form.get('unit'),
      retailPrice: parseInt(form.get('retailPrice') as string),
      vatRate: parseInt(form.get('vatRate') as string),
      requiresPrescription: form.get('requiresPrescription') === 'on',
      availableOnline: form.get('availableOnline') === 'on',
      reorderPoint: parseInt(form.get('reorderPoint') as string) || 10,
      description: form.get('description') || null,
    }

    const res = await fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })

    if (res.ok) {
      router.push('/inventory')
    } else {
      const err = await res.json()
      setError(err.error || 'Lỗi khi tạo sản phẩm')
      setLoading(false)
    }
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <div className="mb-6">
        <a href="/inventory" className="text-sm text-slate-500 hover:text-slate-700">← Kho thuốc</a>
        <h1 className="text-xl font-semibold text-slate-900 mt-1">Thêm sản phẩm mới</h1>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-slate-200 p-6 space-y-4">
        <div className="grid grid-cols-1 gap-4">
          <FormField label="Tên sản phẩm *" name="name" required placeholder="Paracetamol 500mg" />
          <div className="grid grid-cols-2 gap-4">
            <FormField label="Barcode (EAN-13)" name="barcode" placeholder="8934868012345" />
            <FormField label="Số đăng ký (SĐK)" name="registrationNumber" placeholder="VD-12345-12" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Đơn vị tính *</label>
              <select name="unit" required className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                <option value="viên">viên</option>
                <option value="hộp">hộp</option>
                <option value="lọ">lọ</option>
                <option value="chai">chai</option>
                <option value="gói">gói</option>
                <option value="ống">ống</option>
                <option value="tuýp">tuýp</option>
              </select>
            </div>
            <FormField label="Giá bán (VND) *" name="retailPrice" type="number" required placeholder="15000" />
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Thuế VAT</label>
              <select name="vatRate" className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500">
                <option value="8">8% (thông thường)</option>
                <option value="0">0% (miễn thuế)</option>
              </select>
            </div>
            <FormField label="Cảnh báo tồn kho tối thiểu" name="reorderPoint" type="number" placeholder="10" />
          </div>
          <div className="flex gap-6">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" name="requiresPrescription" className="rounded" />
              <span className="text-sm text-slate-700">Thuốc kê đơn</span>
            </label>
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" name="availableOnline" defaultChecked className="rounded" />
              <span className="text-sm text-slate-700">Bán online</span>
            </label>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Mô tả</label>
            <textarea
              name="description"
              rows={3}
              className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Công dụng, liều dùng, lưu ý..."
            />
          </div>
        </div>

        {error && (
          <p className="text-sm text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">{error}</p>
        )}

        <div className="flex gap-3 pt-2">
          <button
            type="submit"
            disabled={loading}
            className="bg-green-600 hover:bg-green-700 text-white text-sm font-medium px-6 py-2 rounded-lg transition-colors disabled:opacity-50"
          >
            {loading ? 'Đang lưu...' : 'Lưu sản phẩm'}
          </button>
          <a href="/inventory" className="text-sm text-slate-600 px-4 py-2 rounded-lg border border-slate-200 hover:bg-slate-50">
            Hủy
          </a>
        </div>
      </form>
    </div>
  )
}

function FormField({
  label, name, type = 'text', placeholder, required,
}: {
  label: string
  name: string
  type?: string
  placeholder?: string
  required?: boolean
}) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-700 mb-1">{label}</label>
      <input
        type={type}
        name={name}
        required={required}
        placeholder={placeholder}
        className="w-full border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
      />
    </div>
  )
}
