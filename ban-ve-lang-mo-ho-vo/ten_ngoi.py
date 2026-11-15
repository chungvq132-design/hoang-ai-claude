# -*- coding: utf-8 -*-
"""Danh sach ten tung ngoi (theo bang chu nha gui 15/11/2026).
Moi hang = 1 block, hang 1 sat AM THO. Cot 12->7 = day trai (Tay, cot 12 sat tuong Tay, cot 7 sat loi di);
cot 6->1 = day phai (Dong, cot 6 sat loi di, cot 1 sat tuong Dong).
Moi o: (ten, do) - do=True: chu do = quy hoach cho nguoi dang song.
"""
R, K = True, False
_ = None
#        cot:  12                         11                      10              9                8                7                 |  6                  5                    4                         3                2               1
T = "A"   # ngoi to tien khong xac dinh duoc ten - danh so theo anh
ROWS = [
    # 2 hang dau (4 block sat am tho): ngoi to tien khong xac dinh ten, danh so theo anh
    [("12", T), ("11", T), ("10", T), ("9", T), ("8", T), ("7", T),
     ("6", T), ("5", T), ("4", T), ("3", T), ("2", T), ("1", T)],
    [("A", T), ("23", T), ("22", T), ("21", T), ("20", T), ("19", T),
     ("18", T), ("17", T), ("16", T), ("14", T), ("14", T), ("13", T)],
    [("Chú Cháu Em", K), ("Chú Phượng", K), ("Bà Bớt", K), ("Ô Tớm", K), ("Bà Hoe", K), ("Ô Bính", K),
     ("Chị Ô Danh (E)", K), ("B", K), ("Bà Tín (triệu hồn)", R), ("Ô Tính", K), ("Bà Em", K), ("Ô Thành", K)],
    [_, _, ("B.Cúc", R), ("Ô Toàn", R), ("B.Liệu", K), ("Ô Châu", K),
     ("B.Qúy", R), ("Ô Nguyên", K), ("B.Manh", K), ("B.Bàng", R), ("Ô Danh", K), ("B.Liên", K)],
    [("Con Chú Hưng (C)", K), ("Cô (D) Phượng", K), ("B.Thơm", R), ("Ô.Trường", R), ("B.Tình", R), ("Ô.Lộng", R),
     ("B.Cúc", R), ("B.Hùng", R), ("B.Minh", K), ("B.Tuấn", R), ("B.Thuần", K), ("Ô.Tường", K)],
    [("Hạnh", R), ("Chung", R), ("Quỳnh", R), ("Vĩnh", R), ("B.Nguyệt", R), ("Ô.Long", R),
     ("Hậu", R), ("Con Ô Danh (N)", K), ("Lê Na", R), ("Thắng", R), ("B.Cúc", R), ("B.Toàn", R)],
    [_, ("Khôi", R), _, ("Vương", R), ("Nhi", R), ("Sơn", R),
     ("B.Tý", R), ("B.Dũng", K), ("Vợ", R), ("A.Giáp", R), ("Vợ", R), ("Hoan", R)],
    [_, ("Kiên", R), _, ("Khang", R), _, ("Đại", R),
     ("Huệ", R), ("Giang", R), ("B.Bích", R), ("B.Minh", K), ("B.Thuận", R), ("B.Thung", K)],
    [_, _, _, _, _, ("Hiếu", R),
     _, ("Đức", R), ("Uyên", R), ("Cường", R), ("Hương", R), ("An", R)],
    [_, _, _, _, _, _,
     _, ("H.Hoàng", R), _, ("Q.Vinh", R), _, ("Nhật", R)],
    [_, _, _, _, _, _,
     _, _, _, _, _, ("Gia Bảo", R)],
]
assert len(ROWS) == 11 and all(len(r) == 12 for r in ROWS)


def cell(row, side, k):
    """row: 1..11 (1 sat am tho); side 'W'/'E'; k: 0..5 thu tu hoc theo toa do y tang dan (tu Tay sang Dong)."""
    r = ROWS[row - 1]
    return r[k] if side == "W" else r[6 + k]   # W: cot 12..7 = chi so 0..5 ; E: cot 6..1 = chi so 6..11


def stats():
    n_k = n_r = n_e = 0
    for r in ROWS:
        for c in r:
            if c is None:
                n_e += 1
            elif c[1] == "A":
                n_e += 0
            elif c[1]:
                n_r += 1
            else:
                n_k += 1
    return n_k, n_r, n_e
