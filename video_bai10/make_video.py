"""Video Bài 10 - Phân tích thành phần chính (Toán cho học máy, ĐH Trà Vinh).
Thời lượng mỗi câu lấy từ tts/durations.json (chạy make_voice.py trước).
Chạy: python make_video.py  -> bai10_pca_silent.mp4 ; sau đó python mux_audio.py
"""
import json, subprocess, textwrap
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from noi_dung import TEXTS

W, H, FPS = 1280, 720, 24
B, O, T, INK, GRID, DARK, LIGHT = '#4a5fc1', '#d97706', '#0e8f7e', '#3a4050', '#dde0ea', '#1c1f2a', '#9aa0b4'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.edgecolor': INK, 'axes.labelcolor': DARK,
                     'xtick.color': INK, 'ytick.color': INK, 'axes.grid': True, 'grid.color': GRID,
                     'axes.spines.top': False, 'axes.spines.right': False, 'mathtext.fontset': 'dejavusans'})
ease = lambda u: 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0, 1))
vn = lambda x, d=2: f'{x:.{d}f}'.replace('.', ',')

# ---- Thời gian: mỗi câu dài = giọng đọc + 1,2 s (tối thiểu cho các câu có hoạt hình dài) ----
DURS = json.load(open('tts/durations.json'))
MINS = {0: 5, 4: 5, 6: 10, 12: 7, 16: 7}
try:  # độ dài khung đã dùng khi dựng hình - giữ cố định để giọng đọc tạo lại không làm lệch hình
    SLOTS = json.load(open('tts/slots.json'))
except FileNotFoundError:
    SLOTS = [float(max(np.ceil((d + 1.2) * 2) / 2, MINS.get(i, 0))) for i, d in enumerate(DURS)]
_T = np.concatenate([[0], np.cumsum(SLOTS)])
SUBS = [(float(_T[i]), float(_T[i + 1]), TEXTS[i]) for i in range(len(TEXTS))]
DUR = float(_T[-1])
NOW = [0.0]
st = lambda i: NOW[0] - _T[i]                              # số giây kể từ khi câu i bắt đầu
pr = lambda i, d=None: float(np.clip(st(i) / (d or SLOTS[i]), 0, 1))  # tiến độ trong câu i

# ---- Dữ liệu 2 chiều minh họa ----
rng = np.random.default_rng(3); N = 150
ang = np.deg2rad(32); R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
MU = np.array([3.2, 2.2])
X = (rng.normal(size=(N, 2)) * [1.7, 0.55]) @ R.T + MU
Xc = X - X.mean(0); S = Xc.T @ Xc / N
LAM, Q = np.linalg.eigh(S); LAM, Q = LAM[::-1], Q[:, ::-1]
U1, U2 = Q[:, 0] * np.sign(Q[0, 0]), Q[:, 1] * np.sign(Q[1, 1])
TH1 = np.degrees(np.arctan2(U1[1], U1[0])) % 180          # góc của thành phần chính thứ nhất
var_th = lambda th: np.array([np.cos(np.radians(th)), np.sin(np.radians(th))]) @ S @ np.array([np.cos(np.radians(th)), np.sin(np.radians(th))])
_, SIG, VT = np.linalg.svd(Xc, full_matrices=False)
V1 = VT[0] * np.sign(VT[0, 0])                            # véc tơ riêng chỉ xác định sai khác dấu

def frame_base(fig, section):
    fig.clf(); fig.patch.set_facecolor('white')
    if section:
        fig.text(0.04, 0.945, 'BÀI 10 · PHÂN TÍCH THÀNH PHẦN CHÍNH', fontsize=11, color=B, weight='bold')
        fig.text(0.04, 0.895, section, fontsize=19, color=DARK, weight='bold')
    sub = next((s for a, b, s in SUBS if a <= NOW[0] < b), '')
    if sub:
        fig.patches.append(FancyBboxPatch((0.06, 0.018), 0.88, 0.085, boxstyle='round,pad=0.006',
                           transform=fig.transFigure, fc='#1c1f2aE6', ec='none'))
        fig.text(0.5, 0.06, '\n'.join(textwrap.wrap(sub, 98)), ha='center', va='center', fontsize=14.5,
                 color='white', linespacing=1.3)

def box(fig, x, y, s, fs=18, color=DARK, ha='center'):
    fig.text(x, y, s, fontsize=fs, color=color, ha=ha, va='center',
             bbox=dict(boxstyle='round,pad=0.5', fc='#f2f4fa', ec=GRID))

