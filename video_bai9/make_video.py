"""Video mẫu Bài 9 - Giải thuật giảm gradient (Toán cho học máy, ĐH Trà Vinh).
Dựng bằng matplotlib + ffmpeg. Chạy: python make_video.py  -> bai9_giam_gradient.mp4 + .srt
"""
import subprocess, textwrap
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

W, H, FPS = 1280, 720, 24
B, O, T, INK, GRID, DARK = '#4a5fc1', '#d97706', '#0e8f7e', '#3a4050', '#dde0ea', '#1c1f2a'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.edgecolor': INK, 'axes.labelcolor': DARK,
                     'xtick.color': INK, 'ytick.color': INK, 'axes.grid': True, 'grid.color': GRID,
                     'axes.spines.top': False, 'axes.spines.right': False, 'mathtext.fontset': 'dejavusans'})
ease = lambda u: 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0, 1))

# ---------------- Phụ đề (lời thoại) ----------------
SLOTS = [6, 7, 7, 7, 12, 8, 8, 8, 8, 8, 8, 10, 9, 8, 12, 8, 9, 9, 8, 7, 7]  # độ dài (giây) mỗi câu, đủ chỗ cho giọng đọc VieNeu-TTS
TEXTS = [
 'Bài 9: Giải thuật giảm gradient — ý tưởng, tốc độ học và các biến thể.',
 'Khi hàm mất mát không có nghiệm dạng đóng, ta tìm cực tiểu bằng phương pháp lặp.',
 'Gradient chỉ hướng hàm số tăng nhanh nhất, nên ta bước theo hướng ngược lại: −∇J.',
 'Công thức cập nhật: w mới bằng w cũ trừ η nhân gradient, trong đó η là tốc độ học.',
 'Với J(w) = (w − 3)², w₀ = 0 và η = 0,1: w₁ = 0,6; w₂ = 1,08; w₃ = 1,464 — tiến dần về 3.',
 'Với nhiều tham số, gradient luôn vuông góc với đường đồng mức.',
 'Mỗi bước đi ngược hướng gradient; càng gần cực tiểu, gradient càng nhỏ nên bước càng ngắn.',
 'Thuật toán tự giảm tốc khi tới gần đích mà không cần can thiệp thêm.',
 'Tốc độ học η là siêu tham số quan trọng nhất. Xét ba cách chọn trên cùng hàm J(w) = (w − 3)².',
 'η quá nhỏ (0,05): thuật toán vẫn hội tụ nhưng cần rất nhiều vòng lặp.',
 'η hợp lý (0,3): hàm mất mát giảm nhanh và đều đặn về giá trị tối ưu.',
 'η quá lớn (1,05): mỗi bước vượt qua điểm cực tiểu, dao động ngày càng mạnh và phân kỳ.',
 'Với hàm lồi mạnh tham số m, gradient Lipschitz hằng số L và η = 1/L, sai số giảm theo cấp số nhân.',
 'Hệ số co (1 − m/L) phụ thuộc số điều kiện L/m: đường đồng mức càng dẹt, hội tụ càng chậm.',
 'Chuẩn hóa dữ liệu làm đường đồng mức tròn hơn, giảm số điều kiện nên thuật toán hội tụ nhanh hơn rõ rệt.',
 'Khi J là trung bình mất mát trên n mẫu, cách ước lượng gradient ở mỗi bước sinh ra ba biến thể.',
 'Theo lô: dùng toàn bộ n mẫu, quỹ đạo mượt nhưng chậm khi n lớn. Ngẫu nhiên (SGD): một mẫu, nhanh nhưng nhiễu.',
 'Theo lô nhỏ (32 đến 512 mẫu) cân bằng cả hai, và là lựa chọn mặc định trong học sâu hiện nay.',
 'Dừng khi chuẩn gradient nhỏ hơn ε, khi mất mát gần như không đổi, hoặc khi đạt số vòng lặp tối đa.',
 'Luôn vẽ đường cong mất mát: đi ngang quá sớm gợi ý η quá nhỏ; răng cưa mạnh gợi ý η quá lớn.',
 'Tóm lại: đi ngược gradient, chọn η hợp lý, chuẩn hóa dữ liệu và theo dõi đường cong mất mát.',
]
_T = np.concatenate([[0], np.cumsum(SLOTS)])
SUBS = [(float(_T[i]), float(_T[i + 1]), TEXTS[i]) for i in range(len(TEXTS))]
DUR = float(_T[-1])
NOW = [0.0]  # thời điểm toàn cục của khung hình đang vẽ

