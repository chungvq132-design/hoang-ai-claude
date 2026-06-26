import {
  pgTable,
  text,
  integer,
  boolean,
  timestamp,
  pgEnum,
  serial,
  varchar,
} from 'drizzle-orm/pg-core'
import { relations } from 'drizzle-orm'

// Enums
export const roleEnum = pgEnum('role', ['OWNER', 'PHARMACIST', 'CASHIER'])
export const paymentMethodEnum = pgEnum('payment_method', [
  'CASH',
  'BANK_TRANSFER',
  'MOMO',
  'ZALOPAY',
])
export const orderStatusEnum = pgEnum('order_status', [
  'PENDING',
  'CONFIRMED',
  'PREPARING',
  'READY',
  'DELIVERED',
  'CANCELLED',
])
export const fulfillmentEnum = pgEnum('fulfillment', ['PICKUP', 'DELIVERY'])
export const prescriptionStatusEnum = pgEnum('prescription_status', [
  'PENDING',
  'PARTIALLY_DISPENSED',
  'FULLY_DISPENSED',
  'EXPIRED',
])
export const alertTypeEnum = pgEnum('alert_type', [
  'LOW_STOCK',
  'EXPIRING_SOON',
  'EXPIRED',
])

// Staff users
export const users = pgTable('users', {
  id: text('id').primaryKey(),
  email: text('email').notNull().unique(),
  name: text('name').notNull(),
  password: text('password'), // hashed
  role: roleEnum('role').notNull().default('PHARMACIST'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Product categories
export const categories = pgTable('categories', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  slug: text('slug').notNull().unique(),
})

// Suppliers
export const suppliers = pgTable('suppliers', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  phone: varchar('phone', { length: 20 }),
  email: text('email'),
  address: text('address'),
  taxId: varchar('tax_id', { length: 20 }),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Products / Medicines
export const products = pgTable('products', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  slug: text('slug').notNull().unique(),
  barcode: varchar('barcode', { length: 50 }).unique(),
  registrationNumber: varchar('registration_number', { length: 50 }), // SĐK Bộ Y tế
  description: text('description'),
  unit: varchar('unit', { length: 20 }).notNull(), // viên, hộp, lọ, chai
  retailPrice: integer('retail_price').notNull(), // VND
  vatRate: integer('vat_rate').notNull().default(8), // 0 or 8 percent
  requiresPrescription: boolean('requires_prescription').notNull().default(false),
  availableOnline: boolean('available_online').notNull().default(true),
  reorderPoint: integer('reorder_point').notNull().default(10),
  categoryId: integer('category_id').references(() => categories.id),
  imageUrl: text('image_url'),
  active: boolean('active').notNull().default(true),
  createdAt: timestamp('created_at').notNull().defaultNow(),
  updatedAt: timestamp('updated_at').notNull().defaultNow(),
})

// Stock batches (lot tracking + expiry)
export const batches = pgTable('batches', {
  id: serial('id').primaryKey(),
  productId: integer('product_id').notNull().references(() => products.id),
  lotNumber: varchar('lot_number', { length: 50 }).notNull(),
  quantityReceived: integer('quantity_received').notNull(),
  quantityRemaining: integer('quantity_remaining').notNull(),
  costPrice: integer('cost_price').notNull(), // VND
  expiryDate: timestamp('expiry_date').notNull(),
  manufactureDate: timestamp('manufacture_date'),
  supplierId: integer('supplier_id').references(() => suppliers.id),
  importDate: timestamp('import_date').notNull().defaultNow(),
})

// Inventory alerts
export const inventoryAlerts = pgTable('inventory_alerts', {
  id: serial('id').primaryKey(),
  productId: integer('product_id').notNull().references(() => products.id),
  alertType: alertTypeEnum('alert_type').notNull(),
  message: text('message').notNull(),
  resolvedAt: timestamp('resolved_at'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Patients (for prescription management)
export const patients = pgTable('patients', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  phone: varchar('phone', { length: 15 }).notNull().unique(),
  dateOfBirth: timestamp('date_of_birth'),
  address: text('address'),
  allergies: text('allergies'),
  notes: text('notes'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Prescriptions
export const prescriptions = pgTable('prescriptions', {
  id: serial('id').primaryKey(),
  patientId: integer('patient_id').notNull().references(() => patients.id),
  doctorName: text('doctor_name').notNull(),
  doctorLicenseNumber: varchar('doctor_license_number', { length: 50 }),
  facility: text('facility'),
  prescribedAt: timestamp('prescribed_at').notNull(),
  dispensedAt: timestamp('dispensed_at'),
  status: prescriptionStatusEnum('status').notNull().default('PENDING'),
  imageUrl: text('image_url'), // uploaded photo of paper prescription
  notes: text('notes'),
  saleId: integer('sale_id'), // linked sale after dispensing
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Prescription line items
export const prescriptionItems = pgTable('prescription_items', {
  id: serial('id').primaryKey(),
  prescriptionId: integer('prescription_id').notNull().references(() => prescriptions.id),
  productId: integer('product_id').references(() => products.id),
  prescribedDrug: text('prescribed_drug').notNull(), // freetext drug name
  dosage: text('dosage').notNull(), // e.g. "2 viên/ngày"
  frequency: text('frequency'), // e.g. "3 lần/ngày"
  duration: text('duration'), // e.g. "7 ngày"
  totalQuantity: integer('total_quantity').notNull(),
  dispensedQuantity: integer('dispensed_quantity').notNull().default(0),
})

// POS Sales
export const sales = pgTable('sales', {
  id: serial('id').primaryKey(),
  invoiceNumber: varchar('invoice_number', { length: 30 }).notNull().unique(),
  userId: text('user_id').notNull().references(() => users.id),
  patientId: integer('patient_id').references(() => patients.id),
  prescriptionId: integer('prescription_id').references(() => prescriptions.id),
  subtotal: integer('subtotal').notNull(), // before VAT
  vatAmount: integer('vat_amount').notNull().default(0),
  total: integer('total').notNull(),
  paymentMethod: paymentMethodEnum('payment_method').notNull().default('CASH'),
  amountTendered: integer('amount_tendered'), // for cash payment
  change: integer('change').default(0),
  notes: text('notes'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Sale line items
export const saleItems = pgTable('sale_items', {
  id: serial('id').primaryKey(),
  saleId: integer('sale_id').notNull().references(() => sales.id),
  productId: integer('product_id').notNull().references(() => products.id),
  batchId: integer('batch_id').references(() => batches.id),
  quantity: integer('quantity').notNull(),
  unitPrice: integer('unit_price').notNull(), // VND at time of sale
  vatRate: integer('vat_rate').notNull().default(8),
  discount: integer('discount').notNull().default(0),
})

// Online customers
export const customers = pgTable('customers', {
  id: serial('id').primaryKey(),
  name: text('name').notNull(),
  phone: varchar('phone', { length: 15 }).notNull().unique(),
  email: text('email'),
  address: text('address'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Online orders
export const orders = pgTable('orders', {
  id: serial('id').primaryKey(),
  customerId: integer('customer_id').references(() => customers.id),
  guestName: text('guest_name'),
  guestPhone: varchar('guest_phone', { length: 15 }),
  status: orderStatusEnum('status').notNull().default('PENDING'),
  fulfillment: fulfillmentEnum('fulfillment').notNull().default('PICKUP'),
  deliveryAddress: text('delivery_address'),
  subtotal: integer('subtotal').notNull(),
  vatAmount: integer('vat_amount').notNull().default(0),
  total: integer('total').notNull(),
  paymentMethod: paymentMethodEnum('payment_method').notNull().default('CASH'),
  prescriptionImageUrl: text('prescription_image_url'),
  notes: text('notes'),
  confirmedAt: timestamp('confirmed_at'),
  createdAt: timestamp('created_at').notNull().defaultNow(),
})

// Order line items
export const orderItems = pgTable('order_items', {
  id: serial('id').primaryKey(),
  orderId: integer('order_id').notNull().references(() => orders.id),
  productId: integer('product_id').notNull().references(() => products.id),
  quantity: integer('quantity').notNull(),
  unitPrice: integer('unit_price').notNull(),
  vatRate: integer('vat_rate').notNull().default(8),
})

// Pharmacy config (single row)
export const taxConfig = pgTable('tax_config', {
  id: integer('id').primaryKey().default(1),
  pharmacyName: text('pharmacy_name').notNull().default('Nhà Thuốc'),
  pharmacyAddress: text('pharmacy_address'),
  taxId: varchar('tax_id', { length: 20 }), // MST
  pharmacyLicenseNumber: varchar('pharmacy_license_number', { length: 50 }),
  vatRate: integer('vat_rate').notNull().default(8),
  invoiceCounter: integer('invoice_counter').notNull().default(0),
})

// Relations
export const productsRelations = relations(products, ({ one, many }) => ({
  category: one(categories, { fields: [products.categoryId], references: [categories.id] }),
  batches: many(batches),
  saleItems: many(saleItems),
  orderItems: many(orderItems),
  prescriptionItems: many(prescriptionItems),
  alerts: many(inventoryAlerts),
}))

export const batchesRelations = relations(batches, ({ one }) => ({
  product: one(products, { fields: [batches.productId], references: [products.id] }),
  supplier: one(suppliers, { fields: [batches.supplierId], references: [suppliers.id] }),
}))

export const salesRelations = relations(sales, ({ one, many }) => ({
  user: one(users, { fields: [sales.userId], references: [users.id] }),
  patient: one(patients, { fields: [sales.patientId], references: [patients.id] }),
  prescription: one(prescriptions, { fields: [sales.prescriptionId], references: [prescriptions.id] }),
  items: many(saleItems),
}))

export const saleItemsRelations = relations(saleItems, ({ one }) => ({
  sale: one(sales, { fields: [saleItems.saleId], references: [sales.id] }),
  product: one(products, { fields: [saleItems.productId], references: [products.id] }),
  batch: one(batches, { fields: [saleItems.batchId], references: [batches.id] }),
}))

export const patientsRelations = relations(patients, ({ many }) => ({
  prescriptions: many(prescriptions),
}))

export const prescriptionsRelations = relations(prescriptions, ({ one, many }) => ({
  patient: one(patients, { fields: [prescriptions.patientId], references: [patients.id] }),
  items: many(prescriptionItems),
}))

export const ordersRelations = relations(orders, ({ one, many }) => ({
  customer: one(customers, { fields: [orders.customerId], references: [customers.id] }),
  items: many(orderItems),
}))

export const orderItemsRelations = relations(orderItems, ({ one }) => ({
  order: one(orders, { fields: [orderItems.orderId], references: [orders.id] }),
  product: one(products, { fields: [orderItems.productId], references: [products.id] }),
}))