def cloud_ax(fig, rect, lim=((-4.6, 4.6), (-3.0, 3.0))):
    ax = fig.add_axes(rect); ax.set_xlim(*lim[0]); ax.set_ylim(*lim[1]); ax.set_aspect('equal')
    ax.set_xlabel('$x_1$', fontsize=12); ax.set_ylabel('$x_2$', fontsize=12); ax.tick_params(labelsize=9)
    return ax

def arrow(ax, v, color, lw=3, origin=(0, 0)):
    ax.annotate('', xy=np.add(origin, v), xytext=origin, arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=18))

# ---------------- Cảnh: tiêu đề ----------------
def s_title(fig):
    frame_base(fig, ''); a = pr(0, 1.2)
    fig.text(0.5, 0.68, 'TOÁN CHO HỌC MÁY', ha='center', fontsize=16, color=B, weight='bold', alpha=a)
    fig.text(0.5, 0.57, 'Bài 10. Phân tích thành phần chính', ha='center', fontsize=34, color=DARK, weight='bold', alpha=a)
    fig.text(0.5, 0.45, r'$\max_{\mathbf{u}}\ \mathbf{u}^{\top}\mathbf{S}\,\mathbf{u}\quad \mathrm{v.đ.k.}\ \ \|\mathbf{u}\|_2=1$',
             ha='center', fontsize=26, color=O, alpha=a)
    fig.text(0.5, 0.33, 'Chương 3 · Ứng dụng toán trong học máy', ha='center', fontsize=14, color=INK, alpha=a)

# ---------------- Cảnh: vì sao giảm chiều ----------------
yy, xx = np.mgrid[0:10, 0:10]
IMG = np.clip(1.2 - np.abs(np.hypot(xx - 4.5, yy - 4.5) - 3.0), 0, 1)  # một "chữ số 0" 10×10
def s_why(fig):
    frame_base(fig, 'Vì sao cần giảm chiều?')
    ax = fig.add_axes([0.06, 0.4, 0.22, 0.4]); ax.imshow(IMG, cmap='Greys', vmin=0, vmax=1.3); ax.set_xticks([]); ax.set_yticks([])
    ax.grid(False); ax.set_title('ảnh xám (minh họa 10×10)', fontsize=11, color=INK)
    if st(1) > 2:
        k = ease((st(1) - 2) / 2.5); n = int(100 * k)
        ax2 = fig.add_axes([0.33, 0.56, 0.6 * max(k, 0.02), 0.06]); ax2.imshow(IMG.reshape(1, -1)[:, :max(n, 1)], cmap='Greys',
                                                                                  vmin=0, vmax=1.3, aspect='auto')
        ax2.set_xticks([]); ax2.set_yticks([]); ax2.grid(False)
        fig.text(0.33, 0.66, 'trải phẳng thành véc tơ', fontsize=13, color=INK)
        if k > 0.95:
            fig.text(0.33, 0.47, r'ảnh $100\times100$  →  $\mathbf{x}\in\mathbb{R}^{10\,000}$', fontsize=20, color=O)
    probs = ['Chi phí tính toán lớn', 'Khó trực quan hóa', 'Dữ liệu thưa thớt → dễ quá khớp']
    for k, p in enumerate(probs):
        if st(2) > 0.5 + 1.6 * k:
            fig.text(0.33 + 0.21 * k, 0.28, p, fontsize=13.5, color=DARK, ha='left',
                     bbox=dict(boxstyle='round,pad=0.5', fc='#fdf3e7' if k == 2 else '#f2f4fa', ec=GRID))