def frame_base(fig, section, t):
    fig.clf(); fig.patch.set_facecolor('white')
    if section:
        fig.text(0.04, 0.945, 'BÀI 9 · GIẢI THUẬT GIẢM GRADIENT', fontsize=11, color=B, weight='bold')
        fig.text(0.04, 0.895, section, fontsize=19, color=DARK, weight='bold')
    t = NOW[0]
    sub = next((s for a, b, s in SUBS if a <= t < b), '')
    if sub:
        fig.patches.append(FancyBboxPatch((0.08, 0.018), 0.84, 0.085, boxstyle='round,pad=0.006',
                           transform=fig.transFigure, fc='#1c1f2aE6', ec='none'))
        fig.text(0.5, 0.06, '\n'.join(textwrap.wrap(sub, 92)), ha='center', va='center',
                 fontsize=15, color='white', linespacing=1.3)

def box(fig, x, y, s, fs=20, color=DARK):
    fig.text(x, y, s, fontsize=fs, color=color, ha='center', va='center',
             bbox=dict(boxstyle='round,pad=0.5', fc='#f2f4fa', ec=GRID))

# ---------------- Cảnh 1: tiêu đề ----------------
def s_title(fig, t):
    frame_base(fig, '', t)
    a = min(1, t / 1.2)
    fig.text(0.5, 0.66, 'TOÁN CHO HỌC MÁY', ha='center', fontsize=16, color=B, weight='bold', alpha=a)
    fig.text(0.5, 0.55, 'Bài 9. Giải thuật giảm gradient', ha='center', fontsize=36, color=DARK, weight='bold', alpha=a)
    fig.text(0.5, 0.43, r'$\mathbf{w}_{t+1} = \mathbf{w}_t - \eta\,\nabla J(\mathbf{w}_t)$', ha='center', fontsize=30, color=O, alpha=a)
    fig.text(0.5, 0.31, 'Chương 3 · Ứng dụng toán trong học máy', ha='center', fontsize=14, color=INK, alpha=a)

# ---------------- Cảnh 2: ý tưởng 1D ----------------
J1 = lambda w: (w - 3) ** 2
dJ1 = lambda w: 2 * (w - 3)
def gd1(w0, eta, n):
    ws = [w0]
    for _ in range(n): ws.append(ws[-1] - eta * dJ1(ws[-1]))
    return np.array(ws)
