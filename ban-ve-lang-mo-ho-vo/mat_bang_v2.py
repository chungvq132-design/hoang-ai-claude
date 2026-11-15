# -*- coding: utf-8 -*-
"""MAT BANG TONG THE - PHIEN BAN 2 (kich thuoc chu nha chot lai ngay 15/11/2026).
Moi kich thuoc bo tri do theo mep ngoai phan noi da hoan thien (tren cot nen).
Chay: python3 mat_bang_v2.py -> mat-bang-v2.svg / .pdf / .png
"""
import os, math
from gen import (SVG, hchain, vchain, fmt, frame, north_arrow, legend_item, title_block, textblock,
                 TILE, PATHFILL, FIN, WALL, HOC_L, HOC_W, N_HOC)

HERE = os.path.dirname(os.path.abspath(__file__))

# ===================== SO LIEU CHOT (mm, hoan thien) =====================
L = 18400            # 1  chieu dai khu dat (canh Tay thang)
W_G = 8440           # 2  rong phia cong
W_IN_MEAS = 8870     # 3  do xien tai hien truong (chi ghi chu)
TAPER = 40           #    canh Dong vat vao 40 o phia am tho
W_I = W_G - TAPER    #    rong vuong goc phia am tho = 8.400
GATE = 1270          # 6
PATH = 1160          # 8
GAP_W = 300          # 9  tuong Tay -> mep block day trai
D_IN = 1580          # 12 tuong am tho -> block dau
GAP = 500            # 13 khoang giua 2 block
N_ROW = 11           # 15
BL = 3050            # 16 block dai (theo chieu 6 hoc, vuong goc loi di)
BT = 930             # 17 block day (doc loi di)
CORE_L = N_HOC * HOC_W + (N_HOC + 1) * WALL + 2 * FIN   # 2.670 (cau tao cu)
CORE_T = HOC_L + 2 * WALL + 2 * FIN                     # 820
RIM_END = (BL - CORE_L) / 2                             # 190
RIM_SIDE = (BT - CORE_T) / 2                            # 55

D_GATE = L - D_IN - N_ROW * BT - (N_ROW - 1) * GAP      # 14 -> 1.590
GAP_E = W_G - GAP_W - 2 * BL - PATH                     # 10 -> 880
GAP_E_IN = W_I - GAP_W - 2 * BL - PATH                  # 11 -> 840
Y_AX = GAP_W + BL + PATH / 2                            # 3.930
G1, G2 = Y_AX - GATE / 2, Y_AX + GATE / 2               # 3.295 .. 4.565
ROW_W = (GAP_W, GAP_W + BL)
ROW_E = (GAP_W + BL + PATH, GAP_W + 2 * BL + PATH)

assert (CORE_L, CORE_T, RIM_END, RIM_SIDE) == (2670, 820, 190, 55)
assert D_GATE == 1590 and GAP_E == 880 and GAP_E_IN == 840
assert D_IN + N_ROW * BT + (N_ROW - 1) * GAP + D_GATE == L
assert GAP_W + BL + PATH + BL + GAP_E == W_G
assert G1 == 3295 and W_G - G2 == 3875
BX = sorted((L - D_IN - i * (BT + GAP) - BT, L - D_IN - i * (BT + GAP)) for i in range(N_ROW))
assert BX[0][0] == D_GATE
east_y = lambda x: W_G - TAPER * x / L                  # canh Dong vat thang
assert east_y(BX[-1][1]) - ROW_E[1] > 800              # block van trong long dat


