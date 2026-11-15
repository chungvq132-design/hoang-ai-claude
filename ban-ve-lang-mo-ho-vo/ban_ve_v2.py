# -*- coding: utf-8 -*-
"""BO BAN VE PHIEN BAN 2 (2 trang A3): trang 1 = mat_bang_v2.page(), trang 2 = chi tiet block & mat cat.
Chay: python3 ban_ve_v2.py
"""
import os
from gen import (SVG, hchain, vchain, fmt, frame, arrow, north_arrow, legend_item, title_block, textblock,
                 TILE, FIN, FIN_OP, FIN_TRAT, WALL, HOC_L, HOC_W, N_HOC, H_NOI, D_AM, SLAB, GIANG)
import mat_bang_v2 as mb
from mat_bang_v2 import BL, BT, CORE_L, CORE_T, RIM_END, RIM_SIDE

HERE = os.path.dirname(os.path.abspath(__file__))
XAY_T = HOC_L + 2 * WALL          # 780
assert XAY_T + 2 * FIN == CORE_T and 2 * RIM_SIDE + CORE_T == BT and 2 * RIM_END + CORE_L == BL


def page2():
    s = SVG()
    frame(s)
    k = 0.1

    # ======================= MAT BANG CHI TIET 1 BLOCK =======================
    X0, Y0 = 38, 27
    Pu = lambda u, v: (X0 + u * k, Y0 + v * k)
    s.text(14, 16.5, "MẶT BẰNG CHI TIẾT 1 BLOCK (6 HỘC) – TL 1/10", size=4.4, anchor="start", weight="bold")
    # vien ngoai
    a = Pu(0, 0)
    s.rect(a[0], a[1], BL * k, BT * k, fill="#d8d2c4", sw=0.35)
    # loi: op 10, to 10, xay
    cu, cv = RIM_END, RIM_SIDE
    a = Pu(cu, cv); s.rect(a[0], a[1], CORE_L * k, CORE_T * k, fill=TILE, sw=0.2)
    a = Pu(cu + FIN_OP, cv + FIN_OP); s.rect(a[0], a[1], (CORE_L - 2 * FIN_OP) * k, (CORE_T - 2 * FIN_OP) * k, fill="url(#render)", sw=0.1)
    a = Pu(cu + FIN, cv + FIN); s.rect(a[0], a[1], (CORE_L - 2 * FIN) * k, XAY_T * k, fill="url(#brick2)", sw=0.3)
    hoc_u = []
    for i in range(N_HOC):
        u = cu + FIN + WALL + i * (HOC_W + WALL)
        hoc_u.append(u)
        a = Pu(u, cv + FIN + WALL)
        s.rect(a[0], a[1], HOC_W * k, HOC_L * k, fill="#fff", sw=0.3)
        cx = a[0] + HOC_W * k / 2
        s.text(cx, a[1] + 9, f"HỘC {i + 1}", size=3.2, weight="bold")
        s.text(cx, a[1] + 14.5, "680 × 380", size=2.6)
        s.text(cx, a[1] + 18, "lọt lòng", size=2.1)
        cy = a[1] + HOC_L * k / 2 + 4
        s.circle(cx, cy, 5, sw=0.3, dash="1,0.6")
        s.line(cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, sw=0.2)
        s.line(cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, sw=0.2)
        s.text(cx, cy + 9, "LỖ ÂM DƯƠNG", size=2.0, weight="bold")
        s.text(cx, cy + 11.8, "(KT, vị trí chờ XN)", size=1.8)
    assert hoc_u[-1] + HOC_W + WALL + FIN == BL - RIM_END
    for u0 in (0, BL - RIM_END):
        cx = Pu(u0 + RIM_END / 2, 0)[0]
        s.text(cx - 1.2, Pu(0, BT / 2)[1], "VIỀN NGOÀI 190", size=2.4, rot=-90, weight="bold", col="#444")
        s.text(cx + 2.6, Pu(0, BT / 2)[1], "(phần nổi)", size=2.1, rot=-90, col="#444")
    a = Pu(hoc_u[0] + 40, cv + FIN + WALL)
    vchain(s, [a[1], a[1] + HOC_L * k], a[0] + 1, a[0], ["680"], size=2.6, ext=0, gap=-1, bold=True)
    # duong cat
    xa_ = Pu(hoc_u[3] + HOC_W / 2, 0)[0]
    ybot = Y0 + BT * k
    for yA, yB, ya in ((Y0 - 2.5, Y0 - 0.5, Y0 - 2.5), (ybot + 0.5, ybot + 2.5, ybot + 2.5)):
        s.line(xa_, yA, xa_, yB, sw=0.8)
    s.line(xa_, ybot + 2.5, xa_ - 4, ybot + 2.5, sw=0.3); arrow(s, xa_ - 4, ybot + 2.5, -1, 0, 1.6)
    s.text(xa_ - 6.5, ybot + 3.6, "A", size=3.2, weight="bold")
    yBm = Pu(0, BT / 2)[1]
    for xB0, xB1 in ((X0 - 27, X0 - 23.5), (Pu(BL, 0)[0] + 1.5, Pu(BL, 0)[0] + 5)):
        s.line(xB0, yBm, xB1, yBm, sw=0.8)
        xm = (xB0 + xB1) / 2
        s.line(xm, yBm, xm, yBm - 5, sw=0.3); arrow(s, xm, yBm - 5, 0, -1, 1.6)
        s.text(xm, yBm - 7.2, "B", size=3.2, weight="bold")
    # kich thuoc mat bang
    hchain(s, [Pu(u, 0)[0] for u in (0, RIM_END, BL - RIM_END, BL)], Y0, Y0 - 5.5,
           ["190", "2.670 = 6×380 + 7×50 + 40 (LÕI 6 HỘC HOÀN THIỆN)", "190"], size=2.6, bold=True)
    us = [0, cu, cu + FIN]
    for i in range(N_HOC):
        us += [hoc_u[i], hoc_u[i] + HOC_W]
    us += [BL - RIM_END - FIN, BL - RIM_END, BL]
    hchain(s, [Pu(u, 0)[0] for u in us], ybot, ybot + 7.5, [fmt(us[i + 1] - us[i]) for i in range(len(us) - 1)], size=2.5, bold=True)
    hchain(s, [Pu(0, 0)[0], Pu(BL, 0)[0]], ybot, ybot + 14, ["3.050 – MÉP NGOÀI BLOCK (PHẦN NỔI HOÀN THIỆN)"], size=2.8, bold=True)
    vs = [0, cv, cv + FIN, cv + FIN + WALL, cv + FIN + WALL + HOC_L, cv + FIN + 2 * WALL + HOC_L, cv + CORE_T, BT]
    vchain(s, [Pu(0, v)[1] for v in vs], X0, X0 - 5.5, ["55", "20", "50", "680", "50", "20", "55"], size=2.3, bold=True)
    vchain(s, [Pu(0, cv)[1], Pu(0, cv + CORE_T)[1]], X0, X0 - 12.5, ["820 LÕI"], size=2.4, bold=True)
    vchain(s, [Pu(0, 0)[1], Pu(0, BT)[1]], X0, X0 - 18.5, ["930"], size=2.6, bold=True)

    # ======================= MAT CAT A-A =======================
    Zy = lambda z: 170 - z * k
    xa = 84
    Wa = lambda w: xa + w * k
    s.text(14, 141, "MẶT CẮT A-A", size=4.2, anchor="start", weight="bold")
    s.text(14, 146, "TỶ LỆ 1/10 (cắt qua hộc 4)", size=2.3, anchor="start")
    s.rect(70, Zy(0), Wa(BT) + 14 - 70, 285 - Zy(0), fill="url(#soil)", sw=0)
    s.line(66, Zy(0), Wa(BT) + 18, Zy(0), sw=0.6)
    w_xay0, w_xay1 = RIM_SIDE + FIN, RIM_SIDE + FIN + XAY_T
    s.rect(Wa(w_xay0 + WALL), Zy(H_NOI), HOC_L * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    hole = 100
    wc = BT / 2
    for (w1, w2) in ((0, wc - hole / 2), (wc + hole / 2, BT)):
        s.rect(Wa(w1), Zy(-D_AM), (w2 - w1) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    s.rect(Wa(wc - hole / 2), Zy(-D_AM), hole * k, SLAB * k, fill="#fff", sw=0)
    for w in (wc - hole / 2, wc + hole / 2):
        s.line(Wa(w), Zy(-D_AM) - 1.5, Wa(w), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    for w0 in (w_xay0, w_xay1 - WALL):
        s.rect(Wa(w0), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    # hoan thien phan noi
    s.rect(Wa(RIM_SIDE), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Wa(RIM_SIDE + FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(w_xay1), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(w_xay1 + FIN_TRAT), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    # vien 55 (giang BTCT tren cot nen tam the hien)
    for w0 in (0, BT - RIM_SIDE):
        s.rect(Wa(w0), Zy(0), RIM_SIDE * k, GIANG * k, fill="url(#concrete)", sw=0.3)
    s.text(Wa(wc), Zy(-250), "HỘC MỘ", size=3.2, weight="bold")
    s.text(Wa(wc), Zy(-330), "lọt lòng 680", size=2.5)
    s.text(Wa(wc), Zy(-420), "(không tô trát", size=2.2)
    s.text(Wa(wc), Zy(-470), "phần dưới cốt nền)", size=2.2)
    s.text(Wa(wc), Zy(-800), "LỖ ÂM DƯƠNG", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-850), "XUYÊN TẤM BTCT", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-900), "(KT, vị trí chờ XN)", size=2.1)
    s.line(Wa(wc), Zy(-915), Wa(wc), Zy(-D_AM - 50), sw=0.25)
    arrow(s, Wa(wc), Zy(-D_AM - 50), 0, 1, 1.6)
    yt = Zy(H_NOI)
    hchain(s, [Wa(w) for w in (0, RIM_SIDE, w_xay0, w_xay0 + WALL, w_xay1 - WALL, w_xay1, w_xay1 + FIN, BT)], yt, 156.5,
           ["55", "20", "50", "680 LỌT LÒNG", "50", "20", "55"], size=2.4, bold=True)
    hchain(s, [Wa(w) for w in (w_xay0, w_xay1)], yt, 150.5, ["780 PHỦ BÌ XÂY"], size=2.4, bold=True)
    hchain(s, [Wa(w) for w in (RIM_SIDE, RIM_SIDE + CORE_T)], yt, 144.5, ["820 LÕI SAU HOÀN THIỆN"], size=2.4, bold=True)
    hchain(s, [Wa(0), Wa(BT)], yt, 138.5, ["930 MÉP NGOÀI BLOCK"], size=2.4, bold=True)
    zs = [H_NOI, 0, -D_AM, -D_AM - SLAB]
    vchain(s, [Zy(z) for z in zs], [Wa(RIM_SIDE), Wa(0), Wa(0), Wa(0)], 64, ["100", "1.000 – PHẦN ÂM", "100"], size=2.6, bold=True, gap=0.6)
    for z, v, d in [(H_NOI, "+0.100", "CỐT ĐỈNH BLOCK (NỔI 100)"), (0, "±0.000", "CỐT NỀN HOÀN THIỆN"),
                    (-D_AM, "≈ -1.000", "CỐT ĐÁY HỘC (dự kiến)"), (-D_AM - SLAB, "≈ -1.100", "ĐÁY TẤM BTCT DÀY 100")]:
        y = Zy(z)
        s.line(14, y, 61, y, sw=0.18)
        s.poly([(57, y), (55.4, y - 2.4), (58.6, y - 2.4)], fill="#000", sw=0)
        s.text(14, y - 0.8, v, size=2.8, anchor="start", weight="bold")
        s.text(14, y + 2.9, d, size=1.95, anchor="start")

    def callout(x_from, y, label, x_to=184, size=2.2):
        s.line(x_from, y, x_to - 0.5, y, sw=0.18)
        s.circle(x_from, y, 0.35, fill="#000", sw=0)
        s.text(x_to, y + size * 0.35, label, size=size, anchor="start")
    xr_ = Wa(w_xay1)
    callout(xr_ + 1.5, Zy(85), "ỐP GẠCH 10")
    callout(xr_ + 0.5, Zy(30), "TÔ TRÁT 10")
    callout(Wa(BT) - 2.5, Zy(-75), "VIỀN 55 (chờ XN)")
    callout(xr_ - 2.5, Zy(-300), "TƯỜNG GẠCH 50")
    callout(Wa(BT) + 10, Zy(-560), "ĐẤT NỀN")
    callout(Wa(BT) - 3, Zy(-D_AM - 50), "TẤM BTCT 100")

    # ======================= MAT CAT B-B =======================
    xb = 226
    Ub = lambda u: xb + u * k
    ubrk = RIM_END + FIN + 2 * (WALL + HOC_W) + WALL / 2 + 0     # cat giua tuong thu 3
    s.text(208, 141, "MẶT CẮT B-B (ĐẦU BLOCK)", size=4.0, anchor="start", weight="bold")
    s.text(208, 146, "TỶ LỆ 1/10 – các hộc còn lại lặp lại đến đủ 6 hộc", size=2.3, anchor="start")
    s.rect(208, Zy(0), Ub(ubrk) - 208, 285 - Zy(0), fill="url(#soil)", sw=0)
    s.line(205, Zy(0), Ub(ubrk), Zy(0), sw=0.6)
    hu = [RIM_END + FIN + WALL + i * (HOC_W + WALL) for i in range(2)]
    for u in hu:
        s.rect(Ub(u), Zy(H_NOI), HOC_W * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    cuts = [0]
    for u in hu:
        c = u + HOC_W / 2
        cuts += [c - hole / 2, c + hole / 2]
    cuts.append(ubrk)
    for i in range(0, len(cuts), 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    for i in range(1, len(cuts) - 1, 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="#fff", sw=0)
        for u in (cuts[i], cuts[i + 1]):
            s.line(Ub(u), Zy(-D_AM) - 1.5, Ub(u), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    s.rect(Ub(0), Zy(-GIANG), RIM_END * k, (D_AM - GIANG) * k, fill="url(#brickthe)", sw=0.35)
    s.rect(Ub(0), Zy(0), RIM_END * k, GIANG * k, fill="url(#concrete)", sw=0.35)
    s.text(Ub(95) - 1.2, Zy(-575), "ĐẾ / VIỀN 190 – MÓNG BAO GẠCH THẺ", size=2.3, rot=-90, weight="bold", bg=True)
    s.text(Ub(95) + 2.9, Zy(-575), "(cấu tạo, cao độ chờ XN)", size=2.1, rot=-90, bg=True)
    s.text(Ub(95), Zy(-95), "GIẰNG BTCT", size=2.0, weight="bold", bg=True)
    for u in (RIM_END + FIN, RIM_END + FIN + WALL + HOC_W):
        s.rect(Ub(u), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    u3 = RIM_END + FIN + 2 * (WALL + HOC_W)
    s.rect(Ub(u3), Zy(H_NOI), (ubrk - u3) * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    s.rect(Ub(RIM_END), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Ub(RIM_END + FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    for i in range(2):
        c = Ub(hu[i] + HOC_W / 2)
        s.text(c, Zy(-300), f"HỘC {i + 1}", size=3.0, weight="bold")
        s.text(c, Zy(-370), "lọt lòng 380", size=2.3)
        s.text(c, Zy(-860), "LỖ ÂM DƯƠNG", size=2.1, weight="bold")
        s.text(c, Zy(-905), "(chờ XN)", size=1.9)
        s.line(c, Zy(-920), c, Zy(-D_AM - 50), sw=0.25)
        arrow(s, c, Zy(-D_AM - 50), 0, 1, 1.6)
    xbk = Ub(ubrk)
    s.poly([(xbk, Zy(H_NOI) - 3), (xbk, Zy(-400)), (xbk + 1.8, Zy(-430)), (xbk - 1.8, Zy(-470)), (xbk, Zy(-500)), (xbk, 285)], closed=False, sw=0.3)
    hchain(s, [Ub(u) for u in (0, RIM_END, RIM_END + FIN, hu[0], hu[0] + HOC_W, hu[1], hu[1] + HOC_W)], Zy(H_NOI), 156.5,
           ["190", "20", "50", "380", "50", "380"], size=2.5, bold=True)
    vchain(s, [Zy(0), Zy(-GIANG)], Ub(0), Ub(0) - 7, ["150"], size=2.5, bold=True)

    # ======================= DAI PHAI =======================
    xs_ = 350
    s.line(xs_, 10, xs_, 287, sw=0.5)
    s.text(xs_ + 3, 16, "CHÚ THÍCH VẬT LIỆU", size=2.9, anchor="start", weight="bold")
    items = [("soil", "Đất nền"), ("brick", "Tường xây gạch 50"), ("brickthe", "Móng bao gạch thẻ"),
             ("concrete", "Bê tông cốt thép"), ("render", "Lớp tô trát 10"), ("tile", "Lớp ốp gạch 10"),
             ("hole", "Lỗ âm dương (chờ XN)")]
    yy = 19.5
    for kk, lab in items:
        legend_item(s, xs_ + 3, yy, kk, lab, size=2.15)
        yy += 6.4
    s.rect(xs_ + 3, yy, 9, 4.5, fill="#d8d2c4", sw=0.25)
    s.text(xs_ + 13.5, yy + 3.1, "Viền ngoài block (mặt bằng)", size=2.15, anchor="start")
    yy += 7
    s.line(xs_, yy, 410, yy, sw=0.3)
    s.text(xs_ + 3, yy + 5.5, "GHI CHÚ", size=2.9, anchor="start", weight="bold")
    notes = [
        "1. Kích thước mm, theo kích thước hoàn thiện phần nổi (trên cốt nền).",
        "2. Block hoàn thiện 3.050 × 930 = lõi 6 hộc 2.670 × 820 + viền 190 mỗi đầu, 55 mỗi bên.",
        "3. Lõi: 6×380 + 7×50 + 2×20 = 2.670; 680 + 2×50 = 780 (xây) + 2×20 = 820.",
        "4. Hộc lọt lòng 680×380; tường gạch 50; tô 10 + ốp 10 chỉ ở phần nổi (±0.000 → +0.100); dưới cốt nền không tô.",
        "5. Tấm BTCT chống lún 100 dưới mỗi block; 6 lỗ âm dương/block xuyên tấm, không đổ kín. KT, vị trí lỗ chờ XN.",
        "6. Đế/viền: móng bao gạch thẻ + giằng BTCT ~150. Cấu tạo, cao độ viền 190/55 và khe 20: tạm thể hiện – chờ XN.",
        "7. 780 là KT xây; 820, 930, 3.050 là KT hoàn thiện – không dùng lẫn trong một chuỗi.",
    ]
    textblock(s, xs_ + 3, yy + 10, notes, size=2.0, lh=2.8, nchar=50)
    north_arrow(s, xs_ + 42, 188, 4.5, label_axis=False)
    s.text(xs_ + 3, 186, "Chiều 6 hộc vuông góc", size=2.0, anchor="start")
    s.text(xs_ + 3, 189, "trục B9°", size=2.0, anchor="start")
    title_block(s, xs_, 198, 60, 89, "MẶT BẰNG CHI TIẾT\nBLOCK & MẶT CẮT", "1/10", "02/02", "LM-02", vertical=True, ngay="15/11/2026")
    return s.svg()


if __name__ == "__main__":
    import cairosvg, pypdfium2 as pdfium
    from pypdf import PdfWriter
    pages = [("trang1-mat-bang-tong-the-PB2", mb.page()), ("trang2-chi-tiet-block-mat-cat-PB2", page2())]
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
