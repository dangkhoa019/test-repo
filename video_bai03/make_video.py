"""Video Bài 3 - Giá trị riêng, phân rã ma trận, gradient và Hessian.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 3 · Giá trị riêng, phân rã ma trận, gradient và Hessian', TEXTS, SPOKEN, 'bai03_gia_tri_rieng',
           mins={0: 5, 2: 9, 9: 8}, chapter='Chương 1 · Một số kiến thức cơ bản')

def s_title(fig):
    L.title(fig, 'Bài 3. Giá trị riêng, gradient và Hessian', r'$\mathbf{Av}=\lambda\mathbf{v},\quad \mathbf{A}=\mathbf{U}\Sigma\mathbf{V}^{\top}$')

A3 = np.array([[4.0, 1.0], [2.0, 3.0]])
def s_eig(fig):
    L.base(fig, 'Giá trị riêng và véc tơ riêng')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-6, 6), (-4.5, 4.5))
    if L.now < L.T[3]:
        th = np.radians(360 * ease(L.st(2) / (L.slots[2] - 0.5))) if L.on(2) else np.radians(20)
        v = np.array([np.cos(th), np.sin(th)]); Av = A3 @ v
        for d, c in [((1, 1), T), ((1, -2), T)]:
            d = np.array(d) / np.linalg.norm(d); ax.plot(*np.c_[-6 * d, 6 * d], color=c, lw=1, alpha=0.4)
        arrow(ax, v, B); arrow(ax, Av, O)
        ax.text(*(v * 1.25), r'$\mathbf{v}$', fontsize=16, color=B); ax.text(*(Av + Av / np.linalg.norm(Av) * 0.4), r'$\mathbf{Av}$', fontsize=16, color=O)
        cross = abs(v[0] * Av[1] - v[1] * Av[0]) / np.linalg.norm(Av)
        box(fig, 0.77, 0.74, r'$\mathbf{Av}=\lambda\mathbf{v},\quad \mathbf{v}\neq\mathbf{0}$', 20)
        fig.text(0.77, 0.6, 'A = [4  1;  2  3]', ha='center', fontsize=17, color=INK)
        if cross < 0.03:
            lam = (Av @ v); fig.text(0.77, 0.47, f'cùng phương!  λ = {vn(lam, 1)}', ha='center', fontsize=22, color=T, weight='bold')
        else:
            fig.text(0.77, 0.47, 'Av đổi phương so với v', ha='center', fontsize=17, color=INK)
        return
    for v, lam, c in [((1, 1), 5, B), ((1, -2), 2, O)]:
        v = np.array(v, float); d = v / np.linalg.norm(v)
        ax.plot(*np.c_[-6 * d, 6 * d], color=c, lw=1, alpha=0.4)
        k = ease((L.st(4) - 1) / 2) if L.on(4) else 0
        arrow(ax, v, c, 2.5)
        if k > 0: arrow(ax, v * (1 + (lam - 1) * k), c, 4)
    ax.text(1.2, 0.6, r'$\mathbf{v}_1$', color=B, fontsize=16); ax.text(1.2, -2.3, r'$\mathbf{v}_2$', color=O, fontsize=16)
    rows = [r'$\det(\mathbf{A}-\lambda\mathbf{I})=(4-\lambda)(3-\lambda)-2$', r'$=\lambda^2-7\lambda+10=0$', r'$\lambda_1=5,\quad \lambda_2=2$']
    for k, r in enumerate(rows):
        if L.st(3) > 1 + 1.5 * k or L.on(4): fig.text(0.58, 0.76 - 0.09 * k, r, fontsize=18, color=DARK if k < 2 else T)
    if L.on(4):
        fig.text(0.58, 0.46, r'$\mathbf{v}_1=(1,1),\ \ \mathbf{Av}_1=5\mathbf{v}_1$', fontsize=17, color=B)
        fig.text(0.58, 0.38, r'$\mathbf{v}_2=(1,-2),\ \ \mathbf{Av}_2=2\mathbf{v}_2$', fontsize=17, color=O)
        if L.st(4) > 4: fig.text(0.58, 0.27, 'λ₁ + λ₂ = 7 = tr A,    λ₁λ₂ = 10 = det A', fontsize=16, color=DARK)

S3 = np.array([[2.0, 1.0], [1.0, 1.5]]); LS, QS = np.linalg.eigh(S3)
def s_spec(fig):
    L.base(fig, 'Ma trận đối xứng và phân rã phổ')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3, 3), (-2.4, 2.4))
    t = np.linspace(0, 2 * np.pi, 200); C = np.vstack([np.cos(t), np.sin(t)])
    k = ease((L.st(6) - 0.5) / 3) if L.on(6) else 0; M_ = np.eye(2) + (S3 - np.eye(2)) * k
    ax.plot(*C, color=LIGHT, lw=1.5); ax.plot(*(M_ @ C), color=B, lw=2.5)
    for i, c in [(1, O), (0, T)]:
        q = QS[:, i] * np.sign(QS[0, i] if QS[0, i] != 0 else 1); arrow(ax, q * (1 + (LS[i] - 1) * k), c, 3)
    box(fig, 0.77, 0.74, r'$\mathbf{A}=\mathbf{Q}\Lambda\mathbf{Q}^{\top}=\sum_i\lambda_i\,\mathbf{q}_i\mathbf{q}_i^{\top}$', 18)
    fig.text(0.77, 0.6, 'A = [2  1;  1  1,5]', ha='center', fontsize=16, color=INK)
    fig.text(0.77, 0.52, f'λ₁ = {vn(LS[1])},  λ₂ = {vn(LS[0])}', ha='center', fontsize=16, color=INK)
    if L.on(7):
        box(fig, 0.77, 0.38, r'$\lambda_{\min}\leq\dfrac{\mathbf{x}^{\top}\mathbf{A}\mathbf{x}}{\mathbf{x}^{\top}\mathbf{x}}\leq\lambda_{\max}$', 18)
        th = np.radians(360 * L.pr(7, 6)); x = np.array([np.cos(th), np.sin(th)]); R_ = x @ S3 @ x
        arrow(ax, x, DARK, 2); fig.text(0.77, 0.25, f'R(x) = {vn(R_)}', ha='center', fontsize=18, color=O)

def s_pd(fig):
    if L.now < L.T[9]:
        L.base(fig, 'Ma trận xác định dương')
        rows = [(r'$\mathbf{A}\succ 0$:  $\mathbf{x}^{\top}\mathbf{A}\mathbf{x}>0\ \ \forall\mathbf{x}\neq\mathbf{0}$', '⇔ mọi λᵢ > 0', DARK),
                (r'$\mathbf{A}\succeq 0$:  $\mathbf{x}^{\top}\mathbf{A}\mathbf{x}\geq 0\ \ \forall\mathbf{x}$', '⇔ mọi λᵢ ≥ 0', DARK),
                (r'$\mathbf{x}^{\top}\mathbf{X}^{\top}\mathbf{X}\mathbf{x}=\|\mathbf{X}\mathbf{x}\|_2^2\geq 0$', '⇒ XᵀX ⪰ 0 với mọi X', T),
                ('Cột của X độc lập tuyến tính', '⇒ XᵀX ≻ 0 và khả nghịch', O)]
        for k, (a, b, c) in enumerate(rows):
            if L.st(8) > 0.5 + 1.6 * k:
                fig.text(0.1, 0.74 - 0.12 * k, a, fontsize=20, color=c); fig.text(0.62, 0.74 - 0.12 * k, b, fontsize=18, color=c)
        return
    L.base(fig, 'Dạng toàn phương: chén và yên ngựa')
    g = np.linspace(-1.5, 1.5, 40); X1, X2 = np.meshgrid(g, g); az = -60 + 40 * L.pr(9)
    for k, (A, lab, c) in enumerate([(np.diag([1.0, 2.0]), 'A ≻ 0: cực tiểu tại gốc', T), (np.diag([1.5, -1.5]), 'A không xác định dấu: yên ngựa', O)]):
        ax = fig.add_axes([0.03 + 0.48 * k, 0.12, 0.46, 0.66], projection='3d')
        Z = A[0, 0] * X1 ** 2 + A[1, 1] * X2 ** 2
        ax.plot_surface(X1, X2, Z, cmap='Blues' if k == 0 else 'Oranges', linewidth=0, alpha=0.9, rstride=2, cstride=2)
        ax.view_init(28, az); ax.set_title(lab, fontsize=14, color=c); ax.tick_params(labelsize=7)

def s_svd(fig):
    if L.now < L.T[11]:
        L.base(fig, 'Phân rã giá trị suy biến (SVD)')
        A = np.array([[1.6, 0.9], [0.3, 1.1]]); U, s, Vt = np.linalg.svd(A)
        stage = L.st(10); t = np.linspace(0, 2 * np.pi, 200); C = np.vstack([np.cos(t), np.sin(t)])
        k1, k2, k3 = [ease((stage - a) / 1.8) for a in (1, 3.2, 5.4)]
        def rot_interp(R, k):
            a = np.arctan2(R[1, 0], R[0, 0]); det = np.linalg.det(R)
            Rk = np.array([[np.cos(a * k), -np.sin(a * k)], [np.sin(a * k), np.cos(a * k)]])
            return Rk if det > 0 else (np.eye(2) + (R - np.eye(2)) * k)
        M_ = rot_interp(U, k3) @ (np.eye(2) + (np.diag(s) - np.eye(2)) * k2) @ rot_interp(Vt, k1)
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2.6, 2.6), (-2, 2))
        ax.plot(*C, color=LIGHT, lw=1.5); ax.plot(*(M_ @ C), color=B, lw=2.5)
        arrow(ax, M_ @ Vt[0], O, 3); arrow(ax, M_ @ Vt[1], T, 3)
        box(fig, 0.77, 0.75, r'$\mathbf{A}=\mathbf{U}\,\Sigma\,\mathbf{V}^{\top}$', 26)
        steps = [('1. Vᵀ: quay', k1), ('2. Σ: co giãn σ₁ = ' + vn(s[0]) + ', σ₂ = ' + vn(s[1]), k2), ('3. U: quay', k3)]
        for i, (lab, k) in enumerate(steps):
            fig.text(0.6, 0.6 - 0.08 * i, lab, fontsize=17, color=O if 0 < k < 1 else (DARK if k >= 1 else LIGHT))
        fig.text(0.6, 0.3, 'số σᵢ khác 0 = hạng của A', fontsize=16, color=T)
        return
    L.base(fig, 'Xấp xỉ hạng thấp bằng SVD')
    for j, k in enumerate([1, 5, 20, None]):
        Ak = IMG if k is None else (IU[:, :k] * IS[:k]) @ IVt[:k]
        if L.st(11) > 0.5 + 1.2 * j:
            ax = fig.add_axes([0.03 + 0.24 * j, 0.32, 0.22, 0.48]); ax.imshow(Ak, cmap='gray', vmin=0, vmax=1); ax.set_xticks([]); ax.set_yticks([]); ax.grid(False)
            err = 0 if k is None else np.linalg.norm(IMG - Ak) / np.linalg.norm(IMG)
            ax.set_title('ảnh gốc (hạng ' + str(np.linalg.matrix_rank(IMG)) + ')' if k is None else f'k = {k}   sai số {vn(100 * err, 1)}%', fontsize=12.5, color=DARK)
    fig.text(0.5, 0.24, 'Giữ k giá trị suy biến lớn nhất: xấp xỉ hạng k tốt nhất theo chuẩn Frobenius', ha='center', fontsize=15, color=T)

def make_img():  # ảnh tổng hợp 120×120 để minh họa nén
    f = plt.figure(figsize=(1.2, 1.2), dpi=100); a = f.add_axes([0, 0, 1, 1]); a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis('off')
    yy, xx = np.mgrid[0:1:120j, 0:1:120j]; a.imshow(0.35 + 0.3 * xx * yy, cmap='gray', vmin=0, vmax=1, extent=(0, 1, 0, 1))
    a.add_patch(plt.Circle((0.3, 0.68), 0.18, color='0.9')); a.add_patch(plt.Rectangle((0.55, 0.15), 0.32, 0.3, color='0.1', angle=12))
    a.text(0.5, 0.3, 'TVU', fontsize=22, ha='center', color='white', weight='bold'); f.canvas.draw()
    im = np.asarray(f.canvas.buffer_rgba())[..., :3].mean(-1) / 255; plt.close(f); return im
IMG = make_img(); IU, IS, IVt = np.linalg.svd(IMG)

FQ = lambda x, y: x ** 2 + 3 * y ** 2 + 0.6 * x * y
def s_grad(fig):
    if L.now < L.T[13]:
        L.base(fig, 'Gradient')
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2.2, 2.2), (-1.6, 1.6))
        g1, g2 = np.meshgrid(np.linspace(-2.2, 2.2, 200), np.linspace(-1.6, 1.6, 200))
        ax.contour(g1, g2, FQ(g1, g2), levels=[0.3, 0.8, 1.6, 2.8, 4.4], colors=B, linewidths=1.2)
        pts = [(1.2, 0.5), (-1.0, 0.6), (0.4, -0.8), (-1.5, -0.3), (1.6, -0.4)]
        for i, (x, y) in enumerate(pts):
            if L.st(12) > 0.8 * i:
                g = np.array([2 * x + 0.6 * y, 6 * y + 0.6 * x]); arrow(ax, g / np.linalg.norm(g) * 0.5, O, 2.5, origin=(x, y)); ax.plot(x, y, 'o', color=O, ms=5)
        box(fig, 0.77, 0.72, r'$\nabla f(\mathbf{x})=\left(\dfrac{\partial f}{\partial x_1},\dots,\dfrac{\partial f}{\partial x_d}\right)^{\top}$', 17)
        fig.text(0.77, 0.55, 'vuông góc với đường đồng mức', ha='center', fontsize=16, color=DARK)
        fig.text(0.77, 0.47, '∇f: hướng tăng nhanh nhất', ha='center', fontsize=16, color=O)
        fig.text(0.77, 0.39, '−∇f: hướng giảm nhanh nhất', ha='center', fontsize=16, color=T)
        return
    if L.now < L.T[14]:
        L.base(fig, 'Ma trận Jacobian và quy tắc chuỗi')
        box(fig, 0.5, 0.74, r'$\mathbf{J}_{\mathbf{f}}=\left[\dfrac{\partial f_i}{\partial x_j}\right]\in\mathbb{R}^{m\times n}$', 22)
        k = L.st(13)
        nodes = [(0.15, r'$\mathbf{x}\in\mathbb{R}^{n}$'), (0.45, r'$\mathbf{g}(\mathbf{x})\in\mathbb{R}^{p}$'), (0.75, r'$\mathbf{f}(\mathbf{g}(\mathbf{x}))\in\mathbb{R}^{m}$')]
        for i, (x, s) in enumerate(nodes):
            if k > 0.8 * i: fig.text(x, 0.5, s, fontsize=20, color=DARK, ha='center', bbox=dict(boxstyle='round,pad=0.5', fc='white', ec=B))
        if k > 1.5: fig.text(0.3, 0.52, '→', fontsize=28, color=INK, ha='center'); fig.text(0.6, 0.52, '→', fontsize=28, color=INK, ha='center')
        if k > 2.5: fig.text(0.5, 0.32, r'$\mathbf{J}_{\mathbf{f}\circ\mathbf{g}}(\mathbf{x})=\mathbf{J}_{\mathbf{f}}(\mathbf{g}(\mathbf{x}))\ \mathbf{J}_{\mathbf{g}}(\mathbf{x})$', ha='center', fontsize=22, color=O)
        if k > 4: fig.text(0.5, 0.22, '(m×p)·(p×n) = m×n   —   lan truyền ngược trong mạng nơ-ron', ha='center', fontsize=15, color=INK)
        return
    L.base(fig, 'Ma trận Hessian')
    box(fig, 0.5, 0.72, r'$\nabla^2 f(\mathbf{x})=\left[\dfrac{\partial^2 f}{\partial x_i\,\partial x_j}\right]_{d\times d}$', 24)
    fig.text(0.5, 0.54, 'Ví dụ  f = x₁² + 3x₂² + 0,6x₁x₂:', ha='center', fontsize=17, color=INK)
    if L.st(14) > 2: fig.text(0.5, 0.45, r'$\nabla^2 f=\left(\genfrac{}{}{0}{}{2\quad\ \ 0{,}6}{0{,}6\quad\ \ 6}\right)$  đối xứng', ha='center', fontsize=20, color=DARK)
    if L.st(14) > 4: fig.text(0.5, 0.3, 'Định lý Clairaut: đạo hàm cấp hai liên tục ⇒ ∂²f/∂x₁∂x₂ = ∂²f/∂x₂∂x₁', ha='center', fontsize=15, color=T)

AE, BE = np.array([[3.0, 1.0], [1.0, 2.0]]), np.array([1.0, 1.0]); XS = np.linalg.solve(AE, BE)
FE = lambda x, y: 0.5 * (3 * x ** 2 + 2 * x * y + 2 * y ** 2) - x - y
def s_rules(fig):
    if L.now < L.T[16]:
        L.base(fig, 'Một số quy tắc giải tích ma trận')
        rows = [(r'$\mathbf{a}^{\top}\mathbf{x}$', r'$\mathbf{a}$', ''), (r'$\mathbf{x}^{\top}\mathbf{A}\mathbf{x}$', r'$(\mathbf{A}+\mathbf{A}^{\top})\mathbf{x}$', 'A vuông'),
                (r'$\mathbf{x}^{\top}\mathbf{A}\mathbf{x}$', r'$2\mathbf{A}\mathbf{x}$', 'A đối xứng'), (r'$\|\mathbf{x}\|_2^2$', r'$2\mathbf{x}$', ''),
                (r'$\|\mathbf{A}\mathbf{x}-\mathbf{b}\|_2^2$', r'$2\mathbf{A}^{\top}(\mathbf{A}\mathbf{x}-\mathbf{b})$', 'bình phương nhỏ nhất')]
        fig.text(0.15, 0.78, 'f(x)', fontsize=17, color=B, weight='bold'); fig.text(0.42, 0.78, '∇f(x)', fontsize=17, color=B, weight='bold')
        for k, (a, b, c) in enumerate(rows):
            if L.st(15) > 0.6 + 1.8 * k:
                fig.text(0.15, 0.68 - 0.09 * k, a, fontsize=21, color=DARK); fig.text(0.42, 0.68 - 0.09 * k, b, fontsize=21, color=O); fig.text(0.72, 0.68 - 0.09 * k, c, fontsize=15, color=INK)
        return
    L.base(fig, 'Ví dụ 1.4: hàm toàn phương')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-1.3, 1.7), (-1.0, 1.6), xl='$x_1$', yl='$x_2$')
    g1, g2 = np.meshgrid(np.linspace(-1.3, 1.7, 200), np.linspace(-1.0, 1.6, 200))
    ax.contour(g1, g2, FE(g1, g2), levels=FE(*XS) + np.array([0.05, 0.25, 0.6, 1.2, 2.0, 3.0]), colors=B, linewidths=1.2, negative_linestyles='solid')
    if L.st(16) > 4: ax.plot(*XS, '*', color=T, ms=18); ax.text(XS[0] + 0.12, XS[1] - 0.18, r'$\mathbf{x}^*$', fontsize=17, color=T)
    fig.text(0.58, 0.76, r'$f(\mathbf{x})=\frac{1}{2}\mathbf{x}^{\top}\mathbf{A}\mathbf{x}-\mathbf{b}^{\top}\mathbf{x}$', fontsize=20, color=DARK)
    if L.st(16) > 1.5: fig.text(0.58, 0.66, r'$\nabla f=\mathbf{A}\mathbf{x}-\mathbf{b},\qquad \nabla^2 f=\mathbf{A}$', fontsize=19, color=O)
    if L.st(16) > 3:
        fig.text(0.58, 0.54, 'A = [3  1;  1  2] ≻ 0,  b = (1, 1)', fontsize=16, color=INK)
        fig.text(0.58, 0.45, f'x* = A⁻¹b = ({vn(XS[0], 1)}; {vn(XS[1], 1)})', fontsize=18, color=T)
        fig.text(0.58, 0.34, 'cực tiểu toàn cục duy nhất', fontsize=16, color=T)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 17, ['Véc tơ riêng: hướng không đổi phương, co giãn hệ số λ', 'A đối xứng: A = QΛQᵀ, λ thực, Q trực giao',
                        'XᵀX ⪰ 0; ≻ 0 khi các cột của X độc lập tuyến tính', 'SVD A = UΣVᵀ cho mọi ma trận; số σᵢ ≠ 0 = hạng',
                        'Gradient: hướng tăng nhanh nhất · Hessian: độ cong'], gap=1.8)

SCENES = [(0, s_title), (1, s_eig), (5, s_spec), (8, s_pd), (10, s_svd), (12, s_grad), (15, s_rules), (17, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