def page():
    s = SVG()
    frame(s)
    S = 1 / 60
    ox, oy = 50, 50
    P = lambda X, Y: (ox + X * S, oy + Y * S)
    t = 200

    s.text(14, 20, "MẶT BẰNG TỔNG THỂ KHU LĂNG MỘ HỌ VÕ", size=5.5, anchor="start", weight="bold")
    s.text(14, 26.5, "TỶ LỆ 1/60  –  22 BLOCK × 6 HỘC = 132 HỘC  –  PHIÊN BẢN 2 (KÍCH THƯỚC CHỐT 15/11/2026)",
           size=3.0, anchor="start", weight="bold")
    s.text(405, 19, "MỌI KÍCH THƯỚC BỐ TRÍ ĐO THEO MÉP NGOÀI PHẦN NỔI ĐÃ HOÀN THIỆN (TRÊN CỐT NỀN)",
           size=2.7, anchor="end", weight="bold", col="#c00000")
    s.text(405, 24, "đế BTCT, móng và phần chìm chỉ thể hiện ở mặt cắt", size=2.3, anchor="end", col="#c00000")

    # ---- loi di
    a, b = P(0, ROW_W[1]), P(L, ROW_E[0])
    s.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=PATHFILL, sw=0)
    # ---- tuong bien (tuong trung, day 200)
    inner = [(0, 0), (L, 0), (L, W_I), (0, W_G)]
    outer = [(-t, -t), (L + t, -t), (L + t, W_I + t), (-t, W_G + t)]
    for (X1, Y1, X2, Y2) in ((-t, -t, L + t, 0), (-t, 0, 0, W_G + t), (L, 0, L + t, W_I + t)):
        a1, a2 = P(X1, Y1), P(X2, Y2)
        s.rect(a1[0], a1[1], a2[0] - a1[0], a2[1] - a1[1], fill="url(#brick)", sw=0)
    q = [P(0, W_G), P(L, W_I), P(L + t, W_I), P(L + t, W_I + t), P(-t, W_G + t), P(-t, W_G)]
    s.poly(q, fill="#f2c9b6", sw=0)
    s.poly([P(*p) for p in inner], sw=0.45)
    s.poly([P(*p) for p in outer], sw=0.45)
    # cong
    g0, g1 = P(-t - 20, G1), P(15, G2)
    s.rect(g0[0], g0[1], g1[0] - g0[0], g1[1] - g0[1], fill="#fff", sw=0)
    for gy, sg in ((G1, 1), (G2, -1)):
        a1, a2 = P(-t, gy), P(0, gy)
        s.line(a1[0], a1[1], a2[0], a2[1], sw=0.45)
        r = GATE / 2 * S
        s.line(a2[0], a2[1], a2[0] + r * 0.5, a2[1] + sg * r * 0.866, sw=0.3)
    a1, a2 = P(-t / 2, G1), P(-t / 2, G2)
    s.line(a1[0], a1[1], a2[0], a2[1], sw=0.18, dash="1,0.7")

    # ---- block
    def block(xl, yt):
        a = P(xl, yt)
        s.rect(a[0], a[1], BT * S, BL * S, fill="#d8d2c4", sw=0)                  # vien ngoai (phan noi)
        c0x, c0y = xl + RIM_SIDE, yt + RIM_END
        a = P(c0x, c0y)
        s.rect(a[0], a[1], CORE_T * S, CORE_L * S, fill=TILE, sw=0)               # op + to
        a = P(c0x + FIN, c0y + FIN)
        s.rect(a[0], a[1], (CORE_T - 2 * FIN) * S, (CORE_L - 2 * FIN) * S, fill="#c4563a", sw=0)
        for k in range(N_HOC):
            a = P(c0x + FIN + WALL, c0y + FIN + WALL + k * (HOC_W + WALL))
            s.rect(a[0], a[1], HOC_L * S, HOC_W * S, fill="#fff", sw=0.08)
        a = P(xl, yt)
        s.rect(a[0], a[1], BT * S, BL * S, sw=0.35)

    for j, (xl, xr) in enumerate(BX):
        block(xl, ROW_W[0])
        block(xl, ROW_E[0])
        cx = P((xl + xr) / 2, 0)[0]
        s.text(cx, P(0, ROW_W[1] + 210)[1], f"T{j + 1}", size=2.3, weight="bold", col="#333")
        s.text(cx, P(0, ROW_E[0] - 70)[1], f"P{j + 1}", size=2.3, weight="bold", col="#333")

    # ---- am tho (tuong trung)
    a, b = P(17000, Y_AX - 950), P(18200, Y_AX + 950)
    s.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill="#fffdf2", sw=0.4, dash="1.4,0.8")
    cx = (a[0] + b[0]) / 2
    s.text(cx, a[1] + 7.0, "AM THỜ", size=3.4, weight="bold")
    s.text(cx, a[1] + 12.5, "– KÍCH THƯỚC", size=2.2)
    s.text(cx, a[1] + 15.5, "CHỜ BỔ SUNG", size=2.2)
    s.text(cx, b[1] - 2.0, "(tượng trưng)", size=1.9, col="#555")

    # ---- truc
    a, b = P(-650, Y_AX), P(L + 450, Y_AX)
    s.line(a[0], a[1], b[0], b[1], sw=0.35, col="#c00000", dash="6,1.2,0.8,1.2")
    s.text(P(9300, 0)[0], P(0, Y_AX)[1] - 1.2, "TRỤC CỔNG – LỐI ĐI – AM THỜ: B9°", size=3.0, weight="bold", col="#c00000")
    s.text(P(9300, 0)[0], P(0, Y_AX)[1] + 4.0, "LỐI ĐI GIỮA – RỘNG THÔNG THỦY 1.160", size=2.5, col="#1d4d1d")
    s.text(P(800, 0)[0], P(0, Y_AX)[1] - 1.2, "CỔNG", size=2.6, weight="bold")
    for (yt_, l1) in ((1300, "DÃY TRÁI (TÂY)"), (5600, "DÃY PHẢI (ĐÔNG)")):
        px, py = P(800, yt_)
        s.text(px, py, l1, size=2.0, weight="bold")
        s.text(px, py + 3.0, "11 block", size=2.0)
        s.text(px, py + 6.0, "× 6 hộc", size=2.0)

    # ---- kich thuoc tren (canh Tay)
    yw = P(0, -t)[1]
    xs, labs = [0, D_GATE], [fmt(D_GATE)]
    for j, (xl, xr) in enumerate(BX):
        if j:
            xs.append(xl); labs.append(fmt(GAP))
        xs.append(xr); labs.append(fmt(BT))
    xs.append(L); labs.append(fmt(D_IN))
    hchain(s, [P(x, 0)[0] for x in xs], yw, yw - 6.5, labs, size=2.6, bold=True)
    hchain(s, [P(0, 0)[0], P(L, 0)[0]], yw, yw - 14, ["18.400 – CHIỀU DÀI LỌT LÒNG (CẠNH TÂY W THẲNG)"], size=3.0, bold=True)

    # ---- kich thuoc duoi
    yb = P(0, W_G + t)[1] + 6.5
    hchain(s, [P(0, 0)[0], P(L, 0)[0]], [P(0, W_G)[1], P(0, W_I)[1]], yb,
           ["18.400 (hình chiếu) – CẠNH ĐÔNG VÁT VÀO 40 VỀ PHÍA AM THỜ"], size=2.8, bold=True)

    # ---- trai (phia cong)
    xw = P(-t, 0)[0]
    vchain(s, [P(0, y)[1] for y in (0, G1, G2, W_G)], xw, xw - 6, [fmt(G1), "1.270 CỔNG", fmt(W_G - G2)], size=2.7, bold=True)
    vchain(s, [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_G)], xw, xw - 13.5,
           [fmt(GAP_W), fmt(BL), fmt(PATH), fmt(BL), fmt(GAP_E)], size=2.7, bold=True)
    vchain(s, [P(0, 0)[1], P(0, W_G)[1]], xw, xw - 21, ["8.440 – RỘNG PHÍA CỔNG"], size=3.0, bold=True)
    # ---- phai (phia am tho)
    xe = P(L + t, 0)[0]
    vchain(s, [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_I)], xe, xe + 8,
           [fmt(GAP_W), fmt(BL), fmt(PATH), fmt(BL), fmt(GAP_E_IN)], size=2.7, bold=True)
    vchain(s, [P(0, 0)[1], P(0, W_I)[1]], xe, xe + 16, ["8.400 – RỘNG PHÍA AM THỜ (VUÔNG GÓC)"], size=2.8, bold=True)
    s.text(xe + 21, P(0, W_I / 2)[1], "(đo xiên hiện trường: 8.870)", size=2.1, rot=-90, col="#c00000")

    for (yy, ch, txt) in ((oy - 10, "W", "CẠNH TÂY"), (P(0, W_G)[1] + 13, "E", "CẠNH ĐÔNG")):
        s.circle(17, yy, 3.2, sw=0.4)
        s.text(17, yy + 1.4, ch, size=3.8, weight="bold")
        s.text(17, yy + 6.6, txt, size=1.9, weight="bold")

    # ================= DAI DUOI =================
    ys0 = 214
    s.line(10, ys0, 410, ys0, sw=0.5)
    s.text(13, ys0 + 5, "GHI CHÚ", size=3.0, anchor="start", weight="bold")
    notes = [
        "1. Kích thước mm, đo theo mép ngoài phần nổi đã hoàn thiện (trên cốt nền). Khu đất: kích thước lọt lòng; tường biên vẽ tượng trưng (chiều dày chờ bổ sung).",
        "2. Chiều dài: 1.590 + 11×930 + 10×500 + 1.580 = 18.400.",
        "3. Chiều ngang phía cổng: 300 + 3.050 + 1.160 + 3.050 + 880 = 8.440. Phía am thờ: 300 + 3.050 + 1.160 + 3.050 + 840 = 8.400.",
        "4. Khu đất xiên: cạnh Tây thẳng; cạnh Đông vát vào 40 về phía am thờ (rộng vuông góc 8.400; đo xiên tại hiện trường 8.870).",
        "5. Block hoàn thiện 3.050 × 930 = lõi 6 hộc 2.670 × 820 (hộc 680×380, tường 50, tô 10 + ốp 10) + viền ngoài 190 mỗi đầu, 55 mỗi bên (cấu tạo viền chờ xác nhận).",
        "6. Cổng 1.270 đặt trùng tim lối đi (cách tường Tây 3.295, tường Đông 3.875); tim cổng = tim lối đi = tim am thờ, hướng B9°Đ.",
        "7. AM THỜ vẽ tượng trưng – kích thước chờ bổ sung.",
    ]
    textblock(s, 13, ys0 + 9.6, notes, size=2.15, nchar=112)
    xk = 150
    s.line(xk, ys0, xk, 287, sw=0.4)
    s.text(xk + 3, ys0 + 5, "BẢNG KIỂM TRA", size=3.0, anchor="start", weight="bold")
    checks = [("Số block", "22 (11 trái + 11 phải)"), ("Hộc / block – tổng", "6 – 132 hộc"),
              ("Tổng chiều dài", "18.400"), ("Rộng cổng / am thờ", "8.440 / 8.400"),
              ("Block hoàn thiện", "3.050 × 930"), ("Lối đi / giữa block", "1.160 / 500"),
              ("Cổng", "1.270, trùng tim lối đi"), ("Tường Tây → block", "300"),
              ("Tên công trình phụ", "AM THỜ"), ("Chuỗi vượt lọt lòng", "không có")]
    yy = ys0 + 9
    for k, v in checks:
        s.text(xk + 3, yy + 2.8, k, size=2.1, anchor="start")
        s.text(xk + 38, yy + 2.8, v, size=2.1, anchor="start")
        s.text(xk + 81, yy + 2.8, "Đạt", size=2.1, weight="bold", col="#0a6b0a")
        yy += 6.3
        s.line(xk, yy - 0.8, xk + 88, yy - 0.8, sw=0.12, col="#999")
    xl_ = 238
    s.line(xl_, ys0, xl_, 287, sw=0.4)
    s.text(xl_ + 3, ys0 + 5, "CHÚ THÍCH", size=3.0, anchor="start", weight="bold")
    items = [("brick", "Xây gạch (tường biên, hộc)"), ("finish", "Hoàn thiện: tô 10 + ốp 10"),
             ("path", "Lối đi giữa 1.160"), ("axis", "Đường tim (gạch chấm)"), ("amtho", "Am thờ – chờ bổ sung")]
    yy = ys0 + 8.5
    for k, lab in items:
        legend_item(s, xl_ + 3, yy, k, lab, size=2.1)
        yy += 9.1
    s.rect(xl_ + 3, yy, 9, 4.5, fill="#d8d2c4", sw=0.25)
    s.text(xl_ + 13.5, yy + 3.1, "Viền ngoài block (phần nổi)", size=2.1, anchor="start")
    xn = 300
    s.line(xn, ys0, xn, 287, sw=0.4)
    s.text(xn + 11, ys0 + 5, "HƯỚNG", size=2.8, weight="bold")
    north_arrow(s, xn + 9, ys0 + 30, 5.5, label_axis=False)
    s.text(xn + 11, ys0 + 42, "TRỤC B9°", size=2.4, weight="bold")
    s.text(xn + 11, ys0 + 50, "Cổng → Am thờ", size=2.0)
    s.text(xn + 11, ys0 + 54, "phương vị 9°", size=1.9)
    s.text(xn + 11, ys0 + 57, "lệch Đông (B9°Đ)", size=1.9)
    s.text(xn + 11, ys0 + 61, "W trên – E dưới", size=2.0)
    title_block(s, 322, ys0, 88, 287 - ys0, "MẶT BẰNG TỔNG THỂ (PB2)", "1/60", "01/02", "LM-01")
    return s.svg()


if __name__ == "__main__":
    import cairosvg, pypdfium2 as pdfium
    f = os.path.join(HERE, "mat-bang-v2.svg")
    open(f, "w", encoding="utf-8").write(page())
    cairosvg.svg2pdf(url=f, write_to=os.path.join(HERE, "mat-bang-v2.pdf"))
    pdfium.PdfDocument(os.path.join(HERE, "mat-bang-v2.pdf"))[0].render(scale=200 / 72).to_pil().save(os.path.join(HERE, "mat-bang-v2.png"))
    print("OK", D_GATE, GAP_E, GAP_E_IN, G1, W_G - G2)
