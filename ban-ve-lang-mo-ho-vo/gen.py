# -*- coding: utf-8 -*-
"""Sinh ban ve ky thuat khu lang mo ho Vo (2 trang A3 ngang, SVG don vi mm).
Chay: python3 gen.py  -> trang1.svg, trang2.svg, ban-ve.html
"""
import math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Liberation Sans, Arial, sans-serif"

# ======================= SO LIEU GOC (mm) - KHONG THAY DOI =======================
L_TOTAL, L_OUT, L_IN = 18400, 14480, 3920
W_OUT, W_IN, TOP_E = 8240, 7840, 400
GATE, PATH = 2000, 1200
BLK = 3070                                     # mep ngoai block gom de 200 hai dau (chi o mat cat)
E_GAP, W_GAP = 850, 850                        # CACH 1 (tam tinh): tuong -> mep ngoai phan noi 2.670
HOC_W, HOC_L, WALL, N_HOC = 380, 680, 50, 6
FIN_TRAT, FIN_OP = 10, 10
FIN = FIN_TRAT + FIN_OP                        # 20 / mat
BASE = 200
BLK_CORE = N_HOC * HOC_W + (N_HOC + 1) * WALL + 2 * FIN   # 2.670
BLK_XAY = HOC_L + 2 * WALL                     # 780
BLK_HT = BLK_XAY + 2 * FIN                     # 820
N_BLK_ROW, GAP_BLK, D_INNER, D_GATE = 11, 530, 1580, 2500
H_NOI, D_AM, SLAB, GIANG, MONG_BAO = 100, 1000, 100, 150, 200

# ======================= KIEM TRA SO HOC =======================
assert L_OUT + L_IN == L_TOTAL
assert W_OUT - TOP_E == W_IN
assert BLK_CORE == 2670 and BASE + BLK_CORE + BASE == BLK == 3070
assert E_GAP + BLK_CORE + PATH + BLK_CORE + W_GAP == W_OUT
assert BLK_XAY == 780 and BLK_HT == 820 and HOC_W + 2 * WALL == 480
assert D_INNER + N_BLK_ROW * BLK_HT + (N_BLK_ROW - 1) * GAP_BLK + D_GATE == L_TOTAL
N_BLOCK = 2 * N_BLK_ROW
assert N_BLOCK == 22 and N_BLOCK * N_HOC == 132
# Tim loi di (tinh tu canh Tay, Y huong xuong = phia Dong)
Y_AXIS = W_GAP + BLK_CORE + PATH / 2            # 4.120 = giua canh 8.240
assert Y_AXIS == 4120 == W_OUT / 2
GATE_Y1, GATE_Y2 = Y_AXIS - GATE / 2, Y_AXIS + GATE / 2   # 3.070 .. 5.070
# Block cuoi phia cong khong vuot qua canh ngoai, block dau trong doan tron 3.920 van trong long dat
BLK_X = []   # (x_trai, x_phai) theo kich thuoc hoan thien, X tinh tu canh ngoai (cong)
for i in range(N_BLK_ROW):
    xr = L_TOTAL - D_INNER - i * (BLK_HT + GAP_BLK)
    BLK_X.append((xr - BLK_HT, xr))
BLK_X.sort()
assert BLK_X[0][0] == D_GATE and BLK_X[-1][1] == L_TOTAL - D_INNER
ROW_W = (W_GAP, W_GAP + BLK_CORE)                         # day trai (phia Tay)  850..3520
ROW_E = (W_GAP + BLK_CORE + PATH, W_GAP + 2 * BLK_CORE + PATH)   # day phai (phia Dong) 4720..7390
assert ROW_E[1] <= W_IN  # day phai van nam trong long dat tai doan tron (con 100)
CLEAR_IN = W_IN - ROW_E[1]                      # 100
assert CLEAR_IN == 450
# de 200 (duoi cot nen) van nam trong long dat
assert ROW_W[0] - BASE > 0 and W_IN - (ROW_E[1] + BASE) > 0