WS = gd1(0.0, 0.1, 10)
def s_idea(fig, t):
    frame_base(fig, 'Ý tưởng: đi ngược hướng gradient', 6 + t)
    ax = fig.add_axes([0.07, 0.2, 0.55, 0.63])
    x = np.linspace(-1, 7, 300); ax.plot(x, J1(x), color=B, lw=3)
    ax.set_xlim(-1, 7); ax.set_ylim(-1, 17); ax.set_xlabel('w', fontsize=13); ax.set_ylabel('J(w)', fontsize=13)
    ax.plot(3, 0, '*', color=T, ms=18, zorder=6); ax.text(3.15, 0.6, 'cực tiểu w* = 3', color=T, fontsize=12)
    if t < 14:
        w = 0.0
        if t > 3:
            k = min(1, (t - 3) / 2); xs = np.linspace(w - 1.2, w + 1.2, 2)
            ax.plot(xs, J1(w) + dJ1(w) * (xs - w), '--', color=INK, lw=1.5, alpha=k)
            ax.text(-0.9, 13.5, "độ dốc J'(0) = −6 < 0", color=INK, fontsize=12, alpha=k)
        if t > 7:
            k = min(1, (t - 7) / 1.5)
            ax.annotate('', xy=(w + 1.6 * k, J1(w)), xytext=(w, J1(w)), arrowprops=dict(arrowstyle='-|>', color=O, lw=3))
            ax.text(0.15, J1(w) + 0.9, '−∇J: hướng giảm nhanh nhất', color=O, fontsize=12, alpha=k)
        ax.plot(w, J1(w), 'o', color=O, ms=13, zorder=7)
    else:
        u = (t - 14) / 2.0; i = int(min(u, len(WS) - 2)); f = ease(u - i) if u < len(WS) - 1 else 1
        w = WS[i] + (WS[i + 1] - WS[i]) * f
        ax.plot(WS[:i + 1], J1(WS[:i + 1]), 'o', color=O, ms=7, alpha=0.45)
        ax.plot(w, J1(w), 'o', color=O, ms=13, zorder=7)
        ax.text(w + 0.25, J1(w) + 1.4, f'w = {w:.3f}'.replace('.', ','), ha='left', color=O, fontsize=12)
    if t > 13:
        box(fig, 0.81, 0.72, r'$w_{t+1} = w_t - \eta\,\nabla J(w_t)$', 21)
    if t > 20:
        rows = ['$J(w)=(w-3)^2,\;\; w_0=0,\;\; \\eta=0{,}1$', '$w_1 = 0 - 0{,}1\\cdot(-6) = 0{,}6$',
                '$w_2 = 0{,}6 - 0{,}1\\cdot(-4{,}8) = 1{,}08$', '$w_3 = 1{,}08 - 0{,}1\\cdot(-3{,}84) = 1{,}464$']
        for k, r in enumerate(rows):
            if t > 20 + 1.5 * k:
                fig.text(0.665, 0.55 - 0.075 * k, r, fontsize=15, color=DARK if k else INK)

# ---------------- Cảnh 3: đường đồng mức 2D ----------------
A2 = np.array([1.0, 4.0]); C2 = np.array([2.4, 1.1])
J2 = lambda w1, w2: 0.5 * (A2[0] * (w1 - C2[0]) ** 2 + A2[1] * (w2 - C2[1]) ** 2)
def path2(w0, eta, n, a=A2, c=C2):
    P = [np.array(w0, float)]
    for _ in range(n): P.append(P[-1] - eta * a * (P[-1] - c))
    return np.array(P)
P2 = path2([-0.5, 2.9], 0.22, 18)
def contour(ax, a, c, lv, lim):
    g1, g2 = np.meshgrid(np.linspace(*lim[0], 200), np.linspace(*lim[1], 200))
    Z = 0.5 * (a[0] * (g1 - c[0]) ** 2 + a[1] * (g2 - c[1]) ** 2)
    ax.contour(g1, g2, Z, levels=lv, colors=B, linewidths=1.3)
    ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_aspect('equal')
    ax.plot(*c, '*', color=T, ms=18, zorder=6)
def draw_path(ax, P, u, color=O):
    i = int(min(u, len(P) - 2)); f = ease(u - i) if u < len(P) - 1 else 1
    cur = P[i] + (P[i + 1] - P[i]) * f
    pts = np.vstack([P[:i + 1], cur]); ax.plot(pts[:, 0], pts[:, 1], '-', color=color, lw=2.2)
    ax.plot(P[:i + 1, 0], P[:i + 1, 1], 'o', color=color, ms=5); ax.plot(*cur, 'o', color=color, ms=11, zorder=7)
    return cur