# ---------------- Cảnh: cực đại phương sai ----------------
def s_var(fig):
    frame_base(fig, 'Tìm hướng giữ nhiều phương sai nhất')
    lim = ((-4.6, 8.4), (-3.2, 5.6)) if NOW[0] < _T[5] else ((-4.6, 4.6), (-3.0, 3.0))
    ax = cloud_ax(fig, [0.04, 0.17, 0.5, 0.7], lim)
    P = X - X.mean(0) * (ease(pr(4, 3.0)) if NOW[0] >= _T[4] else 0)
    ctr = P.mean(0)
    ax.scatter(P[:, 0], P[:, 1], s=16, color=LIGHT, alpha=0.9, zorder=3)
    ax.plot(*ctr, 'o', color=B, ms=9, zorder=5); ax.text(ctr[0] + 0.2, ctr[1] - 0.5, r'$\bar{\mathbf{x}}$', color=B, fontsize=15)
    if NOW[0] < _T[4]:  # câu 3: chiếu lên trục chính
        k = ease(pr(3, 3.5)); d = U1
        ax.plot(*np.c_[ctr - 6 * d, ctr + 6 * d], color=O, lw=2)
        proj = ctr + ((P - ctr) @ d)[:, None] * d
        for p, q in zip(P[::2], proj[::2]): ax.plot([p[0], p[0] + (q[0] - p[0]) * k], [p[1], p[1] + (q[1] - p[1]) * k], color=O, lw=0.6, alpha=0.6)
        ax.scatter(proj[:, 0], proj[:, 1], s=10, color=O, alpha=k, zorder=4)
        fig.text(0.58, 0.6, 'Chiếu dữ liệu xuống\nkhông gian con k chiều', fontsize=18, color=DARK)
        fig.text(0.58, 0.47, '→ giữ lại nhiều phương sai nhất', fontsize=16, color=O)
        return
    if NOW[0] < _T[5]:
        fig.text(0.58, 0.6, r'$\mathbf{x}_i \leftarrow \mathbf{x}_i - \bar{\mathbf{x}}$', fontsize=26, color=B)
        fig.text(0.58, 0.48, 'đưa tâm dữ liệu về gốc tọa độ', fontsize=16, color=DARK)
        return
    # câu 5–7: hướng u xoay, đồ thị phương sai theo góc
    if NOW[0] < _T[6]: th = 0.0
    elif NOW[0] < _T[7]: th = 180 * ease(st(6) / (SLOTS[6] - 1))
    else: th = 180 + (TH1 - 180) * ease(pr(7, 2.5))
    u = np.array([np.cos(np.radians(th)), np.sin(np.radians(th))])
    ax.plot(*np.c_[-7 * u, 7 * u], color=O, lw=2)
    z = Xc @ u; proj = z[:, None] * u
    ax.scatter(proj[:, 0], proj[:, 1], s=10, color=O, zorder=4)
    for p, q in zip(Xc[::3], proj[::3]): ax.plot([p[0], q[0]], [p[1], q[1]], color=O, lw=0.5, alpha=0.4)
    arrow(ax, 1.6 * u, DARK); ax.text(*(1.9 * u + [0.1, 0.1]), r'$\mathbf{u}$', fontsize=16, color=DARK)
    a2 = fig.add_axes([0.6, 0.47, 0.36, 0.36]); ths = np.linspace(0, 180, 181)
    a2.set_xlim(0, 180); a2.set_ylim(0, LAM[0] * 1.15); a2.set_xticks([0, 45, 90, 135, 180])
    a2.set_xlabel('góc của u (độ)', fontsize=11); a2.set_ylabel(r'$\mathbf{u}^{\top}\mathbf{S}\mathbf{u}$', fontsize=12)
    a2.tick_params(labelsize=9)
    traced = ths[ths <= min(th, 180)] if NOW[0] < _T[7] else ths
    a2.plot(traced, [var_th(t) for t in traced], color=B, lw=2.5)
    a2.plot(th if th <= 180 else th - 180, var_th(th), 'o', color=O, ms=9, zorder=5)
    if NOW[0] >= _T[7]:
        a2.axhline(LAM[0], color=T, ls='--', lw=1.2); a2.axhline(LAM[1], color=INK, ls=':', lw=1.2)
        a2.text(3, LAM[0] * 1.03, r'$\lambda_{\max}$', color=T, fontsize=12); a2.text(3, LAM[1] + 0.06, r'$\lambda_{\min}$', color=INK, fontsize=12)
    fig.text(0.78, 0.37, f'phương sai = {vn(var_th(th))}', ha='center', fontsize=17, color=O)
    if NOW[0] >= _T[7]:
        box(fig, 0.78, 0.24, r'$\max_{\mathbf{u}}\ \mathbf{u}^{\top}\mathbf{S}\mathbf{u}\ \ \mathrm{v.đ.k.}\ \|\mathbf{u}\|_2=1$', 15)

