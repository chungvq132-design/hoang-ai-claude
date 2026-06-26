export function formatVND(amount: number): string {
  return amount.toLocaleString('vi-VN', { style: 'currency', currency: 'VND' })
}

export function formatVNDCompact(amount: number): string {
  if (amount >= 1_000_000) {
    return `${(amount / 1_000_000).toFixed(1)}tr`
  }
  if (amount >= 1_000) {
    return `${(amount / 1_000).toFixed(0)}k`
  }
  return `${amount}đ`
}

export function parseVND(str: string): number {
  return parseInt(str.replace(/[^\d]/g, ''), 10) || 0
}

export function calculateVAT(subtotal: number, vatRate: 0 | 8): number {
  return Math.round((subtotal * vatRate) / 100)
}

export function calculateTotal(subtotal: number, vatRate: 0 | 8): number {
  return subtotal + calculateVAT(subtotal, vatRate)
}