def s_contour(fig, t):
    frame_base(fig, 'Quỹ đạo trên đường đồng mức', 34 + t)
    ax = fig.add_axes([0.06, 0.2, 0.56, 0.65])
    contour(ax, A2, C2, [0.3, 1, 2.5, 5, 8.5, 13], [(-1.2, 5.6), (-0.8, 3.4)])
    ax.set_xlabel('$w_1$', fontsize=13); ax.set_ylabel('$w_2$', fontsize=13)
    cur = draw_path(ax, P2, max(0, (t - 3) / 1.1))
    g = A2 * (cur - C2); n = np.linalg.norm(g)
    if n > 0.05:
        d = -g / max(n, 1e-9) * min(1.2, 0.35 + 0.35 * n)
        ax.annotate('', xy=cur + d, xytext=cur, arrowprops=dict(arrowstyle='-|>', color=DARK, lw=2))
    ax.text(*(C2 + [0.15, -0.35]), '$\\mathbf{w}^*$', color=T, fontsize=16)
    box(fig, 0.81, 0.7, r'$\mathbf{w}_{t+1} = \mathbf{w}_t - \eta\,\nabla J(\mathbf{w}_t)$', 18)
    fig.text(0.81, 0.55, f'‖∇J‖ = {n:.3f}'.replace('.', ','), ha='center', fontsize=20, color=O)
    fig.text(0.81, 0.47, 'mũi tên đen: hướng −∇J', ha='center', fontsize=13, color=INK)
    fig.text(0.81, 0.40, 'gradient vuông góc với đường đồng mức', ha='center', fontsize=13, color=INK)

# ---------------- Cảnh 4: tốc độ học ----------------
ETAS = [(0.05, 'η = 0,05 — quá nhỏ', T), (0.3, 'η = 0,3 — hợp lý', B), (1.05, 'η = 1,05 — quá lớn', O)]
NIT = 15
def s_lr(fig, t):
    frame_base(fig, 'Tốc độ học η: ba kịch bản', 58 + t)
    it = np.clip((t - 8) / 1.5, 0, NIT)
    for k, (eta, lab, col) in enumerate(ETAS):
        ax = fig.add_axes([0.06 + 0.31 * k, 0.56, 0.26, 0.26])
        ws = gd1(0.0, eta, NIT); span = (-1, 7) if eta < 1 else (-11, 17)
        x = np.linspace(*span, 300); ax.plot(x, J1(x), color=GRID, lw=2.5)
        ax.set_xlim(*span); ax.set_ylim(-0.05 * J1(span[1]), J1(span[1]) * 1.05); ax.set_title(lab, color=col, fontsize=14)
        ax.tick_params(labelsize=9)
        if True:
            i = int(it); f = ease(it - i); cur = ws[i] + (ws[min(i + 1, NIT)] - ws[i]) * f
            pts = np.append(ws[:i + 1], cur); ax.plot(pts, J1(pts), '-o', color=col, lw=1.4, ms=4)
            ax.plot(cur, J1(cur), 'o', color=col, ms=10, zorder=6)
    ax = fig.add_axes([0.08, 0.21, 0.84, 0.25]); ax.set_yscale('log')
    ax.set_xlim(0, NIT); ax.set_ylim(1e-12, 1e3); ax.set_xlabel('Số vòng lặp t', fontsize=12); ax.set_ylabel('J(w_t)', fontsize=12)
    tt = np.linspace(0, it, 200)
    for eta, lab, col in ETAS:
        ax.plot(tt, 9 * ((1 - 2 * eta) ** 2) ** tt, color=col, lw=2.5, label=lab)
    ax.legend(loc='lower left', fontsize=11, frameon=False, ncol=3)

