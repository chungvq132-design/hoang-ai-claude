# -*- coding: utf-8 -*-
"""Phieu chot kich thuoc: ban ve so bo, moi kich thuoc gan so thu tu de chu nha tra loi."""
import os
from gen import (SVG, hchain, vchain, fmt, frame, arrow, TILE, PATHFILL,
                 L_TOTAL, L_OUT, L_IN, W_OUT, W_IN, GATE, PATH, BLK_CORE, BLK_HT, BLK_XAY,
                 HOC_W, HOC_L, WALL, FIN, FIN_OP, FIN_TRAT, N_HOC, BASE, H_NOI, D_AM, SLAB, GIANG,
                 BLK_X, ROW_W, ROW_E, Y_AXIS, GATE_Y1, GATE_Y2, W_GAP, E_GAP, CLEAR_IN,
                 D_INNER, D_GATE, GAP_BLK, N_BLK_ROW)

HERE = os.path.dirname(os.path.abspath(__file__))
RED = "#c00000"

ITEMS = [
    ("KHU ĐẤT (lọt lòng)", None, None),
    (1, "Chiều dài khu đất (tường cổng → tường am thờ)", fmt(L_TOTAL)),
    (2, "Chiều rộng đoạn ngoài, gần cổng (Tây → Đông)", fmt(W_OUT)),
    (3, "Chiều rộng đoạn trong, gần am thờ (chỗ tóp)", fmt(W_IN)),
    (4, "Chiều dài đoạn tóp (tính từ tường am thờ)", fmt(L_IN)),
    (5, "Chiều dày tường biên", "chưa có"),
    ("CỔNG – LỐI ĐI", None, None),
    (6, "Cổng rộng thông thủy", fmt(GATE)),
    (7, "Mép cổng → tường Tây", fmt(GATE_Y1)),
    (8, "Lối đi giữa (giữa 2 mép block)", fmt(PATH)),
    ("BỐ TRÍ THEO CHIỀU NGANG", None, None),
    (9, "Tường Tây → mép block dãy trái", fmt(W_GAP)),
    (10, "Tường Đông → mép block dãy phải (đoạn ngoài)", fmt(E_GAP)),
    (11, "Tường Đông → mép block dãy phải (đoạn tóp)", fmt(CLEAR_IN)),
    ("BỐ TRÍ THEO CHIỀU DÀI", None, None),
    (12, "Tường am thờ → mép block đầu tiên", fmt(D_INNER)),
    (13, "Khoảng cách giữa 2 block liền nhau", fmt(GAP_BLK)),
    (14, "Mép block cuối → tường phía cổng", fmt(D_GATE)),
    (15, "Số block mỗi dãy (2 dãy)", str(N_BLK_ROW)),
    ("BLOCK – HỘC", None, None),
    (16, "Block dài (phần nổi, theo chiều 6 hộc)", fmt(BLK_CORE)),
    (17, "Block dày (phần nổi đã tô, ốp)", fmt(BLK_HT)),
    (18, "Hộc lọt lòng – chiều dài", fmt(HOC_L)),
    (19, "Hộc lọt lòng – chiều rộng", fmt(HOC_W)),
    (20, "Tường gạch dày", fmt(WALL)),
    (21, "Hoàn thiện mỗi mặt (tô + ốp)", "20 (10+10)"),
    (22, "Số hộc mỗi block", str(N_HOC)),
    ("MẶT CẮT – ĐẾ", None, None),
    (23, "Phần nổi trên cốt nền", fmt(H_NOI)),
    (24, "Chiều sâu hộc dưới cốt nền", fmt(D_AM)),
    (25, "Tấm BTCT chống lún dày", fmt(SLAB)),
    (26, "Đế nhô ra mỗi đầu block", fmt(BASE)),
    (27, "Giằng BTCT dày", fmt(GIANG)),
    (28, "Lỗ âm dương (đường kính / cạnh)", "chưa có"),
    ("AM THỜ", None, None),
    (29, "Am thờ – chiều dài (dọc trục)", "chưa có"),
    (30, "Am thờ – chiều rộng (ngang trục)", "chưa có"),
    (31, "Am thờ → tường phía trong", "chưa có"),
]


def tag(s, x, y, n, r=2.3):
    s.circle(x, y, r, fill="#fff", sw=0.35, col=RED)
    s.text(x, y + 0.95, str(n), size=2.6 if n < 10 else 2.3, weight="bold", col=RED)


