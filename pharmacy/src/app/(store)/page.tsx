import { db } from '@/db'
import { products, batches } from '@/db/schema'
import { eq, and, sql } from 'drizzle-orm'
import { formatVND } from '@/lib/currency'
import Link from 'next/link'

async function getFeaturedProducts() {
  return db
    .select({
      id: products.id,
      name: products.name,
      slug: products.slug,
      unit: products.unit,
      retailPrice: products.retailPrice,
      imageUrl: products.imageUrl,
      description: products.description,
      requiresPrescription: products.requiresPrescription,
      stock: sql<number>`coalesce(sum(${batches.quantityRemaining}), 0)`,
    })
    .from(products)
    .leftJoin(batches, eq(batches.productId, products.id))
    .where(and(eq(products.active, true), eq(products.availableOnline, true)))
    .groupBy(products.id)
    .orderBy(products.name)
    .limit(12)
}

export default async function StorePage() {
  const featured = await getFeaturedProducts()

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-2xl p-6 mb-8 text-white">
        <h1 className="text-2xl font-bold mb-1">Đặt thuốc tận nhà</h1>
        <p className="text-green-100 text-sm mb-4">Giao hàng nhanh trong 2 giờ · Miễn phí với đơn từ 200k</p>
        <Link href="/store/products" className="bg-white text-green-700 text-sm font-medium px-4 py-2 rounded-lg hover:bg-green-50 transition-colors inline-block">
          Xem tất cả sản phẩm →
        </Link>
      </div>

      <div className="mb-6 flex items-center justify-between">
        <h2 className="font-semibold text-slate-800">Sản phẩm phổ biến</h2>
        <Link href="/store/products" className="text-sm text-green-600 hover:underline">Xem tất cả</Link>
      </div>

      {featured.length === 0 ? (
        <div className="text-center py-16 text-slate-400">
          <p className="text-4xl mb-3">🏥</p>
          <p>Chưa có sản phẩm nào được đăng bán</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {featured.map((p) => (
            <ProductCard key={p.id} product={p} />
          ))}
        </div>
      )}
    </div>
  )
}

function ProductCard({ product }: {
  product: {
    id: number; name: string; slug: string; unit: string; retailPrice: number
    imageUrl: string | null; description: string | null; requiresPrescription: boolean; stock: number
  }
}) {
  const inStock = Number(product.stock) > 0

  return (
    <div className="bg-white rounded-xl border border-slate-200 overflow-hidden hover:shadow-sm transition-shadow">
      <div className="aspect-square bg-slate-100 flex items-center justify-center">
        {product.imageUrl ? (
          <img src={product.imageUrl} alt={product.name} className="w-full h-full object-cover" />
        ) : (
          <span className="text-4xl">💊</span>
        )}
      </div>
      <div className="p-3">
        <h3 className="font-medium text-slate-800 text-sm leading-tight mb-1 line-clamp-2">{product.name}</h3>
        <div className="flex items-center justify-between mt-2">
          <span className="font-semibold text-green-700 text-sm">{formatVND(product.retailPrice)}</span>
          <span className="text-xs text-slate-400">/{product.unit}</span>
        </div>
        {product.requiresPrescription && (
          <span className="text-xs bg-orange-100 text-orange-700 px-1.5 py-0.5 rounded mt-1 inline-block">
            Cần toa thuốc
          </span>
        )}
        {!inStock && (
          <span className="text-xs bg-red-100 text-red-600 px-1.5 py-0.5 rounded mt-1 inline-block">
            Hết hàng
          </span>
        )}
        {inStock && !product.requiresPrescription && (
          <Link
            href={`/store/cart?add=${product.id}`}
            className="mt-2 w-full block text-center bg-green-600 hover:bg-green-700 text-white text-xs font-medium py-1.5 rounded-lg transition-colors"
          >
            Thêm vào giỏ
          </Link>
        )}
      </div>
    </div>
  )
}
