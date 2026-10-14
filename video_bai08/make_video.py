"""Video Bài 8 - Các mô hình hồi quy.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 8 · Các mô hình hồi quy', TEXTS, SPOKEN, 'bai08_hoi_quy',
           mins={0: 5, 8: 11, 13: 9}, chapter='Chương 3 · Ứng dụng toán trong học máy')

def s_title(fig):
    L.title(fig, 'Bài 8. Các mô hình hồi quy', r'$P(y=1\mid\mathbf{x})=\sigma(\mathbf{w}^{\top}\mathbf{x})=\dfrac{1}{1+e^{-\mathbf{w}^{\top}\mathbf{x}}}$')

r = np.random.default_rng(4); XL = np.sort(r.uniform(0, 10, 30)); YL = 1.0 + 0.5 * XL + r.normal(0, 0.8, 30); WL = np.polyfit(XL, YL, 1)
def s_lin(fig):
    L.base(fig, 'Hồi quy tuyến tính')
    ax = ax_at(fig, [0.05, 0.17, 0.5, 0.68], (0, 10.5), (-1, 9), equal=False, xl='x', yl='y')
    ax.scatter(XL, YL, color=B, s=25, zorder=3); xs = np.array([0, 10.5]); ax.plot(xs, np.polyval(WL, xs), color=O, lw=2.5)
    if L.on(2):
        for x0 in [2, 5, 8]:
            yy = np.linspace(-2.2, 2.2, 60); m = np.polyval(WL, x0); ax.plot(x0 + 1.2 * np.exp(-yy ** 2 / (2 * 0.64)), m + yy, color=T, lw=1.5)
            ax.plot([x0, x0], [m - 2.2, m + 2.2], color=T, lw=0.6, ls=':')
    box(fig, 0.78, 0.76, r'$y_i=\mathbf{w}^{\top}\mathbf{x}_i+\varepsilon_i,\quad \mathbf{x}_i=(1,x_{i1},\dots,x_{id})$', 14)
    if L.on(2):
        fig.text(0.78, 0.62, r'$\varepsilon_i\ \mathrm{i.i.d.}\sim\mathcal{N}(0,\sigma^2)$', ha='center', fontsize=19, color=T)
        fig.text(0.78, 0.53, '⇒ ước lượng hợp lý cực đại', ha='center', fontsize=16, color=DARK)
        fig.text(0.78, 0.46, '= nghiệm bình phương nhỏ nhất', ha='center', fontsize=16, color=DARK)
    if L.on(3):
        fig.text(0.78, 0.33, r'$y=w_0+w_1x+w_2x^2$', ha='center', fontsize=19, color=O)
        fig.text(0.78, 0.26, 'vẫn là mô hình tuyến tính theo w', ha='center', fontsize=15, color=O)

r2 = np.random.default_rng(12); XT = np.sort(r2.uniform(-1, 1, 15)); f0 = lambda x: np.sin(2.5 * x) + 0.3 * x
YT = f0(XT) + r2.normal(0, 0.25, 15); XV = r2.uniform(-1, 1, 200); YV = f0(XV) + r2.normal(0, 0.25, 200)
Phi = lambda x, k: np.vander(x, k + 1, increasing=True)
def s_poly(fig):
    if L.now < L.T[5]:
        L.base(fig, 'Hồi quy đa thức: mở rộng đặc trưng')
        box(fig, 0.5, 0.74, r'$\phi(x)=(1,\ x,\ x^2,\ \dots,\ x^k),\qquad \hat y=\mathbf{w}^{\top}\phi(x)$', 22)
        x = np.array([-0.8, 0.1, 0.6]); k = 3
        if L.st(4) > 2:
            fig.text(0.2, 0.55, 'x', fontsize=17, color=B, ha='center'); 
            for j in range(k + 1): fig.text(0.38 + 0.1 * j, 0.55, ['1', 'x', 'x²', 'x³'][j], fontsize=17, color=B, ha='center')
            for i, xi in enumerate(x):
                fig.text(0.2, 0.47 - 0.07 * i, vn(xi, 1), fontsize=16, ha='center'); fig.text(0.29, 0.47 - 0.07 * i, '→', fontsize=16, ha='center', color=INK)
                for j in range(k + 1): fig.text(0.38 + 0.1 * j, 0.47 - 0.07 * i, vn(xi ** j, 3 if j else 0), fontsize=16, ha='center')
            fig.text(0.5, 0.2, 'ma trận thiết kế Φ — vẫn giải bằng bình phương nhỏ nhất', ha='center', fontsize=15, color=T)
        return
    L.base(fig, 'Dưới khớp, khớp vừa và quá khớp')
    xs = np.linspace(-1, 1, 300)
    for j, (k, lab, c) in enumerate([(1, 'bậc 1 — dưới khớp', T), (4, 'bậc 4 — khớp vừa', B), (12, 'bậc 12 — quá khớp', O)]):
        if L.st(5) > 0.4 + 1.5 * j:
            w = np.linalg.lstsq(Phi(XT, k), YT, rcond=None)[0]; ax = ax_at(fig, [0.04 + 0.32 * j, 0.3, 0.28, 0.48], (-1, 1), (-2, 2), equal=False, fs=8)
            ax.scatter(XT, YT, color=DARK, s=18, zorder=4); ax.plot(xs, Phi(xs, k) @ w, color=c, lw=2.2); ax.set_title(lab, fontsize=13, color=c)
            tr = np.mean((Phi(XT, k) @ w - YT) ** 2); te = np.mean((Phi(XV, k) @ w - YV) ** 2)
            fig.text(0.18 + 0.32 * j, 0.22, f'MSE huấn luyện {vn(tr, 3)}', ha='center', fontsize=13, color=INK)
            fig.text(0.18 + 0.32 * j, 0.17, 'MSE kiểm tra ' + (vn(te, 3) if te < 100 else '≫ 1'), ha='center', fontsize=13, color=RED if te > 1 else INK)

# ---------- ridge và LASSO: đường đi của hệ số ----------
r3 = np.random.default_rng(5); n, d = 60, 6
XR = r3.normal(size=(n, d)); XR = (XR - XR.mean(0)) / XR.std(0); WTRUE = np.array([3.0, -2.0, 1.5, 0, 0, 0])
YR = XR @ WTRUE + r3.normal(0, 1.0, n); YR = YR - YR.mean()
LAMS = np.logspace(-1, 3.3, 60)
def lasso_cd(lam, iters=300):
    w = np.zeros(d); nrm = (XR ** 2).sum(0)
    for _ in range(iters):
        for j in range(d):
            rho = XR[:, j] @ (YR - XR @ w + XR[:, j] * w[j]); w[j] = np.sign(rho) * max(abs(rho) - lam / 2, 0) / nrm[j]
    return w
RIDGE = np.array([np.linalg.solve(XR.T @ XR + l * np.eye(d), XR.T @ YR) for l in LAMS]); LASSO = np.array([lasso_cd(l) for l in LAMS])
# đường sai số theo λ: ridge trên đặc trưng đa thức bậc 12 (chuẩn hóa), không phạt hệ số tự do
PT, PV = Phi(XT, 12)[:, 1:], Phi(XV, 12)[:, 1:]; MU, SD = PT.mean(0), PT.std(0); PT, PV = (PT - MU) / SD, (PV - MU) / SD
LG = np.logspace(-6, 2, 60)
def ridge_fit(l):
    w = np.linalg.solve(PT.T @ PT + l * np.eye(12), PT.T @ (YT - YT.mean())); return w, YT.mean()
ERR = np.array([[np.mean((PT @ w + b - YT) ** 2), np.mean((PV @ w + b - YV) ** 2)] for w, b in map(ridge_fit, LG)])
def s_reg(fig):
    if L.now < L.T[8]:
        L.base(fig, 'Điều chuẩn: ridge và LASSO')
        box(fig, 0.5, 0.74, r'$J_{\mathrm{ridge}}=\|\mathbf{y}-\mathbf{Xw}\|_2^2+\lambda\|\mathbf{w}\|_2^2\qquad J_{\mathrm{LASSO}}=\|\mathbf{y}-\mathbf{Xw}\|_2^2+\lambda\|\mathbf{w}\|_1$', 18)
        if not L.on(7) and L.st(6) > 3:
            fig.text(0.5, 0.55, 'λ ≥ 0 điều khiển mức phạt:  λ = 0 → bình phương nhỏ nhất thông thường', ha='center', fontsize=17, color=DARK)
            fig.text(0.5, 0.46, 'λ lớn → trọng số bị kéo mạnh về 0', ha='center', fontsize=17, color=DARK)
        if L.on(7):
            fig.text(0.5, 0.55, r'$\mathbf{w}_{\mathrm{ridge}}=(\mathbf{X}^{\top}\mathbf{X}+\lambda\mathbf{I})^{-1}\mathbf{X}^{\top}\mathbf{y}$', ha='center', fontsize=24, color=O)
            if L.st(7) > 3: fig.text(0.5, 0.42, 'mọi giá trị riêng được cộng thêm λ  ⇒  XᵀX + λI ≻ 0 khi λ > 0', ha='center', fontsize=16, color=DARK)
            if L.st(7) > 6: fig.text(0.5, 0.33, 'thường không phạt w₀: căn giữa X và y trước khi giải', ha='center', fontsize=15, color=T)
        return
    if L.now < L.T[9]:
        L.base(fig, 'Đường đi của hệ số theo λ')
        fig.text(0.96, 0.9, 'dữ liệu mô phỏng: 6 đặc trưng, chỉ 3 đặc trưng có ích', ha='right', fontsize=13, color=INK)
        cur = LAMS[0] * (LAMS[-1] / LAMS[0]) ** L.pr(8, L.slots[8] - 1)
        for k, (Wp, lab) in enumerate([(RIDGE, 'Ridge (ℓ₂)'), (LASSO, 'LASSO (ℓ₁)')]):
            ax = ax_at(fig, [0.07 + 0.47 * k, 0.2, 0.4, 0.58], (LAMS[0], LAMS[-1]), (-2.5, 3.3), equal=False, xl='λ (thang log)', yl='hệ số' if k == 0 else None, fs=8)
            ax.set_xscale('log'); m = LAMS <= cur
            for j in range(d): ax.plot(LAMS[m], Wp[m, j], lw=2, color=[B, O, T, INK, LIGHT, RED][j])
            ax.axvline(cur, color=DARK, lw=1, ls=':'); ax.axhline(0, color=INK, lw=0.8); ax.set_title(lab, fontsize=14)
            i = np.searchsorted(LAMS, cur) - 1; nz = (np.abs(Wp[max(i, 0)]) > 1e-8).sum()
            fig.text(0.27 + 0.47 * k, 0.83, f'{nz}/6 hệ số khác 0', ha='center', fontsize=14, color=O if nz < 6 else INK)
        return
    L.base(fig, 'Chọn λ: sai số huấn luyện và kiểm tra')
    ax = ax_at(fig, [0.07, 0.19, 0.5, 0.62], (LG[0], LG[-1]), (0, ERR.max() * 1.05), equal=False, xl='λ (thang log)', yl='MSE', fs=9)
    ax.set_xscale('log'); m = int(max(2, ease(L.pr(9, 4)) * len(LG)))
    ax.plot(LG[:m], ERR[:m, 0], color=T, lw=2.5, label='huấn luyện'); ax.plot(LG[:m], ERR[:m, 1], color=O, lw=2.5, label='kiểm tra')
    ax.legend(fontsize=11, loc='upper left')
    if m == len(LG):
        i = ERR[:, 1].argmin(); ax.plot(LG[i], ERR[i, 1], 'o', color=O, ms=10); ax.annotate('λ tốt nhất', (LG[i], ERR[i, 1]), (LG[i] * 3, ERR[i, 1] + 0.12), color=O, fontsize=13, arrowprops=dict(arrowstyle='-', color=O))
    fig.text(0.62, 0.68, 'Ridge trên đa thức bậc 12', fontsize=16, color=DARK)
    fig.text(0.62, 0.6, '15 điểm huấn luyện, 200 điểm kiểm tra', fontsize=14, color=INK)
    fig.text(0.62, 0.48, 'λ nhỏ: quá khớp', fontsize=16, color=RED); fig.text(0.62, 0.41, 'λ lớn: dưới khớp', fontsize=16, color=T)
    fig.text(0.62, 0.3, 'chọn λ bằng kiểm định chéo', fontsize=16, color=O)

sig = lambda z: 1 / (1 + np.exp(-z))
r4 = np.random.default_rng(9); NA = 60
XA = np.vstack([r4.normal([-1.2, -0.6], 0.8, (NA, 2)), r4.normal([1.1, 0.9], 0.8, (NA, 2))]); YA = np.r_[np.zeros(NA), np.ones(NA)]
XA1 = np.c_[np.ones(2 * NA), XA]
def logistic_path(eta=0.5, steps=60):
    w = np.array([0.0, -1.0, 2.0]); P = [w.copy()]; Ls = []
    for _ in range(steps):
        p = sig(XA1 @ w); Ls.append(-np.mean(YA * np.log(p + 1e-12) + (1 - YA) * np.log(1 - p + 1e-12)))
        w = w - eta * XA1.T @ (p - YA) / len(YA); P.append(w.copy())
    return np.array(P), np.array(Ls)
WP, LP = logistic_path()
def s_logit(fig):
    if L.now < L.T[13]:
        L.base(fig, 'Hồi quy logistic cho phân loại nhị phân')
        z = np.linspace(-6, 6, 200); ax = ax_at(fig, [0.06, 0.2, 0.46, 0.6], (-6, 6), (-0.05, 1.05), equal=False, xl=r'$z=\mathbf{w}^{\top}\mathbf{x}$', yl='P(y = 1 | x)')
        ax.plot(z, sig(z), color=B, lw=2.5); ax.axhline(0.5, color=INK, ls='--', lw=1); ax.plot(0, 0.5, 'o', color=O, ms=9)
        ax.text(0.3, 0.42, 'ngưỡng quyết định z = 0', fontsize=12, color=O)
        box(fig, 0.78, 0.76, r'$\sigma(z)=\dfrac{1}{1+e^{-z}}\in(0,1)$', 20)
        if L.on(11):
            fig.text(0.78, 0.58, r'$J(\mathbf{w})=-\sum_i\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right]$', ha='center', fontsize=14.5, color=DARK)
            fig.text(0.78, 0.5, 'entropy chéo — hàm lồi', ha='center', fontsize=15, color=T)
        if L.on(12):
            fig.text(0.78, 0.38, r'$\nabla J(\mathbf{w})=\mathbf{X}^{\top}(\mathbf{p}-\mathbf{y})$', ha='center', fontsize=20, color=O)
            fig.text(0.78, 0.29, 'không có nghiệm dạng đóng', ha='center', fontsize=15, color=RED)
        return
    L.base(fig, 'Huấn luyện hồi quy logistic bằng giảm gradient')
    i = int(min(len(LP) - 1, ease(L.pr(13, L.slots[13] - 1)) * (len(LP) - 1))); w = WP[i]
    ax = ax_at(fig, [0.04, 0.16, 0.5, 0.72], (-3.5, 3.5), (-3, 3.5), fs=8)
    g1, g2 = np.meshgrid(np.linspace(-3.5, 3.5, 150), np.linspace(-3, 3.5, 150))
    ax.contourf(g1, g2, sig(w[0] + w[1] * g1 + w[2] * g2), levels=np.linspace(0, 1, 11), cmap='RdBu_r', alpha=0.25)
    ax.scatter(*XA[:NA].T, color=B, s=18, label='y = 0'); ax.scatter(*XA[NA:].T, color=O, s=18, label='y = 1')
    x = np.linspace(-3.5, 3.5, 2); ax.plot(x, -(w[0] + w[1] * x) / w[2], color=DARK, lw=2.5); ax.legend(loc='lower right', fontsize=10)
    a2 = ax_at(fig, [0.62, 0.3, 0.33, 0.4], (0, len(LP)), (0, LP.max() * 1.1), equal=False, xl='vòng lặp', yl='entropy chéo (TB)', fs=8)
    a2.plot(np.arange(i + 1), LP[:i + 1], color=O, lw=2.5)
    acc = np.mean((XA1 @ w > 0) == (YA == 1))
    fig.text(0.785, 0.78, f'vòng lặp {i}', ha='center', fontsize=16, color=DARK); fig.text(0.785, 0.2, f'độ chính xác huấn luyện: {vn(100 * acc, 0)}%', ha='center', fontsize=15, color=T)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 14, ['Hồi quy tuyến tính: tuyến tính theo tham số w', 'Mở rộng đặc trưng ϕ(x): mô hình hóa quan hệ phi tuyến',
                        'Bậc thấp: dưới khớp · bậc cao: quá khớp', 'Ridge: nghiệm dạng đóng, hệ số nhỏ lại · LASSO: nghiệm thưa',
                        'Logistic: sigmoid + entropy chéo (lồi), giải bằng giảm gradient'], gap=1.9)

SCENES = [(0, s_title), (1, s_lin), (4, s_poly), (6, s_reg), (10, s_logit), (14, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