def dimtag(s, xs, yobj, ydim, tags, vertical=False):
    """Chuoi kich thuoc khong ghi so, chi gan so thu tu tren doan can hoi."""
    if vertical:
        vchain(s, xs, yobj, ydim, None)
    else:
        hchain(s, xs, yobj, ydim, None)
    for i, n in tags.items():
        m = (xs[i] + xs[i + 1]) / 2
        if vertical:
            tag(s, ydim - 3.0, m, n)
        else:
            tag(s, m, ydim - 3.0, n)


def page():
    s = SVG()
    frame(s)
    s.text(14, 20, "PHIẾU CHỐT KÍCH THƯỚC – KHU LĂNG MỘ HỌ VÕ", size=5.2, anchor="start", weight="bold")
    s.text(14, 26, "Bản vẽ sơ bộ: mỗi kích thước có 1 số thứ tự (vòng đỏ). Anh trả lời theo số, ghi số đo thực tế vào cột “SỐ ĐO CHỐT”.",
           size=2.6, anchor="start")

    # ================= MAT BANG SO BO 1/80 =================
    S = 1 / 100
    ox, oy = 46, 52
    P = lambda X, Y: (ox + X * S, oy + Y * S)
    t = 200
    s.text(14, 34, "MẶT BẰNG SƠ BỘ (TL ~1/100)", size=3.4, anchor="start", weight="bold")
    a, b = P(0, ROW_W[1]), P(L_TOTAL, ROW_E[0])
    s.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill=PATHFILL, sw=0)
    for (X1, Y1, X2, Y2) in ((-t, -t, L_TOTAL + t, 0), (-t, 0, 0, W_OUT + t), (0, W_OUT, L_OUT + t, W_OUT + t),
                             (L_TOTAL, 0, L_TOTAL + t, W_IN + t), (L_OUT, W_IN, L_TOTAL, W_IN + t), (L_OUT, W_IN, L_OUT + t, W_OUT + t)):
        a1, a2 = P(X1, Y1), P(X2, Y2)
        s.rect(a1[0], a1[1], a2[0] - a1[0], a2[1] - a1[1], fill="#e8b9a4", sw=0)
    pts = [(0, 0), (L_TOTAL, 0), (L_TOTAL, W_IN), (L_OUT, W_IN), (L_OUT, W_OUT), (0, W_OUT)]
    s.poly([P(*p) for p in pts], sw=0.4)
    s.poly([P(*p) for p in [(-t, -t), (L_TOTAL + t, -t), (L_TOTAL + t, W_IN + t), (L_OUT + t, W_IN + t), (L_OUT + t, W_OUT + t), (-t, W_OUT + t)]], sw=0.4)
    g0, g1 = P(-t - 10, GATE_Y1), P(10, GATE_Y2)
    s.rect(g0[0], g0[1] + 0.2, g1[0] - g0[0], g1[1] - g0[1] - 0.4, fill="#fff", sw=0)
    for xl, xr in BLK_X:
        for y0 in (ROW_W[0], ROW_E[0]):
            a = P(xl, y0)
            s.rect(a[0], a[1], BLK_HT * S, BLK_CORE * S, fill="#c4563a", sw=0.25)
            for k in range(N_HOC):
                yy = y0 + FIN + WALL + k * (HOC_W + WALL)
                c = P(xl + FIN + WALL, yy)
                s.rect(c[0], c[1], HOC_L * S, HOC_W * S, fill="#fff", sw=0)
    am0, am1 = P(17000, Y_AXIS - 900), P(18000, Y_AXIS + 900)
    s.rect(am0[0], am0[1], am1[0] - am0[0], am1[1] - am0[1], fill="#fffdf2", sw=0.35, dash="1.2,0.7")
    s.text((am0[0] + am1[0]) / 2, (am0[1] + am1[1]) / 2 + 1, "AM THỜ", size=2.2, weight="bold", rot=-90)
    x1, x2 = P(-500, Y_AXIS), P(L_TOTAL + 400, Y_AXIS)
    s.line(x1[0], x1[1], x2[0], x2[1], sw=0.3, col=RED, dash="5,1,0.7,1")
    s.text(P(1250, 0)[0], P(0, Y_AXIS)[1] - 1.2, "CỔNG", size=2.4, weight="bold")
    s.text(P(9000, 0)[0], P(0, Y_AXIS)[1] - 1.2, "LỐI ĐI GIỮA – TRỤC B9°", size=2.4, weight="bold", col=RED)
    s.text(P(1250, 0)[0], P(0, 1700)[1], "W (Tây) ↑", size=2.2, weight="bold")
    s.text(P(1250, 0)[0], P(0, 6800)[1], "E (Đông) ↓", size=2.2, weight="bold")
    # so block
    bx = P((BLK_X[4][0] + BLK_X[6][1]) / 2, ROW_E[1])
    s.text(bx[0] - 3, bx[1] + 3.6, "11 block / dãy", size=2.2, anchor="end", col="#333")
    tag(s, bx[0], bx[1] + 2.8, 15)
    # tuong bien
    w = P(6000, -t)
    s.line(w[0], w[1] + 1.25, w[0] + 6, w[1] - 3, sw=0.2)
    tag(s, w[0] + 8, w[1] - 3.5, 5)

    ytop = P(0, -t)[1]
    xs = [0, D_GATE]
    for j, (xl, xr) in enumerate(BLK_X):
        if j:
            xs.append(xl)
        xs.append(xr)
    xs.append(L_TOTAL)
    xsp = [P(x, 0)[0] for x in xs]
    dimtag(s, xsp, ytop, ytop - 5.5, {0: 14, 1: 17, 2: 13, len(xs) - 2: 12})
    dimtag(s, [P(0, 0)[0], P(L_TOTAL, 0)[0]], ytop, ytop - 12.5, {0: 1})
    yb = P(0, W_OUT + t)[1] + 6
    dimtag(s, [P(0, 0)[0], P(L_OUT, 0)[0], P(L_TOTAL, 0)[0]], [P(0, W_OUT)[1]] * 2 + [P(0, W_IN)[1]], yb, {1: 4})
    s.text((P(0, 0)[0] + P(L_OUT, 0)[0]) / 2, yb - 1, "(= số 1 trừ số 4)", size=2.0, col="#666")
    xw = P(-t, 0)[0]
    dimtag(s, [P(0, y)[1] for y in (0, GATE_Y1, GATE_Y2, W_OUT)], xw, xw - 5.5, {0: 7, 1: 6}, vertical=True)
    dimtag(s, [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_OUT)], xw, xw - 13, {0: 9, 1: 16, 2: 8, 4: 10}, vertical=True)
    dimtag(s, [P(0, 0)[1], P(0, W_OUT)[1]], xw, xw - 20.5, {0: 2}, vertical=True)
    xe = P(L_TOTAL + t, 0)[0]
    vchain(s, [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_IN)], xe, xe + 6, None)
    tag(s, xe + 9.5, (P(0, ROW_E[1])[1] + P(0, W_IN)[1]) / 2 + 1.5, 11)
    vchain(s, [P(0, 0)[1], P(0, W_IN)[1]], xe, xe + 15, None)
    tag(s, xe + 18.5, P(0, W_IN / 2)[1], 3)
    # am tho
    ya = am1[1] + 3.5
    hchain(s, [am0[0], am1[0]], am1[1], ya, None)
    tag(s, (am0[0] + am1[0]) / 2, ya + 3.2, 29)
    hchain(s, [am1[0], P(L_TOTAL, 0)[0]], am1[1], ya + 7.5, None)
    tag(s, am1[0] + 2.5, ya + 10.8, 31)
    vchain(s, [am0[1], am1[1]], am0[0], am0[0] - 2.5, None)
    tag(s, am0[0] - 5.5, (am0[1] + am1[1]) / 2, 30)

    # ================= CHI TIET BLOCK 1/20 =================
    k = 1 / 25
    X0, Y0 = 30, 205
    s.text(14, 190, "BLOCK & HỘC (sơ bộ ~1/25)", size=3.4, anchor="start", weight="bold")
    Pu = lambda u, v: (X0 + u * k, Y0 + v * k)
    a = Pu(0, 0)
    s.rect(a[0], a[1], BLK_CORE * k, BLK_HT * k, fill=TILE, sw=0.3)
    a = Pu(FIN, FIN)
    s.rect(a[0], a[1], (BLK_CORE - 2 * FIN) * k, BLK_XAY * k, fill="#f2c9b6", sw=0.25)
    hu = []
    for i in range(N_HOC):
        u = FIN + WALL + i * (HOC_W + WALL)
        hu.append(u)
        c = Pu(u, FIN + WALL)
        s.rect(c[0], c[1], HOC_W * k, HOC_L * k, fill="#fff", sw=0.25)
        s.text(c[0] + HOC_W * k / 2, c[1] + HOC_L * k / 2 + 1, f"H{i + 1}", size=2.4, weight="bold", col="#555")
    tag(s, Pu(BLK_CORE, 0)[0] + 4, Y0 - 3, 22)
    s.text(Pu(BLK_CORE, 0)[0] + 7, Y0 - 2.1, "số hộc", size=2.1, anchor="start")
    yo = Y0 + BLK_HT * k
    us = [0, FIN, FIN + WALL, hu[0] + HOC_W, hu[1]]
    dimtag(s, [Pu(u, 0)[0] for u in us], yo, yo + 9, {2: 19})
    tag(s, Pu(0, 0)[0] - 4.5, yo + 9, 21)
    tag(s, Pu(FIN + WALL / 2, 0)[0] + 1, yo + 13.5, 20)
    dimtag(s, [Pu(0, 0)[0], Pu(BLK_CORE, 0)[0]], yo, yo + 21, {0: 16})
    xr = Pu(BLK_CORE, 0)[0]
    vs = [0, FIN + WALL, FIN + WALL + HOC_L, BLK_HT]
    vchain(s, [Pu(0, v)[1] for v in vs], xr, xr + 5, None)
    tag(s, xr + 8.5, Pu(0, FIN + WALL + HOC_L / 2)[1], 18)
    vchain(s, [Pu(0, 0)[1], Pu(0, BLK_HT)[1]], xr, xr + 13, None)
    tag(s, xr + 16.5, Pu(0, BLK_HT / 2)[1] + 6, 17)
    s.text(X0, 272, "Mặt bằng chỉ vẽ phần nổi; đế 200 ở 2 đầu block nằm dưới cốt nền (xem mặt cắt B-B).", size=2.1, anchor="start", col="#555")

    # ================= MAT CAT A-A 1/20 =================
    k = 1 / 25
    zx = 182
    Zy = lambda z: 212 - z * k
    s.text(160, 190, "MẶT CẮT A-A", size=3.0, anchor="start", weight="bold")
    W = lambda w: zx + w * k
    s.rect(W(-300), Zy(0), (BLK_HT + 600) * k, (D_AM + SLAB + 250) * k, fill="url(#soil)", sw=0)
    s.line(W(-350), Zy(0), W(BLK_HT + 350), Zy(0), sw=0.5)
    s.rect(W(FIN + WALL), Zy(H_NOI), HOC_L * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    for w0 in (FIN, FIN + WALL + HOC_L):
        s.rect(W(w0), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="#f2c9b6", sw=0.25)
    s.rect(W(0), Zy(H_NOI), FIN * k, H_NOI * k, fill=TILE, sw=0)
    s.rect(W(FIN + BLK_XAY), Zy(H_NOI), FIN * k, H_NOI * k, fill=TILE, sw=0)
    c = BLK_HT / 2
    for w1, w2 in ((FIN, c - 50), (c + 50, FIN + BLK_XAY)):
        s.rect(W(w1), Zy(-D_AM), (w2 - w1) * k, SLAB * k, fill="url(#concrete)", sw=0.25)
    s.rect(W(c - 50), Zy(-D_AM), 100 * k, SLAB * k, fill="#fff", sw=0)
    tag(s, W(c), Zy(-D_AM) - 4.5, 28)
    s.text(W(c), Zy(-D_AM) - 8.3, "lỗ âm dương", size=1.9)
    vchain(s, [Zy(z) for z in (H_NOI, 0, -D_AM, -D_AM - SLAB)], W(-300), W(-300) - 3, None)
    tag(s, W(-300) - 6, Zy(50) - 4.5, 23)
    tag(s, W(-300) - 6, Zy(-500), 24)
    tag(s, W(-300) - 6, Zy(-1050) + 4.5, 25)
    s.text(W(-300) - 9, Zy(0) + 0.8, "±0.000", size=1.9, anchor="end")

    # ================= MAT CAT B-B (dau block) =================
    bx0 = 232
    Ub = lambda u: bx0 + u * k
    s.text(222, 190, "MẶT CẮT B-B", size=3.0, anchor="start", weight="bold")
    s.rect(Ub(-250), Zy(0), (250 + 560) * k, (D_AM + SLAB + 250) * k, fill="url(#soil)", sw=0)
    s.line(Ub(-280), Zy(0), Ub(560), Zy(0), sw=0.5)
    s.rect(Ub(0), Zy(-GIANG), BASE * k, (D_AM - GIANG) * k, fill="url(#brickthe)", sw=0.25)
    s.rect(Ub(0), Zy(0), BASE * k, GIANG * k, fill="url(#concrete)", sw=0.25)
    s.rect(Ub(BASE), Zy(H_NOI), FIN * k, H_NOI * k, fill=TILE, sw=0)
    s.rect(Ub(BASE + FIN), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="#f2c9b6", sw=0.25)
    s.rect(Ub(BASE + FIN + WALL), Zy(H_NOI), 290 * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    s.rect(Ub(0), Zy(-D_AM), 560 * k, SLAB * k, fill="url(#concrete)", sw=0.25)
    hchain(s, [Ub(0), Ub(BASE)], Zy(H_NOI), Zy(H_NOI) - 4, None)
    tag(s, Ub(BASE / 2), Zy(H_NOI) - 7.2, 26)
    vchain(s, [Zy(0), Zy(-GIANG)], Ub(0), Ub(0) - 3, None)
    tag(s, Ub(0) - 6, Zy(-GIANG / 2), 27)
    s.text(Ub(100), Zy(-600), "ĐẾ", size=2.0, weight="bold", rot=-90)

    # ================= BANG TRA LOI =================
    tx = 268
    s.line(tx - 2, 10, tx - 2, 287, sw=0.5)
    cols = [tx, tx + 9, tx + 84, tx + 106, 410]
    y = 14
    s.rect(tx, y, 410 - tx - 2, 7, fill="#222", sw=0)
    for x, h in zip(cols, ["SỐ", "NỘI DUNG KÍCH THƯỚC", "HIỆN TẠI", "SỐ ĐO CHỐT"]):
        s.text(x + 1.2, y + 4.9, h, size=2.3, anchor="start", weight="bold", col="#fff")
    y += 7
    rh = 6.75
    for n, desc, cur in ITEMS:
        if desc is None:
            s.rect(tx, y, 410 - tx - 2, rh - 1.2, fill="#e9eef6", sw=0)
            s.text(tx + 1.2, y + 4.1, n, size=2.4, anchor="start", weight="bold", col="#1d3d6d")
            y += rh - 1.2
            continue
        tag(s, tx + 4.3, y + rh / 2, n, r=2.2)
        s.text(cols[1] + 1, y + rh / 2 + 0.9, desc, size=2.2, anchor="start")
        s.text(cols[2] + 1, y + rh / 2 + 0.9, cur, size=2.3, anchor="start", weight="bold",
               col="#999" if cur == "chưa có" else "#000")
        s.line(cols[3] + 2, y + rh - 1.6, 406, y + rh - 1.6, sw=0.15, col="#999", dash="0.6,0.6")
        y += rh
        s.line(tx, y, 408, y, sw=0.12, col="#bbb")
    for x in cols[1:4]:
        s.line(x, 14, x, y, sw=0.15, col="#bbb")
    s.text(tx, y + 5, "Đơn vị: mm. Lối đi 8, khoảng 9–14 đo theo mép ngoài phần nổi đã tô, ốp.", size=2.0, anchor="start")
    s.text(tx, y + 8.5, "Trả lời mẫu:  1 ok · 2 8.250 · 5 200 · 29 1.200 ...", size=2.0, anchor="start", col=RED)
    return s.svg()


if __name__ == "__main__":
    import cairosvg
    svg = page()
    f = os.path.join(HERE, "phieu-chot-kich-thuoc.svg")
    open(f, "w", encoding="utf-8").write(svg)
    cairosvg.svg2pdf(url=f, write_to=os.path.join(HERE, "phieu-chot-kich-thuoc.pdf"))
    import pypdfium2 as p
    d = p.PdfDocument(os.path.join(HERE, "phieu-chot-kich-thuoc.pdf"))
    d[0].render(scale=200 / 72).to_pil().save(os.path.join(HERE, "phieu-chot-kich-thuoc.png"))
    print("OK")