def fmt(n):
    n = int(round(n))
    return f"{n:,}".replace(",", ".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ======================= THU VIEN VE SVG =======================
class SVG:
    def __init__(self):
        self.e = []
        self.nclip = 0

    def _hatch(self, kind, clip_inner, bx, by, bw, bh):
        """To ky hieu vat lieu bang hinh hoc that, cat theo clipPath (khong dung pattern de tranh dut net)."""
        tw_, th_, bg, inner = TILES[kind]
        self.nclip += 1
        cid = f"c{self.nclip}"
        out = [f'<clipPath id="{cid}">{clip_inner}</clipPath><g clip-path="url(#{cid})">',
               f'<rect x="{bx:.3f}" y="{by:.3f}" width="{bw:.3f}" height="{bh:.3f}" fill="{bg}"/>']
        x0 = math.floor(bx / tw_) * tw_
        y0 = math.floor(by / th_) * th_
        y = y0
        while y < by + bh:
            x = x0
            while x < bx + bw:
                out.append(f'<use href="#t_{kind}" x="{x:.3f}" y="{y:.3f}"/>')
                x += tw_
            y += th_
        out.append("</g>")
        self.add("".join(out))

    def add(self, s):
        self.e.append(s)

    def line(self, x1, y1, x2, y2, sw=0.25, col="#000", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{col}" stroke-width="{sw}"{d}/>')

    def rect(self, x, y, w, h, fill="none", sw=0.25, col="#000", dash=None, extra=""):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        st = f'stroke="{col}" stroke-width="{sw}"' if sw else 'stroke="none"'
        if fill.startswith("url(#"):
            self._hatch(fill[5:-1], f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}"/>', x, y, w, h)
            fill = "none"
        self.add(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" {st}{d} {extra}/>')

    def poly(self, pts, fill="none", sw=0.25, col="#000", closed=True, dash=None):
        p = " ".join(f"{x:.3f},{y:.3f}" for x, y in pts)
        tag = "polygon" if closed else "polyline"
        d = f' stroke-dasharray="{dash}"' if dash else ""
        st = f'stroke="{col}" stroke-width="{sw}"' if sw else 'stroke="none"'
        self.add(f'<{tag} points="{p}" fill="{fill}" {st}{d} stroke-linejoin="miter"/>')

    def path(self, d, fill="none", sw=0.25, col="#000", rule="nonzero", dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        st = f'stroke="{col}" stroke-width="{sw}"' if sw else 'stroke="none"'
        if fill.startswith("url(#"):
            nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
            xs_, ys_ = nums[0::2], nums[1::2]
            self._hatch(fill[5:-1], f'<path d="{d}" clip-rule="{rule}"/>', min(xs_), min(ys_), max(xs_) - min(xs_), max(ys_) - min(ys_))
            fill = "none"
        self.add(f'<path d="{d}" fill="{fill}" fill-rule="{rule}" {st}{da}/>')

    def circle(self, cx, cy, r, fill="none", sw=0.25, col="#000", dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r:.3f}" fill="{fill}" stroke="{col}" stroke-width="{sw}"{d}/>')

    def text(self, x, y, s, size=3.0, anchor="middle", rot=0, weight="normal", col="#000", bg=False, italic=False):
        tr = f' transform="rotate({rot} {x:.3f} {y:.3f})"' if rot else ""
        if bg:
            w = tw(s, size) + 0.8
            h = size * 1.05
            if anchor == "middle":
                bx = x - w / 2
            elif anchor == "end":
                bx = x - w + 0.4
            else:
                bx = x - 0.4
            self.add(f'<rect x="{bx:.3f}" y="{y - size * 0.85:.3f}" width="{w:.3f}" height="{h:.3f}" fill="#fff"{tr}/>')
        it = ' font-style="italic"' if italic else ""
        self.add(f'<text x="{x:.3f}" y="{y:.3f}" font-family="{FONT}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}" fill="{col}"{it}{tr}>{esc(s)}</text>')

    def svg(self, w=420, h=297):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">'
                + DEFS + '<rect x="0" y="0" width="420" height="297" fill="#fff"/>' + "\n".join(self.e) + "</svg>")


def tw(s, size):
    """Uoc luong chieu dai chu (mm)."""
    w = 0
    for c in s:
        if c in " .,:;-–()/=+×≈±'":
            w += 0.36
        elif c.isupper():
            w += 0.68
        else:
            w += 0.60
    return w * size


DEFS = """<defs>
<pattern id="brick" patternUnits="userSpaceOnUse" width="1.4" height="1.4">
 <rect width="1.4" height="1.4" fill="#f2c9b6"/><path d="M0 1.4 L1.4 0 M-0.7 0.7 L0.7 -0.7 M0.7 2.0999999999999996 L2.0999999999999996 0.7" stroke="#9c3b1f" stroke-width="0.2"/></pattern>
<pattern id="brick2" patternUnits="userSpaceOnUse" width="2.2" height="2.2">
 <rect width="2.2" height="2.2" fill="#f2c9b6"/><path d="M0 2.2 L2.2 0 M-1.1 1.1 L1.1 -1.1 M1.1 3.3000000000000003 L3.3000000000000003 1.1" stroke="#9c3b1f" stroke-width="0.25"/></pattern>
<pattern id="brickthe" patternUnits="userSpaceOnUse" width="4" height="2">
 <rect width="4" height="2" fill="#efbfa5"/><path d="M0 0H4M0 1H4M1 0V1M3 1V2" stroke="#8a2f14" stroke-width="0.2"/>
 <line x1="0" y1="2" x2="2" y2="0" stroke="#8a2f14" stroke-width="0.15"/></pattern>
<pattern id="concrete" patternUnits="userSpaceOnUse" width="4" height="4">
 <rect width="4" height="4" fill="#d6d9de"/>
 <path d="M0.6 1.2 L1.5 0.5 L1.7 1.5 Z M2.6 2.6 L3.5 2.3 L3.0 3.4 Z" fill="none" stroke="#333" stroke-width="0.15"/>
 <circle cx="2.8" cy="0.9" r="0.22" fill="#333"/><circle cx="0.9" cy="3.1" r="0.22" fill="#333"/><circle cx="2.0" cy="1.9" r="0.15" fill="#333"/></pattern>
<pattern id="sand" patternUnits="userSpaceOnUse" width="3" height="3">
 <rect width="3" height="3" fill="#fbf1c7"/>
 <circle cx="0.6" cy="0.7" r="0.18" fill="#9a7b2f"/><circle cx="2.1" cy="1.2" r="0.14" fill="#9a7b2f"/><circle cx="1.2" cy="2.3" r="0.2" fill="#9a7b2f"/><circle cx="2.6" cy="2.6" r="0.12" fill="#9a7b2f"/></pattern>
<pattern id="soil" patternUnits="userSpaceOnUse" width="5" height="5">
 <rect width="5" height="5" fill="#f1e7cf"/>
 <path d="M0.5 2 L2 0.5 M1.2 2.4 L2.7 0.9 M1.9 2.8 L3.4 1.3 M2.5 4.8 L4.0 3.3" stroke="#7b5a2c" stroke-width="0.2"/>
 <circle cx="4.2" cy="1" r="0.18" fill="#7b5a2c"/><circle cx="0.8" cy="4.2" r="0.18" fill="#7b5a2c"/></pattern>
<pattern id="render" patternUnits="userSpaceOnUse" width="0.8" height="0.8">
 <rect width="0.8" height="0.8" fill="#f6e27a"/><circle cx="0.4" cy="0.4" r="0.12" fill="#8a7300"/></pattern>
<pattern id="solid" patternUnits="userSpaceOnUse" width="1.6" height="1.6">
 <rect width="1.6" height="1.6" fill="#4a4a4a"/><path d="M0 1.6 L1.6 0 M-0.8 0.8 L0.8 -0.8 M0.8 2.4000000000000004 L2.4000000000000004 0.8 M0 0 L1.6 1.6 M-0.8 0.8 L0.8 2.4000000000000004 M0.8 -0.8 L2.4000000000000004 0.8" stroke="#bdbdbd" stroke-width="0.16"/></pattern>
<pattern id="solid2" patternUnits="userSpaceOnUse" width="3.0" height="3.0">
 <rect width="3.0" height="3.0" fill="#4a4a4a"/><path d="M0 3.0 L3.0 0 M-1.5 1.5 L1.5 -1.5 M1.5 4.5 L4.5 1.5 M0 0 L3.0 3.0 M-1.5 1.5 L1.5 4.5 M1.5 -1.5 L4.5 1.5" stroke="#c8c8c8" stroke-width="0.22"/></pattern>
</defs>"""
TILES = {}
for _m in re.finditer(r'<pattern id="(\w+)"[^>]*width="([\d.]+)" height="([\d.]+)">\s*<rect [^>]*fill="([^"]+)"/>(.*?)</pattern>', DEFS, re.S):
    TILES[_m.group(1)] = (float(_m.group(2)), float(_m.group(3)), _m.group(4), _m.group(5))
DEFS = "<defs>" + "".join(f'<g id="t_{k}">{v[3]}</g>' for k, v in TILES.items()) + "</defs>"
TILE = "#2f62a8"
PATHFILL = "#eef3e6"


def arrow(svg, x, y, dx, dy, L=2.0, W=0.55, col="#000"):
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = x - ux * L, y - uy * L
    px, py = -uy * W, ux * W
    svg.poly([(x, y), (bx + px, by + py), (bx - px, by - py)], fill=col, sw=0)


def hchain(svg, xs, yobj, ydim, labels=None, size=2.8, L=2.0, ext=1.5, gap=0.8, sw=0.18, lift_dir=-1, bold=False):
    """Chuoi kich thuoc ngang. xs: toa do giay; yobj: y diem dong (so hoac list)."""
    if not isinstance(yobj, (list, tuple)):
        yobj = [yobj] * len(xs)
    for x, yo in zip(xs, yobj):
        s = 1 if ydim > yo else -1
        svg.line(x, yo + s * gap, x, ydim + s * ext, sw=sw)
    svg.line(xs[0], ydim, xs[-1], ydim, sw=sw)
    for i in range(len(xs) - 1):
        x1, x2 = xs[i], xs[i + 1]
        span = x2 - x1
        if span >= 2 * L + 0.8:
            arrow(svg, x1, ydim, -1, 0, L)
            arrow(svg, x2, ydim, 1, 0, L)
        else:
            arrow(svg, x1, ydim, 1, 0, L * 0.8)
            arrow(svg, x2, ydim, -1, 0, L * 0.8)
            if i == 0:
                svg.line(x1 - L - 1, ydim, x1, ydim, sw=sw)
            if i == len(xs) - 2:
                svg.line(x2, ydim, x2 + L + 1, ydim, sw=sw)
        lab = labels[i] if labels else None
        if lab is None:
            continue
        t = lab
        w = tw(t, size)
        y = ydim - 0.7
        if w > span - 0.6:
            y = ydim - 0.7 - size * 1.0 if lift_dir < 0 else ydim + size + 0.9
        svg.text((x1 + x2) / 2, y, t, size=size, weight="bold" if bold else "normal")


def vchain(svg, ys, xobj, xdim, labels=None, size=2.8, L=2.0, ext=1.5, gap=0.8, sw=0.18, bold=False):
    if not isinstance(xobj, (list, tuple)):
        xobj = [xobj] * len(ys)
    for y, xo in zip(ys, xobj):
        s = 1 if xdim > xo else -1
        svg.line(xo + s * gap, y, xdim + s * ext, y, sw=sw)
    svg.line(xdim, ys[0], xdim, ys[-1], sw=sw)
    for i in range(len(ys) - 1):
        y1, y2 = ys[i], ys[i + 1]
        span = y2 - y1
        if span >= 2 * L + 0.8:
            arrow(svg, xdim, y1, 0, -1, L)
            arrow(svg, xdim, y2, 0, 1, L)
        else:
            arrow(svg, xdim, y1, 0, 1, L * 0.8)
            arrow(svg, xdim, y2, 0, -1, L * 0.8)
            if i == 0:
                svg.line(xdim, y1 - L - 1, xdim, y1, sw=sw)
            if i == len(ys) - 2:
                svg.line(xdim, y2, xdim, y2 + L + 1, sw=sw)
        lab = labels[i] if labels else None
        if lab is None:
            continue
        w = tw(lab, size)
        x = xdim - 0.7
        if w > span - 0.6:
            x = xdim - 0.7 - size * 1.0
        svg.text(x, (y1 + y2) / 2, lab, size=size, rot=-90, weight="bold" if bold else "normal")


def frame(svg):
    svg.rect(5, 5, 410, 287, sw=0.25)
    svg.rect(10, 10, 400, 277, sw=0.7)


def wrap(s, n):
    out, cur = [], ""
    for w in s.split(" "):
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = "   " + w if out or True else w
        else:
            cur = (cur + " " + w) if cur else w
    if cur:
        out.append(cur)
    return out


def textblock(svg, x, y, lines, size=2.4, lh=None, nchar=90, weight="normal"):
    lh = lh or size * 1.38
    for ln in lines:
        for i, part in enumerate(wrap(ln, nchar)):
            svg.text(x, y, part, size=size, anchor="start", weight=weight)
            y += lh
    return y


def title_block(svg, x, y, w, h, ten_bv, tyle, to, kyhieu, vertical=False, ngay="14/11/2026"):
    svg.rect(x, y, w, h, sw=0.6)
    rows = [
        ("CÔNG TRÌNH", "KHU LĂNG MỘ HỌ VÕ", 3.6, True),
        ("TÊN BẢN VẼ", ten_bv, 2.9, True),
        ("TỶ LỆ", tyle, 2.8, False),
        ("KHỔ GIẤY / ĐƠN VỊ", "A3 ngang – mm (cao độ: m)", 2.5, False),
        ("KÝ HIỆU / TỜ", f"{kyhieu}   –   TỜ {to}", 2.8, True),
        ("THIẾT KẾ", "........................", 2.5, False),
        ("KIỂM TRA", "........................", 2.5, False),
        ("CHỦ ĐẦU TƯ", "........................", 2.5, False),
        ("NGÀY", ngay, 2.5, False),
    ]
    rh = h / len(rows)
    lw = 0.34 * w if not vertical else w
    for i, (k, v, sz, b) in enumerate(rows):
        yy = y + i * rh
        if i:
            svg.line(x, yy, x + w, yy, sw=0.25)
        if vertical:
            svg.text(x + 1.2, yy + 2.6, k, size=1.8, anchor="start", col="#444")
            lines = v.split("\n")
            for j, l in enumerate(lines):
                svg.text(x + 1.2, yy + 2.6 + (j + 1) * sz * 1.15, l, size=sz, anchor="start", weight="bold" if b else "normal")
        else:
            svg.text(x + 1.2, yy + rh / 2 + 0.8, k, size=2.0, anchor="start", col="#444")
            lines = v.split("\n")
            y0 = yy + rh / 2 + 1.0 - (len(lines) - 1) * sz * 0.55
            for j, l in enumerate(lines):
                svg.text(x + lw + 1.2, y0 + j * sz * 1.1, l, size=sz, anchor="start", weight="bold" if b else "normal")
    if not vertical:
        svg.line(x + lw, y, x + lw, y + h, sw=0.25)


def north_arrow(svg, cx, cy, r, label_axis=True):
    """Truc cong->am tho la B9°D (phuong vi 9°, theo la ban do tai hien truong): huong Bac lech 9° nguoc chieu kim dong ho so voi truc (+x)."""
    a = math.radians(9)
    ux, uy = math.cos(a), -math.sin(a)       # huong Bac tren giay
    svg.circle(cx, cy, r, sw=0.35)
    # truc
    svg.line(cx - r * 1.05, cy, cx + r * 1.25, cy, sw=0.25, dash="3,0.8,0.6,0.8")
    # mui ten bac
    tipx, tipy = cx + ux * r * 1.15, cy + uy * r * 1.15
    tx, ty = cx - ux * r * 0.75, cy - uy * r * 0.75
    px, py = -uy, ux
    W = r * 0.28
    svg.poly([(tipx, tipy), (tx + px * W, ty + py * W), (cx, cy), (tx - px * W, ty - py * W)], fill="#fff", sw=0.3)
    svg.poly([(tipx, tipy), (tx + px * W, ty + py * W), (cx, cy)], fill="#000", sw=0.3)
    svg.text(tipx - 1.0, tipy - 2.6, "B (N)", size=2.8, weight="bold")
    # cung goc 9°
    rr = r * 0.95
    x1, y1 = cx + rr, cy
    x2, y2 = cx + ux * rr, cy + uy * rr
    svg.path(f"M{x1:.3f},{y1:.3f} A{rr:.3f},{rr:.3f} 0 0 0 {x2:.3f},{y2:.3f}", sw=0.25)
    if label_axis:
        svg.text(cx + r * 0.2, cy + r * 0.62, "TRỤC B9°", size=2.4, weight="bold", anchor="start")


def legend_item(svg, x, y, kind, label, size=2.3):
    w, h = 9, 4.5
    if kind == "brick":
        svg.rect(x, y, w, h, fill="url(#brick2)", sw=0.25)
    elif kind == "brickthe":
        svg.rect(x, y, w, h, fill="url(#brickthe)", sw=0.25)
    elif kind == "concrete":
        svg.rect(x, y, w, h, fill="url(#concrete)", sw=0.25)
    elif kind == "sand":
        svg.rect(x, y, w, h, fill="url(#sand)", sw=0.25)
    elif kind == "soil":
        svg.rect(x, y, w, h, fill="url(#soil)", sw=0.25)
    elif kind == "render":
        svg.rect(x, y, w, h, fill="url(#render)", sw=0.25)
    elif kind == "tile":
        svg.rect(x, y, w, h, fill=TILE, sw=0.25)
    elif kind == "solid":
        svg.rect(x, y, w, h, fill="url(#solid2)", sw=0.25)
    elif kind == "path":
        svg.rect(x, y, w, h, fill=PATHFILL, sw=0.25)
    elif kind == "hole":
        svg.rect(x, y, w, h, fill="#fff", sw=0.25)
        svg.circle(x + w / 2, y + h / 2, 1.8, sw=0.3, dash="0.8,0.5")
        svg.line(x + w / 2 - 1.3, y + h / 2 - 1.3, x + w / 2 + 1.3, y + h / 2 + 1.3, sw=0.2)
        svg.line(x + w / 2 - 1.3, y + h / 2 + 1.3, x + w / 2 + 1.3, y + h / 2 - 1.3, sw=0.2)
    elif kind == "axis":
        svg.line(x, y + h / 2, x + w, y + h / 2, sw=0.3, col="#c00000", dash="3,0.8,0.6,0.8")
    elif kind == "amtho":
        svg.rect(x, y, w, h, sw=0.35, dash="1.2,0.7")
    elif kind == "finish":
        svg.rect(x, y, w, h, fill=TILE, sw=0.25)
        svg.rect(x + 0.8, y + 0.8, w - 1.6, h - 1.6, fill="url(#brick2)", sw=0.1)
    svg.text(x + w + 1.5, y + h / 2 + size * 0.36, label, size=size, anchor="start")


# =====================================================================================
#                                       TRANG 1
# =====================================================================================
def page1():
    s = SVG()
    frame(s)
    S = 1 / 60
    ox, oy = 50, 52
    P = lambda X, Y: (ox + X * S, oy + Y * S)
    t = 200  # chieu day tuong bien the hien tuong trung

    s.text(14, 21, "MẶT BẰNG TỔNG THỂ KHU LĂNG MỘ HỌ VÕ", size=5.5, anchor="start", weight="bold")
    s.text(14, 27.5, "TỶ LỆ 1/60  –  22 BLOCK × 6 HỘC = 132 HỘC", size=3.4, anchor="start", weight="bold")
    s.text(405, 20, "MỌI KÍCH THƯỚC BỐ TRÍ ĐO THEO MÉP NGOÀI PHẦN NỔI ĐÃ TÔ, ỐP CỦA BLOCK", size=2.9, anchor="end", weight="bold", col="#c00000")
    s.text(405, 25, "(block phần nổi 2.670 × 820 – đế BTCT 200 và phần chìm chỉ thể hiện ở mặt cắt)", size=2.4, anchor="end", col="#c00000")

    # ---- nen loi di giua
    x0, y0 = P(0, ROW_W[1])
    x1, y1 = P(L_TOTAL, ROW_E[0])
    s.rect(x0, y0, x1 - x0, y1 - y0, fill=PATHFILL, sw=0)

    # ---- tuong bien (evenodd)
    out = [(-t, -t), (L_TOTAL + t, -t), (L_TOTAL + t, W_IN + t), (L_OUT + t, W_IN + t), (L_OUT + t, W_OUT + t), (-t, W_OUT + t)]
    inn = [(0, 0), (L_TOTAL, 0), (L_TOTAL, W_IN), (L_OUT, W_IN), (L_OUT, W_OUT), (0, W_OUT)]
    def pd(pts):
        return "M" + " L".join(f"{P(*p)[0]:.3f},{P(*p)[1]:.3f}" for p in pts) + " Z"
    for (X1, Y1, X2, Y2) in ((-t, -t, L_TOTAL + t, 0), (-t, 0, 0, W_OUT + t), (0, W_OUT, L_OUT + t, W_OUT + t),
                             (L_TOTAL, 0, L_TOTAL + t, W_IN + t), (L_OUT, W_IN, L_TOTAL, W_IN + t), (L_OUT, W_IN, L_OUT + t, W_OUT + t)):
        a1, a2 = P(X1, Y1), P(X2, Y2)
        s.rect(a1[0], a1[1], a2[0] - a1[0], a2[1] - a1[1], fill="url(#brick)", sw=0)
    s.path(pd(out) + " " + pd(inn), fill="none", sw=0.45)
    # o cong
    gx0, gy0 = P(-t - 20, GATE_Y1)
    gx1, gy1 = P(20, GATE_Y2)
    s.rect(gx0, gy0, gx1 - gx0, gy1 - gy0, fill="#fff", sw=0)
    s.rect(*P(0, GATE_Y1), 0.1, 0, sw=0)
    for gy in (GATE_Y1, GATE_Y2):
        a, b = P(-t, gy), P(0, gy)
        s.line(a[0], a[1], b[0], b[1], sw=0.45)
    # canh cong (cua 2 canh) - net manh
    for gy, sgn in ((GATE_Y1, 1), (GATE_Y2, -1)):
        a = P(0, gy)
        r = (GATE / 2) * S
        s.line(a[0], a[1], a[0] + r * math.cos(math.radians(60)), a[1] + sgn * r * math.sin(math.radians(60)), sw=0.3)
        ex, ey = a[0] + r * math.cos(math.radians(60)), a[1] + sgn * r * math.sin(math.radians(60))
    # mieng cong ve net dut
    a, b = P(-t / 2, GATE_Y1), P(-t / 2, GATE_Y2)
    s.line(a[0], a[1], b[0], b[1], sw=0.18, dash="1,0.7")

    # ---- block
    def draw_block(xl, yt):
        # xl: X trai (hoan thien), yt: Y tren (mep ngoai block, gom mong/de)
        # mong / de 2 dau
        # chi ve phan noi 2.670 (de BTCT 200 hai dau chi the hien o mat cat)
        yt = yt - BASE
        a = P(xl, yt + BASE)
        s.rect(a[0], a[1], BLK_HT * S, BLK_CORE * S, fill=TILE, sw=0)
        a = P(xl + FIN, yt + BASE + FIN)
        s.rect(a[0], a[1], BLK_XAY * S, (BLK_CORE - 2 * FIN) * S, fill="#c4563a", sw=0)
        for k in range(N_HOC):
            yy = yt + BASE + FIN + WALL + k * (HOC_W + WALL)
            a = P(xl + FIN + WALL, yy)
            s.rect(a[0], a[1], HOC_L * S, HOC_W * S, fill="#fff", sw=0.08)
        a = P(xl, yt + BASE)
        s.rect(a[0], a[1], BLK_HT * S, BLK_CORE * S, sw=0.35)

    for j, (xl, xr) in enumerate(BLK_X):
        draw_block(xl, ROW_W[0])
        draw_block(xl, ROW_E[0])
        cx = P((xl + xr) / 2, 0)[0]
        s.text(cx, P(0, ROW_W[1] + 210)[1], f"T{j + 1}", size=2.3, weight="bold", col="#333")
        s.text(cx, P(0, ROW_E[0] - 70)[1], f"P{j + 1}", size=2.3, weight="bold", col="#333")

    # ---- am tho (tuong trung, khong kich thuoc)
    a = P(16960, Y_AXIS - 950)
    b = P(18260, Y_AXIS + 950)
    s.rect(a[0], a[1], b[0] - a[0], b[1] - a[1], fill="#fffdf2", sw=0.4, dash="1.4,0.8")
    cx = (a[0] + b[0]) / 2
    s.text(cx, a[1] + 7.0, "AM THỜ", size=3.6, weight="bold")
    s.text(cx, a[1] + 12.5, "– KÍCH THƯỚC", size=2.3)
    s.text(cx, a[1] + 15.6, "CHỜ BỔ SUNG", size=2.3)
    s.text(cx, b[1] - 2.0, "(tượng trưng)", size=1.9, italic=True, col="#555")

    # ---- truc tim
    a, b = P(-650, Y_AXIS), P(L_TOTAL + 450, Y_AXIS)
    s.line(a[0], a[1], b[0], b[1], sw=0.35, col="#c00000", dash="6,1.2,0.8,1.2")
    s.text(P(9200, 0)[0], P(0, Y_AXIS)[1] - 1.2, "TRỤC CỔNG – LỐI ĐI – AM THỜ: B9°", size=3.0, weight="bold", col="#c00000")
    s.text(P(9200, 0)[0], P(0, Y_AXIS)[1] + 4.0, "LỐI ĐI GIỮA – RỘNG THÔNG THỦY 1.200", size=2.5, col="#1d4d1d")
    s.text(P(1250, 0)[0], P(0, Y_AXIS)[1] - 1.2, "CỔNG VÀO", size=2.8, weight="bold")
    s.text(P(1250, 0)[0], P(0, Y_AXIS)[1] + 3.6, "→ hướng B9°", size=2.2)

    # chu thich day block
    for (y_txt, l1) in ((1500, "DÃY TRÁI (PHÍA TÂY)"), (5800, "DÃY PHẢI (PHÍA ĐÔNG)")):
        px_, py_ = P(1250, y_txt)
        s.text(px_, py_, l1, size=2.2, weight="bold")
        s.text(px_, py_ + 3.3, "11 BLOCK × 6 HỘC", size=2.2)
        s.text(px_, py_ + 6.6, "= 66 HỘC", size=2.2)
    px_, py_ = P(1250, 7300)
    s.text(px_, py_, "Đế BTCT 200 hai đầu block:", size=1.9, italic=True)
    s.text(px_, py_ + 2.8, "chỉ thể hiện ở mặt cắt", size=1.9, italic=True)

    # ---- KICH THUOC TREN (canh Tay)
    ywall_top = P(0, -t)[1]
    xs = [0]
    labs = []
    xs.append(D_GATE); labs.append(fmt(D_GATE))
    for j, (xl, xr) in enumerate(BLK_X):
        if j:
            xs.append(xl); labs.append(fmt(GAP_BLK))
        xs.append(xr); labs.append(fmt(BLK_HT))
    xs.append(L_TOTAL); labs.append(fmt(D_INNER))
    assert len(labs) == 1 + 11 + 10 + 1
    hchain(s, [P(x, 0)[0] for x in xs], ywall_top, ywall_top - 6.5, labs, size=2.8, bold=True)
    hchain(s, [P(0, 0)[0], P(L_TOTAL, 0)[0]], ywall_top, ywall_top - 14,
           ["18.400 – TỔNG CHIỀU DÀI LỌT LÒNG  (CẠNH TÂY W THẲNG SUỐT)"], size=3.0, bold=True)
    # nhan 2.500 & 1.580
    s.text(P(D_GATE / 2, 0)[0], ywall_top - 2.2, "khoảng phía cổng", size=1.8, italic=True)
    s.text(P(L_TOTAL - D_INNER / 2, 0)[0], ywall_top - 2.2, "tường trong → block đầu", size=1.8, italic=True)

    # ---- KICH THUOC DUOI (canh Dong)
    yb = P(0, W_OUT + t)[1] + 7
    hchain(s, [P(0, 0)[0], P(L_OUT, 0)[0], P(L_TOTAL, 0)[0]],
           [P(0, W_OUT)[1], P(0, W_OUT)[1], P(0, W_IN)[1]], yb,
           ["14.480 – ĐOẠN PHÍA NGOÀI (GẦN CỔNG)", "3.920 – ĐOẠN TRONG"], size=3.0, bold=True)
    s.text(P(L_TOTAL / 2, 0)[0], yb + 6.5, "CẠNH ĐÔNG (E): THẲNG TẠI ĐOẠN NGOÀI 14.480 – TÓP VÀO 400 TẠI ĐOẠN TRONG 3.920 (GẦN AM THỜ)",
           size=2.7, weight="bold")

    # tóp 400 tai vi tri gay
    xj = P(L_OUT - 190, 0)[0]
    s.line(P(L_OUT, 0)[0] - 0.8, P(0, W_IN)[1], xj - 1.5, P(0, W_IN)[1], sw=0.18)
    vchain(s, [P(0, W_IN)[1], P(0, W_OUT)[1]], [xj + 3, xj + 3], xj, ["400"], size=2.6, bold=True, ext=0, gap=3)
    s.text(P(L_OUT + 120, 0)[0], P(0, W_OUT)[1] - 1.3, "← TÓP 400", size=2.2, anchor="start", weight="bold", col="#c00000")

    # ---- KICH THUOC TRAI (phia cong)
    xw = P(-t, 0)[0]
    ysg = [P(0, y)[1] for y in (0, GATE_Y1, GATE_Y2, W_OUT)]
    vchain(s, ysg, xw, xw - 6, [fmt(GATE_Y1), "2.000 – CỔNG", fmt(W_OUT - GATE_Y2)], size=2.8, bold=True)
    ysl = [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_OUT)]
    vchain(s, ysl, xw, xw - 13.5, [fmt(W_GAP), fmt(BLK_CORE), fmt(PATH), fmt(BLK_CORE), fmt(E_GAP)], size=2.8, bold=True)
    vchain(s, [ysl[0], ysl[-1]], xw, xw - 21, ["8.240 – RỘNG PHÍA NGOÀI"], size=3.0, bold=True)

    # ---- KICH THUOC PHAI (doan tron)
    xe = P(L_TOTAL + t, 0)[0]
    ysr = [P(0, y)[1] for y in (0, ROW_W[0], ROW_W[1], ROW_E[0], ROW_E[1], W_IN)]
    vchain(s, ysr, xe, xe + 9, [fmt(W_GAP), fmt(BLK_CORE), fmt(PATH), fmt(BLK_CORE), fmt(CLEAR_IN)], size=2.8, bold=True)
    vchain(s, [P(0, 0)[1], P(0, W_IN)[1], P(0, W_OUT)[1]], [xe, xe, P(L_OUT, 0)[0]], xe + 17,
           ["7.840 – RỘNG PHÍA TRONG", "400"], size=3.0, bold=True)
    s.text(xe + 22.5, P(0, W_IN + 200)[1], "tóp", size=2.2, rot=-90, col="#c00000", weight="bold")

    # nhan canh W / E
    for (yy, ch, txt) in ((oy - 10, "W", "CẠNH TÂY"), (P(0, W_OUT)[1] + 12, "E", "CẠNH ĐÔNG")):
        s.circle(17, yy, 3.2, sw=0.4)
        s.text(17, yy + 1.4, ch, size=3.8, weight="bold")
        s.text(17, yy + 6.6, txt, size=1.9, weight="bold")

    # ================= DAI DUOI: ghi chu, kiem tra, chu thich, huong bac, khung ten
    ys0 = 214
    s.line(10, ys0, 410, ys0, sw=0.5)
    # Ghi chu
    s.text(13, ys0 + 5, "GHI CHÚ", size=3.0, anchor="start", weight="bold")
    notes = [
        "1. MỌI KÍCH THƯỚC BỐ TRÍ ĐO THEO MÉP NGOÀI PHẦN NỔI ĐÃ TÔ, ỐP CỦA BLOCK (lối đi 1.200, khoảng 530, 850/850 đến tường, 1.580); đế BTCT 200 và phần chìm chỉ thể hiện ở mặt cắt. Kích thước ghi bằng mm, cao độ ghi bằng m. Kích thước khu đất là kích thước LỌT LÒNG (mặt trong tường biên). Chiều dày tường biên chưa có số liệu – thể hiện tượng trưng.",
        "2. Chuỗi chiều dài theo kích thước HOÀN THIỆN block 820:  1.580 + 11×820 + 10×530 + 2.500 = 18.400. Khoảng 530 đo giữa 2 mép ngoài hoàn thiện. (780 là phần xây – chỉ dùng ở trang 2.)",
        "3. Chuỗi ngang (TẠM TÍNH – CÁCH 1, chờ đo lại) tại đoạn rộng 8.240:  850 + 2.670 + 1.200 + 2.670 + 850 = 8.240. Tại đoạn trong:  450 + 2.670 + 1.200 + 2.670 + 850 = 7.840. Lối đi 1.200 đo giữa 2 mép ngoài phần nổi.",
        "4. Block phần nổi 2.670 × 820 (6×380 + 7×50 + 40). Đế BTCT 200 hai đầu block (không phải hộc mộ) nằm dưới cốt nền – không vẽ trên mặt bằng, xem mặt cắt B-B trang 2.",
        "5. Cổng 2.000 nằm chính giữa cạnh 8.240 (3.120 – 2.000 – 3.120). Tim cổng = tim lối đi = tim am thờ, cách mỗi cạnh 4.120.",
        "6. AM THỜ vẽ tượng trưng (nét đứt), kích thước chờ bổ sung. Hướng trục cổng → am thờ: B9° lệch Đông (phương vị 9°), theo la bàn đo tại hiện trường.",
    ]
    textblock(s, 13, ys0 + 9.6, notes, size=2.15, nchar=112)

    # Bang kiem tra
    xk = 150
    s.line(xk, ys0, xk, 287, sw=0.4)
    s.text(xk + 3, ys0 + 5, "BẢNG KIỂM TRA", size=3.0, anchor="start", weight="bold")
    checks = [
        ("Số block", "22 (11 trái + 11 phải)", "Đạt"),
        ("Số hộc / block", "6", "Đạt"),
        ("Tổng số hộc", "22 × 6 = 132", "Đạt"),
        ("Tổng chiều dài", "14.480 + 3.920 = 18.400", "Đạt"),
        ("Rộng ngoài / trong", "8.240 / 7.840", "Đạt"),
        ("Cạnh Tây / cạnh Đông", "thẳng / tóp 400", "Đạt"),
        ("Cổng – lối đi", "2.000 / 1.200, cùng trục", "Đạt"),
        ("Cổng giữa cạnh 8.240", "3.120 / 3.120", "Đạt"),
        ("Tên công trình phụ", "AM THỜ", "Đạt"),
        ("Chuỗi vượt lọt lòng", "không có", "Đạt"),
    ]
    yy = ys0 + 9
    for k, v, ok in checks:
        s.text(xk + 3, yy + 2.8, k, size=2.1, anchor="start")
        s.text(xk + 37, yy + 2.8, v, size=2.1, anchor="start")
        s.text(xk + 80, yy + 2.8, ok, size=2.1, anchor="middle", weight="bold", col="#0a6b0a" if ok == "Đạt" else "#c00000")
        yy += 6.3
        s.line(xk, yy - 0.8, xk + 88, yy - 0.8, sw=0.12, col="#999")

    # Chu thich vat lieu
    xl_ = 238
    s.line(xl_, ys0, xl_, 287, sw=0.4)
    s.text(xl_ + 3, ys0 + 5, "CHÚ THÍCH", size=3.0, anchor="start", weight="bold")
    items = [("brick", "Xây gạch (tường biên, block)"), ("finish", "Hoàn thiện: tô 10 + ốp 10"),
             ("path", "Lối đi giữa 1.200"),
             ("axis", "Đường tim (gạch chấm)"), ("amtho", "Am thờ – chờ bổ sung"),
             ("hole", "Lỗ âm dương (xem trang 2)")]
    yy = ys0 + 8.5
    for k, lab in items:
        legend_item(s, xl_ + 3, yy, k, lab, size=2.1)
        yy += 9.1

    # Huong bac
    xn = 300
    s.line(xn, ys0, xn, 287, sw=0.4)
    s.text(xn + 11, ys0 + 5, "HƯỚNG", size=2.8, weight="bold")
    north_arrow(s, xn + 9, ys0 + 30, 5.5, label_axis=False)
    s.text(xn + 11, ys0 + 42, "TRỤC B9°", size=2.4, weight="bold")
    s.text(xn + 11, ys0 + 50, "Cổng → Am thờ", size=2.0)
    s.text(xn + 11, ys0 + 53.5, "hướng B9°", size=2.4, weight="bold")
    s.text(xn + 11, ys0 + 57.5, "phương vị 9°", size=1.9)
    s.text(xn + 11, ys0 + 60.5, "lệch Đông (B9°Đ)", size=1.9)
    s.text(xn + 11, ys0 + 64.5, "W trên – E dưới", size=2.0)

    # Khung ten
    title_block(s, 322, ys0, 88, 287 - ys0, "MẶT BẰNG TỔNG THỂ", "1/60", "01/02", "LM-01")
    return s.svg()


# =====================================================================================
#                                       TRANG 2
# =====================================================================================
def page2():
    s = SVG()
    frame(s)
    k = 0.1   # 1/10

    # ---------------- MAT BANG CHI TIET BLOCK ----------------
    X0, Y0 = 37, 27
    Pu = lambda u, v: (X0 + u * k, Y0 + v * k)
    s.text(14, 17.5, "MẶT BẰNG CHI TIẾT 1 BLOCK (6 HỘC) – TL 1/10", size=4.6, anchor="start", weight="bold")
    s.text(343, 16.5, "MỌI KÍCH THƯỚC BỐ TRÍ ĐO THEO MÉP NGOÀI PHẦN NỔI ĐÃ TÔ, ỐP", size=2.6, anchor="end", weight="bold", col="#c00000")
    s.text(343, 21, "Đế BTCT, phần chìm: chỉ thể hiện ở mặt cắt kết cấu", size=2.2, anchor="end", col="#c00000")
    s.text(14, 23, "(Block xoay nằm ngang để thể hiện; chiều 6 hộc vuông góc lối đi giữa)", size=2.3, anchor="start", italic=True)

    # mong/de 2 dau
    # op gach (lop ngoai 10), to trat (10), xay
    a = Pu(BASE, 0)
    s.rect(a[0], a[1], BLK_CORE * k, BLK_HT * k, fill=TILE, sw=0.2)
    a = Pu(BASE + FIN_OP, FIN_OP)
    s.rect(a[0], a[1], (BLK_CORE - 2 * FIN_OP) * k, (BLK_HT - 2 * FIN_OP) * k, fill="url(#render)", sw=0.1)
    a = Pu(BASE + FIN, FIN)
    s.rect(a[0], a[1], (BLK_CORE - 2 * FIN) * k, BLK_XAY * k, fill="url(#brick2)", sw=0.3)
    hoc_u = []
    for i in range(N_HOC):
        u = BASE + FIN + WALL + i * (HOC_W + WALL)
        hoc_u.append(u)
        a = Pu(u, FIN + WALL)
        s.rect(a[0], a[1], HOC_W * k, HOC_L * k, fill="#fff", sw=0.3)
        cx = a[0] + HOC_W * k / 2
        s.text(cx, a[1] + 9, f"HỘC {i + 1}", size=3.2, weight="bold")
        s.text(cx, a[1] + 14.5, "680 × 380", size=2.6)
        s.text(cx, a[1] + 18, "lọt lòng", size=2.1, italic=True)
        cy = a[1] + HOC_L * k / 2 + 4
        s.circle(cx, cy, 5, sw=0.3, dash="1,0.6")
        s.line(cx - 3.5, cy - 3.5, cx + 3.5, cy + 3.5, sw=0.2)
        s.line(cx - 3.5, cy + 3.5, cx + 3.5, cy - 3.5, sw=0.2)
        s.text(cx, cy + 9, "LỖ ÂM DƯƠNG", size=2.0, weight="bold")
        s.text(cx, cy + 11.8, "(KT, vị trí chờ XN)", size=1.8, italic=True)
    assert hoc_u[-1] + HOC_W + WALL + FIN == BLK - BASE
    # nhan mong/de
    # kich thuoc 680 trong hoc 1
    a = Pu(hoc_u[0] + 40, FIN + WALL)
    vchain(s, [a[1], a[1] + HOC_L * k], a[0] + 1, a[0], ["680"], size=2.6, ext=0, gap=-1, bold=True)
    # 380 trong hoc 6 (ngang) da co o chuoi duoi

    # mat cat A-A (doc qua hoc 4) & B-B (ngang)
    ua = hoc_u[3] + HOC_W / 2
    xa_ = Pu(ua, 0)[0]
    for (yA, yB) in ((Y0 - 6.5, Y0 - 1.5), (Y0 + BLK_HT * k + 1.5, Y0 + BLK_HT * k + 5.0)):
        s.line(xa_, yA, xa_, yB, sw=0.8)
    s.line(xa_, Y0 - 6.5, xa_ - 5, Y0 - 6.5, sw=0.3); arrow(s, xa_ - 5, Y0 - 6.5, -1, 0, 1.8)
    s.text(xa_ - 7.8, Y0 - 5.4, "A", size=3.4, weight="bold")
    yb_ = Y0 + BLK_HT * k + 5.0
    s.line(xa_, yb_, xa_ - 5, yb_, sw=0.3); arrow(s, xa_ - 5, yb_, -1, 0, 1.8)
    s.text(xa_ - 7.8, yb_ + 1.2, "A", size=3.4, weight="bold")
    yBm = Pu(0, BLK_HT / 2)[1]
    for xB0, xB1 in ((Pu(BASE, 0)[0] - 25.5, Pu(BASE, 0)[0] - 22), (Pu(BLK - BASE, 0)[0] + 2, Pu(BLK - BASE, 0)[0] + 5.5)):
        s.line(xB0, yBm, xB1, yBm, sw=0.8)
        xm = (xB0 + xB1) / 2
        s.line(xm, yBm, xm, yBm - 5, sw=0.3); arrow(s, xm, yBm - 5, 0, -1, 1.8)
        s.text(xm, yBm - 7.3, "B", size=3.4, weight="bold")

    # chuoi kich thuoc duoi mat bang
    yobj = Y0 + BLK_HT * k
    us = [BASE, BASE + FIN]
    for i in range(N_HOC):
        us += [hoc_u[i], hoc_u[i] + HOC_W]
    us += [BLK - BASE - FIN, BLK - BASE]
    labs = []
    for i in range(len(us) - 1):
        labs.append(fmt(us[i + 1] - us[i]))
    hchain(s, [Pu(u, 0)[0] for u in us], yobj, yobj + 9.5, labs, size=2.6, bold=True)
    hchain(s, [Pu(BASE, 0)[0], Pu(BLK - BASE, 0)[0]], yobj, yobj + 16.5,
           ["2.670 = 6×380 + 7×50 + 40 – MÉP NGOÀI PHẦN NỔI ĐÃ TÔ, ỐP"], size=2.9, bold=True)
    s.text(Pu(BLK / 2, 0)[0], yobj + 22.5, "Đế BTCT 200 hai đầu block không thể hiện trên mặt bằng – xem mặt cắt B-B", size=2.4, italic=True, col="#c00000")
    # chuoi doc ben trai
    vs = [0, FIN, FIN + WALL, FIN + WALL + HOC_L, FIN + 2 * WALL + HOC_L, BLK_HT]
    vchain(s, [Pu(0, v)[1] for v in vs], X0 + BASE * k, X0 + BASE * k - 5.5, ["20", "50", "680", "50", "20"], size=2.5, bold=True)
    vchain(s, [Pu(0, FIN)[1], Pu(0, FIN + BLK_XAY)[1]], X0 + BASE * k, X0 + BASE * k - 12, ["780 XÂY"], size=2.6, bold=True)
    vchain(s, [Pu(0, 0)[1], Pu(0, BLK_HT)[1]], X0 + BASE * k, X0 + BASE * k - 18.5, ["820 HOÀN THIỆN"], size=2.6, bold=True)

    # ---------------- MAT CAT A-A ----------------
    zt, z0 = 100, 0
    Zy = lambda z: 168 - z * k
    xa = 84
    Wa = lambda w: xa + w * k
    s.text(14, 141.5, "MẶT CẮT A-A", size=4.4, anchor="start", weight="bold")
    s.text(14, 146.5, "TỶ LỆ 1/10 (cắt qua hộc 4)", size=2.4, anchor="start")
    # dat nen
    s.rect(70, Zy(0), 98, 285 - Zy(0), fill="url(#soil)", sw=0)
    s.line(66, Zy(0), 172, Zy(0), sw=0.6)
    # long hoc: khong gian rong
    s.rect(Wa(FIN + WALL), Zy(H_NOI), HOC_L * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    # tam BTCT
    hole = 100   # tuong trung, chua co kich thuoc
    ws, we = FIN, FIN + BLK_XAY
    wc = BLK_HT / 2
    for (w1, w2) in ((ws, wc - hole / 2), (wc + hole / 2, we)):
        s.rect(Wa(w1), Zy(-D_AM), (w2 - w1) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    # lo am duong
    s.rect(Wa(wc - hole / 2), Zy(-D_AM), hole * k, SLAB * k, fill="#fff", sw=0)
    for w in (wc - hole / 2, wc + hole / 2):
        s.line(Wa(w), Zy(-D_AM) - 1.5, Wa(w), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    # tuong gach
    for (w1, w2) in ((FIN, FIN + WALL), (FIN + WALL + HOC_L, FIN + 2 * WALL + HOC_L)):
        s.rect(Wa(w1), Zy(H_NOI), WALL * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    # hoan thien phan noi: to trat 10 (trong) + op gach 10 (ngoai)
    for (wr, wo) in ((FIN_OP, 0), (FIN + 2 * WALL + HOC_L, FIN + 2 * WALL + HOC_L + FIN_TRAT)):
        pass
    s.rect(Wa(FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(0), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Wa(FIN + BLK_XAY), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    s.rect(Wa(FIN + BLK_XAY + FIN_TRAT), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    # chu trong hoc
    s.text(Wa(wc), Zy(-250), "HỘC MỘ", size=3.2, weight="bold")
    s.text(Wa(wc), Zy(-330), "lọt lòng 680", size=2.5)
    s.text(Wa(wc), Zy(-420), "(không tô trát", size=2.2, italic=True)
    s.text(Wa(wc), Zy(-470), "phần dưới cốt nền)", size=2.2, italic=True)
    s.text(Wa(wc), Zy(-800), "LỖ ÂM DƯƠNG", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-850), "XUYÊN TẤM BTCT", size=2.4, weight="bold")
    s.text(Wa(wc), Zy(-900), "(KT, vị trí chờ XN)", size=2.1, italic=True)
    s.line(Wa(wc), Zy(-915), Wa(wc), Zy(-D_AM - 50), sw=0.25)
    arrow(s, Wa(wc), Zy(-D_AM - 50), 0, 1, 1.6)
    # kich thuoc tren
    hchain(s, [Wa(w) for w in (0, FIN, FIN + WALL, FIN + WALL + HOC_L, FIN + 2 * WALL + HOC_L, BLK_HT)], Zy(H_NOI), 152.5,
           ["20", "50", "680 LỌT LÒNG", "50", "20"], size=2.6, bold=True)
    hchain(s, [Wa(FIN), Wa(FIN + BLK_XAY)], Zy(H_NOI), 145.5, ["780 PHỦ BÌ XÂY"], size=2.6, bold=True)
    hchain(s, [Wa(0), Wa(BLK_HT)], Zy(H_NOI), 138.5, ["820 PHỦ BÌ SAU HOÀN THIỆN"], size=2.6, bold=True)
    # kich thuoc dung (trai) + cao do
    zs = [H_NOI, 0, -D_AM, -D_AM - SLAB]
    vchain(s, [Zy(z) for z in zs], [Wa(0), Wa(0) - 14, Wa(FIN), Wa(FIN)], 64, ["100", "1.000 – PHẦN ÂM", "100"], size=2.6, bold=True, gap=0.6)
    elevs = [(H_NOI, "+0.100", "CỐT ĐỈNH BLOCK (NỔI 100)"), (0, "±0.000", "CỐT NỀN HOÀN THIỆN"),
             (-D_AM, "≈ -1.000", "CỐT ĐÁY HỘC (dự kiến)"), (-D_AM - SLAB, "≈ -1.100", "ĐÁY TẤM BTCT DÀY 100")]
    for z, v, d in elevs:
        y = Zy(z)
        s.line(14, y, 61, y, sw=0.18)
        s.poly([(57, y), (55.4, y - 2.4), (58.6, y - 2.4)], fill="#000", sw=0)
        s.text(14, y - 0.8, v, size=2.8, anchor="start", weight="bold")
        s.text(14, y + 2.9, d, size=1.95, anchor="start")
    # chu thich ben phai (duong dan ngan, ngang)
    def callout(x_from, y, label, size=2.25, x_to=176):
        s.line(x_from, y, x_to - 0.5, y, sw=0.18)
        s.circle(x_from, y, 0.35, fill="#000", sw=0)
        s.text(x_to, y + size * 0.35, label, size=size, anchor="start")
    xr_ = Wa(BLK_HT)
    callout(xr_ - 0.5, Zy(80), "ỐP GẠCH 10", x_to=172)
    callout(xr_ - 1.5, Zy(25), "TÔ TRÁT 10", x_to=172)
    s.text(172, Zy(-60), "→ hoàn thiện 20/mặt", size=2.0, anchor="start", italic=True)
    s.text(172, Zy(-90), "(chỉ phần nổi)", size=2.0, anchor="start", italic=True)
    callout(Wa(FIN + BLK_XAY) - 2.5, Zy(-300), "TƯỜNG GẠCH 50", x_to=172)
    callout(166, Zy(-560), "ĐẤT NỀN", x_to=172)
    callout(Wa(FIN + BLK_XAY) - 3, Zy(-D_AM - 50), "TẤM BTCT 100", x_to=172)

    # ---------------- MAT CAT B-B (trich doan dau block) ----------------
    xb = 224
    Ub = lambda u: xb + u * k
    ubrk = 1105
    s.text(206, 141.5, "MẶT CẮT B-B (TRÍCH ĐOẠN ĐẦU BLOCK)", size=4.0, anchor="start", weight="bold")
    s.text(206, 146.5, "TỶ LỆ 1/10 – các hộc còn lại lặp lại đến đủ 6 hộc", size=2.3, anchor="start")
    s.rect(206, Zy(0), Ub(ubrk) - 206, 285 - Zy(0), fill="url(#soil)", sw=0)
    s.line(204, Zy(0), Ub(ubrk), Zy(0), sw=0.6)
    # tam BTCT (lien duoi ca block), lo am duong moi hoc
    hu = [BASE + FIN + WALL + i * (HOC_W + WALL) for i in range(3)]
    for u in hu[:2]:
        s.rect(Ub(u), Zy(H_NOI), HOC_W * k, (H_NOI + D_AM) * k, fill="#fff", sw=0)
    cuts = [0]
    for u in hu[:2]:
        c = u + HOC_W / 2
        cuts += [c - hole / 2, c + hole / 2]
    cuts.append(ubrk)
    for i in range(0, len(cuts), 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="url(#concrete)", sw=0.35)
    for i in range(1, len(cuts) - 1, 2):
        s.rect(Ub(cuts[i]), Zy(-D_AM), (cuts[i + 1] - cuts[i]) * k, SLAB * k, fill="#fff", sw=0)
        for u in (cuts[i], cuts[i + 1]):
            s.line(Ub(u), Zy(-D_AM) - 1.5, Ub(u), Zy(-D_AM - SLAB) + 1.5, sw=0.25, dash="0.8,0.5")
    # mong bao gach the + giang BTCT
    s.rect(Ub(0), Zy(-GIANG), MONG_BAO * k, (D_AM - GIANG) * k, fill="url(#brickthe)", sw=0.35)
    s.rect(Ub(0), Zy(0), MONG_BAO * k, GIANG * k, fill="url(#concrete)", sw=0.35)
    s.text(Ub(100) - 1.2, Zy(-575), "ĐẾ 200 – MÓNG BAO GẠCH THẺ", size=2.4, rot=-90, weight="bold", bg=True)
    s.text(Ub(100) + 3.0, Zy(-575), "(chỉ thể hiện ở mặt cắt)", size=2.2, rot=-90, weight="bold", bg=True)
    s.text(Ub(100), Zy(-95), "GIẰNG BTCT", size=2.1, weight="bold", bg=True)
    # tuong + hoan thien phan noi o dau
    for u in (BASE + FIN, BASE + FIN + WALL + HOC_W, BASE + FIN + 2 * (WALL + HOC_W)):
        w = WALL if u + WALL <= ubrk else ubrk - u
        s.rect(Ub(u), Zy(H_NOI), w * k, (H_NOI + D_AM) * k, fill="url(#brick2)", sw=0.35)
    s.rect(Ub(BASE), Zy(H_NOI), FIN_OP * k, H_NOI * k, fill=TILE, sw=0.15)
    s.rect(Ub(BASE + FIN_OP), Zy(H_NOI), FIN_TRAT * k, H_NOI * k, fill="url(#render)", sw=0.15)
    for i in range(2):
        c = Ub(hu[i] + HOC_W / 2)
        s.text(c, Zy(-300), f"HỘC {i + 1}", size=3.0, weight="bold")
        s.text(c, Zy(-370), "lọt lòng 380", size=2.3)
        s.text(c, Zy(-860), "LỖ ÂM DƯƠNG", size=2.1, weight="bold")
        s.text(c, Zy(-905), "(chờ XN)", size=1.9, italic=True)
        s.line(c, Zy(-920), c, Zy(-D_AM - 50), sw=0.25)
        arrow(s, c, Zy(-D_AM - 50), 0, 1, 1.6)
    # duong cat (break line)
    xbk = Ub(ubrk)
    pts = [(xbk, Zy(H_NOI) - 3), (xbk, Zy(-400)), (xbk + 1.8, Zy(-430)), (xbk - 1.8, Zy(-470)), (xbk, Zy(-500)), (xbk, 285)]
    s.poly(pts, closed=False, sw=0.3)
    # kich thuoc B-B
    hchain(s, [Ub(u) for u in (0, BASE, BASE + FIN, hu[0], hu[0] + HOC_W, hu[1], hu[1] + HOC_W, hu[2])], Zy(H_NOI), 152.5,
           ["200", "20", "50", "380", "50", "380", "50"], size=2.6, bold=True)
    vchain(s, [Zy(0), Zy(-GIANG)], Ub(0), Ub(0) - 7, ["150"], size=2.5, bold=True)

    # ---------------- DAI PHAI: chu thich, ghi chu, khung ten ----------------
    xs_ = 350
    s.line(xs_, 10, xs_, 287, sw=0.5)
    s.text(xs_ + 3, 16, "CHÚ THÍCH VẬT LIỆU", size=2.9, anchor="start", weight="bold")
    items = [("soil", "Đất nền"), ("brick", "Tường xây gạch 50"), ("brickthe", "Móng bao gạch thẻ 200"),
             ("concrete", "Bê tông cốt thép (tấm, giằng)"), ("render", "Lớp tô trát 10"), ("tile", "Lớp ốp gạch 10"),
             ("hole", "Lỗ âm dương (chờ XN)")]
    yy = 19.5
    for kk, lab in items:
        legend_item(s, xs_ + 3, yy, kk, lab, size=2.15)
        yy += 6.6
    s.line(xs_, yy + 0.5, 410, yy + 0.5, sw=0.3)
    s.text(xs_ + 3, yy + 6, "GHI CHÚ", size=2.9, anchor="start", weight="bold")
    notes = [
        "1. Hộc lọt lòng 680×380; tường gạch 50; phủ bì xây 1 hộc 780×480.",
        "2. Chiều 680: 680 + 2×50 = 780 (xây) + 2×20 = 820 (hoàn thiện).",
        "3. Chiều 6 hộc (phần nổi): 6×380 + 7×50 + 40 = 2.670. Kể cả đế 2 đầu (dưới cốt nền): 200 + 2.670 + 200 = 3.070.",
        "4. Hoàn thiện 20/mặt = tô trát 10 + ốp gạch 10, chỉ ở phần nổi (±0.000 → +0.100). Phần tường dưới cốt nền không tô trát.",
        "5. Tấm BTCT chống lún dày 100 dưới mỗi block; mỗi hộc 1 lỗ âm dương xuyên tấm (6 lỗ/block), không đổ bê tông kín vị trí lỗ. Kích thước và vị trí lỗ âm dương chờ xác nhận.",
        "6. Đế 200 hai đầu block nằm dưới cốt nền: móng bao gạch thẻ rộng 200, trên có giằng BTCT ~150. Chỉ thể hiện ở mặt cắt, không vẽ và không làm mốc trên mặt bằng. Cao độ giằng, chiều sâu móng, khe 20: tạm thể hiện – chờ XN.",
        "7. 780 là KT phần xây, 820 là KT sau hoàn thiện – không dùng lẫn trong cùng một chuỗi kích thước mặt bằng.",
        "8. Chiều sâu hộc ~1.000, cốt đáy dự kiến ~-1.000.",
        "9. Mọi kích thước bố trí mặt bằng đo theo mép ngoài phần nổi đã tô, ốp; đế BTCT và phần chìm không dùng làm mốc bố trí.",
    ]
    textblock(s, xs_ + 3, yy + 10.5, notes, size=2.05, lh=2.85, nchar=48)
    # huong bac nho
    north_arrow(s, xs_ + 42, 188, 4.5, label_axis=False)
    s.text(xs_ + 3, 186, "Chiều 6 hộc vuông góc", size=2.0, anchor="start")
    s.text(xs_ + 3, 189, "trục B9°", size=2.0, anchor="start")
    title_block(s, xs_, 198, 60, 89, "MẶT BẰNG CHI TIẾT\nBLOCK & MẶT CẮT", "1/10", "02/02", "LM-02", vertical=True)
    return s.svg()


if __name__ == "__main__":
    p1, p2 = page1(), page2()
    open(os.path.join(HERE, "trang1-mat-bang-tong-the.svg"), "w", encoding="utf-8").write(p1)
    open(os.path.join(HERE, "trang2-chi-tiet-block-mat-cat.svg"), "w", encoding="utf-8").write(p2)
    html = ("<!doctype html><html><head><meta charset='utf-8'><style>@page{size:420mm 297mm;margin:0}"
            "html,body{margin:0;padding:0}.pg{width:420mm;height:297mm;page-break-after:always;overflow:hidden}"
            ".pg:last-child{page-break-after:auto}svg{display:block}</style></head><body>"
            f"<div class='pg'>{p1}</div><div class='pg'>{p2}</div></body></html>")
    open(os.path.join(HERE, "ban-ve.html"), "w", encoding="utf-8").write(html)
    print("OK – tat ca kiem tra so hoc dat")