# ---------------- Cảnh: Lagrange → véc tơ riêng ----------------
def s_eig(fig):
    frame_base(fig, 'Lời giải: véc tơ riêng của ma trận hiệp phương sai')
    ax = cloud_ax(fig, [0.04, 0.17, 0.5, 0.7])
    ax.scatter(Xc[:, 0], Xc[:, 1], s=16, color=LIGHT, zorder=3)
    k = ease(pr(8, 2.5))
    arrow(ax, 2 * np.sqrt(LAM[0]) * U1 * k, O, 3.5); arrow(ax, 2 * np.sqrt(LAM[1]) * U2 * k, T, 3.5)
    if k > 0.9:
        ax.text(*(2 * np.sqrt(LAM[0]) * U1 + [0.15, 0.0]), r'$\mathbf{u}_1$', color=O, fontsize=17)
        ax.text(*(2 * np.sqrt(LAM[1]) * U2 + [0.15, -0.2]), r'$\mathbf{u}_2$', color=T, fontsize=17)
    box(fig, 0.78, 0.76, r'$L=\mathbf{u}^{\top}\mathbf{S}\mathbf{u}-\lambda(\mathbf{u}^{\top}\mathbf{u}-1)$', 15)
    fig.text(0.78, 0.64, r'$\nabla_{\mathbf{u}}L=0\ \ \Rightarrow\ \ \mathbf{S}\mathbf{u}=\lambda\mathbf{u}$', ha='center', fontsize=20, color=DARK)
    fig.text(0.78, 0.55, r'$\mathbf{u}^{\top}\mathbf{S}\mathbf{u}=\lambda\,\mathbf{u}^{\top}\mathbf{u}=\lambda$', ha='center', fontsize=18, color=DARK)
    if st(8) > 4:
        fig.text(0.78, 0.44, f'λ₁ = {vn(LAM[0])}     λ₂ = {vn(LAM[1])}', ha='center', fontsize=17, color=INK)
    if NOW[0] >= _T[9]:
        fig.text(0.78, 0.31, 'Thành phần chính thứ nhất:\nvéc tơ riêng của λ lớn nhất', ha='center', fontsize=16, color=O, weight='bold')

# ---------------- Cảnh: thuật toán ----------------
STEPS = [r'1. Trừ trung bình (chuẩn hóa nếu khác đơn vị)', r'2. $\mathbf{S}=\frac{1}{n}\mathbf{X}_c^{\top}\mathbf{X}_c$  (d×d, đối xứng, nửa xđd)',
         r'3. $\mathbf{S}=\mathbf{Q}\Lambda\mathbf{Q}^{\top}$, sắp $\lambda_1\geq\dots\geq\lambda_d$', r'4. Lấy $\mathbf{U}_k=[\mathbf{u}_1\cdots\mathbf{u}_k]$',
         r'5. Chiếu $\mathbf{Z}=\mathbf{X}_c\mathbf{U}_k$;  khôi phục $\hat{\mathbf{X}}_c=\mathbf{Z}\mathbf{U}_k^{\top}$']
def s_algo(fig):
    frame_base(fig, 'Thuật toán PCA')
    ax = cloud_ax(fig, [0.04, 0.17, 0.46, 0.7])
    k = ease(pr(12, 4.0)) if NOW[0] >= _T[12] else 0
    rec = (Xc @ U1)[:, None] * U1; P = Xc + (rec - Xc) * k
    ax.plot(*np.c_[-6 * U1, 6 * U1], color=O, lw=1.5, alpha=0.7)
    if k > 0:
        for p, q in zip(Xc[::2], P[::2]): ax.plot([p[0], q[0]], [p[1], q[1]], color=O, lw=0.5, alpha=0.35)
    ax.scatter(P[:, 0], P[:, 1], s=16, color=B if k < 1 else O, zorder=3)
    arrow(ax, 2 * np.sqrt(LAM[0]) * U1, O, 3); arrow(ax, 2 * np.sqrt(LAM[1]) * U2, T, 3)
    cur = 0 if NOW[0] < _T[10] + SLOTS[10] / 3 else (1 if NOW[0] < _T[10] + 2 * SLOTS[10] / 3 else 2) if NOW[0] < _T[11] else (3 if NOW[0] < _T[11] + SLOTS[11] / 2 else 4)
    for i, s in enumerate(STEPS):
        on = i == cur and NOW[0] < _T[12]
        fig.text(0.53, 0.78 - 0.1 * i, s, fontsize=14.5, color=O if on else (DARK if i <= cur else LIGHT),
                 weight='bold' if on else 'normal')
    if NOW[0] >= _T[12]:
        fig.text(0.53, 0.25, f'k = 1: giữ {vn(100 * LAM[0] / LAM.sum(), 1)}% phương sai', fontsize=16, color=O)

