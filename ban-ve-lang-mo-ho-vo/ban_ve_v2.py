# -*- coding: utf-8 -*-
"""BO BAN VE PHIEN BAN 2 (2 trang A3): trang 1 = mat_bang_v2.page(), trang 2 = chi tiet block & mat cat.
Chay: python3 ban_ve_v2.py
"""
import os
from gen import (SVG, hchain, vchain, fmt, frame, arrow, north_arrow, legend_item, title_block, textblock,
                 TILE, FIN, FIN_OP, FIN_TRAT, WALL, HOC_L, HOC_W, N_HOC, H_NOI, D_AM, SLAB, GIANG)
import mat_bang_v2 as mb
from mat_bang_v2 import BL, BT, W_SIDE, W_END, XAY_L, XAY_T, SLAB_OV, HOC_X, HOC_Y
HOC_W, HOC_L = HOC_X, HOC_Y      # hoc ve theo kich thuoc thuc te (chi ghi >= 680 x 380)

HERE = os.path.dirname(os.path.abspath(__file__))


def page2():
    s = SVG()
    frame(s)
    k = 0.1
    hole = 100
    # vi tri hoc theo chieu dai block (tu dau block)
    hoc_u = [FIN + W_END + i * (HOC_W + WALL) for i in range(N_HOC)]
    assert abs(hoc_u[-1] + HOC_W + W_END + FIN - BL) < 1e-6

    # ======================= MAT BANG CHI TIET 1 BLOCK =======================
    X0, Y0 = 38, 28
    Pu = lambda u, v: (X0 + u * k, Y0 + v * k)
    s.text(14, 16.5, "MẶT BẰNG CHI TIẾT 1 BLOCK (6 HỘC) – TL 1/10", size=4.4, anchor="start", weight="bold")
    s.text(343, 16.5, "Thân block hoàn thiện 3.050 × 930 – mốc của mọi kích thước bố trí", size=2.4, anchor="end", col="#c00000")
    a = Pu(0, 0); s.rect(a[0], a[1], BL * k, BT * k, fill=TILE, sw=0.35)
    a = Pu(FIN_OP, FIN_OP); s.rect(a[0], a[1], (BL - 2 * FIN_OP) * k, (BT - 2 * FIN_OP) * k, fill="url(#render)", sw=0.1)
    a = Pu(FIN, FIN); s.rect(a[0], a[1], XAY_L * k, XAY_T * k, fill="url(#brick2)", sw=0.3)
    for i, u in enumerate(hoc_u):
        a = Pu(u, FIN + W_SIDE)
        s.rect(a[0], a[1], HOC_W * k, HOC_L * k, fill="#fff", sw=0.3)
        cx = a[0] + HOC_W * k / 2
        s.text(cx, a[1] + 9, f"HỘC {i + 1}", size=3.2, weight="bold")
        s.text(cx, a[1] + 14.5, "đặt tiểu", size=2.3)
        s.text(cx, a[1] + 18, "(≥ 680 × 380)", size=2.0)
        cy = a[1] + HOC_L * k / 2
        s.rect(cx - 5, cy - 5, 10, 10, fill="#fff", sw=0.3, dash="1,0.6")
        s.line(cx - 5, cy - 5, cx + 5, cy + 5, sw=0.2); s.line(cx - 5, cy + 5, cx + 5, cy - 5, sw=0.2)
        s.text(cx, cy + 9, "LỖ ÂM DƯƠNG", size=2.0, weight="bold")
        s.text(cx, cy + 11.8, "100 × 100 (giữa hộc)", size=1.8)
    a = Pu(hoc_u[0] + 40, FIN + W_SIDE)
    # duong cat
    xa_ = Pu(hoc_u[3] + HOC_W / 2, 0)[0]
    ybot = Y0 + BT * k
    s.line(xa_, ybot + 0.5, xa_, ybot + 3, sw=0.8)
    s.line(xa_, ybot + 3, xa_ - 4, ybot + 3, sw=0.3); arrow(s, xa_ - 4, ybot + 3, -1, 0, 1.6)
    s.text(xa_ - 6.5, ybot + 4.1, "A", size=3.2, weight="bold")
    yBm = Pu(0, BT / 2)[1]
    for xB0, xB1 in ((X0 - 27, X0 - 23.5), (Pu(BL, 0)[0] + 1.5, Pu(BL, 0)[0] + 5)):
        s.line(xB0, yBm, xB1, yBm, sw=0.8)
        xm = (xB0 + xB1) / 2
        s.line(xm, yBm, xm, yBm - 5, sw=0.3); arrow(s, xm, yBm - 5, 0, -1, 1.6)
        s.text(xm, yBm - 7.2, "B", size=3.2, weight="bold")
    # kich thuoc
    hchain(s, [Pu(0, 0)[0], Pu(BL, 0)[0]], ybot, ybot + 8, ["3.050 – MÉP NGOÀI BLOCK HOÀN THIỆN"], size=2.8, bold=True)
    vs = [0, FIN, FIN + W_SIDE, FIN + W_SIDE + HOC_L, BT - FIN, BT]
    vchain(s, [Pu(0, 0)[1], Pu(0, BT)[1]], X0, X0 - 18.5, ["930"], size=2.6, bold=True)

    # ======================= MAT CAT A-A =======================
    Zy = lambda z: 170 - z * k
    xa = 82
    Wa = lambda w: xa + w * k
    s.text(14, 141, "MẶT CẮT A-A", size=4.2, anchor="start", weight="bold")
    s.text(14, 146, "TỶ LỆ 1/10 (cắt qua hộc 4)", size=2.3, anchor="start")
    s.rect(Wa(-SLAB_OV - 120), Zy(0), (BT + 2 * SLAB_OV + 240) * k, D_AM * k, fill="url(#sand)", sw=0)
    s.rect(Wa(-SLAB_OV - 120), Zy(-D_AM), (BT + 2 * SLAB_OV + 240) * k, 285 - Zy(-D_AM), fill="url(#soil)", sw=0)
    s.line(Wa(-SLAB_OV - 120), Zy(-D_AM), Wa(BT + SLAB_OV + 120), Zy(-D_AM), sw=0.25, dash="2,1")
    s.line(Wa(-SLAB_OV - 160), Zy(0), Wa(BT + SLAB_OV + 160), Zy(0), sw=0.6)
    w0, w1 = FIN, BT - FIN                      # mep xay
    s.rect(Wa(w0 + W_SIDE), Zy(H_NOI), HOC_L * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    wc = BT / 2
    for (x1, x2) in ((-SLAB_OV, wc - hole / 2), (wc + hole / 2, BT + SLAB_OV)):
        s.rect(Wa(x1), Zy(-D_AM), (x2 - x1) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    s.rect(Wa(wc - hole / 2), Zy(-D_AM), hole * k, SLAB * k, fill="#fff", sw=0)
    for w in (wc - hole / 2, wc + hole / 2):
        s.line(Wa(w), Zy(-D_AM) - 1.5, Wa(w), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    ym = Zy(-D_AM - SLAB / 2)
    for (x1, x2) in ((-SLAB_OV + 25, wc - hole / 2 - 15), (wc + hole / 2 + 15, BT + SLAB_OV - 25)):
        s.line(Wa(x1), ym, Wa(x2), ym, sw=0.35, col="#b00000")
    for xx in range(-SLAB_OV + 40, BT + SLAB_OV - 20, 400):
        if abs(xx - wc) > hole / 2 + 10:
            s.circle(Wa(xx), ym, 0.45, fill="#b00000", sw=0)
    for x in (w0, w1 - W_SIDE):
        s.rect(Wa(x), Zy(H_NOI), W_SIDE * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    s.rect(Wa(0), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Wa(FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(w1), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(w1 + FIN_TRAT), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.text(Wa(wc), Zy(-250), "HỘC MỘ", size=3.2, weight="bold")
    s.text(Wa(wc), Zy(-330), "(đặt tiểu, lọt lòng ≥ 680)", size=2.3)
    s.text(Wa(wc), Zy(-420), "(không tô trát", size=2.2)
    s.text(Wa(wc), Zy(-470), "phần dưới cốt nền)", size=2.2)
    s.text(Wa(wc), Zy(-800), "LỖ ÂM DƯƠNG", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-850), "XUYÊN TẤM BTCT", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-900), "100 × 100, giữa hộc", size=2.1)
    s.line(Wa(wc), Zy(-915), Wa(wc), Zy(-D_AM - 50), sw=0.25)
    arrow(s, Wa(wc), Zy(-D_AM - 50), 0, 1, 1.6)
    yt = Zy(H_NOI)
    hchain(s, [Wa(0), Wa(w0)], yt, 156.5, ["20"], size=2.4, bold=True)
    hchain(s, [Wa(w1), Wa(BT)], yt, 156.5, ["20"], size=2.4, bold=True)
    hchain(s, [Wa(0), Wa(BT)], yt, 144.5, ["930 MÉP NGOÀI BLOCK HOÀN THIỆN"], size=2.4, bold=True)
    ys_ = Zy(-D_AM - SLAB)
    hchain(s, [Wa(-SLAB_OV), Wa(0), Wa(BT), Wa(BT + SLAB_OV)], ys_, ys_ + 4.5, [fmt(SLAB_OV), "930", fmt(SLAB_OV)], size=2.3, bold=True)
    zs = [H_NOI, 0, -D_AM, -D_AM - SLAB]
    xd = Wa(-SLAB_OV) - 6
    vchain(s, [Zy(z) for z in zs], [Wa(0), Wa(0), Wa(-SLAB_OV), Wa(-SLAB_OV)], xd, ["100", "1.000 – PHẦN ÂM", "100"], size=2.6, bold=True, gap=0.6)
    for z, v, d in [(H_NOI, "+0.100", "CỐT ĐỈNH BLOCK (NỔI 100)"), (0, "±0.000", "CỐT NỀN HOÀN THIỆN"),
                    (-D_AM, "≈ -1.000", "CỐT ĐÁY HỘC (dự kiến)"), (-D_AM - SLAB, "≈ -1.100", "ĐÁY TẤM BTCT DÀY 100")]:
        y = Zy(z)
        s.line(14, y, xd - 3, y, sw=0.18)
        s.poly([(xd - 7, y), (xd - 8.6, y - 2.4), (xd - 5.4, y - 2.4)], fill="#000", sw=0)
        s.text(14, y - 0.8, v, size=2.8, anchor="start", weight="bold")
        s.text(14, y + 2.9, d, size=1.95, anchor="start")

    def callout(x_from, y, label, x_to=Wa(BT + SLAB_OV) + 3, size=2.1):
        s.line(x_from, y, x_to - 0.5, y, sw=0.18)
        s.circle(x_from, y, 0.35, fill="#000", sw=0)
        s.text(x_to, y + size * 0.35, label, size=size, anchor="start")
    callout(Wa(BT) - 0.5, Zy(85), "ỐP GẠCH 10")
    callout(Wa(BT) - 1.5, Zy(30), "TÔ TRÁT 10")
    callout(Wa(w1) - 5, Zy(-300), "TƯỜNG GẠCH THẺ 50")
    callout(Wa(BT + 60), Zy(-560), "CÁT SAN LẤP")
    callout(Wa(BT + SLAB_OV + 60), Zy(-1085), "ĐẤT NỀN")
    callout(Wa(BT + SLAB_OV) - 3, Zy(-D_AM - 30), "TẤM BTCT 100, Ø6 a400")

    # ======================= MAT CAT B-B =======================
    xb = 252
    Ub = lambda u: xb + u * k
    ubrk = hoc_u[1] + 150
    s.text(226, 141, "MẶT CẮT B-B (ĐẦU BLOCK)", size=4.0, anchor="start", weight="bold")
    s.text(226, 146, "TỶ LỆ 1/10 – lặp lại đến đủ 6 hộc", size=2.3, anchor="start")
    s.rect(Ub(-SLAB_OV - 100), Zy(0), (ubrk + SLAB_OV + 100) * k, D_AM * k, fill="url(#sand)", sw=0)
    s.rect(Ub(-SLAB_OV - 100), Zy(-D_AM), (ubrk + SLAB_OV + 100) * k, 285 - Zy(-D_AM), fill="url(#soil)", sw=0)
    s.line(Ub(-SLAB_OV - 140), Zy(0), Ub(ubrk), Zy(0), sw=0.6)
    hu = hoc_u[:3]
    s.rect(Ub(hu[0]), Zy(H_NOI), HOC_W * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    s.rect(Ub(hu[1]), Zy(H_NOI), (ubrk - hu[1]) * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    cuts = [-SLAB_OV]
    c = hu[0] + HOC_W / 2
    cuts += [c - hole / 2, c + hole / 2]
    cuts.append(ubrk)
    for i in range(0, len(cuts), 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    for i in range(1, len(cuts) - 1, 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="#fff", sw=0)
        for u in (cuts[i], cuts[i + 1]):
            s.line(Ub(u), Zy(-D_AM) - 1.5, Ub(u), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    s.rect(Ub(FIN), Zy(H_NOI), W_END * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    s.rect(Ub(hu[0] + HOC_W), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    s.rect(Ub(0), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Ub(FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.text(Ub(-SLAB_OV - 60), Zy(-500), "CÁT SAN LẤP", size=2.2, rot=-90, weight="bold", bg=True)
    for i in range(1):
        c = Ub(hu[i] + HOC_W / 2)
        s.text(c, Zy(-300), f"HỘC {i + 1}", size=3.0, weight="bold")
        s.text(c, Zy(-370), "(≥ 380)", size=2.3)
        s.text(c, Zy(-860), "LỖ ÂM DƯƠNG", size=2.1, weight="bold")
        s.text(c, Zy(-905), "100×100", size=1.9)
        s.line(c, Zy(-920), c, Zy(-D_AM - 50), sw=0.25)
        arrow(s, c, Zy(-D_AM - 50), 0, 1, 1.6)
    xbk = Ub(ubrk)
    s.poly([(xbk, Zy(H_NOI) - 3), (xbk, Zy(-400)), (xbk + 1.8, Zy(-430)), (xbk - 1.8, Zy(-470)), (xbk, Zy(-500)), (xbk, 285)], closed=False, sw=0.3)
    hchain(s, [Ub(u) for u in (0, FIN)], Zy(H_NOI), 156.5, ["20"], size=2.5, bold=True)
    hchain(s, [Ub(-SLAB_OV), Ub(0)], ys_, ys_ + 4.5, [fmt(SLAB_OV)], size=2.3, bold=True)

    # ======================= DAI PHAI =======================
    xs_ = 350
    s.line(xs_, 10, xs_, 287, sw=0.5)
    s.text(xs_ + 3, 16, "CHÚ THÍCH VẬT LIỆU", size=2.9, anchor="start", weight="bold")
    yy = 19.5
    for kk, lab in (("sand", "Cát san lấp (±0.000 → -1.000)"), ("soil", "Đất nền"), ("brick", "Tường gạch thẻ 50"), ("concrete", "Bê tông cốt thép"),
                    ("render", "Lớp tô trát 10"), ("tile", "Lớp ốp gạch 10"), ("hole", "Lỗ âm dương 100×100")):
        legend_item(s, xs_ + 3, yy, kk, lab, size=2.15)
        yy += 6.4
    s.line(xs_, yy + 1, 410, yy + 1, sw=0.3)
    s.text(xs_ + 3, yy + 6.5, "GHI CHÚ", size=2.9, anchor="start", weight="bold")
    notes = [
        "1. Kích thước mm. Thân block hoàn thiện 3.050 × 930 (phần nổi, trên cốt nền) là mốc mọi kích thước bố trí.",
        "2. Tất cả tường block (ngăn, dọc, đầu) xây gạch thẻ dày 50, không giằng phía trên. Hộc lọt lòng ≥ 680 × 380 (dự phòng để đặt vừa tiểu – chỉ mô tả).",
        "3. Kích thước tổng thể block 3.050 × 930 theo đo thực tế. Từ ±0.000 xuống -1.000 là cát san lấp; tấm BTCT đặt trên đất nền.",
        "4. Tấm BTCT dày 70÷100 (vẽ 100), lưới thép Ø6 a400 đan 2 chiều; 22 block – 22 tấm.",
        "5. Tô 10 + ốp 10 chỉ ở phần nổi (±0.000 → +0.100); dưới cốt nền không tô.",
        "6. Tấm BTCT rộng hơn block 100 mỗi bên (3.250 × 1.130); chỉ thể hiện ở mặt cắt.",
        "7. 6 lỗ âm dương 100×100/block, giữa hộc, xuyên tấm; không đổ bê tông kín vị trí lỗ.",
    ]
    textblock(s, xs_ + 3, yy + 11, notes, size=2.0, lh=2.8, nchar=50)
    north_arrow(s, xs_ + 42, 188, 4.5, label_axis=False)
    s.text(xs_ + 3, 186, "Chiều 6 hộc vuông góc", size=2.0, anchor="start")
    s.text(xs_ + 3, 189, "trục B9°", size=2.0, anchor="start")
    title_block(s, xs_, 198, 60, 89, "MẶT BẰNG CHI TIẾT\nBLOCK & MẶT CẮT", "1/10", "02/03", "LM-02", vertical=True, ngay="15/11/2026")
    return s.svg()


def page3():
    s = SVG()
    frame(s)
    k = 0.1
    s.text(14, 17, "CHI TIẾT MÓNG TƯỜNG BIÊN – TL 1/10", size=4.4, anchor="start", weight="bold")
    s.text(14, 22.5, "Móng xây gạch thẻ 50 × 100 (bậc 300 / 200, mép ngoài thẳng), trên cùng giằng BTCT dày 150", size=2.4, anchor="start")
    # ---- mat cat mong tuong bien (x = 0 tai mep ngoai, duong vao trong khu dat)
    x0m = 120
    Zy = lambda z: 90 - z * k
    X = lambda x: x0m + x * k
    H_G, H_TR, H_DU = 150, 500, 500
    B_TR, B_DU = 200, 300
    z_top, z_t0, z_t1, z_d1 = H_G, 0, -H_TR, -H_TR - H_DU     # +0.150, 0, -0.500, -1.000
    # trong khu dat: cat san lap 0 -> -1.000, duoi la dat nen
    s.rect(X(B_TR), Zy(0), 700 * k, 1000 * k, fill="url(#sand)", sw=0)
    s.rect(X(B_DU), Zy(z_d1), 600 * k, 0, sw=0)
    s.rect(X(-600), Zy(z_d1), 1500 * k, 350 * k, fill="url(#soil)", sw=0)
    s.line(X(B_TR), Zy(0), X(900), Zy(0), sw=0.6)
    s.line(X(-650), Zy(z_d1), X(0), Zy(z_d1), sw=0.6)
    s.rect(X(0), Zy(z_t1), B_DU * k, H_DU * k, fill="url(#brickthe)", sw=0.4)
    s.rect(X(0), Zy(z_t0), B_TR * k, H_TR * k, fill="url(#brickthe)", sw=0.4)
    s.rect(X(0), Zy(z_top), B_TR * k, H_G * k, fill="url(#concrete)", sw=0.4)
    s.text(X(100), Zy(75) + 1, "GIẰNG", size=2.2, weight="bold", bg=True)
    s.text(X(100), Zy(-250), "GẠCH THẺ", size=2.2, weight="bold", bg=True)
    s.text(X(150), Zy(-750), "GẠCH THẺ", size=2.2, weight="bold", bg=True)
    s.text(X(-330), Zy(-300), "PHÍA NGOÀI", size=2.6, weight="bold", col="#555")
    s.text(X(-330), Zy(-300) + 4, "KHU ĐẤT", size=2.6, weight="bold", col="#555")
    s.text(X(560), Zy(-300), "PHÍA TRONG KHU ĐẤT", size=2.6, weight="bold", col="#555", bg=True)
    s.text(X(560), Zy(-300) + 4, "CÁT SAN LẤP", size=2.4, bg=True)
    s.text(X(100), Zy(z_top) - 3, "(phía trên: tường đá – không thể hiện)", size=2.1, col="#555")
    # kich thuoc
    hchain(s, [X(0), X(B_TR)], Zy(z_top), Zy(z_top) - 9, ["200"], size=2.6, bold=True)
    hchain(s, [X(0), X(B_TR), X(B_DU)], Zy(z_d1), Zy(z_d1) + 8, ["200", "100"], size=2.6, bold=True)
    hchain(s, [X(0), X(B_DU)], Zy(z_d1), Zy(z_d1) + 15, ["300 – BẬC DƯỚI"], size=2.6, bold=True)
    xd = X(B_DU) + 50
    vchain(s, [Zy(z) for z in (z_top, z_t0, z_t1, z_d1)], [X(B_TR), X(B_TR), X(B_DU), X(B_DU)], xd + 4, ["150", "500", "500"], size=2.6, bold=True)
    vchain(s, [Zy(z_t0), Zy(z_d1)], X(B_DU), xd + 12, ["1.000"], size=2.6, bold=True)
    for z, v, d in ((z_top, "+0.150", "đỉnh giằng"), (0, "±0.000", "cốt san lấp / nền"), (z_t1, "≈ -0.500", "đổi bậc móng"), (z_d1, "≈ -1.000", "đáy móng – đất nền")):
        y = Zy(z)
        s.line(xd + 16, y, xd + 52, y, sw=0.18)
        s.poly([(xd + 20, y), (xd + 18.4, y - 2.4), (xd + 21.6, y - 2.4)], fill="#000", sw=0)
        s.text(xd + 23, y - 0.8, v, size=2.7, anchor="start", weight="bold")
        s.text(xd + 23, y + 2.9, d, size=2.0, anchor="start")
    s.text(14, 240, "MẶT CẮT MÓNG TƯỜNG BIÊN – TL 1/10", size=3.4, anchor="start", weight="bold")
    s.text(14, 245, "Mép ngoài 2 bậc móng thẳng hàng; bậc dưới nhô 100 vào phía trong khu đất. Cao độ giằng tạm thể hiện – chờ XN.", size=2.2, anchor="start")

    # ---- chi tiet lo am duong trong 1 hoc
    x0, y0 = 250, 45
    s.text(222, 30, "CHI TIẾT LỖ ÂM DƯƠNG – TL 1/10", size=3.4, anchor="start", weight="bold")
    s.text(222, 35, "(mặt bằng 1 hộc, nhìn xuống tấm BTCT)", size=2.2, anchor="start")
    s.rect(x0 - WALL * k, y0 - WALL * k, (HOC_W + 2 * WALL) * k, (HOC_L + 2 * WALL) * k, fill="url(#brick2)", sw=0.35)
    s.rect(x0, y0, HOC_W * k, HOC_L * k, fill="url(#concrete)", sw=0.35)
    hx, hy = x0 + (HOC_W - 100) / 2 * k, y0 + (HOC_L - 100) / 2 * k
    s.rect(hx, hy, 10, 10, fill="#fff", sw=0.4)
    s.line(hx, hy, hx + 10, hy + 10, sw=0.2); s.line(hx, hy + 10, hx + 10, hy, sw=0.2)
    s.text(x0 + HOC_W * k / 2, hy - 2, "LỖ 100×100", size=2.2, weight="bold", bg=True)
    yb = y0 + HOC_L * k + WALL * k
    hchain(s, [hx, hx + 10], yb, yb + 7, ["100"], size=2.5, bold=True)
    xr = x0 + HOC_W * k + WALL * k
    vchain(s, [hy, hy + 10], xr, xr + 7, ["100"], size=2.5, bold=True)
    s.line(x0, hy + 5, x0 + HOC_W * k, hy + 5, sw=0.2, col="#c00000", dash="3,0.8,0.6,0.8")
    s.line(hx + 5, y0, hx + 5, y0 + HOC_L * k, sw=0.2, col="#c00000", dash="3,0.8,0.6,0.8")
    s.text(x0 + HOC_W * k / 2, y0 + HOC_L * k - 3, "tâm lỗ = tâm hộc", size=2.0, bg=True)
    s.text(222, 152, "Lỗ âm dương 100 × 100 đặt giữa hộc, xuyên suốt", size=2.3, anchor="start")
    s.text(222, 156, "tấm BTCT dày 100; không đổ bê tông kín vị trí lỗ.", size=2.3, anchor="start")
    s.text(222, 160, "6 lỗ / block – tổng 132 lỗ.", size=2.3, anchor="start")

    # ---- dai phai
    xs_ = 350
    s.line(xs_, 10, xs_, 287, sw=0.5)
    s.text(xs_ + 3, 16, "CHÚ THÍCH VẬT LIỆU", size=2.9, anchor="start", weight="bold")
    yy = 19.5
    for kk, lab in (("sand", "Cát san lấp"), ("soil", "Đất nền"), ("brickthe", "Gạch thẻ 50×100 (móng)"), ("brick", "Tường xây gạch"),
                    ("concrete", "Bê tông cốt thép"), ("hole", "Lỗ âm dương 100×100")):
        legend_item(s, xs_ + 3, yy, kk, lab, size=2.15)
        yy += 6.4
    s.line(xs_, yy + 1, 410, yy + 1, sw=0.3)
    s.text(xs_ + 3, yy + 6.5, "GHI CHÚ", size=2.9, anchor="start", weight="bold")
    notes = [
        "1. Kích thước mm, cao độ m.",
        "2. Móng tường biên xây gạch thẻ 50×100: bậc dưới rộng 300 cao ~500, bậc trên rộng 200 cao ~500; mép ngoài 2 bậc thẳng hàng.",
        "3. Phần xây cao 1.000 (từ đất nền -1.000 lên ±0.000); trên cùng giằng BTCT dày 150 rộng 200.",
        "4. Trong khu đất san lấp bằng cát từ ±0.000 xuống -1.000.",
        "5. Phía trên giằng là tường đá – không thể hiện trong bản vẽ này.",
        "6. Lỗ âm dương 100×100 tại tâm mỗi hộc, xuyên tấm BTCT chống lún.",
    ]
    textblock(s, xs_ + 3, yy + 11, notes, size=2.0, lh=2.8, nchar=50)
    title_block(s, xs_, 198, 60, 89, "CHI TIẾT MÓNG\nTƯỜNG BIÊN & LỖ ÂM DƯƠNG", "1/10", "03/03", "LM-03", vertical=True, ngay="15/11/2026")
    return s.svg()


if __name__ == "__main__":
    import cairosvg, pypdfium2 as pdfium
    from pypdf import PdfWriter
    pages = [("trang1-mat-bang-tong-the-PB2", mb.page()), ("trang2-chi-tiet-block-mat-cat-PB2", page2()),
             ("trang3-chi-tiet-mong-tuong-bien-PB2", page3())]
    w = PdfWriter()
    for name, svg in pages:
        f = os.path.join(HERE, name + ".svg")
        open(f, "w", encoding="utf-8").write(svg)
        cairosvg.svg2pdf(url=f, write_to=os.path.join(HERE, name + ".pdf"))
        w.append(os.path.join(HERE, name + ".pdf"))
        pdfium.PdfDocument(os.path.join(HERE, name + ".pdf"))[0].render(scale=200 / 72).to_pil().save(os.path.join(HERE, name + ".png"))
        os.remove(os.path.join(HERE, name + ".pdf"))
    w.write(os.path.join(HERE, "ban-ve-lang-mo-ho-vo-A3-PB2.pdf"))
    print("OK")
