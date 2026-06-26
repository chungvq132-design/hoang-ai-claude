# Pharmacy App

Phần mềm quản lý nhà thuốc — Next.js 14 + Drizzle ORM + PostgreSQL (Supabase)

## Tech Stack
- Next.js 14 App Router + TypeScript
- Drizzle ORM + PostgreSQL (via Supabase)
- NextAuth.js (credentials provider)
- TailwindCSS
- Deployed on Vercel

## Commands
```bash
npm run dev          # Start dev server on :3000
npm run db:generate  # Generate Drizzle migrations
npm run db:push      # Push schema changes directly (dev only)
npm run db:migrate   # Run migrations
npm run db:studio    # Open Drizzle Studio (visual DB browser)
npm run db:seed      # Seed with sample data
```

## Environment Variables
Copy `.env.example` to `.env.local` and fill in:
- `DATABASE_URL` — Supabase PostgreSQL connection string
- `NEXTAUTH_SECRET` — Random secret (use: `openssl rand -base64 32`)
- `NEXTAUTH_URL` — App URL (http://localhost:3000 for dev)

## Project Structure
```
src/
├── app/
│   ├── (auth)/        # Login page (public)
│   ├── (staff)/       # Staff portal (requires auth)
│   │   ├── dashboard/ # Overview
│   │   ├── pos/       # Point of Sale
│   │   ├── inventory/ # Product & stock management
│   │   ├── prescriptions/ # Prescription management
│   │   ├── customers/ # Customer profiles
│   │   └── orders/    # Online order management
│   ├── (store)/       # Customer-facing store (public)
│   └── api/           # REST API routes
├── db/
│   ├── schema.ts      # Drizzle schema (source of truth)
│   └── index.ts       # DB connection
└── lib/
    ├── auth.ts        # NextAuth config
    └── currency.ts    # VND formatting
```

## Domain Rules
- All monetary values stored as `Int` (VND, no decimals)
- Never sell `requiresPrescription=true` products without `prescriptionId`
- VAT: 8% standard, 0% for some essential medicines (check `Product.vatRate`)
- Invoice numbers: `PH-YYYYMMDD-NNNN`
- Stock deduction uses FEFO (First Expiry, First Out) order
- Staff portal requires session; store pages are public

## Roles
- `OWNER` — Full access including financial reports
- `PHARMACIST` — Can dispense prescriptions, manage inventory
- `CASHIER` — POS only, no inventory/prescription write access

## Default Login (after seed)
- Admin: `admin@nhathuoc.com` / `admin123`
- Pharmacist: `duocsi@nhathuoc.com` / `duocsi123`
