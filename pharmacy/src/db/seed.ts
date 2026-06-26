import { db } from './index'
import { users, categories, products, batches, taxConfig } from './schema'
import { createHash } from 'crypto'

function hashPassword(password: string): string {
  return createHash('sha256').update(password + (process.env.NEXTAUTH_SECRET || 'secret')).digest('hex')
}

async function seed() {
  console.log('🌱 Seeding database...')

  // Tax config
  await db.insert(taxConfig).values({
    id: 1,
    pharmacyName: 'Nhà Thuốc Hoàng',
    pharmacyAddress: '123 Đường ABC, Phường 1, Quận 1, TP.HCM',
    taxId: '0123456789',
    vatRate: 8,
    invoiceCounter: 0,
  }).onConflictDoNothing()

  // Categories
  const cats = await db.insert(categories).values([
    { name: 'Thuốc không kê đơn (OTC)', slug: 'otc' },
    { name: 'Thuốc kê đơn', slug: 'ke-don' },
    { name: 'Thực phẩm chức năng', slug: 'thuc-pham-chuc-nang' },
    { name: 'Dụng cụ y tế', slug: 'dung-cu-y-te' },
    { name: 'Chăm sóc cá nhân', slug: 'cham-soc-ca-nhan' },
  ]).returning()
  console.log('✅ Categories created')

  // Staff users
  await db.insert(users).values([
    {
      id: 'admin-001',
      email: 'admin@nhathuoc.com',
      name: 'Quản trị viên',
      password: hashPassword('admin123'),
      role: 'OWNER',
    },
    {
      id: 'pharmacist-001',
      email: 'duocsi@nhathuoc.com',
      name: 'Dược Sĩ Nguyễn',
      password: hashPassword('duocsi123'),
      role: 'PHARMACIST',
    },
  ]).onConflictDoNothing()
  console.log('✅ Staff users created')

  // Sample products
  const otcCat = cats.find((c) => c.slug === 'otc')!
  const kdCat = cats.find((c) => c.slug === 'ke-don')!
  const tpcnCat = cats.find((c) => c.slug === 'thuc-pham-chuc-nang')!

  const productList = await db.insert(products).values([
    {
      name: 'Paracetamol 500mg',
      slug: 'paracetamol-500mg',
      barcode: '8934868012345',
      unit: 'viên',
      retailPrice: 1500,
      vatRate: 8,
      requiresPrescription: false,
      availableOnline: true,
      reorderPoint: 50,
      categoryId: otcCat.id,
      description: 'Giảm đau, hạ sốt. Dùng cho người lớn và trẻ em trên 12 tuổi.',
    },
    {
      name: 'Vitamin C 1000mg',
      slug: 'vitamin-c-1000mg',
      barcode: '8934868023456',
      unit: 'viên',
      retailPrice: 8000,
      vatRate: 0,
      requiresPrescription: false,
      availableOnline: true,
      reorderPoint: 30,
      categoryId: tpcnCat.id,
      description: 'Bổ sung Vitamin C, tăng đề kháng.',
    },
    {
      name: 'Amoxicillin 500mg',
      slug: 'amoxicillin-500mg',
      barcode: '8934868034567',
      registrationNumber: 'VD-12345-12',
      unit: 'viên',
      retailPrice: 5000,
      vatRate: 8,
      requiresPrescription: true,
      availableOnline: false,
      reorderPoint: 20,
      categoryId: kdCat.id,
      description: 'Kháng sinh nhóm penicillin. Chỉ dùng khi có toa bác sĩ.',
    },
    {
      name: 'Omeprazole 20mg',
      slug: 'omeprazole-20mg',
      barcode: '8934868045678',
      registrationNumber: 'VD-23456-13',
      unit: 'viên',
      retailPrice: 3000,
      vatRate: 8,
      requiresPrescription: true,
      availableOnline: false,
      reorderPoint: 15,
      categoryId: kdCat.id,
      description: 'Điều trị loét dạ dày, trào ngược. Cần kê đơn.',
    },
    {
      name: 'Nước muối sinh lý 0.9%',
      slug: 'nuoc-muoi-sinh-ly',
      barcode: '8934868056789',
      unit: 'chai',
      retailPrice: 12000,
      vatRate: 0,
      requiresPrescription: false,
      availableOnline: true,
      reorderPoint: 20,
      categoryId: otcCat.id,
      description: 'Vệ sinh mắt, mũi, họng.',
    },
    {
      name: 'Gel rửa tay sát khuẩn',
      slug: 'gel-rua-tay-sat-khuan',
      barcode: '8934868067890',
      unit: 'chai',
      retailPrice: 35000,
      vatRate: 8,
      requiresPrescription: false,
      availableOnline: true,
      reorderPoint: 10,
      categoryId: cats.find((c) => c.slug === 'cham-soc-ca-nhan')!.id,
      description: 'Sát khuẩn tay nhanh, không cần nước.',
    },
  ]).returning()
  console.log('✅ Products created')

  // Stock batches
  const expiryDate1 = new Date()
  expiryDate1.setFullYear(expiryDate1.getFullYear() + 2)

  const expiryDate2 = new Date()
  expiryDate2.setMonth(expiryDate2.getMonth() + 3) // expiring soon for demo

  await db.insert(batches).values([
    {
      productId: productList[0].id, // Paracetamol
      lotNumber: 'LOT-2024-001',
      quantityReceived: 500,
      quantityRemaining: 480,
      costPrice: 800,
      expiryDate: expiryDate1,
    },
    {
      productId: productList[1].id, // Vitamin C
      lotNumber: 'LOT-2024-002',
      quantityReceived: 200,
      quantityRemaining: 165,
      costPrice: 5000,
      expiryDate: expiryDate1,
    },
    {
      productId: productList[2].id, // Amoxicillin
      lotNumber: 'LOT-2024-003',
      quantityReceived: 100,
      quantityRemaining: 8, // low stock demo
      costPrice: 3000,
      expiryDate: expiryDate1,
    },
    {
      productId: productList[3].id, // Omeprazole
      lotNumber: 'LOT-2024-004',
      quantityReceived: 150,
      quantityRemaining: 140,
      costPrice: 1500,
      expiryDate: expiryDate2, // expiring soon
    },
    {
      productId: productList[4].id, // Nước muối
      lotNumber: 'LOT-2024-005',
      quantityReceived: 100,
      quantityRemaining: 85,
      costPrice: 7000,
      expiryDate: expiryDate1,
    },
    {
      productId: productList[5].id, // Gel rửa tay
      lotNumber: 'LOT-2024-006',
      quantityReceived: 50,
      quantityRemaining: 42,
      costPrice: 20000,
      expiryDate: expiryDate1,
    },
  ])
  console.log('✅ Stock batches created')

  console.log('\n🎉 Seed complete!')
  console.log('Login credentials:')
  console.log('  Admin: admin@nhathuoc.com / admin123')
  console.log('  Pharmacist: duocsi@nhathuoc.com / duocsi123')
  process.exit(0)
}

seed().catch((e) => {
  console.error('Seed failed:', e)
  process.exit(1)
})
