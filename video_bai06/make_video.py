"""Video Bài 6 - Nhân tử Lagrange, tính đối ngẫu và điều kiện KKT.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 6 · Nhân tử Lagrange, tính đối ngẫu và điều kiện KKT', TEXTS, SPOKEN, 'bai06_lagrange_kkt',
           mins={0: 5}, chapter='Chương 2 · Một số bài toán tối ưu')

def s_title(fig):
    L.title(fig, 'Bài 6. Lagrange, đối ngẫu và KKT', r'$\nabla f(\mathbf{x}^*)+\lambda\,\nabla h(\mathbf{x}^*)=\mathbf{0}$')

def circles(ax, lim=3, lv=(0.5, 1, 2, 3, 4.5, 6.5)):
    t = np.linspace(0, 2 * np.pi, 200)
    for r2 in lv: ax.plot(np.sqrt(r2) * np.cos(t), np.sqrt(r2) * np.sin(t), color=GRID, lw=1.2)
def s_lag(fig):
    L.base(fig, 'Ràng buộc đẳng thức và nhân tử Lagrange')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-1.5, 3), (-1.5, 3), xl='$x_1$', yl='$x_2$')
    circles(ax); x = np.linspace(-1.5, 3, 2); ax.plot(x, 2 - x, color=O, lw=2.5); ax.text(2.1, -0.3, '$x_1+x_2=2$', color=O, fontsize=14)
    if L.now < L.T[2]:
        s = L.st(1); p = np.array([2.6, -0.6]) + (np.array([-0.4, 2.4]) - np.array([2.6, -0.6])) * (0.5 + 0.5 * np.sin(s * 0.9))
        ax.plot(*p, 'o', color=B, ms=10); arrow(ax, (-p[0], -p[1]) / np.linalg.norm(p) * 0.6, RED, 2.5, origin=p)
        fig.text(0.6, 0.7, '−∇f chỉ về gốc, nhưng điểm phải', fontsize=16, color=DARK)
        fig.text(0.6, 0.63, 'nằm trên đường ràng buộc', fontsize=16, color=DARK)
        fig.text(0.6, 0.5, f'f = x₁² + x₂² = {vn(p @ p)}', fontsize=18, color=B)
        return
    r = np.sqrt(2) * ease(L.pr(2, 3)); t = np.linspace(0, 2 * np.pi, 200); ax.plot(r * np.cos(t), r * np.sin(t), color=B, lw=2.5)
    if r > 1.4:
        ax.plot(1, 1, 'o', color=T, ms=11); arrow(ax, (0.8, 0.8), B, 3, origin=(1, 1)); arrow(ax, (0.4, 0.4), O, 3, origin=(1, 1))
        ax.text(1.85, 1.75, r'$\nabla f$', fontsize=16, color=B); ax.text(1.45, 1.15, r'$\nabla h$', fontsize=15, color=O)
    box(fig, 0.77, 0.74, r'$\nabla f(\mathbf{x}^*)+\lambda\nabla h(\mathbf{x}^*)=\mathbf{0},\ \ h(\mathbf{x}^*)=0$', 15)
    if L.on(3): fig.text(0.77, 0.62, r'$L(\mathbf{x},\lambda)=f(\mathbf{x})+\lambda h(\mathbf{x})$', ha='center', fontsize=20, color=DARK)
    if L.on(4):
        rows = [r'$L=x_1^2+x_2^2+\lambda(x_1+x_2-2)$', r'$2x_1+\lambda=0,\ \ 2x_2+\lambda=0$', r'$x_1=x_2=-\lambda/2,\ \ -\lambda=2$',
                r'$\lambda=-2,\ \ \mathbf{x}^*=(1,1),\ \ f^*=2$']
        for k, rr in enumerate(rows):
            if L.st(4) > 1 + 2.6 * k: fig.text(0.58, 0.5 - 0.075 * k, rr, fontsize=17, color=T if k == 3 else DARK)

def s_dual(fig):
    if L.now < L.T[6]:
        L.base(fig, 'Hàm Lagrange tổng quát và hàm đối ngẫu')
        box(fig, 0.5, 0.72, r'$L(\mathbf{x},\lambda,\nu)=f_0(\mathbf{x})+\sum_i\lambda_i f_i(\mathbf{x})+\sum_j\nu_j h_j(\mathbf{x}),\quad \lambda_i\geq 0$', 20)
        if L.st(5) > 3: box(fig, 0.5, 0.52, r'$g(\lambda,\nu)=\inf_{\mathbf{x}}\ L(\mathbf{x},\lambda,\nu)$', 22)
        if L.st(5) > 6: fig.text(0.5, 0.36, 'cận dưới đúng của một họ hàm afin  ⇒  g luôn lõm  ⇒  bài toán đối ngẫu luôn lồi', ha='center', fontsize=16, color=T)
        return
    if L.now < L.T[7]:
        L.base(fig, 'Đối ngẫu yếu và đối ngẫu mạnh')
        lg = np.linspace(0, 4, 200); g = 3.2 - 0.55 * (lg - 2.3) ** 2
        for k, (p, title) in enumerate([(3.2, '(a) Đối ngẫu mạnh: p* − d* = 0'), (4.1, '(b) Có khoảng trống: p* − d* > 0')]):
            ax = ax_at(fig, [0.06 + 0.48 * k, 0.2, 0.4, 0.55], (-0.2, 4.2), (-1, 5), equal=False, xl=r'$\lambda\geq 0$', fs=8)
            ax.plot(lg, g, color=B, lw=2.2); ax.axhline(p, color=O, ls='--', lw=2); ax.plot(2.3, 3.2, 'o', color=T, ms=7)
            ax.text(3.6, p + 0.15, '$p^*$', color=O, fontsize=14); ax.text(2.0, 2.5, '$d^*=g(\\lambda^*)$', color=T, fontsize=12); ax.set_title(title, fontsize=13)
        fig.text(0.5, 0.82, 'd* ≤ p*  (luôn đúng)', ha='center', fontsize=18, color=DARK)
        return
    L.base(fig, 'Điều kiện Slater')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 2), (-2, 2))
    t = np.linspace(0, 2 * np.pi, 200); ax.fill(1.3 * np.cos(t), 1.0 * np.sin(t), color=B, alpha=0.2); ax.plot(1.3 * np.cos(t), np.sin(t), color=B, lw=2)
    if L.st(7) > 2: ax.plot(0.2, 0.1, '*', color=T, ms=18); ax.text(0.3, 0.2, 'điểm trong chặt: fᵢ(x) < 0', fontsize=13, color=T)
    fig.text(0.58, 0.7, 'Bài toán lồi', fontsize=18, color=DARK)
    fig.text(0.58, 0.61, '+ tồn tại x chấp nhận được với fᵢ(x) < 0', fontsize=16, color=DARK)
    fig.text(0.58, 0.48, '⇒ đối ngẫu mạnh: d* = p*', fontsize=20, color=T, weight='bold')

def s_kkt(fig):
    L.base(fig, 'Điều kiện Karush – Kuhn – Tucker')
    rows = [('Chấp nhận được (gốc)', r'$f_i(\mathbf{x}^*)\leq 0,\ \ h_j(\mathbf{x}^*)=0$', DARK), ('Chấp nhận được (đối ngẫu)', r'$\lambda_i^*\geq 0$', DARK),
            ('Điều kiện bù', r'$\lambda_i^* f_i(\mathbf{x}^*)=0$', O),
            ('Điều kiện dừng', r'$\nabla f_0(\mathbf{x}^*)+\sum_i\lambda_i^*\nabla f_i(\mathbf{x}^*)+\sum_j\nu_j^*\nabla h_j(\mathbf{x}^*)=\mathbf{0}$', DARK)]
    for k, (a, b, c) in enumerate(rows):
        if L.st(8) > 0.5 + 1.4 * k or L.on(9):
            fig.text(0.06, 0.74 - 0.1 * k, f'{k + 1}. ' + a, fontsize=17, color=c, weight='bold' if c == O else 'normal'); fig.text(0.38, 0.74 - 0.1 * k, b, fontsize=18, color=c)
    if L.on(9):
        fig.text(0.1, 0.28, 'λᵢ* > 0  ⇒  fᵢ(x*) = 0   (ràng buộc hoạt động)', fontsize=17, color=O)
        fig.text(0.1, 0.2, 'fᵢ(x*) < 0  ⇒  λᵢ* = 0   (ràng buộc không hoạt động)', fontsize=17, color=T)

def s_ex(fig):
    L.base(fig, 'Ví dụ 2.5: ràng buộc hoạt động và không hoạt động')
    for k, (c, lab, xs, lam, col, show) in enumerate([(2, 'x₁ + x₂ ≥ 2: hoạt động', (1, 1), 2, O, True), (-1, 'x₁ + x₂ ≥ −1: không hoạt động', (0, 0), 0, T, L.on(11))]):
        if not show: continue
        ax = ax_at(fig, [0.04 + 0.47 * k, 0.24, 0.42, 0.56], (-2, 3), (-2, 3), fs=8)
        circles(ax); x = np.linspace(-2, 3, 50); ax.fill_between(x, c - x, 3, color=col, alpha=0.15); ax.plot(x, c - x, color=col, lw=2)
        ax.plot(*xs, '*', color=RED, ms=17); ax.set_title(lab, fontsize=14, color=col)
        fig.text(0.04 + 0.47 * k + 0.21, 0.17, f'x* = {xs},  λ* = {lam}'.replace(', ', '; ', 1).replace('(1; 1)', '(1, 1)').replace('(0; 0)', '(0, 0)'), ha='center', fontsize=16, color=DARK)
    if not L.on(11):
        rows = ['f₁(x) = 2 − x₁ − x₂ ≤ 0', 'L = x₁² + x₂² + λ(2 − x₁ − x₂)', 'λ = 0 ⇒ x = 0: vi phạm ràng buộc ✗', 'λ > 0 ⇒ x₁ + x₂ = 2 ⇒ λ = 2, x* = (1, 1) ✓']
        for k, r in enumerate(rows):
            if L.st(10) > 1 + 2.5 * k: fig.text(0.55, 0.72 - 0.09 * k, r, fontsize=16, color=[DARK, DARK, RED, T][k])

def s_suff(fig):
    L.base(fig, 'KKT: cần và đủ cho bài toán lồi')
    fig.text(0.5, 0.62, 'Bài toán lồi  +  điều kiện Slater', ha='center', fontsize=24, color=DARK)
    fig.text(0.5, 0.5, '⇓', ha='center', fontsize=30, color=INK)
    fig.text(0.5, 0.38, 'x* tối ưu  ⇔  (x*, λ*, ν*) thỏa KKT', ha='center', fontsize=24, color=T, weight='bold')

# ---------- SVM lề cứng: nghiệm chính xác bằng cách duyệt tập véc tơ hỗ trợ ----------
r = np.random.default_rng(11)
XP = r.normal([2.0, 2.2], 0.55, (14, 2)); XN = r.normal([-0.2, 0.0], 0.55, (14, 2))
XS = np.vstack([XP, XN]); YS = np.r_[np.ones(14), -np.ones(14)]
def svm_hard(X, y):
    best = None
    P, N = X[y > 0], X[y < 0]
    cands = []
    for p, q in itertools.product(P, N):
        n = p - q; cands.append((n, (p + q) / 2))
    for A, Bc in [(P, N), (N, P)]:
        for (a1, a2), c in itertools.product(itertools.combinations(A, 2), Bc):
            d = a2 - a1; n = np.array([-d[1], d[0]])
            if (c - a1) @ n > 0: n = -n
            n = n if (A is P) else -n
            off = ((c - a1) @ n) / 2; cands.append((n, a1 + n / np.linalg.norm(n) ** 2 * off))
    for n, x0 in cands:
        u = n / np.linalg.norm(n); s = y * ((X - x0) @ u)
        if s.min() > 1e-9 and (best is None or s.min() > best[0]): best = (s.min(), u, x0)
    m, u, x0 = best; w = u / m; b = -w @ x0
    return w, b
W, B0 = svm_hard(XS, YS); MARG = 1 / np.linalg.norm(W)
SV = np.abs(YS * (XS @ W + B0) - 1) < 1e-6
def s_svm(fig):
    L.base(fig, 'Ứng dụng: máy véc tơ hỗ trợ (SVM) lề cứng')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 4), (-1.8, 4))
    ax.scatter(*XP.T, color=B, s=40, zorder=3, label='yᵢ = +1'); ax.scatter(*XN.T, color=O, s=40, zorder=3, label='yᵢ = −1')
    k = ease((L.st(13) - 2) / 4) if L.now < L.T[14] else 1
    x = np.linspace(-2, 4, 2)
    for off, ls in [(0, '-'), (1, '--'), (-1, '--')]:
        if W[1] != 0: ax.plot(x, (off * k - B0 - W[0] * x) / W[1], color=DARK, ls=ls, lw=2 if off == 0 else 1.3)
    if L.on(15):
        ax.scatter(*XS[SV].T, s=220, facecolors='none', edgecolors=RED, linewidths=2.5, zorder=4)
    ax.legend(loc='lower right', fontsize=11)
    box(fig, 0.77, 0.76, r'$\min_{\mathbf{w},b}\ \frac{1}{2}\|\mathbf{w}\|_2^2\ \ \mathrm{v.đ.k.}\ \ y_i(\mathbf{w}^{\top}\mathbf{x}_i+b)\geq 1$', 14)
    fig.text(0.77, 0.64, f'lề = 2/‖w‖₂ = {vn(2 * MARG)}', ha='center', fontsize=17, color=DARK)
    if L.on(14):
        box(fig, 0.77, 0.48, r'$\max_{\alpha\succeq 0}\ \sum_i\alpha_i-\frac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j\,\mathbf{x}_i^{\top}\mathbf{x}_j$', 13)
        fig.text(0.77, 0.38, r'v.đ.k.  $\sum_i\alpha_i y_i=0$', ha='center', fontsize=15, color=INK)
    if L.on(15):
        fig.text(0.77, 0.27, f'{SV.sum()} véc tơ hỗ trợ (αᵢ > 0)', ha='center', fontsize=17, color=RED)
        fig.text(0.77, 0.2, r'$\mathbf{w}^*=\sum_i\alpha_i^* y_i\mathbf{x}_i$ chỉ gồm các điểm này', ha='center', fontsize=14, color=INK)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 16, ['Lagrange: ràng buộc đẳng thức → điểm dừng của L(x, λ)', 'Hàm đối ngẫu luôn lõm; đối ngẫu yếu d* ≤ p*',
                        'Lồi + Slater ⇒ đối ngẫu mạnh; KKT vừa cần vừa đủ', 'Điều kiện bù: chỉ ràng buộc hoạt động có λ > 0',
                        'SVM: véc tơ hỗ trợ là các điểm có αᵢ > 0'], gap=1.9)

SCENES = [(0, s_title), (1, s_lag), (5, s_dual), (8, s_kkt), (10, s_ex), (12, s_suff), (13, s_svm), (16, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
