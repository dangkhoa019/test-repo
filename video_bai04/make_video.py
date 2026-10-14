"""Video Bài 4 - Đạo hàm và bài toán cực trị không ràng buộc.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 4 · Đạo hàm và bài toán cực trị không ràng buộc', TEXTS, SPOKEN, 'bai04_cuc_tri',
           mins={0: 5, 1: 8.5, 8: 9}, chapter='Chương 2 · Một số bài toán tối ưu')

def s_title(fig):
    L.title(fig, 'Bài 4. Đạo hàm và cực trị', r'$\nabla f(\mathbf{x}^*)=\mathbf{0},\qquad \nabla^2 f(\mathbf{x}^*)\succ 0$')

F1 = lambda x: 0.3 * x ** 3 - x ** 2 + 0.4 * x + 2.2; D1 = lambda x: 0.9 * x ** 2 - 2 * x + 0.4; D2 = lambda x: 1.8 * x - 2
def s_deriv(fig):
    xs = np.linspace(-1.5, 4, 300)
    if L.now < L.T[2]:
        L.base(fig, 'Đạo hàm: hệ số góc của tiếp tuyến')
        x0 = -1.0 + 4.6 * ease(L.pr(1, L.slots[1] - 0.5))
        ax = ax_at(fig, [0.05, 0.17, 0.52, 0.68], (-1.5, 4), (-1.5, 4.5), equal=False, xl='x', yl='f(x)')
        ax.plot(xs, F1(xs), color=B, lw=2.5); h = np.array([-1, 1])
        ax.plot(x0 + h, F1(x0) + D1(x0) * h, color=O, lw=2); ax.plot(x0, F1(x0), 'o', color=O, ms=10)
        arrow(ax, (-0.6 * np.sign(D1(x0)), 0), T, 2.5, origin=(x0, F1(x0) - 0.6))
        box(fig, 0.79, 0.74, r"$f'(x)=\lim_{h\to 0}\dfrac{f(x+h)-f(x)}{h}$", 17)
        fig.text(0.79, 0.56, f"f′(x) = {vn(D1(x0))}", ha='center', fontsize=22, color=O)
        fig.text(0.79, 0.45, 'mũi tên xanh: hướng làm f giảm', ha='center', fontsize=14, color=T)
        fig.text(0.79, 0.37, '(ngược dấu đạo hàm)', ha='center', fontsize=14, color=T)
        return
    L.base(fig, 'Khai triển Taylor')
    x0 = 0.5; ax = ax_at(fig, [0.05, 0.17, 0.52, 0.68], (-1.5, 4), (-1.5, 4.5), equal=False, xl='x', yl='f(x)')
    ax.plot(xs, F1(xs), color=B, lw=2.5, label='f(x)'); ax.plot(x0, F1(x0), 'o', color=DARK, ms=8)
    if L.st(2) > 2: ax.plot(xs, F1(x0) + D1(x0) * (xs - x0), color=O, lw=2, label='bậc nhất')
    if L.st(2) > 4.5: ax.plot(xs, F1(x0) + D1(x0) * (xs - x0) + 0.5 * D2(x0) * (xs - x0) ** 2, color=T, lw=2, ls='--', label='bậc hai')
    ax.legend(loc='upper right', fontsize=11)
    box(fig, 0.79, 0.72, r"$f(x+h)\approx f(x)+f'(x)h+\frac{1}{2}f''(x)h^2$", 15)
    if L.on(3):
        box(fig, 0.79, 0.5, r'$f(\mathbf{x}+\mathbf{h})\approx f(\mathbf{x})+\nabla f(\mathbf{x})^{\top}\mathbf{h}+\frac{1}{2}\mathbf{h}^{\top}\nabla^2 f(\mathbf{x})\,\mathbf{h}$', 13)

F21 = lambda x, y: x ** 2 + 3 * x * y + 2 * y ** 2
def s_dir(fig):
    L.base(fig, 'Đạo hàm theo hướng')
    x0 = np.array([1.0, 2.0]); g = np.array([8.0, 11.0])
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-0.5, 2.5), (0.5, 3.5), xl='$x_1$', yl='$x_2$')
    g1, g2 = np.meshgrid(np.linspace(-0.5, 2.5, 200), np.linspace(0.5, 3.5, 200))
    ax.contour(g1, g2, F21(g1, g2), levels=np.arange(4, 60, 5), colors=B, linewidths=1)
    ax.plot(*x0, 'o', color=DARK, ms=8); arrow(ax, g / np.linalg.norm(g) * 1.0, O, 3, origin=x0)
    ax.text(*(x0 + g / np.linalg.norm(g) * 1.05 + [0.05, 0]), r'$\nabla f$', fontsize=16, color=O)
    if L.now < L.T[5]: th = np.radians(-30 + 360 * L.pr(4, L.slots[4] - 0.5))
    else: th = np.arctan2(4, 3) if L.st(5) > 3 else np.radians(330 + 53.13 * ease(L.st(5) / 3))
    u = np.array([np.cos(th), np.sin(th)]); arrow(ax, u * 0.8, T, 3, origin=x0); ax.text(*(x0 + u * 0.9), r'$\mathbf{u}$', fontsize=16, color=T)
    box(fig, 0.77, 0.74, r'$D_{\mathbf{u}}f(\mathbf{x})=\nabla f(\mathbf{x})^{\top}\mathbf{u}\leq\|\nabla f(\mathbf{x})\|_2$', 16)
    fig.text(0.77, 0.6, f'D_u f = {vn(g @ u)}', ha='center', fontsize=22, color=T)
    fig.text(0.77, 0.52, f'‖∇f‖₂ = √185 ≈ {vn(np.linalg.norm(g))}', ha='center', fontsize=17, color=O)
    if L.on(5):
        fig.text(0.58, 0.4, 'f = x₁² + 3x₁x₂ + 2x₂²,  x₀ = (1, 2)', fontsize=15, color=INK)
        fig.text(0.58, 0.32, '∇f = (2x₁ + 3x₂, 3x₁ + 4x₂) = (8, 11)', fontsize=15, color=INK)
        if L.st(5) > 3: fig.text(0.58, 0.24, 'u = (3/5, 4/5):  8·3/5 + 11·4/5 = 68/5 = 13,6', fontsize=15, color=T)

F3 = lambda x: 0.25 * x ** 4 - 0.5 * x ** 3 - 1.6 * x ** 2 + 1.2 * x + 3; D3 = lambda x: x ** 3 - 1.5 * x ** 2 - 3.2 * x + 1.2
CR = np.sort(np.roots([1, -1.5, -3.2, 1.2]).real)
def gd_path(x0, eta=0.05, n=80):
    P = [x0]
    for _ in range(n): P.append(P[-1] - eta * D3(P[-1]))
    return np.array(P)
def s_opt(fig):
    if L.now < L.T[7]:
        L.base(fig, 'Bài toán tối ưu tổng quát')
        box(fig, 0.5, 0.7, r'$\min_{\mathbf{x}}\ f_0(\mathbf{x})\quad \mathrm{v.đ.k.}\quad f_i(\mathbf{x})\leq 0,\ \ h_j(\mathbf{x})=0$', 24)
        rows = [('f₀', 'hàm mục tiêu (hàm mất mát)'), ('fᵢ ≤ 0, hⱼ = 0', 'các ràng buộc'), ('X = {x : fᵢ(x) ≤ 0, hⱼ(x) = 0}', 'tập chấp nhận được'),
                ('max f  ⇔  min (−f)', 'luôn phát biểu dạng cực tiểu')]
        for k, (a, b) in enumerate(rows):
            if L.st(6) > 1 + 1.2 * k:
                fig.text(0.16, 0.52 - 0.08 * k, a, fontsize=17, color=O); fig.text(0.56, 0.52 - 0.08 * k, b, fontsize=16, color=DARK)
        return
    L.base(fig, 'Cực tiểu địa phương và toàn cục')
    xs = np.linspace(-2.6, 3.1, 300); ax = ax_at(fig, [0.05, 0.17, 0.55, 0.68], (-2.7, 3.2), (-3, 9.5), equal=False, xl='x', yl='f(x)')
    ax.plot(xs, F3(xs), color=B, lw=2.5)
    for x, lab, c in [(CR[0], 'cực tiểu địa phương', O), (CR[1], 'cực đại địa phương', T), (CR[2], 'cực tiểu toàn cục', RED)]:
        ax.plot(x, F3(x), 'o', color=c, ms=9); ax.text(x, F3(x) + (0.7 if c != RED else -1.2), lab, ha='center', fontsize=12, color=c)
    if L.on(8):
        for x0, c in [(-2.5, O), (1.0, RED)]:
            P = gd_path(x0); i = int(min(L.st(8) * 10, len(P) - 1)); ax.plot(P[i], F3(P[i]), 'o', color=c, ms=14, mfc='none', mew=3)
        fig.text(0.64, 0.68, 'Giảm gradient từ hai điểm xuất phát:', fontsize=15, color=DARK)
        fig.text(0.64, 0.6, f'x₀ = −2,5  →  {vn(CR[0])}  (mắc kẹt)', fontsize=15, color=O)
        fig.text(0.64, 0.53, f'x₀ = 1,0  →  {vn(CR[2])}  (toàn cục)', fontsize=15, color=RED)
        fig.text(0.64, 0.42, '→ lý do bài toán lồi (Bài 5) quan trọng', fontsize=15, color=T)
    else:
        fig.text(0.64, 0.66, 'f(x) = 0,25x⁴ − 0,5x³ − 1,6x² + 1,2x + 3', fontsize=13.5, color=INK)

def s_first(fig):
    L.base(fig, 'Điều kiện cần bậc nhất')
    if L.now < L.T[10]:
        box(fig, 0.5, 0.74, r'$\mathbf{x}^*$ cực tiểu địa phương, $f\in C^1$  $\Rightarrow$  $\nabla f(\mathbf{x}^*)=\mathbf{0}$', 22)
        steps = ['Giả sử ∇f(x*) ≠ 0, chọn hướng h = −∇f(x*)', 'Taylor: f(x* + th) ≈ f(x*) − t‖∇f(x*)‖₂² < f(x*) với t > 0 đủ nhỏ',
                 'Mâu thuẫn với giả thiết x* là cực tiểu địa phương  ◻']
        for k, s in enumerate(steps):
            if L.st(9) > 1.5 + 1.6 * k: fig.text(0.1, 0.56 - 0.1 * k, f'{k + 1}. ' + s, fontsize=17, color=DARK if k < 2 else T)
        return
    xs = np.linspace(-1.6, 1.6, 200); ax = ax_at(fig, [0.06, 0.17, 0.5, 0.66], (-1.6, 1.6), (-3, 3), equal=False, xl='x', yl='f(x) = x³')
    ax.plot(xs, xs ** 3, color=B, lw=2.5); ax.plot([-0.8, 0.8], [0, 0], color=O, lw=2.5); ax.plot(0, 0, 'o', color=O, ms=10)
    fig.text(0.62, 0.66, "f′(0) = 0  nhưng 0 không là cực trị", fontsize=18, color=O)
    fig.text(0.62, 0.55, '∇f = 0 chỉ là điều kiện CẦN', fontsize=18, color=DARK)
    fig.text(0.62, 0.45, '→ cần kiểm tra thêm bằng đạo hàm bậc hai', fontsize=15, color=T)

def mini(fig, rect, A, title, col):
    ax = ax_at(fig, rect, (-1.5, 1.5), (-1.5, 1.5), fs=7); g = np.linspace(-1.5, 1.5, 120); X, Y = np.meshgrid(g, g)
    Z = A[0] * X ** 2 + A[1] * Y ** 2 if A[1] != 0 else X ** 2 + Y ** 4; ax.contour(X, Y, Z, levels=12, colors=col, linewidths=1, negative_linestyles='solid')
    ax.plot(0, 0, 'o', color=DARK, ms=6); ax.set_title(title, fontsize=13, color=col); ax.set_xticks([]); ax.set_yticks([])
def s_second(fig):
    L.base(fig, 'Điều kiện bậc hai: phân loại điểm dừng')
    box(fig, 0.5, 0.79, r'$f(\mathbf{x}^*+\mathbf{h})\approx f(\mathbf{x}^*)+\frac{1}{2}\,\mathbf{h}^{\top}\nabla^2 f(\mathbf{x}^*)\,\mathbf{h}$', 20)
    if not L.on(12):
        rows = ['hᵀ∇²f h > 0 với mọi h ≠ 0  ⇒  f tăng theo mọi hướng', 'hᵀ∇²f h < 0 với mọi h ≠ 0  ⇒  f giảm theo mọi hướng',
                'đổi dấu theo hướng  ⇒  vừa tăng vừa giảm']
        for k, r in enumerate(rows):
            if L.st(11) > 2 + 1.3 * k: fig.text(0.14, 0.6 - 0.1 * k, r, fontsize=18, color=[T, B, O][k])
    if L.on(12):
        cases = [((1, 1), 'xác định dương\n→ cực tiểu ngặt', T), ((-1, -1), 'xác định âm\n→ cực đại ngặt', B), ((1, -1), 'không xác định dấu\n→ yên ngựa', O),
                 ((1, 0), 'suy biến, vd x₁² + x₂⁴\n→ chưa kết luận', INK)]
        for k, (A, t, c) in enumerate(cases):
            if L.st(12) > 0.3 + 1.5 * k: mini(fig, [0.03 + 0.245 * k, 0.2, 0.2, 0.42], A, t, c)

F22 = lambda x, y: x ** 2 + y ** 3 - 3 * y
def s_ex(fig):
    L.base(fig, 'Ví dụ 2.2: tìm và phân loại điểm dừng')
    if L.now < L.T[15]:
        ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-2, 2), (-2.2, 2.2), xl='$x_1$', yl='$x_2$')
        g1, g2 = np.meshgrid(np.linspace(-2, 2, 250), np.linspace(-2.2, 2.2, 250))
        ax.contour(g1, g2, F22(g1, g2), levels=np.linspace(-3, 5, 17), colors=B, linewidths=1, negative_linestyles='solid')
        if L.st(13) > 4 or L.on(14):
            ax.plot(0, 1, 'o', color=T, ms=12); ax.plot(0, -1, 'o', color=O, ms=12)
        fig.text(0.58, 0.76, 'f = x₁² + x₂³ − 3x₂', fontsize=19, color=DARK)
        fig.text(0.58, 0.67, '∇f = (2x₁,  3x₂² − 3) = 0', fontsize=17, color=INK)
        if L.st(13) > 4 or L.on(14): fig.text(0.58, 0.59, '⇒ (0, 1) và (0, −1)', fontsize=17, color=DARK)
        if L.on(14):
            fig.text(0.58, 0.48, '∇²f = diag(2, 6x₂)', fontsize=17, color=INK)
            if L.st(14) > 2: fig.text(0.58, 0.39, '(0, 1): diag(2, 6) ≻ 0 → cực tiểu ngặt', fontsize=16, color=T)
            if L.st(14) > 6: fig.text(0.58, 0.31, '(0, −1): diag(2, −6) → yên ngựa', fontsize=16, color=O)
        return
    x2 = np.linspace(-3, 2.5, 200); ax = ax_at(fig, [0.06, 0.17, 0.5, 0.66], (-3, 2.5), (-15, 8), equal=False, xl='$x_2$', yl='$f(0, x_2)$')
    ax.plot(x2, x2 ** 3 - 3 * x2, color=B, lw=2.5); ax.plot(1, -2, 'o', color=T, ms=10); ax.plot(-1, 2, 'o', color=O, ms=10)
    arrow(ax, (-0.6, -5), RED, 2.5, origin=(-2.2, -4))
    fig.text(0.62, 0.66, 'f(0, x₂) = x₂³ − 3x₂ → −∞', fontsize=18, color=RED)
    fig.text(0.62, 0.57, 'khi x₂ → −∞', fontsize=18, color=RED)
    fig.text(0.62, 0.45, '→ không có cực tiểu toàn cục', fontsize=17, color=DARK)
    fig.text(0.62, 0.37, '(0, 1) chỉ là cực tiểu địa phương', fontsize=15, color=T)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 16, ['Taylor bậc hai: công cụ phân tích hàm quanh một điểm', 'D_u f = ∇fᵀu; gradient chỉ hướng tăng nhanh nhất',
                        '∇f(x*) = 0 là điều kiện cần (điểm dừng)', 'Hessian: ≻ 0 cực tiểu, ≺ 0 cực đại, không xác định dấu: yên ngựa',
                        'Phi lồi: có thể mắc kẹt ở cực tiểu địa phương'], gap=1.6)

SCENES = [(0, s_title), (1, s_deriv), (4, s_dir), (6, s_opt), (9, s_first), (11, s_second), (13, s_ex), (16, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
