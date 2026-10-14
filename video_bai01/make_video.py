"""Video Bài 1 - Ma trận và các phép toán trên ma trận.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 1 · Ma trận và các phép toán', TEXTS, SPOKEN, 'bai01_ma_tran',
           mins={0: 5, 5: 11, 10: 9, 11: 9}, chapter='Chương 1 · Một số kiến thức cơ bản')

def s_title(fig):
    L.title(fig, 'Bài 1. Ma trận và các phép toán', r'$(\mathbf{AB})_{ij}=\sum_{k} a_{ik}\,b_{kj}$')

# ---------- véc tơ ----------
U, V = np.array([3.0, 1.0]), np.array([1.0, 2.2])
def s_vec(fig):
    L.base(fig, 'Véc tơ trong không gian thực')
    rows = [('Ảnh xám 28×28', r'$\mathbf{x}\in\mathbb{R}^{784}$'), ('Khách hàng', '(tuổi, thu nhập, số lần mua, …)'),
            ('Câu văn', 'véc tơ tần suất từ')]
    for k, (a, b) in enumerate(rows):
        if L.st(1) > 0.8 + 1.5 * k or L.on(2):
            fig.text(0.06, 0.74 - 0.09 * k, a, fontsize=15, color=DARK); fig.text(0.24, 0.74 - 0.09 * k, '→  ' + b, fontsize=15, color=B)
    if L.on(2):
        box(fig, 0.22, 0.36, r'$\mathbf{x}+\mathbf{y}=\begin{bmatrix}x_1+y_1\\ \vdots\\ x_n+y_n\end{bmatrix}$'.replace(r'\begin{bmatrix}', '(').replace(r'\end{bmatrix}', ')').replace(r'\\', ',').replace(r'\vdots', r'\ldots'), 20)
        ax = ax_at(fig, [0.5, 0.16, 0.46, 0.7], (-0.5, 5), (-0.5, 4), xl='$x_1$', yl='$x_2$')
        k = ease(L.pr(2, 2.5)); arrow(ax, U, B); arrow(ax, V, T)
        ax.text(*(U + [0.1, -0.35]), r'$\mathbf{u}$', color=B, fontsize=17); ax.text(*(V + [-0.45, 0.05]), r'$\mathbf{v}$', color=T, fontsize=17)
        ax.plot(*np.c_[U, U + V * k], '--', color=T, lw=1.5); ax.plot(*np.c_[V, V + U * k], '--', color=B, lw=1.5)
        if k > 0.95:
            arrow(ax, U + V, O, 3.5); ax.text(*(U + V + [0.1, 0.05]), r'$\mathbf{u}+\mathbf{v}$', color=O, fontsize=17)

# ---------- ba cách nhìn ma trận ----------
M = np.array([[3, 1, 4, 1], [5, 9, 2, 6], [5, 3, 5, 8]])
def grid(fig, x0, y0, A, cw=0.05, rh=0.07, hi=None, fs=16, color=DARK, fill='#f2f4fa', label=None, vis=None):
    """vẽ ma trận như một bảng; hi(i,j) -> màu nền nếu cần tô; vis(i,j) -> có hiện số không"""
    m, n = A.shape
    for i in range(m):
        for j in range(n):
            c = hi(i, j) if hi else None
            fig.patches.append(FancyBboxPatch((x0 + j * cw, y0 - (i + 1) * rh), cw * 0.94, rh * 0.9, boxstyle='round,pad=0.002',
                               transform=fig.transFigure, fc=c or fill, ec=GRID))
            if vis is None or vis(i, j):
                v = A[i, j]; s = vn(v, 0) if float(v).is_integer() else vn(v, 2)
                fig.text(x0 + (j + 0.47) * cw, y0 - (i + 0.55) * rh, s, ha='center', va='center', fontsize=fs, color=color)
    if label: fig.text(x0 + n * cw / 2, y0 + 0.03, label, ha='center', fontsize=16, color=DARK, weight='bold')
def s_views(fig):
    L.base(fig, 'Ma trận và ba cách nhìn')
    s = L.st(3); mode = 0 if s < 2 else (1 if s < 4 else 2)
    hi = [lambda i, j: '#dfe4f7', lambda i, j: '#fde7cc' if j == 1 else None, lambda i, j: '#d5efe9' if i == 1 else None][mode]
    grid(fig, 0.12, 0.72, M, cw=0.08, rh=0.11, hi=hi, fs=20, label=r'$\mathbf{A}\in\mathbb{R}^{3\times 4}$')
    labs = ['Theo phần tử: bảng số $a_{ij}$', 'Theo cột: $\\mathbf{A}=[\\mathbf{a}_1\\ \\mathbf{a}_2\\ \\cdots\\ \\mathbf{a}_n]$',
            'Theo hàng: mỗi hàng là một quan sát']
    for k, s_ in enumerate(labs):
        fig.text(0.56, 0.66 - 0.1 * k, s_, fontsize=16, color=[B, O, T][k] if k == mode else LIGHT, weight='bold' if k == mode else 'normal')

# ---------- nhân ma trận ----------
A1 = np.array([[1, 2, 0], [3, -1, 4]]); B1 = np.array([[2, 1], [0, -3], [5, 2]]); C1 = A1 @ B1
def s_mul(fig):
    L.base(fig, 'Phép nhân hai ma trận')
    if L.now < L.T[7]:
        if L.now < L.T[5]: cur = (0, 0)
        elif L.now < L.T[6]: cur = [(0, 0), (0, 1), (1, 0), (1, 1)][min(3, int(L.st(5) / (L.slots[5] / 4)))]
        else: cur = None
        done = lambda i, j: L.on(6) or (L.on(5) and (i * 2 + j) < (cur[0] * 2 + cur[1]) + (L.st(5) % (L.slots[5] / 4) > 1.2))
        grid(fig, 0.08, 0.72, A1, hi=(lambda i, j: '#dfe4f7' if cur and i == cur[0] else None), label=r'$\mathbf{A}\ (2\times3)$')
        grid(fig, 0.33, 0.79, B1, hi=(lambda i, j: '#fde7cc' if cur and j == cur[1] else None), label=r'$\mathbf{B}\ (3\times2)$')
        grid(fig, 0.55, 0.72, C1, hi=(lambda i, j: '#d5efe9' if cur and (i, j) == cur else None), vis=done, color=T,
             label=r'$\mathbf{C}=\mathbf{AB}\ (2\times2)$')
        fig.text(0.29, 0.62, '×', fontsize=26, color=INK); fig.text(0.5, 0.62, '=', fontsize=26, color=INK)
        if cur and L.on(5) or (cur and L.st(4) > 3):
            i, j = cur; p = lambda v: vn(v, 0) if v >= 0 else f'({vn(v, 0)})'
            terms = ' + '.join(f'{p(A1[i, k])}·{p(B1[k, j])}' for k in range(3))
            fig.text(0.08, 0.38, f'c{"₁₂"[i]}{"₁₂"[j]} = {terms} = {vn(C1[i, j], 0)}', fontsize=20, color=DARK)
        fig.text(0.08, 0.27, 'số cột của A (3) = số hàng của B (3)  ✓', fontsize=15, color=INK)
        if L.on(6):
            fig.text(0.62, 0.38, 'BA có cỡ 3×3  ⇒  AB ≠ BA', fontsize=18, color=O)
        return
    # tổ hợp tuyến tính các cột
    a1, a2, x = np.array([2.0, 0.6]), np.array([-0.8, 1.5]), np.array([1.5, 1.2])
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 4.5), (-0.6, 3.2))
    k1, k2 = ease(L.pr(7, 2)), ease((L.st(7) - 2) / 2)
    arrow(ax, a1, LIGHT, 2); arrow(ax, a2, LIGHT, 2)
    ax.text(*(a1 + [0.05, -0.3]), r'$\mathbf{a}_1$', fontsize=15, color=INK); ax.text(*(a2 + [-0.4, 0.05]), r'$\mathbf{a}_2$', fontsize=15, color=INK)
    arrow(ax, x[0] * a1 * k1, B); 
    if k2 > 0: arrow(ax, x[1] * a2 * k2, T, origin=x[0] * a1)
    if k2 > 0.95:
        arrow(ax, x[0] * a1 + x[1] * a2, O, 3.5); ax.text(*(x[0] * a1 + x[1] * a2 + [0.1, 0.1]), r'$\mathbf{Ax}$', fontsize=18, color=O)
    box(fig, 0.77, 0.66, r'$\mathbf{Ax}=x_1\mathbf{a}_1+x_2\mathbf{a}_2+\cdots+x_n\mathbf{a}_n$', 17)
    fig.text(0.77, 0.52, '$x_1=1{,}5,\\ \\ x_2=1{,}2$', ha='center', fontsize=17, color=INK)
    fig.text(0.77, 0.4, 'tập mọi tích Ax = không gian cột', ha='center', fontsize=15, color=DARK)

# ---------- tính chất ----------
def s_props(fig):
    L.base(fig, 'Tính chất của phép nhân và chuyển vị')
    rows = [('Kết hợp', '(AB)C = A(BC)'), ('Phân phối', 'A(B + C) = AB + AC'), ('Phần tử đơn vị', 'IₘA = AIₙ = A'),
            ('Không giao hoán', 'AB ≠ BA  (nói chung)'), ('Chuyển vị của tích', '(AB)ᵀ = BᵀAᵀ')]
    for k, (a, b) in enumerate(rows):
        if L.st(8) > 0.4 + 0.9 * k:
            col = O if k >= 3 else DARK
            fig.text(0.12, 0.74 - 0.1 * k, a, fontsize=19, color=col, weight='bold' if k >= 3 else 'normal')
            fig.text(0.46, 0.74 - 0.1 * k, b, fontsize=21, color=col)

# ---------- hình học: trực giao, định thức ----------
SQ = np.array([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]).T
def poly(ax, A, color, alpha=0.25, lw=2):
    P = A @ SQ; ax.fill(P[0], P[1], color=color, alpha=alpha); ax.plot(P[0], P[1], color=color, lw=lw)
def s_geo(fig):
    if L.now < L.T[10]:
        L.base(fig, 'Ma trận trực giao: quay hoặc phản xạ')
        th = np.radians(50 * ease(L.pr(9, 4))); Q = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-1.6, 2.2), (-0.5, 2.2))
        poly(ax, np.eye(2), LIGHT, 0.12, 1); poly(ax, Q, B)
        x = np.array([1.6, 0.6]); arrow(ax, x, LIGHT, 2); arrow(ax, Q @ x, O)
        fig.text(0.77, 0.72, r'$\mathbf{Q}^{\top}\mathbf{Q}=\mathbf{I}$', ha='center', fontsize=24, color=DARK)
        fig.text(0.77, 0.6, r'$(\mathbf{Qx})^{\top}(\mathbf{Qy})=\mathbf{x}^{\top}\mathbf{y}$', ha='center', fontsize=20, color=DARK)
        fig.text(0.77, 0.47, f'‖x‖ = {vn(np.linalg.norm(x))}    ‖Qx‖ = {vn(np.linalg.norm(Q @ x))}', ha='center', fontsize=17, color=O)
        fig.text(0.77, 0.37, f'góc quay {vn(np.degrees(th), 0)}°', ha='center', fontsize=15, color=INK)
        fig.text(0.77, 0.28, r'$\mathbf{Q}^{-1}=\mathbf{Q}^{\top}$', ha='center', fontsize=20, color=T)
        return
    L.base(fig, 'Định thức: hệ số co giãn diện tích')
    A = np.array([[1.5, 0.5], [0.3, 1.2]]); Z = np.array([[1.5, 0.75], [0.6, 0.3]])
    if L.now < L.T[11]: M_ = np.eye(2) + (A - np.eye(2)) * ease(L.pr(10, 3))
    else: M_ = A + (Z - A) * ease((L.st(11) - 1) / 3.5)
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-0.4, 2.6), (-0.4, 1.9))
    poly(ax, np.eye(2), LIGHT, 0.1, 1); poly(ax, M_, O if L.on(11) else B)
    d = np.linalg.det(M_)
    box(fig, 0.77, 0.74, r'$\det\begin{pmatrix}a&b\\ c&d\end{pmatrix}=ad-bc$'.replace(r'\begin{pmatrix}a&b\\ c&d\end{pmatrix}', r'\left(\genfrac{}{}{0}{}{a\ \ b}{c\ \ d}\right)'), 20)
    fig.text(0.77, 0.58, f'A = [{vn(M_[0,0])}  {vn(M_[0,1])};  {vn(M_[1,0])}  {vn(M_[1,1])}]', ha='center', fontsize=16, color=INK)
    fig.text(0.77, 0.48, f'diện tích = |det A| = {vn(abs(d))}', ha='center', fontsize=20, color=O if abs(d) < 0.05 else B)
    if L.on(11):
        fig.text(0.77, 0.36, 'det A ≠ 0  ⇔  A khả nghịch', ha='center', fontsize=18, color=DARK)
        if abs(d) < 0.02: fig.text(0.77, 0.27, 'det A = 0: ép dẹt, không đảo ngược được', ha='center', fontsize=15, color=O)

# ---------- giải hệ, hạng ----------
def s_rank(fig):
    if L.now < L.T[13]:
        L.base(fig, 'Giải hệ Ax = b trong thực hành')
        code = ['import numpy as np', '', '# không nên', 'x = np.linalg.inv(A) @ b', '', '# nên dùng', 'x = np.linalg.solve(A, b)']
        for k, c in enumerate(code):
            if L.st(12) > 0.3 * k:
                fig.text(0.12, 0.76 - 0.065 * k, c, fontsize=19, family='DejaVu Sans Mono', color=(LIGHT if c.startswith('#') else (RED if 'inv' in c else (T if 'solve' in c else DARK))))
        fig.text(0.62, 0.62, 'Phân rã LU / Cholesky / QR', fontsize=17, color=DARK)
        fig.text(0.62, 0.54, '→ chính xác hơn, nhanh hơn', fontsize=17, color=T)
        return
    if L.now < L.T[14]:
        L.base(fig, 'Hạng và số nghiệm của hệ Ax = b')
        x = np.linspace(-1, 4, 10)
        cases = [('Nghiệm duy nhất', [(1, 1, 3), (1, -1, 0)], T, 'rank A = n'), ('Vô nghiệm', [(1, 1, 3), (1, 1, 1.5)], O, 'rank[A|b] > rank A'),
                 ('Vô số nghiệm', [(1, 1, 3), (2, 2, 6)], B, 'rank A < n, tương thích')]
        for k, (lab, eqs, col, cond) in enumerate(cases):
            if L.st(13) > 0.8 + 1.6 * k:
                ax = ax_at(fig, [0.05 + 0.31 * k, 0.3, 0.27, 0.45], (-1, 4), (-1, 4), fs=8)
                for j, (a, b_, c) in enumerate(eqs):
                    ax.plot(x, (c - a * x) / b_, color=[DARK, col][j], lw=2.5 if j else 2, ls='-' if j == 0 else ('--' if k == 2 else '-'))
                if k == 0: ax.plot(1.5, 1.5, 'o', color=T, ms=10)
                ax.set_title(lab, color=col, fontsize=15); fig.text(0.05 + 0.31 * k + 0.135, 0.22, cond, ha='center', fontsize=13, color=INK)
        return
    L.base(fig, 'Hệ quá xác định trong học máy')
    r = np.random.default_rng(2); xs = np.sort(r.uniform(0, 10, 25)); ys = 1 + 0.6 * xs + r.normal(0, 0.8, 25)
    ax = ax_at(fig, [0.06, 0.18, 0.5, 0.68], (0, 10), (0, 9), equal=False, xl='x', yl='y')
    ax.scatter(xs, ys, color=B, s=25, zorder=3)
    if L.st(14) > 3:
        w = np.polyfit(xs, ys, 1); ax.plot([0, 10], np.polyval(w, [0, 10]), color=O, lw=2.5)
    fig.text(0.62, 0.68, '25 phương trình, 2 ẩn', fontsize=19, color=DARK)
    fig.text(0.62, 0.58, 'không đường thẳng nào đi qua mọi điểm', fontsize=15, color=INK)
    if L.st(14) > 3: fig.text(0.62, 0.46, '→ nghiệm bình phương nhỏ nhất (Bài 7)', fontsize=16, color=O)

# ---------- ma trận thiết kế ----------
X0 = np.array([[1.0, 2.0], [2.0, 1.5], [3.0, 4.2]]); W0 = np.array([0.5, -1.2]); Y0 = X0 @ W0
def s_design(fig):
    L.base(fig, 'Biểu diễn dữ liệu bằng ma trận thiết kế')
    s = L.st(15); hr = int(s // 1.2) % 3 if L.now < L.T[16] else None
    grid(fig, 0.1, 0.72, X0, cw=0.08, rh=0.1, fs=18, hi=(lambda i, j: '#d5efe9' if hr is not None and i == hr else None),
         label=r'$\mathbf{X}\in\mathbb{R}^{3\times2}$')
    fig.text(0.1, 0.36, '3 mẫu (hàng) × 2 đặc trưng (cột)', fontsize=15, color=INK)
    if L.on(16):
        k = L.st(16)
        fig.text(0.28, 0.58, '×', fontsize=26, color=INK)
        grid(fig, 0.31, 0.67, W0.reshape(2, 1), cw=0.08, rh=0.1, fs=18, label=r'$\mathbf{w}$')
        fig.text(0.41, 0.58, '=', fontsize=26, color=INK)
        grid(fig, 0.44, 0.72, Y0.reshape(3, 1), cw=0.1, rh=0.1, fs=18, color=O, vis=lambda i, j: k > 1 + 0.8 * i,
             label=r'$\hat{\mathbf{y}}=\mathbf{Xw}$')
        if k > 3.5:
            code = ['X = np.array([[1.0, 2.0],', '              [2.0, 1.5],', '              [3.0, 4.2]])',
                    'w = np.array([0.5, -1.2])', 'y_hat = X @ w', '# [-1.9  -0.8  -3.54]']
            for j, c in enumerate(code):
                fig.text(0.62, 0.72 - 0.06 * j, c, fontsize=14, family='DejaVu Sans Mono', color=LIGHT if c.startswith('#') else DARK)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 17, ['Véc tơ là véc tơ cột; ma trận nhìn theo phần tử, cột hoặc hàng', 'Phép nhân: kết hợp, phân phối, KHÔNG giao hoán',
                        '(AB)ᵀ = BᵀAᵀ  ·  Q trực giao: Q⁻¹ = Qᵀ', 'det A ≠ 0 ⇔ A khả nghịch; hạng quyết định số nghiệm',
                        'Ma trận thiết kế X ∈ ℝⁿˣᵈ:  ŷ = Xw'], gap=1.3)

SCENES = [(0, s_title), (1, s_vec), (3, s_views), (4, s_mul), (8, s_props), (9, s_geo), (12, s_rank), (15, s_design), (17, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
