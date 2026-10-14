"""Video Bài 5 - Tập lồi, hàm lồi và bài toán tối ưu lồi.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 5 · Tập lồi, hàm lồi và bài toán tối ưu lồi', TEXTS, SPOKEN, 'bai05_toi_uu_loi',
           mins={0: 5, 1: 10}, chapter='Chương 2 · Một số bài toán tối ưu')

def s_title(fig):
    L.title(fig, 'Bài 5. Tập lồi, hàm lồi và tối ưu lồi', r'$f(t\mathbf{x}+(1-t)\mathbf{y})\leq t f(\mathbf{x})+(1-t)f(\mathbf{y})$')

# ---------- tập lồi ----------
tt = np.linspace(0, 2 * np.pi, 400)
ELL = np.c_[1.3 * np.cos(tt), 0.9 * np.sin(tt)]
BLOB = np.c_[(1 + 0.5 * np.cos(3 * tt)) * np.cos(tt), (1 + 0.5 * np.cos(3 * tt)) * np.sin(tt)]
from matplotlib.path import Path
def s_sets(fig):
    if L.now < L.T[2]:
        L.base(fig, 'Tập lồi')
        u = L.pr(1, L.slots[1] - 0.5)
        for k, (S, lab) in enumerate([(ELL, '(a) tập lồi'), (BLOB, '(b) tập không lồi')]):
            ax = ax_at(fig, [0.04 + 0.47 * k, 0.17, 0.42, 0.62], (-1.6, 1.6), (-1.4, 1.4), fs=8)
            ax.fill(*S.T, color=B, alpha=0.15); ax.plot(*S.T, color=B, lw=2)
            if k == 0: x, y = np.array([-0.9, -0.4]), np.array([0.6 + 0.4 * np.cos(4 * u), 0.5 * np.sin(4 * u)])
            else:
                a2 = 2.0944 + 0.12 * np.sin(4 * u); x, y = np.array([1.38, 0.0]), 1.38 * np.array([np.cos(a2), np.sin(a2)])
            seg = np.linspace(0, 1, 60)[:, None] * x + (1 - np.linspace(0, 1, 60)[:, None]) * y
            inside = Path(S).contains_points(seg)
            ax.scatter(*seg.T, s=8, c=[T if i else RED for i in inside], zorder=4)
            ax.plot(*x, 'o', color=DARK, ms=7); ax.plot(*y, 'o', color=DARK, ms=7)
            ax.set_title(lab + ('' if inside.all() else ': đoạn thẳng ra ngoài'), fontsize=14, color=T if inside.all() else RED)
        return
    L.base(fig, 'Một số tập lồi thường gặp')
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 2), (-2, 2))
    g = np.linspace(-2, 2, 2)
    hs = [((1, 1), 1.2), ((-1, 0.6), 1.2), ((0.3, -1), 1.1)]
    for i, (a, b) in enumerate(hs):
        if L.st(2) > 0.5 + 1.2 * i:
            a = np.array(a); x = np.linspace(-2, 2, 50)
            ax.plot(x, (b - a[0] * x) / a[1], color=LIGHT, lw=1.5)
    if L.st(2) > 4.5:
        G = np.meshgrid(np.linspace(-2, 2, 300), np.linspace(-2, 2, 300)); P = np.dstack(G)
        ok = np.ones(P.shape[:2], bool)
        for a, b in hs: ok &= P @ np.array(a) <= b
        ax.contourf(G[0], G[1], ok.astype(float), levels=[0.5, 1.5], colors=[T], alpha=0.35)
        ax.text(-0.5, -0.1, 'giao các nửa\nkhông gian', fontsize=13, color=T)
    items = ['ℝᵈ', 'nửa không gian {x : aᵀx ≤ b}', 'hình cầu {x : ‖x − c‖ ≤ r} (mọi chuẩn)', 'mọi không gian con', 'giao của các tập lồi']
    for k, s in enumerate(items):
        if L.st(2) > 0.3 + 1.0 * k: fig.text(0.58, 0.74 - 0.08 * k, '• ' + s, fontsize=16, color=DARK if k < 4 else T)

# ---------- hàm lồi ----------
FC = lambda x: 0.35 * (x - 0.5) ** 2 + 0.6
def s_func(fig):
    if L.now < L.T[4]:
        L.base(fig, 'Hàm lồi: dây cung nằm trên đồ thị')
        xs = np.linspace(-2.5, 3.5, 300); a, b = -1.8, 2.8; t = 0.5 + 0.45 * np.sin(2 * np.pi * L.st(3) / 4)
        ax = ax_at(fig, [0.05, 0.17, 0.52, 0.68], (-2.5, 3.5), (0, 5), equal=False, xl='x', yl='f(x)')
        ax.plot(xs, FC(xs), color=B, lw=2.5); ax.plot([a, b], [FC(a), FC(b)], color=O, lw=2)
        xm = t * a + (1 - t) * b; ax.plot([xm, xm], [FC(xm), t * FC(a) + (1 - t) * FC(b)], color=T, lw=2.5)
        ax.plot(xm, FC(xm), 'o', color=B, ms=9); ax.plot(xm, t * FC(a) + (1 - t) * FC(b), 'o', color=O, ms=9)
        fig.text(0.78, 0.66, f't = {vn(t)}', ha='center', fontsize=20, color=DARK)
        fig.text(0.78, 0.56, f'f(tx + (1−t)y) = {vn(FC(xm))}', ha='center', fontsize=16, color=B)
        fig.text(0.78, 0.48, f't f(x) + (1−t) f(y) = {vn(t * FC(a) + (1 - t) * FC(b))}', ha='center', fontsize=16, color=O)
        fig.text(0.78, 0.38, 'luôn ≤  ✓', ha='center', fontsize=18, color=T)
        return
    if L.now < L.T[5]:
        L.base(fig, 'Lồi, lồi ngặt, lồi mạnh')
        xs = np.linspace(-1.5, 1.5, 200)
        cases = [(np.abs(xs), 'f = |x|: lồi, không lồi ngặt', INK), (xs ** 4, 'f = x⁴: lồi ngặt, không lồi mạnh', B), (xs ** 2, 'f = x²: lồi mạnh (m = 2)', T)]
        for k, (y, lab, c) in enumerate(cases):
            if L.st(4) > 0.5 + 1.8 * k:
                ax = ax_at(fig, [0.04 + 0.32 * k, 0.24, 0.28, 0.48], (-1.5, 1.5), (-0.2, 2.3), equal=False, fs=8)
                ax.plot(xs, y, color=c, lw=2.5); ax.set_title(lab, fontsize=12.5, color=c)
        return
    L.base(fig, 'Quan hệ giữa các mức độ lồi')
    lev = [('lồi mạnh', 'hội tụ tuyến tính của giảm gradient\n(khi gradient còn Lipschitz)', T), ('lồi ngặt', 'nghiệm duy nhất (nếu tồn tại)', B), ('lồi', 'không có cực tiểu địa phương giả', INK)]
    for k, (a, b, c) in enumerate(lev):
        if L.st(5) > 0.5 + 1.4 * k:
            fig.text(0.2, 0.7 - 0.15 * k, a, fontsize=24, color=c, weight='bold', ha='center', bbox=dict(boxstyle='round,pad=0.5', fc='white', ec=c))
            fig.text(0.38, 0.7 - 0.15 * k, b, fontsize=16, color=DARK, va='center')
            if k < 2: fig.text(0.2, 0.62 - 0.15 * k, '⇓', fontsize=24, color=INK, ha='center')

def s_crit(fig):
    xs = np.linspace(-2.5, 3.5, 300)
    if L.now < L.T[7]:
        L.base(fig, 'Tiêu chuẩn bậc nhất: tiếp tuyến nằm dưới đồ thị')
        ax = ax_at(fig, [0.05, 0.17, 0.52, 0.68], (-2.5, 3.5), (-0.5, 5), equal=False, xl='x', yl='f(x)')
        ax.plot(xs, FC(xs), color=B, lw=2.5)
        x0 = -2 + 5 * L.pr(6, L.slots[6] - 0.5); d = 0.7 * (x0 - 0.5)
        ax.plot(xs, FC(x0) + d * (xs - x0), color=O, lw=2); ax.plot(x0, FC(x0), 'o', color=O, ms=9)
        box(fig, 0.79, 0.68, r'$f(\mathbf{y})\geq f(\mathbf{x})+\nabla f(\mathbf{x})^{\top}(\mathbf{y}-\mathbf{x})$', 15)
        fig.text(0.79, 0.52, 'với mọi x, y', ha='center', fontsize=16, color=INK)
        return
    L.base(fig, 'Tiêu chuẩn bậc hai')
    rows = [(r'$f$ lồi', r'$\Leftrightarrow\ \nabla^2 f(\mathbf{x})\succeq 0\ \ \forall\mathbf{x}$', DARK),
            (r'$\nabla^2 f(\mathbf{x})\succ 0\ \ \forall\mathbf{x}$', r'$\Rightarrow\ f$ lồi ngặt', B),
            (r'$f$ lồi mạnh tham số $m$', r'$\Leftrightarrow\ \nabla^2 f(\mathbf{x})\succeq m\mathbf{I}\ \ \forall\mathbf{x}$', T)]
    for k, (a, b, c) in enumerate(rows):
        if L.st(7) > 0.5 + 2.5 * k:
            fig.text(0.08, 0.74 - 0.1 * k, a, fontsize=21, color=c); fig.text(0.42, 0.74 - 0.1 * k, b, fontsize=21, color=c)
    if L.st(7) > 8:
        ax = ax_at(fig, [0.12, 0.17, 0.35, 0.25], (-1.5, 1.5), (-1, 28), equal=False, fs=8); x = np.linspace(-1.5, 1.5, 200)
        ax.plot(x, 12 * x ** 2, color=B, lw=2.5); ax.set_title("x⁴:  f″ = 12x² ≥ 0, bằng 0 tại 0 → không lồi mạnh", fontsize=12, color=B)

def s_ops(fig):
    if L.now < L.T[9]:
        L.base(fig, 'Các phép toán bảo toàn tính lồi')
        rows = [('Nhân với số α ≥ 0', 'αf lồi', 'hệ số điều chuẩn λ ≥ 0'), ('Tổng', 'f + g lồi', 'mất mát + số hạng điều chuẩn'),
                ('Hợp với ánh xạ afin', 'f(Ax + b) lồi', '‖Xw − y‖₂²'), ('Lấy cực đại', 'max(f, g) lồi', 'mất mát bản lề của SVM'), ('Mọi chuẩn', '‖·‖ lồi', 'điều chuẩn ℓ₁, ℓ₂')]
        for c, h in zip([0.08, 0.38, 0.6], ['Phép toán', 'Phát biểu', 'Ví dụ trong học máy']): fig.text(c, 0.78, h, fontsize=16, color=B, weight='bold')
        for k, r in enumerate(rows):
            if L.st(8) > 0.4 + 1.2 * k:
                for c, s in zip([0.08, 0.38, 0.6], r): fig.text(c, 0.68 - 0.085 * k, s, fontsize=16, color=DARK)
        return
    L.base(fig, 'Ví dụ 2.3: hàm mất mát ridge là lồi mạnh')
    # X có hai cột trùng nhau ⇒ XᵀX suy biến; λ làm bài toán có nghiệm duy nhất
    r = np.random.default_rng(1); x = r.normal(size=30); X = np.c_[x, x]; y = 1.5 * x + r.normal(0, 0.3, 30)
    lam = 3.0 * ease((L.st(9) - 3) / 3)
    g1, g2 = np.meshgrid(np.linspace(-1, 3, 200), np.linspace(-1, 3, 200)); W = np.dstack([g1, g2])
    J = ((W @ X.T - y) ** 2).sum(-1) + lam * (W ** 2).sum(-1)
    ax = ax_at(fig, [0.04, 0.16, 0.48, 0.72], (-1, 3), (-1, 3), xl='$w_1$', yl='$w_2$')
    ax.contour(g1, g2, J, levels=np.quantile(J, [0.01, 0.04, 0.1, 0.2, 0.35, 0.55]), colors=B, linewidths=1.2)
    if lam > 0.05:
        w = np.linalg.solve(X.T @ X + lam * np.eye(2), X.T @ y); ax.plot(*w, '*', color=T, ms=18)
    fig.text(0.56, 0.76, 'X có hai cột trùng nhau ⇒ XᵀX suy biến', fontsize=15, color=INK)
    fig.text(0.56, 0.67, r'$\nabla^2 J=2\mathbf{X}^{\top}\mathbf{X}+2\lambda\mathbf{I}\succeq 2\lambda\mathbf{I}\succ 0$', fontsize=20, color=DARK)
    fig.text(0.56, 0.55, f'λ = {vn(lam)}', fontsize=22, color=O)
    fig.text(0.56, 0.45, 'λ = 0: thung lũng phẳng, vô số nghiệm' if lam < 0.05 else 'λ > 0: lồi mạnh, nghiệm duy nhất ★', fontsize=16, color=RED if lam < 0.05 else T)

def s_cvx(fig):
    if L.now < L.T[11]:
        L.base(fig, 'Bài toán tối ưu lồi')
        box(fig, 0.5, 0.72, r'$\min\ f_0(\mathbf{x})$  v.đ.k.  $f_i(\mathbf{x})\leq 0$ (lồi),  $h_j(\mathbf{x})=0$ (afin)', 22)
        if L.st(10) > 3: fig.text(0.5, 0.52, 'Định lý: mọi cực tiểu địa phương đều là cực tiểu toàn cục', ha='center', fontsize=21, color=T, weight='bold')
        if L.st(10) > 6: fig.text(0.5, 0.4, 'f₀ lồi ngặt ⇒ nghiệm tối ưu (nếu tồn tại) là duy nhất', ha='center', fontsize=18, color=DARK)
        return
    if L.now < L.T[12]:
        L.base(fig, 'Ý chứng minh')
        f = lambda x: 0.25 * (x - 2.5) ** 2 + 0.5; xs = np.linspace(-1, 4.5, 300); xs_, xb = 0.0, 3.0
        ax = ax_at(fig, [0.05, 0.17, 0.52, 0.68], (-1, 4.5), (0, 3), equal=False, xl='x', yl='f(x)')
        ax.plot(xs, f(xs), color=B, lw=2.5); ax.plot([xs_, xb], [f(xs_), f(xb)], color=O, lw=2)
        ax.plot(xs_, f(xs_), 'o', color=RED, ms=10); ax.text(xs_ + 0.05, f(xs_) + 0.12, 'x* (giả sử cực tiểu địa phương)', fontsize=12, color=RED)
        ax.plot(xb, f(xb), 'o', color=T, ms=10); ax.text(xb - 0.3, f(xb) - 0.25, 'x: f(x) < f(x*)', fontsize=12, color=T)
        tval = 0.15 + 0.8 * ease((L.st(11) - 2) / 4); xt = tval * xs_ + (1 - tval) * xb
        ax.plot(xt, f(xt), 'o', color=O, ms=9); ax.axhline(f(xs_), color=RED, ls=':', lw=1)
        fig.text(0.6, 0.7, r'$\mathbf{x}_t=t\mathbf{x}^*+(1-t)\mathbf{x}$', fontsize=19, color=DARK)
        fig.text(0.6, 0.6, r'$f(\mathbf{x}_t)\leq t f(\mathbf{x}^*)+(1-t)f(\mathbf{x})<f(\mathbf{x}^*)$', fontsize=17, color=DARK)
        fig.text(0.6, 0.48, f't = {vn(tval)}: x_t tiến sát x*', fontsize=17, color=O)
        fig.text(0.6, 0.38, '→ mâu thuẫn với tính cực tiểu địa phương  ◻', fontsize=16, color=T)
        return
    L.base(fig, 'Vì sao học máy ưa chuộng hàm mất mát lồi')
    x = np.linspace(-3, 3, 300)
    for k, (y, lab, c) in enumerate([(0.4 * x ** 2, 'Lồi: hồi quy tuyến tính, logistic, SVM', T), (0.25 * x ** 2 + np.sin(3 * x) + 0.4 * np.cos(7 * x), 'Phi lồi: mạng nơ-ron sâu', O)]):
        if L.st(12) > 0.5 + 3 * k:
            ax = ax_at(fig, [0.05 + 0.47 * k, 0.22, 0.42, 0.52], (-3, 3), (-2, 4), equal=False, fs=8)
            ax.plot(x, y, color=c, lw=2.5); ax.set_title(lab, fontsize=14, color=c)
    if L.st(12) > 6: fig.text(0.5, 0.15, 'Lồi: tìm được điểm dừng là có nghiệm tốt nhất', ha='center', fontsize=15, color=DARK)

def s_lp(fig):
    L.base(fig, 'Quy hoạch tuyến tính và quy hoạch toàn phương')
    box(fig, 0.76, 0.74, r'LP:  $\min\ \mathbf{c}^{\top}\mathbf{x}$  v.đ.k.  $\mathbf{Ax}\leq\mathbf{b}$', 17)
    box(fig, 0.76, 0.6, r'QP:  $\min\ \frac{1}{2}\mathbf{x}^{\top}\mathbf{Px}+\mathbf{q}^{\top}\mathbf{x}$, $\mathbf{P}\succeq 0$', 16)
    fig.text(0.76, 0.46, 'SVM lề cứng là một QP (Bài 6)', ha='center', fontsize=15, color=T)
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-0.5, 4), (-0.5, 4), xl='$x_1$', yl='$x_2$')
    V = np.array([[0, 0], [3, 0], [3, 1.2], [1.6, 3], [0, 2.5], [0, 0]])
    ax.fill(*V.T, color=B, alpha=0.2); ax.plot(*V.T, color=B, lw=2)
    c = np.array([-1.0, -1.4]); lv = max(-0.5 - 6.0 * ease((L.st(13) - 1) / 4), (V[:-1] @ c).min()); x = np.linspace(-0.5, 4, 2)
    ax.plot(x, (lv - c[0] * x) / c[1], color=O, lw=2, ls='--')
    vals = V[:-1] @ c; best = V[np.argmin(vals)]
    if lv <= vals.min() + 1e-6: ax.plot(*best, '*', color=T, ms=20); ax.text(best[0] + 0.1, best[1] + 0.1, 'nghiệm tại một đỉnh', fontsize=13, color=T)
    fig.text(0.76, 0.34, 'đường mức cᵀx = hằng số trượt\ntới đỉnh tối ưu của đa giác', ha='center', fontsize=14, color=INK)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 14, ['Tập lồi chứa trọn đoạn thẳng; giao các tập lồi vẫn lồi', 'Hàm lồi: dây cung trên đồ thị, tiếp tuyến dưới đồ thị',
                        'Kiểm tra: ∇²f ⪰ 0, hoặc dùng phép toán bảo toàn tính lồi', 'Bài toán lồi: cực tiểu địa phương = toàn cục',
                        'LP và QP là hai lớp bài toán lồi chuẩn'], gap=1.6)

SCENES = [(0, s_title), (1, s_sets), (3, s_func), (6, s_crit), (8, s_ops), (10, s_cvx), (13, s_lp), (14, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
