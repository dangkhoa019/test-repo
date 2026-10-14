"""Video Bài 7 - Phương pháp bình phương nhỏ nhất.  Chạy: python make_video.py [voice|render|mux|all]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'video_common'))
from engine import *
from noi_dung import TEXTS, SPOKEN

L = Lesson('Bài 7 · Phương pháp bình phương nhỏ nhất', TEXTS, SPOKEN, 'bai07_binh_phuong_nho_nhat',
           mins={0: 5, 2: 10, 9: 10}, chapter='Chương 3 · Ứng dụng toán trong học máy')

def s_title(fig):
    L.title(fig, 'Bài 7. Bình phương nhỏ nhất', r'$\mathbf{X}^{\top}\mathbf{X}\,\mathbf{w}=\mathbf{X}^{\top}\mathbf{y}$')

r = np.random.default_rng(8); XD = np.sort(r.uniform(0, 10, 14)); YD = 1.2 + 0.55 * XD + r.normal(0, 0.7, 14)
WLS = np.polyfit(XD, YD, 1)[::-1]; CX, CY = XD.mean(), YD.mean(); TH0 = np.arctan(WLS[1])
sse = lambda w0, w1, x=XD, y=YD: ((y - w0 - w1 * x) ** 2).sum()
def s_ls(fig):
    L.base(fig, 'Đặt bài toán bình phương nhỏ nhất')
    ax = ax_at(fig, [0.05, 0.17, 0.5, 0.68], (0, 10.5), (0, 9), equal=False, xl='x', yl='y')
    x, y = XD.copy(), YD.copy()
    if L.on(3) and L.st(3) > 5:  # thêm một điểm ngoại lai
        k = ease((L.st(3) - 5) / 2); x = np.r_[x, 9.5]; y = np.r_[y, 6.4 - 5.5 * k]
    ax.scatter(x, y, color=B, s=36, zorder=4)
    if L.now < L.T[2]: th = TH0 + 0.5
    elif L.now < L.T[3]: th = TH0 + 0.5 * np.cos(np.pi * 1.5 * L.pr(2, L.slots[2] - 1.5)) * (1 - ease((L.st(2) - (L.slots[2] - 2.5)) / 2))
    else: th = TH0
    if L.on(3):
        w1, w0 = np.polyfit(x, y, 1); 
    else:
        w1 = np.tan(th); w0 = CY - w1 * CX
    xs = np.array([0, 10.5]); ax.plot(xs, w0 + w1 * xs, color=O, lw=2.5)
    for xi, yi in zip(x, y): ax.plot([xi, xi], [yi, w0 + w1 * xi], color=T, lw=1.3)
    box(fig, 0.78, 0.76, r'$J(\mathbf{w})=\sum_i (y_i-\mathbf{w}^{\top}\mathbf{x}_i)^2=\|\mathbf{y}-\mathbf{Xw}\|_2^2$', 14)
    fig.text(0.78, 0.63, f'J = {vn(sse(w0, w1, x, y))}', ha='center', fontsize=24, color=O)
    if L.on(2) and not L.on(3):
        a2 = fig.add_axes([0.62, 0.22, 0.32, 0.3]); ths = np.linspace(TH0 - 0.55, TH0 + 0.55, 100)
        a2.plot(np.degrees(ths), [sse(CY - np.tan(t) * CX, np.tan(t)) for t in ths], color=B, lw=2); a2.plot(np.degrees(th), sse(w0, w1), 'o', color=O, ms=8)
        a2.set_xlabel('góc của đường thẳng (độ)', fontsize=10); a2.set_ylabel('J', fontsize=10); a2.tick_params(labelsize=8)
    if L.on(3):
        items = ['khả vi mọi nơi', 'hàm toàn phương lồi → nghiệm dạng đóng', 'nhiễu chuẩn → trùng ước lượng hợp lý cực đại']
        for k, s in enumerate(items): fig.text(0.6, 0.5 - 0.07 * k, '✓ ' + s, fontsize=14, color=DARK)
        if L.st(3) > 5: fig.text(0.6, 0.27, '✗ một điểm ngoại lai kéo lệch cả đường', fontsize=14, color=RED)

def s_deriv(fig):
    L.base(fig, 'Hệ phương trình chuẩn tắc')
    rows = [(4, 0, r'$J(\mathbf{w})=\mathbf{w}^{\top}\mathbf{X}^{\top}\mathbf{X}\mathbf{w}-2\mathbf{y}^{\top}\mathbf{X}\mathbf{w}+\mathbf{y}^{\top}\mathbf{y}$', DARK),
            (4, 2.5, r'$\nabla J(\mathbf{w})=2\mathbf{X}^{\top}\mathbf{X}\mathbf{w}-2\mathbf{X}^{\top}\mathbf{y}$', DARK),
            (5, 0.5, r'$\mathbf{X}^{\top}\mathbf{X}\,\mathbf{w}=\mathbf{X}^{\top}\mathbf{y}$', O),
            (5, 3, r'$\Rightarrow\ \mathbf{w}=(\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top}\mathbf{y}$  (khi khả nghịch)', DARK),
            (6, 0.5, r'$\nabla^2 J=2\mathbf{X}^{\top}\mathbf{X}\succeq 0\ \Rightarrow\ J$ lồi, điểm dừng = cực tiểu toàn cục', T),
            (6, 4, 'cột của X độc lập tuyến tính ⇒ XᵀX ≻ 0 ⇒ nghiệm duy nhất', T)]
    for k, (i, d, s, c) in enumerate(rows):
        if L.on(i) and L.st(i) > d: fig.text(0.08, 0.76 - 0.1 * k, s, fontsize=22 if c == O else 19, color=c)

PX = np.array([[1, 0], [1, 1], [1, 2]], float); PY = np.array([1.0, 3.0, 4.0]); PW = np.linalg.solve(PX.T @ PX, PX.T @ PY)
def mat(fig, x, y, M, fmt=lambda v: vn(v, 0), dx=0.045, dy=0.06, col=DARK, fs=17):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]): fig.text(x + j * dx, y - i * dy, fmt(M[i, j]), fontsize=fs, color=col, ha='center')
    h = (M.shape[0] - 1) * dy; fig.text(x - 0.03, y - h / 2, '[', fontsize=30 + 12 * (M.shape[0] - 1), color=INK, ha='center', va='center', family='DejaVu Sans', alpha=0.6)
    fig.text(x + (M.shape[1] - 1) * dx + 0.03, y - h / 2, ']', fontsize=30 + 12 * (M.shape[0] - 1), color=INK, ha='center', va='center', alpha=0.6)
def s_ex(fig):
    L.base(fig, 'Ví dụ: đường hồi quy qua ba điểm')
    ax = ax_at(fig, [0.05, 0.17, 0.42, 0.66], (-0.5, 2.6), (0, 5), equal=False, xl='x', yl='y')
    ax.scatter(PX[:, 1], PY, color=B, s=60, zorder=4)
    fig.text(0.53, 0.78, 'X =', fontsize=18, color=DARK); mat(fig, 0.6, 0.79, PX)
    fig.text(0.72, 0.78, 'y =', fontsize=18, color=DARK); mat(fig, 0.79, 0.79, PY.reshape(3, 1))
    if L.on(8):
        s = L.st(8)
        fig.text(0.53, 0.5, 'XᵀX =', fontsize=17, color=DARK); mat(fig, 0.63, 0.51, PX.T @ PX)
        if s > 2: fig.text(0.74, 0.5, 'Xᵀy =', fontsize=17, color=DARK); mat(fig, 0.84, 0.51, (PX.T @ PY).reshape(2, 1))
        if s > 4: fig.text(0.53, 0.3, 'w₀ = 7/6 ≈ 1,17,   w₁ = 3/2 = 1,5', fontsize=19, color=T)
        if s > 4:
            k = ease((s - 4) / 2); xs = np.array([-0.5, 2.6]); ax.plot(xs, PW[0] + PW[1] * xs * 1, color=O, lw=2.5, alpha=k)
            for xi, yi in zip(PX[:, 1], PY): ax.plot([xi, xi], [yi, PW[0] + PW[1] * xi], color=T, lw=1.5, alpha=k)

GY = np.array([1.0, 4.0, 2.0])  # véc tơ minh họa riêng để thấy rõ phần dư trong ℝ³
YH = PX @ np.linalg.solve(PX.T @ PX, PX.T @ GY); E = GY - YH; PM = PX @ np.linalg.inv(PX.T @ PX) @ PX.T
def s_geo(fig):
    L.base(fig, 'Ý nghĩa hình học: phép chiếu trực giao')
    ax = fig.add_axes([0.0, 0.1, 0.55, 0.8], projection='3d')
    a, b = PX[:, 0], PX[:, 1]; s_, t_ = np.meshgrid(np.linspace(-0.3, 2.0, 6), np.linspace(-0.8, 1.6, 6))
    P = s_[..., None] * a + t_[..., None] * b
    ax.plot_surface(P[..., 0], P[..., 1], P[..., 2], color=B, alpha=0.15, linewidth=0)
    def vec(v, c, lw=2.5, o=np.zeros(3)): ax.plot(*np.c_[o, o + v], color=c, lw=lw)
    vec(a, LIGHT, 2); vec(b, LIGHT, 2); vec(GY, DARK, 3)
    k = ease((L.st(9) - 1) / 2.5); vec(YH * k, O, 3)
    if k > 0.2: vec(E * min(1, k), T, 2.5, YH)
    if k > 0.9:
        u1 = -E / np.linalg.norm(E) * 0.25; u2 = -YH / np.linalg.norm(YH) * 0.25; q = YH + 0 * u1
        ax.plot(*np.c_[YH - u1 * -1, YH - u1 * -1 + u2, YH + u2], color=DARK, lw=1)
    ax.text(*GY, ' y', fontsize=14, color=DARK)

    if k > 0.9: ax.text(*YH, ' ŷ = Xw', fontsize=13, color=O); ax.text(*(YH + E / 2), ' e', fontsize=13, color=T)
    nrm = E / np.linalg.norm(E); inpl = np.array([1, 1, 1]) / np.sqrt(3); sw = np.radians(5 + 25 * L.pr(9))
    inpl = np.cos(sw) * inpl + np.sin(sw) * np.cross(nrm, inpl); d = np.cos(np.radians(28)) * inpl + np.sin(np.radians(28)) * nrm
    ax.view_init(np.degrees(np.arcsin(d[2])), np.degrees(np.arctan2(d[1], d[0]))); ax.set_xlim(0, 4); ax.set_ylim(0, 4); ax.set_zlim(0, 4); ax.set_box_aspect((1, 1, 1))
    ax.tick_params(labelsize=7); fig.text(0.27, 0.13, 'mặt phẳng col(X) ⊂ ℝ³ — minh họa với y = (1, 4, 2)', ha='center', fontsize=12, color=B)
    fig.text(0.58, 0.78, f'ŷ = ({vn(YH[0])}; {vn(YH[1])}; {vn(YH[2])})', fontsize=16, color=O)
    fig.text(0.58, 0.7, f'e = y − ŷ = ({vn(E[0])}; {vn(E[1])}; {vn(E[2])})', fontsize=16, color=T)
    fig.text(0.58, 0.62, f'Xᵀe = ({vn(abs(PX[:, 0] @ E))}; {vn(abs(PX[:, 1] @ E))})  ⇒  e ⟂ col(X)'.replace('⟂', 'vuông góc'), fontsize=16, color=DARK)
    if L.on(10):
        fig.text(0.58, 0.48, r'$\mathbf{P}=\mathbf{X}(\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top},\ \ \mathbf{P}^2=\mathbf{P}=\mathbf{P}^{\top}$', fontsize=17, color=DARK)
        mat(fig, 0.66, 0.36, PM, fmt=lambda v: vn(v, 2), dx=0.07, dy=0.055, fs=14)
        fig.text(0.86, 0.31, 'đối xứng ✓', fontsize=14, color=T)

def s_num(fig):
    if L.now < L.T[12]:
        L.base(fig, 'Khi ma trận chuẩn tắc suy biến')
        items = [('Giả nghịch đảo Moore – Penrose X⁺ (từ SVD)', 'nghiệm có chuẩn ℓ₂ nhỏ nhất'), ('Thêm điều chuẩn λ‖w‖₂²', 'XᵀX + λI luôn khả nghịch'),
                 ('Loại bớt đặc trưng / giảm chiều bằng PCA', 'loại bỏ cột dư thừa')]
        fig.text(0.08, 0.76, 'Cột của X phụ thuộc tuyến tính ⇒ XᵀX suy biến ⇒ vô số nghiệm', fontsize=17, color=RED)
        for k, (a, b) in enumerate(items):
            if L.st(11) > 1.5 + 1.8 * k:
                fig.text(0.1, 0.62 - 0.12 * k, f'{k + 1}. ' + a, fontsize=18, color=DARK); fig.text(0.14, 0.565 - 0.12 * k, '→ ' + b, fontsize=15, color=T)
        return
    L.base(fig, 'Giải số học ổn định')
    code = ['rng = np.random.default_rng(0)', 'X = np.c_[np.ones(100), rng.normal(size=(100, 2))]', 'w_true = np.array([1.5, -2.0, 0.8])',
            'y = X @ w_true + rng.normal(scale=0.3, size=100)', '', 'w1 = np.linalg.inv(X.T @ X) @ X.T @ y     # không nên',
            'w2 = np.linalg.solve(X.T @ X, X.T @ y)    # tốt hơn', 'w3 = np.linalg.lstsq(X, y, rcond=None)[0] # ổn định nhất (SVD)',
            'print(np.round(w3, 3))   # [ 1.451 -2.032  0.852]']
    for k, c in enumerate(code):
        if L.st(12) > 0.25 * k:
            fig.text(0.07, 0.78 - 0.065 * k, c, fontsize=15, family='DejaVu Sans Mono',
                     color=RED if 'không nên' in c else (T if 'ổn định' in c else (O if 'print' in c else DARK)))

r2 = np.random.default_rng(21); XT = np.sort(r2.uniform(0, 1, 10)); YT = np.sin(2 * np.pi * XT) + r2.normal(0, 0.2, 10)
XV = r2.uniform(0, 1, 40); YV = np.sin(2 * np.pi * XV) + r2.normal(0, 0.2, 40)
def r2s(y, yh): return 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()
def s_eval(fig):
    L.base(fig, 'Đánh giá chất lượng mô hình')
    if L.now < L.T[14]:
        box(fig, 0.5, 0.72, r'$\mathrm{MSE}=\frac{1}{n}\sum_i(y_i-\hat y_i)^2,\quad \mathrm{RMSE}=\sqrt{\mathrm{MSE}},\quad R^2=1-\dfrac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}$', 19)
        rows = ['R² = 1: khớp hoàn hảo', 'R² = 0: không tốt hơn luôn dự đoán ȳ', 'R² < 0: tệ hơn cả dự đoán trung bình']
        for k, s in enumerate(rows):
            if L.st(13) > 2 + 1.5 * k: fig.text(0.2, 0.5 - 0.08 * k, '• ' + s, fontsize=18, color=[T, DARK, RED][k])
        return
    xs = np.linspace(0, 1, 200)
    for k, deg in enumerate([3, 9]):
        c = np.polyfit(XT, YT, deg); ax = ax_at(fig, [0.06 + 0.47 * k, 0.3, 0.4, 0.48], (0, 1), (-2, 2), equal=False, fs=8)
        ax.scatter(XT, YT, color=B, s=30, zorder=4, label='huấn luyện'); ax.scatter(XV, YV, color=O, s=12, alpha=0.6, label='kiểm tra')
        ax.plot(xs, np.polyval(c, xs), color=DARK, lw=2); ax.set_title(f'đa thức bậc {deg}', fontsize=13)
        if k == 0: ax.legend(fontsize=9, loc='lower left')
        fig.text(0.26 + 0.47 * k, 0.21, f'R² huấn luyện = {vn(r2s(YT, np.polyval(c, XT)))}   R² kiểm tra = ' + (vn(r2s(YV, np.polyval(c, XV))) if r2s(YV, np.polyval(c, XV)) > -10 else '≪ 0 (rất tệ)'),
                 ha='center', fontsize=13.5, color=RED if deg == 9 else T)

def s_sum(fig):
    L.base(fig, 'Tóm tắt')
    L.bullets(fig, 15, ['Cực tiểu ‖y − Xw‖₂²: hàm toàn phương lồi', 'Hệ chuẩn tắc XᵀXw = Xᵀy',
                        'ŷ là hình chiếu trực giao của y lên col(X); e ⟂ col(X)'.replace('⟂', 'vuông góc'), 'Nghiệm duy nhất ⇔ cột của X độc lập tuyến tính',
                        'Giải bằng QR/SVD; đánh giá trên tập kiểm tra'], gap=1.7)

SCENES = [(0, s_title), (1, s_ls), (4, s_deriv), (7, s_ex), (9, s_geo), (11, s_num), (13, s_eval), (15, s_sum)]
if __name__ == '__main__':
    L.main(SCENES)
