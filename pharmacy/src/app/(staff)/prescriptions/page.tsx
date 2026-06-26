import { db } from '@/db'
import { prescriptions, patients } from '@/db/schema'
import { eq, desc } from 'drizzle-orm'
import Link from 'next/link'

async function getPrescriptions() {
  return db
    .select({
      id: prescriptions.id,
      status: prescriptions.status,
      doctorName: prescriptions.doctorName,
      facility: prescriptions.facility,
      prescribedAt: prescriptions.prescribedAt,
      createdAt: prescriptions.createdAt,
      patientName: patients.name,
      patientPhone: patients.phone,
    })
    .from(prescriptions)
    .leftJoin(patients, eq(prescriptions.patientId, patients.id))
    .orderBy(desc(prescriptions.createdAt))
    .limit(50)
}

const statusLabel: Record<string, { label: string; color: string }> = {
  PENDING: { label: 'Chờ cấp phát', color: 'bg-yellow-100 text-yellow-700' },
  PARTIALLY_DISPENSED: { label: 'Cấp phát một phần', color: 'bg-blue-100 text-blue-700' },
  FULLY_DISPENSED: { label: 'Đã cấp đủ', color: 'bg-green-100 text-green-700' },
  EXPIRED: { label: 'Hết hạn', color: 'bg-red-100 text-red-600' },
}

export default async function PrescriptionsPage() {
  const rxList = await getPrescriptions()

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-slate-900">Toa thuốc</h1>
          <p className="text-sm text-slate-500 mt-0.5">{rxList.length} toa gần nhất</p>
        </div>
        <div className="flex gap-2">
          <Link href="/patients" className="border border-slate-200 text-slate-600 text-sm px-4 py-2 rounded-lg hover:bg-slate-50">
            Hồ sơ bệnh nhân
          </Link>
          <Link href="/prescriptions/new" className="bg-green-600 text-white text-sm px-4 py-2 rounded-lg hover:bg-green-700 transition-colors">
            + Nhập toa thuốc
          </Link>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-slate-50 border-b border-slate-200">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Bệnh nhân</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Bác sĩ / Phòng khám</th>
              <th className="text-left px-4 py-3 font-medium text-slate-600">Ngày kê đơn</th>
              <th className="text-center px-4 py-3 font-medium text-slate-600">Trạng thái</th>
              <th className="px-4 py-3"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {rxList.map((rx) => {
              const s = statusLabel[rx.status] ?? { label: rx.status, color: 'bg-slate-100 text-slate-600' }
              return (
                <tr key={rx.id} className="hover:bg-slate-50">
                  <td className="px-4 py-3">
                    <div className="font-medium text-slate-800">{rx.patientName ?? 'Không rõ'}</div>
                    <div className="text-xs text-slate-400">{rx.patientPhone}</div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="text-slate-700">{rx.doctorName}</div>
                    {rx.facility && <div className="text-xs text-slate-400">{rx.facility}</div>}
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    {new Date(rx.prescribedAt).toLocaleDateString('vi-VN')}
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className={`text-xs px-2 py-0.5 rounded-full ${s.color}`}>{s.label}</span>
                  </td>
                  <td className="px-4 py-3">
                    <Link href={`/prescriptions/${rx.id}`} className="text-xs text-green-600 hover:underline">
                      Chi tiết
                    </Link>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
        {rxList.length === 0 && (
          <div className="text-center py-12 text-slate-400">
            <p className="text-3xl mb-2">📋</p>
            <p className="text-sm">Chưa có toa thuốc nào</p>
            <Link href="/prescriptions/new" className="text-green-600 text-sm hover:underline mt-1 inline-block">
              Nhập toa thuốc đầu tiên →
            </Link>
          </div>
        )}
      </div>
    </div>
  )
}