# ---------------- Cảnh 5: số điều kiện ----------------
def s_cond(fig, t):
    frame_base(fig, 'Số điều kiện và chuẩn hóa dữ liệu', 92 + t)
    cases = [(np.array([1.0, 10.0]), 'Chưa chuẩn hóa: L/m = 10', O), (np.array([1.0, 1.0]), 'Đã chuẩn hóa: L/m = 1', T)]
    c = np.array([0.0, 0.0]); w0 = [-3.0, 1.2]
    for k, (a, lab, col) in enumerate(cases):
        ax = fig.add_axes([0.05 + 0.31 * k, 0.2, 0.29, 0.62])
        contour(ax, a, c, [0.1, 0.5, 1.2, 2.5, 4.5, 7], [(-3.6, 3.6), (-2.2, 2.2)])
        ax.set_title(lab, color=col, fontsize=14); ax.tick_params(labelsize=9)
        P = path2(w0, 1 / a.max(), 25, a, c)
        cur = draw_path(ax, P, max(0, (t - 4) / 0.8), col)
        ax.text(-3.4, -2.0, f't = {int(min(max(0, (t - 4) / 0.8), 25))}', fontsize=12, color=INK)
    box(fig, 0.82, 0.68, r'$J(\mathbf{w}_t)-J^* \leq \left(1-\frac{m}{L}\right)^{t}\,(J(\mathbf{w}_0)-J^*)$', 15)
    fig.text(0.82, 0.55, 'với η = 1/L', ha='center', fontsize=14, color=INK)
    if t > 8:
        fig.text(0.82, 0.44, 'L/m = 10  →  hệ số co 0,9', ha='center', fontsize=15, color=O)
        fig.text(0.82, 0.37, 'L/m = 1  →  hệ số co 0', ha='center', fontsize=15, color=T)
    if t > 16:
        fig.text(0.82, 0.25, 'Chuẩn hóa z-score (mục 2.6)\n→ đường đồng mức tròn hơn', ha='center', fontsize=13, color=DARK)

# ---------------- Cảnh 6: batch / SGD / mini-batch ----------------
rng = np.random.default_rng(0); NS = 1000
Xs = rng.normal(size=NS); Ys = 1.5 - 2.0 * Xs + rng.normal(scale=0.8, size=NS)
Xd = np.c_[np.ones(NS), Xs]; WSTAR = np.linalg.lstsq(Xd, Ys, rcond=None)[0]
def gd_var(bs, steps=45, eta=0.08, seed=1):
    r = np.random.default_rng(seed); w = np.array([-1.5, 1.0]); P = [w.copy()]
    for _ in range(steps):
        idx = np.arange(NS) if bs is None else r.choice(NS, bs, replace=False)
        g = 2 / len(idx) * Xd[idx].T @ (Xd[idx] @ w - Ys[idx]); w = w - eta * g; P.append(w.copy())
    return np.array(P)
VARS = [(gd_var(None), 'Theo lô (n mẫu)', B), (gd_var(1), 'Ngẫu nhiên — SGD (1 mẫu)', O), (gd_var(32), 'Lô nhỏ (32 mẫu)', T)]
def s_var(fig, t):
    frame_base(fig, 'Ba biến thể theo cách lấy mẫu', 120 + t)
    ax = fig.add_axes([0.05, 0.2, 0.5, 0.65])
    g0, g1 = np.meshgrid(np.linspace(-2.2, 3.2, 160), np.linspace(-3.2, 1.6, 160))
    Z = ((Xd @ np.vstack([g0.ravel(), g1.ravel()]) - Ys[:, None]) ** 2).mean(0).reshape(g0.shape)
    ax.contour(g0, g1, Z, levels=[0.8, 1.2, 2, 3.5, 6, 10, 15], colors=GRID, linewidths=1.3)
    ax.set_xlim(-2.2, 3.2); ax.set_ylim(-3.2, 1.6); ax.set_aspect('equal')
    ax.set_xlabel('$w_0$ (hệ số tự do)', fontsize=12); ax.set_ylabel('$w_1$', fontsize=12)
    ax.plot(*WSTAR, '*', color=DARK, ms=16, zorder=8)
    u = max(0, (t - 2) * 2.2)
    show = [0] if t < 8 else ([0, 1] if t < 17 else [0, 1, 2])
    for k in show:
        P, lab, col = VARS[k]; draw_path(ax, P, u, col); ax.plot([], [], color=col, lw=3, label=lab)
    ax.legend(loc='lower left', fontsize=11, frameon=True)
    rows = [('Biến thể', 'Mẫu/bước', 'Ưu điểm', DARK), ('Theo lô', 'n', 'mượt, chính xác', B),
            ('SGD', '1', 'cập nhật rất nhanh', O), ('Lô nhỏ', '32–512', 'cân bằng, tận dụng GPU', T)]
    for k, (a, b, c, col) in enumerate(rows):
        if k == 0 or k - 1 in show:
            y = 0.72 - 0.09 * k; wt = 'bold' if k == 0 else 'normal'
            for x, s in [(0.6, a), (0.72, b), (0.81, c)]:
                fig.text(x, y, s, fontsize=13, color=col, weight=wt)
    fig.text(0.6, 0.27, 'Bài toán minh họa: hồi quy tuyến tính, n = 1000,\ncùng η = 0,08 và 45 bước cập nhật', fontsize=11, color=INK)