# ---------------- Cảnh: SVD ----------------
def s_svd(fig):
    frame_base(fig, 'Tính PCA qua phân rã SVD')
    box(fig, 0.5, 0.74, r'$\mathbf{X}_c=\mathbf{U}\Sigma\mathbf{V}^{\top}\ \Rightarrow\ \mathbf{S}=\frac{1}{n}\mathbf{X}_c^{\top}\mathbf{X}_c=\mathbf{V}\,\frac{\Sigma^2}{n}\,\mathbf{V}^{\top}$', 22)
    fig.text(0.5, 0.6, 'Kiểm tra trên dữ liệu minh họa (n = 150):', ha='center', fontsize=15, color=INK)
    rows = [('', 'Phân rã phổ của S', 'SVD của Xc'), ('λ₁', vn(LAM[0], 4), vn(SIG[0] ** 2 / N, 4)), ('λ₂', vn(LAM[1], 4), vn(SIG[1] ** 2 / N, 4)),
            ('u₁', f'({vn(U1[0], 3)}; {vn(U1[1], 3)})', f'({vn(V1[0], 3)}; {vn(V1[1], 3)})')]
    for r, row in enumerate(rows):
        if st(13) > 1 + 1.2 * r:
            for c, s in enumerate(row):
                fig.text([0.3, 0.47, 0.7][c], 0.5 - 0.075 * r, s, ha='center', fontsize=16, color=DARK if r else B, weight='bold' if r == 0 else 'normal')
    if st(13) > 6:
        fig.text(0.5, 0.18, 'Không cần lập S tường minh → chính xác hơn về số học, nhanh hơn khi d lớn', ha='center', fontsize=14, color=T)

# ---------------- Cảnh: chọn k ----------------
RATIO = np.array([42, 24.5, 13.5, 8, 5, 3.5, 2, 1.5]); CUM = np.cumsum(RATIO)
def s_k(fig):
    frame_base(fig, 'Chọn số thành phần chính k')
    ax = fig.add_axes([0.07, 0.19, 0.5, 0.65]); n = len(RATIO); x = np.arange(1, n + 1)
    g = ease(pr(14, 4)) * n
    ax.set_xlim(0.4, n + 0.6); ax.set_ylim(0, 108); ax.set_xticks(x); ax.set_xlabel('Thành phần chính', fontsize=12)
    ax.set_ylabel('Phần trăm phương sai (%)', fontsize=12)
    ax.bar(x, RATIO * np.clip(g - (x - 1), 0, 1), color=B, width=0.6, label='từng thành phần')
    m = int(np.clip(np.ceil(g), 1, n)); ax.plot(x[:m], CUM[:m], '-o', color=O, lw=2.5, label='tích lũy $\\rho_k$')
    ax.legend(loc='center right', fontsize=11, frameon=False)
    if NOW[0] >= _T[15]:
        ax.axhline(90, color=DARK, ls='--', lw=1.2); ax.text(0.55, 91.5, 'ngưỡng 90%', fontsize=11)
        ax.axhline(95, color=LIGHT, ls=':', lw=1.2); ax.text(0.55, 96.5, '95%', fontsize=10, color=INK)
    if NOW[0] >= _T[16]:
        for kk, col in [(4, INK), (5, T)]:
            ax.plot(kk, CUM[kk - 1], 'o', ms=14, mfc='none', mec=col, mew=2.5)
            ax.text(kk + 0.15, CUM[kk - 1] - 7, f'k={kk}: {vn(CUM[kk - 1], 0)}%', color=col, fontsize=12, weight='bold')
    box(fig, 0.79, 0.72, r'$\rho_k=\dfrac{\lambda_1+\cdots+\lambda_k}{\lambda_1+\cdots+\lambda_d}$', 20)
    if NOW[0] >= _T[15]:
        fig.text(0.79, 0.52, 'k nhỏ nhất với ρₖ ≥ ngưỡng', ha='center', fontsize=15, color=DARK)
        fig.text(0.79, 0.45, 'hoặc điểm gãy của đồ thị', ha='center', fontsize=15, color=DARK)
    if NOW[0] >= _T[16]:
        fig.text(0.79, 0.33, 'Ngưỡng 90%  →  k = 5', ha='center', fontsize=18, color=T, weight='bold')

