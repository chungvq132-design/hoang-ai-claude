import { db } from '@/db'
import { products, batches, inventoryAlerts, categories } from '@/db/schema'
import { eq, sql, isNull, lte } from 'drizzle-orm'
import { formatVND } from '@/lib/currency'
import Link from 'next/link'

async function getProducts() {
  const rows = await db
    .select({
      id: products.id,
      name: products.name,
      barcode: products.barcode,
      unit: products.unit,
      retailPrice: products.retailPrice,
      requiresPrescription: products.requiresPrescription,
      reorderPoint: products.reorderPoint,
      categoryName: categories.name,
      stock: sql<number>`coalesce(sum(${batches.quantityRemaining}), 0)`,
    })
    .from(products)
    .leftJoin(categories, eq(products.categoryId, categories.id))
    .leftJoin(batches, eq(batches.productId, products.id))
    .where(eq(products.active, true))
    .groupBy(products.id, categories.name)
    .orderBy(products.name)

  return rows
}

async function getAlerts() {
  return db
    .select()
    .from(inventoryAlerts)
    .where(isNull(inventoryAlerts.resolvedAt))
    .orderBy(inventoryAlerts.createdAt)
    .limit(5)
}

export default async function InventoryPage() {
  const [productRows, alerts] = await Promise.all([getProducts(), getAlerts()])

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">Kho thuốc</h1>
          <p className="text-sm text-slate-500 mt-0.5">{productRows.length} sản phẩm</p>
        </div>
        <div className="flex gap-2">
          <Link
            href="/inventory/products/new"
            className="bg-green-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
          >
            + Thêm sản phẩm
          </Link>
        </div>
      </div>

      {alerts.length > 0 && (
        <div className="mb-4 p-3 bg-red-50 border border-red-100 rounded-xl">
          <p className="text-sm font-medium text-red-700 mb-1">⚠️ {alerts.length} cảnh báo kho</p>
          {alerts.map((a) => (
            <p key={a.id} className="text-xs text-red-600 mt-0.5">• {a.message}</p>
          ))}
        </div>
      )}

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Tên sản phẩm</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Barcode</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Đơn vị</th>
              <th className="text-right px-4 py-3 font-medium text-slate-600">Giá bán</th>
              <th className="text-right px-4 py-3 font-medium text-slate-600">Tồn kho</th>
              <th className="text-center px-4 py-3 font-medium text-slate-600">Kê đơn</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {productRows.map((p) => (
              <tr key={p.id} className="hover:bg-slate-50">
                <td className="px-4 py-3 font-medium text-slate-800">{p.name}</td>
                <td className="px-4 py-3 text-slate-500 font-mono text-xs">{p.barcode ?? '—'}</td>
                <td className="px-4 py-3 text-slate-600">{p.unit}</td>
                <td className="px-4 py-3 text-right text-slate-800">{formatVND(p.retailPrice)}</td>
                <td className="px-4 py-3 text-right">
                  <span
                    className={`font-medium ${
                      Number(p.stock) === 0
                        ? 'text-red-600'
                        : Number(p.stock) <= p.reorderPoint
                        ? 'text-orange-600'
                        : 'text-slate-800'
                    }`}
                  >
                    {Number(p.stock)}
                  </span>
                </td>
                <td className="px-4 py-3 text-center">
                  {p.requiresPrescription ? (
                    <span className="text-xs bg-orange-100 text-orange-700 px-2 py-0.5 rounded-full">Có</span>
                  ) : (
                    <span className="text-xs bg-slate-100 text-slate-500 px-2 py-0.5 rounded-full">Không</span>
                  )}
                </td>
                <td className="px-4 py-3">
                  <Link
                    href={`/inventory/products/${p.id}`}
                    className="text-xs text-green-600 hover:underline"
                  >
                    Sửa
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {productRows.length === 0 && (
          <div className="text-center py-12 text-slate-400">
            <p className="text-3xl mb-2">📦</p>
            <p className="text-sm">Chưa có sản phẩm nào</p>
            <Link href="/inventory/products/new" className="text-green-600 text-sm hover:underline mt-1 inline-block">
              Thêm sản phẩm đầu tiên →
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
