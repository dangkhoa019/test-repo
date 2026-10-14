"""Video Bài 2 - Không gian véc tơ, ánh xạ tuyến tính và chuẩn.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 2 · Không gian véc tơ, ánh xạ tuyến tính và chuẩn', TEXTS, SPOKEN, 'bai02_khong_gian_vec_to',
           mins={0: 5}, chapter='Chương 1 · Một số kiến thức cơ bản')

def s_title(fig):
    L.title(fig, 'Bài 2. Không gian véc tơ và chuẩn', r'$\|\mathbf{x}\|_p=\left(\sum_i |x_i|^p\right)^{1/p}$')

# ---------- không gian con ----------
def s_sub(fig):
    L.base(fig, 'Không gian véc tơ và không gian con')
    if L.now < L.T[2]:
        items = [r'$\mathbb{R}^n$', r'tập ma trận cùng cỡ $\mathbb{R}^{m\times n}$', 'tập đa thức bậc ≤ k', 'tập hàm liên tục trên một đoạn']
        fig.text(0.1, 0.76, 'Tám tiên đề: giao hoán, kết hợp, phần tử 0, phần tử đối, 1·x = x, (αβ)x = α(βx), hai luật phân phối',
                 fontsize=13.5, color=INK)
        for k, s in enumerate(items):
            if L.st(1) > 1 + 1.3 * k: fig.text(0.12, 0.64 - 0.09 * k, '• ' + s, fontsize=19, color=DARK)
        return
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3, 3), (-2.5, 3.5), xl='$x_1$', yl='$x_2$')
    x = np.linspace(-3, 3, 10)
    ax.plot(x, 2 * x, color=T, lw=2.5); ax.plot(0, 0, 'o', color=DARK, ms=7)
    ax.text(0.25, -2.2, r'$S_1:\ x_2=2x_1$', color=T, fontsize=15)
    if L.now < L.T[3]:
        u, v = np.array([0.5, 1.0]), np.array([0.8, 1.6]); k = ease((L.st(2) - 1.5) / 2)
        arrow(ax, u, B); arrow(ax, v, O)
        if k > 0: arrow(ax, (u + v) * k, DARK, 2.5)
        if k > 0.95:
            ax.text(*(u + v + [0.1, -0.2]), r'$\mathbf{u}+\mathbf{v}\in S_1$', fontsize=15, color=DARK)
            arrow(ax, -1.6 * u, LIGHT, 2.5); ax.text(-1.2, -1.9, r'$-1{,}6\,\mathbf{u}\in S_1$', fontsize=14, color=INK)
        fig.text(0.6, 0.7, r'$\mathbf{0}\in S_1$  ✓', fontsize=20, color=T)
        fig.text(0.6, 0.6, 'khép kín với phép cộng  ✓', fontsize=18, color=T)
        fig.text(0.6, 0.5, 'khép kín với nhân vô hướng  ✓', fontsize=18, color=T)
        fig.text(0.6, 0.36, '→ không gian con: đường thẳng qua gốc', fontsize=16, color=DARK)
        return
    ax.plot(x, 2 * x + 1, color=O, lw=2.5); ax.text(-2.9, -1.6, r'$S_2:\ x_2=2x_1+1$', color=O, fontsize=15)
    u, v = np.array([0.0, 1.0]), np.array([0.5, 2.0]); k = ease((L.st(3) - 1) / 2)
    ax.plot(*u, 'o', color=O, ms=8); ax.plot(*v, 'o', color=O, ms=8)
    if k > 0:
        w = (u + v) * k; arrow(ax, w, RED, 2.5)
        if k > 0.95: ax.text(*(u + v + [0.1, 0]), r'$\mathbf{u}+\mathbf{v}\notin S_2$', fontsize=15, color=RED)
    fig.text(0.6, 0.7, r'$\mathbf{0}\notin S_2$  ✗', fontsize=20, color=RED)
    fig.text(0.6, 0.58, 'Trong ℝ², không gian con chỉ có thể là:', fontsize=15, color=DARK)
    fig.text(0.62, 0.5, '{0},  một đường thẳng qua gốc,  hoặc ℝ²', fontsize=15, color=DARK)

# ---------- độc lập tuyến tính, cơ sở ----------
def s_basis(fig):
    if L.now < L.T[5]:
        L.base(fig, 'Độc lập tuyến tính và cơ sở')
        v1, v2 = np.array([1.0, 0.4]), np.array([0.3, 1.0])
        for k, (w2, title, col) in enumerate([(v2, 'v₁, v₂ độc lập → sinh ra cả ℝ²', T), (2 * v1, 'v₂ = 2v₁: phụ thuộc → chỉ sinh một đường', O)]):
            ax = ax_at(fig, [0.05 + 0.47 * k, 0.17, 0.42, 0.62], (-3, 3), (-3, 3), fs=8)
            n = int(ease(L.pr(4, 5)) * 9) + 1; a = np.linspace(-2, 2, 9)[:n]
            if n > 0:
                A1, A2 = np.meshgrid(np.linspace(-2, 2, 9), a)
                P = A1[..., None] * v1 + A2[..., None] * w2
                ax.scatter(P[..., 0].ravel(), P[..., 1].ravel(), s=10, color=col, alpha=0.6)
            arrow(ax, v1, B); arrow(ax, w2, DARK, 2.5)
            ax.set_title(title, fontsize=13.5, color=col)
        return
    L.base(fig, 'Số chiều và đa cộng tuyến')
    r = np.random.default_rng(4); h = r.normal(1.65, 0.08, 40)
    ax = ax_at(fig, [0.06, 0.18, 0.42, 0.66], (1.4, 1.9), (140, 190), equal=False, xl='chiều cao (m)', yl='chiều cao (cm)')
    ax.scatter(h, 100 * h + r.normal(0, 0.3, 40), s=20, color=B)
    X = np.c_[np.ones(40), h, 100 * h + r.normal(0, 0.3, 40)]
    fig.text(0.56, 0.74, r'$\dim\mathbb{R}^n=n$  (cơ sở chính tắc $\mathbf{e}_1,\dots,\mathbf{e}_n$)', fontsize=16, color=DARK)
    if L.st(5) > 3:
        fig.text(0.56, 0.6, 'Hai cột gần như tỉ lệ (m và cm):', fontsize=16, color=DARK)
        c = np.linalg.cond(X.T @ X); e = int(np.floor(np.log10(c)))
        fig.text(0.56, 0.5, f'số điều kiện của XᵀX ≈ {vn(c / 10 ** e, 1)}·10' + ''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(ch)] for ch in str(e)), fontsize=17, color=O)
        fig.text(0.56, 0.4, '→ XᵀX gần suy biến, nghiệm rất nhạy với nhiễu', fontsize=15, color=INK)
        fig.text(0.56, 0.31, '→ khắc phục: điều chuẩn (Bài 8)', fontsize=15, color=T)

# ---------- ánh xạ tuyến tính ----------
def warp(ax, M_, color, n=7, lw=1.2):
    g = np.linspace(-3, 3, n)
    for c in g:
        P = M_ @ np.vstack([np.full(50, c), np.linspace(-3, 3, 50)]); ax.plot(P[0], P[1], color=color, lw=lw)
        P = M_ @ np.vstack([np.linspace(-3, 3, 50), np.full(50, c)]); ax.plot(P[0], P[1], color=color, lw=lw)
def s_map(fig):
    if L.now < L.T[7]:
        L.base(fig, 'Ánh xạ tuyến tính = ma trận')
        A = np.array([[1.2, 0.6], [0.3, 1.1]]); M_ = np.eye(2) + (A - np.eye(2)) * ease((L.st(6) - 1) / 3)
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3, 3), (-2.6, 2.6))
        warp(ax, np.eye(2), GRID, lw=0.8); warp(ax, M_, '#b9c2ea')
        arrow(ax, M_[:, 0], B); arrow(ax, M_[:, 1], O); ax.plot(0, 0, 'o', color=DARK, ms=6)
        ax.text(*(M_[:, 0] + [0.1, -0.3]), r'$T(\mathbf{e}_1)$', color=B, fontsize=15); ax.text(*(M_[:, 1] + [-0.6, 0.15]), r'$T(\mathbf{e}_2)$', color=O, fontsize=15)
        box(fig, 0.77, 0.72, r'$\mathbf{A}=[\,T(\mathbf{e}_1)\ \ T(\mathbf{e}_2)\,]$', 18)
        fig.text(0.77, 0.58, f'A = [{vn(A[0,0],1)}  {vn(A[0,1],1)};  {vn(A[1,0],1)}  {vn(A[1,1],1)}]', ha='center', fontsize=16, color=INK)
        fig.text(0.77, 0.46, 'đường thẳng → đường thẳng', ha='center', fontsize=15, color=DARK)
        fig.text(0.77, 0.39, 'gốc tọa độ giữ nguyên', ha='center', fontsize=15, color=DARK)
        return
    L.base(fig, 'Không gian nghiệm, không gian cột và định lý hạng – số chiều')
    A = np.array([[1.0, 2.0], [0.5, 1.0]]); k = ease((L.st(7) - 1) / 3); M_ = np.eye(2) + (A - np.eye(2)) * k
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3, 3), (-2.6, 2.6))
    t = np.linspace(-1.2, 1.2, 9); N = np.c_[2 * t, -t]          # null(A) = span{(2, −1)}
    P = (M_ @ N.T).T; ax.scatter(P[:, 0], P[:, 1], color=O, s=30, zorder=4)
    ax.plot(*(M_ @ np.c_[[-2.4, 1.2], [2.4, -1.2]]), color=O, lw=1.5, ls='--')
    ax.plot([-2.4, 2.4], [1.2, -1.2], color=O, lw=1, alpha=0.3)  # null(A) trước khi biến đổi
    C = M_ @ np.vstack([np.linspace(-3, 3, 2), np.zeros(2)]); ax.plot(*C, color=T, lw=2.5)
    fig.text(0.6, 0.76, 'A = [1  2;  0,5  1]   (det A = 0)', fontsize=16, color=INK)
    fig.text(0.6, 0.66, 'null(A) = span{(2, −1)}  → bị ép về 0', fontsize=16, color=O)
    fig.text(0.6, 0.58, 'col(A) = span{(1; 0,5)}: một đường thẳng', fontsize=16, color=T)
    box(fig, 0.75, 0.44, r'$\dim\,\mathrm{null}(\mathbf{A})+\mathrm{rank}\,\mathbf{A}=n$', 18)
    fig.text(0.75, 0.33, '1 + 1 = 2', ha='center', fontsize=18, color=DARK)

# ---------- tích vô hướng và hình chiếu ----------
def s_dot(fig):
    ax = None
    if L.now < L.T[9]:
        L.base(fig, 'Tích vô hướng, độ dài và góc')
        th2 = np.radians(25 + 95 * ease(L.pr(8, 6)))
        x, y = np.array([2.2, 0.0]) @ np.array([[np.cos(.3), np.sin(.3)], [-np.sin(.3), np.cos(.3)]]), 1.8 * np.array([np.cos(th2), np.sin(th2)])
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 2.8), (-0.6, 2.4))
        arrow(ax, x, B); arrow(ax, y, O)
        a0, a1 = np.arctan2(x[1], x[0]), np.arctan2(y[1], y[0]); arc = np.linspace(a0, a1, 30)
        ax.plot(0.6 * np.cos(arc), 0.6 * np.sin(arc), color=DARK, lw=1.5); ax.text(0.7 * np.cos((a0 + a1) / 2), 0.7 * np.sin((a0 + a1) / 2), 'θ', fontsize=16)
        c = x @ y / np.linalg.norm(x) / np.linalg.norm(y)
        box(fig, 0.77, 0.72, r'$\cos\theta=\dfrac{\langle\mathbf{x},\mathbf{y}\rangle}{\|\mathbf{x}\|_2\,\|\mathbf{y}\|_2}$', 20)
        fig.text(0.77, 0.52, f'cos θ = {vn(c)}', ha='center', fontsize=22, color=O)
        fig.text(0.77, 0.42, 'cos θ = 0 ⇔ x ⟂ y (trực giao)'.replace('⟂', 'vuông góc'), ha='center', fontsize=14, color=INK)
        fig.text(0.77, 0.33, '|⟨x, y⟩| ≤ ‖x‖₂‖y‖₂  (Cauchy – Schwarz)', ha='center', fontsize=14, color=INK)
        return
    L.base(fig, 'Hình chiếu trực giao')
    u, y = np.array([2.6, 0.9]), np.array([1.2, 2.0]); p = (y @ u) / (u @ u) * u; k = ease((L.st(9) - 1) / 3)
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-0.5, 3.2), (-0.4, 2.4))
    ax.plot(*np.c_[-0.4 * u / np.linalg.norm(u), 3.4 * u / np.linalg.norm(u)], color=LIGHT, lw=1.5)
    arrow(ax, u, B); arrow(ax, y, DARK); ax.text(*(u + [0.05, -0.25]), r'$\mathbf{u}$', fontsize=16, color=B); ax.text(*(y + [0.05, 0.05]), r'$\mathbf{y}$', fontsize=16)
    q = y + (p - y) * k; ax.plot(*np.c_[y, q], ls='--', color=O, lw=2)
    if k > 0.95:
        arrow(ax, p, O, 3.5); ax.text(*(p + [0.05, -0.28]), r'proj$_{\mathbf{u}}\mathbf{y}$', fontsize=15, color=O)
        d = (y - p) / np.linalg.norm(y - p) * 0.12; e = u / np.linalg.norm(u) * 0.12
        ax.plot(*np.c_[p + d, p + d - e, p - e], color=DARK, lw=1.2)
    box(fig, 0.77, 0.7, r'$\mathrm{proj}_{\mathbf{u}}\mathbf{y}=\dfrac{\langle\mathbf{y},\mathbf{u}\rangle}{\langle\mathbf{u},\mathbf{u}\rangle}\,\mathbf{u}$', 20)
    fig.text(0.77, 0.5, 'phần dư y − proj vuông góc với u', ha='center', fontsize=15, color=DARK)
    fig.text(0.77, 0.4, '→ điểm gần y nhất trên đường thẳng', ha='center', fontsize=15, color=T)

# ---------- chuẩn ----------
def unit_ball(p, n=400):
    t = np.linspace(0, 2 * np.pi, n); c, s = np.cos(t), np.sin(t)
    if np.isinf(p): r = 1 / np.maximum(abs(c), abs(s))
    else: r = 1 / (abs(c) ** p + abs(s) ** p) ** (1 / p)
    return r * c, r * s
# bài toán minh họa LASSO: cực tiểu (w−c)ᵀΣ(w−c) trên hình cầu ‖w‖ ≤ 1
SIG = np.array([[1.5, 0.3], [0.3, 1.0]]); CEN = np.array([1.8, 0.8])
loss = lambda W: np.einsum('...i,ij,...j->...', W - CEN, SIG, W - CEN)
def ball_min(p):
    x, y = unit_ball(p, 4000); P = np.c_[x, y]; i = np.argmin(loss(P)); return P[i]
W1, W2 = ball_min(1), ball_min(2)
def s_norm(fig):
    if L.now < L.T[12]:
        L.base(fig, 'Các chuẩn ℓ₁, ℓ₂, ℓ∞ và hình cầu đơn vị')
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-1.6, 1.6), (-1.3, 1.3))
        if L.now < L.T[11]:
            u = L.pr(10, 8); p = 1 + 9 * u ** 3 if u < 0.97 else np.inf
            for q, col in [(1, B), (2, O), (np.inf, T)]: ax.plot(*unit_ball(q), color=col, lw=1, alpha=0.35)
            ax.plot(*unit_ball(p), color=DARK, lw=3)
            fig.text(0.77, 0.6, 'p = ∞' if np.isinf(p) else f'p = {vn(p, 1)}', ha='center', fontsize=26, color=DARK)
            box(fig, 0.77, 0.75, r'$\|\mathbf{x}\|_p=\left(\sum_i|x_i|^p\right)^{1/p}$', 18)
            fig.text(0.77, 0.45, r'$\|\mathbf{x}\|_\infty=\max_i |x_i|$', ha='center', fontsize=18, color=T)
        else:
            for q, col, lab in [(1, B, 'ℓ₁'), (2, O, 'ℓ₂'), (np.inf, T, 'ℓ∞')]: ax.plot(*unit_ball(q), color=col, lw=2.5, label=lab)
            ax.legend(loc='lower right', fontsize=12)
            vals = [('‖x‖₁ = |3| + |−4| = 7', B), ('‖x‖₂ = √(9 + 16) = 5', O), ('‖x‖∞ = max(3, 4) = 4', T)]
            fig.text(0.6, 0.76, 'x = (3, −4)', fontsize=22, color=DARK)
            for k, (s, c) in enumerate(vals):
                if L.st(11) > 1 + 1.4 * k: fig.text(0.6, 0.64 - 0.1 * k, s, fontsize=20, color=c)
        return
    L.base(fig, 'Vì sao ℓ₁ cho nghiệm thưa?')
    for k, (p, w, col, lab) in enumerate([(1, W1, B, 'Ràng buộc ℓ₁ (LASSO)'), (2, W2, O, 'Ràng buộc ℓ₂ (ridge)')]):
        ax = ax_at(fig, [0.05 + 0.47 * k, 0.17, 0.42, 0.66], (-1.5, 2.5), (-1.3, 1.9), fs=8)
        g1, g2 = np.meshgrid(np.linspace(-1.5, 2.5, 200), np.linspace(-1.3, 1.9, 200)); Z = loss(np.dstack([g1, g2]))
        lv = loss(w); ax.contour(g1, g2, Z, levels=[lv * f for f in (0.25, 0.55, 1)] + [lv * 1.8, lv * 3], colors=[LIGHT] * 2 + [DARK] + [LIGHT] * 2, linewidths=1.2)
        ax.fill(*unit_ball(p), color=col, alpha=0.25); ax.plot(*unit_ball(p), color=col, lw=2.5)
        ax.plot(*CEN, '+', color=DARK, ms=12, mew=2)
        if L.st(12) > 2:
            ax.plot(*w, 'o', color=RED, ms=11, zorder=6)
            ax.text(w[0] + 0.08, w[1] + 0.12, f'w* = ({vn(w[0])}; {vn(w[1])})', fontsize=12, color=RED)
        ax.set_title(lab, fontsize=14, color=col)

# ---------- khoảng cách, chuẩn hóa ----------
def s_dist(fig):
    r = np.random.default_rng(5)
    if L.now < L.T[14]:
        L.base(fig, 'Khoảng cách và k láng giềng gần nhất')
        P = r.uniform(-3, 3, (40, 2)); q = np.array([0.4, 0.2]); d = np.linalg.norm(P - q, axis=1); idx = np.argsort(d)[:5]
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3.2, 3.2), (-3.2, 3.2))
        ax.scatter(*P.T, s=25, color=LIGHT); ax.plot(*q, '*', color=O, ms=18, zorder=5)
        k = ease((L.st(13) - 1) / 2.5); rad = d[idx[-1]] * k
        t = np.linspace(0, 2 * np.pi, 100); ax.plot(q[0] + rad * np.cos(t), q[1] + rad * np.sin(t), color=O, lw=1.5)
        if k > 0.95:
            ax.scatter(*P[idx].T, s=50, color=B, zorder=4)
            for i in idx: ax.plot(*np.c_[q, P[i]], color=B, lw=1)
        box(fig, 0.77, 0.7, r'$d(\mathbf{x},\mathbf{y})=\|\mathbf{x}-\mathbf{y}\|$', 20)
        fig.text(0.77, 0.55, '5 láng giềng gần nhất (ℓ₂)', ha='center', fontsize=16, color=B)
        fig.text(0.77, 0.45, 'đổi chuẩn → đổi láng giềng', ha='center', fontsize=15, color=INK)
        return
    L.base(fig, 'Chuẩn hóa dữ liệu z-score')
    yrs = r.uniform(0, 10, 50); inc = 5 + 2.5 * yrs + r.normal(0, 6, 50)
    X = np.c_[yrs, inc]; Z = (X - X.mean(0)) / X.std(0); k = ease((L.st(14) - 2) / 3)
    P = X + (Z - X) * k
    ax = ax_at(fig, [0.06, 0.18, 0.45, 0.66], (-0.5 - 2.5 * k, 10.5 - 7.5 * k), (-5 + 2 * k, 45 - 42 * k), equal=False,
               xl='số năm kinh nghiệm' if k < 0.5 else 'z (năm)', yl='thu nhập (triệu đồng)' if k < 0.5 else 'z (thu nhập)')
    ax.scatter(*P.T, s=22, color=B)
    box(fig, 0.77, 0.7, r'$z_{ij}=\dfrac{x_{ij}-\mu_j}{\sigma_j}$', 22)
    fig.text(0.77, 0.52, 'mỗi cột: trung bình 0, độ lệch chuẩn 1', ha='center', fontsize=15, color=DARK)
    fig.text(0.77, 0.43, '→ các đặc trưng đóng góp cân bằng', ha='center', fontsize=15, color=T)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 15, ['Không gian con chứa gốc, khép kín với cộng và nhân vô hướng', 'Cơ sở: độc lập tuyến tính + sinh; số phần tử = số chiều',
                        'Ánh xạ tuyến tính ↔ ma trận; dim null(A) + rank A = n', 'Tích vô hướng cho độ dài, góc, hình chiếu trực giao',
                        'ℓ₁ khuyến khích nghiệm thưa, ℓ₂ nghiệm nhỏ; cần chuẩn hóa dữ liệu'], gap=1.6)

SCENES = [(0, s_title), (1, s_sub), (4, s_basis), (6, s_map), (8, s_dot), (10, s_norm), (13, s_dist), (15, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