# ---------------- Cảnh: lưu ý ----------------
r2 = np.random.default_rng(7); M = 120
CA = np.c_[r2.normal(0, 2.0, M), r2.normal(0.6, 0.25, M)]; CB = np.c_[r2.normal(0, 2.0, M), r2.normal(-0.6, 0.25, M)]
def s_note(fig):
    frame_base(fig, 'Lưu ý khi áp dụng PCA')
    if NOW[0] < _T[18]:
        ax = fig.add_axes([0.05, 0.2, 0.45, 0.62]); ax.set_xlim(-6, 6); ax.set_ylim(-3, 3); ax.set_aspect('equal'); ax.tick_params(labelsize=9)
        ax.scatter(*CA.T, s=12, color=B, label='lớp A'); ax.scatter(*CB.T, s=12, color=O, label='lớp B')
        arrow(ax, (4, 0), DARK); ax.text(4.1, 0.25, 'PC1', fontsize=13, color=DARK); arrow(ax, (0, 1.6), T); ax.text(0.15, 1.7, 'PC2', fontsize=13, color=T)
        ax.legend(loc='lower left', fontsize=10, frameon=True)
        k = ease((st(17) - 2) / 2)
        for j, (dim, lab, col) in enumerate([(0, 'chiếu lên PC1: hai lớp chồng lấn', DARK), (1, 'chiếu lên PC2: hai lớp tách rời', T)]):
            a = fig.add_axes([0.58, 0.58 - 0.3 * j, 0.38, 0.2]); bins = np.linspace(-6, 6, 40) if dim == 0 else np.linspace(-1.6, 1.6, 40)
            a.hist(CA[:, dim], bins=bins, color=B, alpha=0.6 * k); a.hist(CB[:, dim], bins=bins, color=O, alpha=0.6 * k)
            a.set_title(lab, fontsize=12.5, color=col); a.set_yticks([]); a.tick_params(labelsize=8)
    else:
        items = [('Chuẩn hóa z-score khi các đặc trưng khác đơn vị đo', DARK),
                 ('Ước lượng trung bình, độ lệch chuẩn và Uₖ chỉ trên tập huấn luyện', DARK),
                 ('Áp dụng đúng phép biến đổi đó cho tập kiểm tra', DARK),
                 ('Nếu ước lượng trên toàn bộ dữ liệu → rò rỉ dữ liệu', O)]
        for i, (s, c) in enumerate(items):
            if st(18) > 0.5 + 1.4 * i:
                fig.text(0.1, 0.72 - 0.11 * i, ('⚠ ' if c == O else '• ') + s, fontsize=18, color=c)

# ---------------- Cảnh: tóm tắt ----------------
def s_sum(fig):
    frame_base(fig, 'Tóm tắt')
    items = ['PCA tìm không gian con giữ nhiều phương sai nhất', 'Thành phần chính = véc tơ riêng của S, sắp theo λ giảm dần',
             'Dẫn dắt từ thương Rayleigh và nhân tử Lagrange', 'Chọn k theo tỉ lệ phương sai tích lũy hoặc điểm gãy',
             'Không giám sát, nhạy với thang đo, chỉ nắm bắt quan hệ tuyến tính']
    for i, s in enumerate(items):
        if st(19) > 0.3 + 1.0 * i:
            fig.text(0.1, 0.74 - 0.1 * i, '✓ ' + s, fontsize=18, color=DARK)

FIRST = [0, 1, 3, 8, 10, 13, 14, 17, 19]
FNS = [s_title, s_why, s_var, s_eig, s_algo, s_svd, s_k, s_note, s_sum]
SCENES = [(float(_T[a]), float(_T[b]) if b else DUR, f) for a, b, f in zip(FIRST, FIRST[1:] + [0], FNS)]

if __name__ == '__main__':
    json.dump(SLOTS, open('tts/slots.json', 'w'))
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
    ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                           '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
                           '-movflags', '+faststart', 'bai10_pca_silent.mp4'], stdin=subprocess.PIPE)
    for n in range(int(DUR * FPS)):
        t = n / FPS; NOW[0] = t
        fn = next(f for a, b, f in SCENES if a <= t < b)
        fn(fig); fig.canvas.draw(); ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
        if n % (FPS * 20) == 0: print(f'{t:.0f}/{DUR:.0f}s', flush=True)
    ff.stdin.close(); ff.wait()