# ---------------- Cảnh 7: dừng & tóm tắt ----------------
def s_stop(fig, t):
    frame_base(fig, 'Tiêu chuẩn dừng và tóm tắt', 146 + t)
    ax = fig.add_axes([0.07, 0.21, 0.42, 0.58]); ax.set_yscale('log')
    it = np.arange(0, 60); ax.set_xlim(0, 60); ax.set_ylim(1e-3, 50)
    ax.plot(it, 9 * 0.995 ** it + 0.0, color=T, lw=2.5, label='đi ngang quá sớm → η quá nhỏ')
    zig = 9 * 0.9 ** it * (1 + 0.6 * (-1) ** it) + 2e-3
    ax.plot(it, zig, color=O, lw=1.8, label='răng cưa mạnh → η quá lớn')
    ax.plot(it, 9 * 0.8 ** it + 1e-3, color=B, lw=2.5, label='giảm đều → η hợp lý')
    ax.set_xlabel('Số vòng lặp', fontsize=12); ax.set_ylabel('Hàm mất mát', fontsize=12)
    ax.legend(loc='lower left', fontsize=10.5, frameon=False)
    items = ['Dừng khi ‖∇J(w_t)‖₂ < ε', 'hoặc khi J thay đổi rất ít giữa hai vòng lặp', 'hoặc khi đạt số vòng lặp tối đa']
    for k, s in enumerate(items):
        fig.text(0.55, 0.74 - 0.065 * k, '• ' + s, fontsize=14, color=DARK)
    if t > 14:
        summ = ['Đi ngược gradient một bước η', 'η quá nhỏ: chậm · quá lớn: phân kỳ', 'Chuẩn hóa dữ liệu → hội tụ nhanh hơn',
                'Lô nhỏ là mặc định trong học sâu', 'Luôn theo dõi đường cong mất mát']
        fig.text(0.55, 0.47, 'TÓM TẮT', fontsize=13, color=B, weight='bold')
        for k, s in enumerate(summ):
            fig.text(0.55, 0.41 - 0.05 * k, '✓ ' + s, fontsize=13, color=DARK)

_FIRST = [0, 1, 5, 8, 12, 15, 18]  # câu phụ đề mở đầu mỗi cảnh
_FNS = [s_title, s_idea, s_contour, s_lr, s_cond, s_var, s_stop]
SCENES = [(float(_T[a]), float(_T[b]) if b else DUR, f) for a, b, f in zip(_FIRST, _FIRST[1:] + [0], _FNS)]

def srt_time(x):
    h, r = divmod(int(x * 1000), 3600000); m, r = divmod(r, 60000); s, ms = divmod(r, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'

if __name__ == '__main__':
    with open('bai9_giam_gradient.srt', 'w', encoding='utf-8') as f:
        for i, (a, b, s) in enumerate(SUBS, 1):
            f.write(f'{i}\n{srt_time(a)} --> {srt_time(b)}\n{s}\n\n')
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
                           '-movflags', '+faststart', 'bai9_giam_gradient_silent.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)):
        t = n / FPS
        a, b, fn = next(s for s in SCENES if s[0] <= t < s[1])
        NOW[0] = t; fn(fig, t - a); fig.canvas.draw()
        ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
        if n % (FPS * 10) == 0: print(f'{t:.0f}s', flush=True)
    ff.stdin.close(); ff.wait()
