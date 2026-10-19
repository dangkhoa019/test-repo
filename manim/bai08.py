"""Bài 8 - Các mô hình hồi quy (Manim)."""
from common import *

r = np.random.default_rng(4); XL = np.sort(r.uniform(0, 10, 30)); YL = 1.0 + 0.5 * XL + r.normal(0, 0.8, 30); WL = np.polyfit(XL, YL, 1)
r2 = np.random.default_rng(12); XT = np.sort(r2.uniform(-1, 1, 15)); f0 = lambda x: np.sin(2.5 * x) + 0.3 * x
YT = f0(XT) + r2.normal(0, 0.25, 15); XV = r2.uniform(-1, 1, 200); YV = f0(XV) + r2.normal(0, 0.25, 200)
Phi = lambda x, k: np.vander(np.atleast_1d(x), k + 1, increasing=True)

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
COLS = [B, O, T, INK, LIGHT, R]


class Bai(Lesson):
    LESSON = 'video_bai08'; LABEL = 'BÀI 8 · CÁC MÔ HÌNH HỒI QUY'; TEXTS = load_texts('video_bai08')
    MINS = {0: 5, 8: 11, 13: 9}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 8. Các mô hình hồi quy', 46, WHITE, BOLD),
                   M(r'P(y=1\mid\mathbf{x})=\sigma(\mathbf{w}^{\top}\mathbf{x})=\frac{1}{1+e^{-\mathbf{w}^{\top}\mathbf{x}}}', 46, O), VT('Chương 3 · Ứng dụng toán trong học máy', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–3 — hồi quy tuyến tính
        self.section('Hồi quy tuyến tính'); self.line(1)
        ax = axes([0, 10.5, 2], [-1, 9, 2], 6.4, 5.0, LEFT * 3.2 + DOWN * 0.45)
        dots = VGroup(*[Dot(ax.c2p(x, y), color=B, radius=0.06) for x, y in zip(XL, YL)])
        P1 = panel(M(r'y_i=\mathbf{w}^{\top}\mathbf{x}_i+\varepsilon_i,\quad \mathbf{x}_i=(1,x_{i1},\dots,x_{id})', 32)).move_to(RIGHT * 3.4 + UP * 2.1)
        self.play(Create(ax), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), run_time=2)
        self.play(Create(ax.plot(lambda x: np.polyval(WL, x), x_range=[0, 10.5], color=O, stroke_width=4)), FadeIn(P1), run_time=1.5)
        self.finish(1)
        self.line(2)
        bells = VGroup()
        for x0 in [2, 5, 8]:
            m = np.polyval(WL, x0)
            bells.add(ParametricFunction(lambda u, x0=x0, m=m: ax.c2p(x0 + 1.2 * np.exp(-u ** 2 / 1.28), m + u), t_range=[-2.2, 2.2], color=T, stroke_width=3),
                      DashedLine(ax.c2p(x0, m - 2.2), ax.c2p(x0, m + 2.2), color=T, stroke_width=1.5))
        self.play(LaggedStart(*[Create(b_) for b_ in bells], lag_ratio=0.3), run_time=2)
        ml = VGroup(M(r'\varepsilon_i\ \text{i.i.d.}\sim\mathcal{N}(0,\sigma^2)', 36, T), VT('⇒ ước lượng hợp lý cực đại', 24), VT('= nghiệm bình phương nhỏ nhất', 24)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + UP * 0.5)
        self.play(FadeIn(ml), run_time=1); self.finish(2)
        self.line(3)
        self.play(FadeIn(VGroup(M(r'y=w_0+w_1x+w_2x^2', 38, O), VT('vẫn là mô hình tuyến tính theo w', 24, O)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 1.6)), run_time=1)
        self.finish(3); self.clear_body()

        # 4–5 — hồi quy đa thức
        self.section('Hồi quy đa thức: mở rộng đặc trưng'); self.line(4)
        P1 = panel(M(r'\phi(x)=(1,\ x,\ x^2,\ \dots,\ x^k),\qquad \hat y=\mathbf{w}^{\top}\phi(x)', 40)).move_to(UP * 1.9)
        self.play(FadeIn(P1), run_time=1)
        xs = [-0.8, 0.1, 0.6]
        cells = [[M('x', 32, B), M(r'\to', 30, BG)] + [M(s_, 32, B) for s_ in ['1', 'x', 'x^2', 'x^3']]]
        for xi in xs: cells.append([M(vn(xi, 1).replace('−', '-').replace(',', '{,}'), 32), M(r'\to', 30, LIGHT)] + [M(vn(xi ** j, 3 if j else 0).replace('−', '-').replace(',', '{,}'), 32) for j in range(4)])
        tb = VGroup()
        for i, rr in enumerate(cells):
            for j, c in enumerate(rr): tb.add(c.move_to([-3.6 + [0, 1.1, 2.4, 3.9, 5.4, 6.9][j], 0.6 - 0.62 * i, 0]))
        self.wait(0.6)
        self.play(LaggedStart(*[FadeIn(c) for c in tb], lag_ratio=0.04), run_time=2.5)
        self.play(FadeIn(VT('ma trận thiết kế Φ — vẫn giải bằng bình phương nhỏ nhất', 24, T).move_to(DOWN * 2.4)), run_time=0.8)
        self.finish(4); self.clear_body()
        self.section('Dưới khớp, khớp vừa và quá khớp'); self.line(5)
        for j, (k, lab, c) in enumerate([(1, 'bậc 1 — dưới khớp', T), (4, 'bậc 4 — khớp vừa', B), (12, 'bậc 12 — quá khớp', O)]):
            w = np.linalg.lstsq(Phi(XT, k), YT, rcond=None)[0]; a_ = axes([-1, 1, 0.5], [-2, 2, 1], 3.7, 3.0, RIGHT * 4.2 * (j - 1) + DOWN * 0.1, nums=False)
            tr = np.mean((Phi(XT, k) @ w - YT) ** 2); te = np.mean((Phi(XV, k) @ w - YV) ** 2)
            info = VGroup(VT(f'MSE huấn luyện {vn(tr, 3)}', 19), VT('MSE kiểm tra ' + (vn(te, 3) if te < 100 else '≫ 1'), 19, R if te > 1 else INK)).arrange(DOWN, buff=0.1).next_to(a_, DOWN, buff=0.2)
            self.play(Create(a_), FadeIn(VGroup(*[Dot(a_.c2p(x, y), color=INK, radius=0.05) for x, y in zip(XT, YT)])),
                      Create(plot_clipped(a_, lambda x, w=w: np.polyval(w[::-1], x), [-1, 1], [-2, 2], color=c, stroke_width=3.5)),
                      FadeIn(VT(lab, 22, c).next_to(a_, UP, buff=0.15)), FadeIn(info), run_time=1.5)
            self.wait(0.4)
        self.finish(5); self.clear_body()

        # 6–7 — điều chuẩn
        self.section('Điều chuẩn: ridge và LASSO'); self.line(6)
        P1 = panel(VGroup(M(r'J_{\mathrm{ridge}}=\|\mathbf{y}-\mathbf{Xw}\|_2^2+\lambda\|\mathbf{w}\|_2^2', 38), M(r'J_{\mathrm{LASSO}}=\|\mathbf{y}-\mathbf{Xw}\|_2^2+\lambda\|\mathbf{w}\|_1', 38)).arrange(RIGHT, buff=0.9)).move_to(UP * 1.8)
        self.play(FadeIn(P1), run_time=1.2); self.wait(2)
        tx = VGroup(VT('λ ≥ 0 điều khiển mức phạt:  λ = 0 → bình phương nhỏ nhất thông thường', 24), VT('λ lớn → trọng số bị kéo mạnh về 0', 24)).arrange(DOWN, buff=0.3).move_to(DOWN * 0.1)
        self.play(FadeIn(tx), run_time=1); self.finish(6)
        self.line(7)
        self.play(FadeOut(tx), run_time=0.5)
        rr = VGroup(M(r'\mathbf{w}_{\mathrm{ridge}}=(\mathbf{X}^{\top}\mathbf{X}+\lambda\mathbf{I})^{-1}\mathbf{X}^{\top}\mathbf{y}', 46, O),
                    VT('mọi giá trị riêng được cộng thêm λ  ⇒  XᵀX + λI ≻ 0 khi λ > 0', 24), VT('thường không phạt w₀: căn giữa X và y trước khi giải', 22, T)).arrange(DOWN, buff=0.4).move_to(DOWN * 0.5)
        self.play(FadeIn(rr[0]), run_time=1); self.wait(2.2); self.play(FadeIn(rr[1]), run_time=0.8); self.wait(2.2); self.play(FadeIn(rr[2]), run_time=0.8)
        self.finish(7); self.clear_body()

        # 8 — đường đi hệ số
        self.section('Đường đi của hệ số theo λ'); self.line(8)
        self.play(FadeIn(VT('dữ liệu mô phỏng: 6 đặc trưng, chỉ 3 đặc trưng có ích', 18, LIGHT).to_corner(UR, buff=0.4).shift(DOWN * 0.45)), run_time=0.5)
        L0, L1 = np.log10(LAMS[0]), np.log10(LAMS[-1]); cur = ValueTracker(L0 + 0.01)
        groups = []
        for k, (Wp, lab) in enumerate([(RIDGE, 'Ridge (ℓ₂)'), (LASSO, 'LASSO (ℓ₁)')]):
            a_ = axes([0, L1 - L0, 1], [-2.5, 3.3, 1], 5.4, 3.8, RIGHT * 3.3 * (2 * k - 1) + DOWN * 0.5, nums=False)
            ttl = VT(lab, 24).next_to(a_, UP, buff=0.5)
            xl = VT('log λ', 18, LIGHT).next_to(a_, DOWN, buff=0.1)

            def paths(a_=a_, Wp=Wp):
                g = VGroup(); m = np.log10(LAMS) <= cur.get_value() + 1e-9
                if m.sum() >= 2:
                    for j in range(d): g.add(VMobject(color=COLS[j], stroke_width=3).set_points_as_corners([a_.c2p(x - L0, y) for x, y in zip(np.log10(LAMS)[m], Wp[m, j])]))
                g.add(DashedLine(a_.c2p(cur.get_value() - L0, -2.5), a_.c2p(cur.get_value() - L0, 3.3), color=LIGHT, stroke_width=1.5))
                i = max(int(m.sum()) - 1, 0); nz = (np.abs(Wp[i]) > 1e-8).sum()
                g.add(VT(f'{nz}/6 hệ số khác 0', 20, O if nz < 6 else INK).next_to(a_, UP, buff=0.08))
                return g
            pg = always_redraw(paths); groups.append(pg)
            self.add(a_, ttl, xl, pg)
        self.play(cur.animate.set_value(L1), run_time=self.slots[8] - 1.2, rate_func=linear)
        for g in groups: g.clear_updaters()
        self.finish(8); self.clear_body()

        # 9 — chọn λ
        self.section('Chọn λ: sai số huấn luyện và kiểm tra'); self.line(9)
        G0, G1 = np.log10(LG[0]), np.log10(LG[-1])
        a_ = axes([0, G1 - G0, 1], [0, ERR.max() * 1.05, 0.2], 6.2, 4.4, LEFT * 3.3 + DOWN * 0.45, nums=False)
        lab = VGroup(VT('log λ', 18, LIGHT).next_to(a_, DOWN, buff=0.1), VT('MSE', 18, LIGHT).next_to(a_, LEFT, buff=0.1))
        tr = VMobject(color=T, stroke_width=4).set_points_smoothly([a_.c2p(np.log10(l) - G0, e) for l, e in zip(LG, ERR[:, 0])])
        te = VMobject(color=O, stroke_width=4).set_points_smoothly([a_.c2p(np.log10(l) - G0, e) for l, e in zip(LG, ERR[:, 1])])
        leg = VGroup(row('—', 'huấn luyện', size=20, color=T), row('—', 'kiểm tra', size=20, color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(a_.c2p((G1 - G0) * 0.5, ERR.max() * 0.92))
        self.play(Create(a_), FadeIn(lab), FadeIn(leg), run_time=1)
        self.play(Create(tr), Create(te), run_time=3)
        i = ERR[:, 1].argmin()
        self.play(FadeIn(Dot(a_.c2p(np.log10(LG[i]) - G0, ERR[i, 1]), color=O, radius=0.1)), FadeIn(VT('λ tốt nhất', 20, O).next_to(a_.c2p(np.log10(LG[i]) - G0, ERR[i, 1]), UP, buff=0.25)), run_time=0.8)
        rt = VGroup(VT('Ridge trên đa thức bậc 12', 24), VT('15 điểm huấn luyện, 200 điểm kiểm tra', 20, LIGHT), VT('λ nhỏ: quá khớp', 24, R), VT('λ lớn: dưới khớp', 24, T),
                    VT('chọn λ bằng kiểm định chéo', 24, O)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 0.9 + DOWN * 0.3, aligned_edge=LEFT)
        self.play(FadeIn(rt), run_time=1)
        self.finish(9); self.clear_body()

        # 10–12 — logistic
        self.section('Hồi quy logistic cho phân loại nhị phân'); self.line(10)
        a_ = axes([-6, 6, 2], [0, 1, 0.5], 6.2, 4.2, LEFT * 3.3 + DOWN * 0.45)
        lab = VGroup(M(r'z=\mathbf{w}^{\top}\mathbf{x}', 28, LIGHT).next_to(a_, DOWN, buff=0.1), VT('P(y = 1 | x)', 18, LIGHT).next_to(a_, UP, buff=0.1).align_to(a_, LEFT))
        self.play(Create(a_), FadeIn(lab), run_time=1)
        self.play(Create(a_.plot(sig, x_range=[-6, 6], color=B, stroke_width=4)), Create(DashedLine(a_.c2p(-6, 0.5), a_.c2p(6, 0.5), color=LIGHT, stroke_width=1.5)),
                  FadeIn(Dot(a_.c2p(0, 0.5), color=O, radius=0.09)), FadeIn(VT('ngưỡng quyết định z = 0', 18, O).next_to(a_.c2p(0, 0.5), DR, buff=0.15)), run_time=1.5)
        P1 = panel(M(r'\sigma(z)=\frac{1}{1+e^{-z}}\in(0,1)', 40)).move_to(RIGHT * 3.4 + UP * 2.0)
        self.play(FadeIn(P1), run_time=0.8); self.finish(10)
        self.line(11)
        self.play(FadeIn(VGroup(M(r'J(\mathbf{w})=-\sum_i\left[y_i\log p_i+(1-y_i)\log(1-p_i)\right]', 30), VT('entropy chéo — hàm lồi', 22, T)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + UP * 0.4)), run_time=1)
        self.finish(11)
        self.line(12)
        self.play(FadeIn(VGroup(M(r'\nabla J(\mathbf{w})=\mathbf{X}^{\top}(\mathbf{p}-\mathbf{y})', 38, O), VT('không có nghiệm dạng đóng', 22, R)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.4 + DOWN * 1.3)), run_time=1)
        self.finish(12); self.clear_body()

        # 13 — huấn luyện logistic
        self.section('Huấn luyện hồi quy logistic bằng giảm gradient'); self.line(13)
        XR_, YR_ = [-3.5, 3.5], [-3, 3.5]
        ax = axes([*XR_, 1], [*YR_, 1], 5.4, 5.0, LEFT * 3.6 + DOWN * 0.45, nums=False)
        it = ValueTracker(0)
        sq = [(XR_[0], YR_[0]), (XR_[1], YR_[0]), (XR_[1], YR_[1]), (XR_[0], YR_[1])]

        def board():
            w = WP[int(it.get_value())]; g = VGroup()
            for sgn, c in [(1, O), (-1, B)]:
                P = clip_poly(sq, -sgn * w[1:], sgn * w[0])
                if len(P) >= 3: g.add(Polygon(*[ax.c2p(*p) for p in P], color=c, fill_opacity=0.12, stroke_width=0))
            se = seg_in_box(w[1:], -w[0], XR_, YR_)
            if se is not None: g.add(Line(ax.c2p(*se[0]), ax.c2p(*se[1]), color=WHITE, stroke_width=4))
            return g
        bd = always_redraw(board)
        pts = VGroup(*[Dot(ax.c2p(*p), color=B, radius=0.05) for p in XA[:NA]], *[Dot(ax.c2p(*p), color=O, radius=0.05) for p in XA[NA:]])
        leg = VGroup(row('●', 'y = 0', size=18, color=B), row('●', 'y = 1', size=18, color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to(ax.c2p(2.7, -2.4))
        a2 = axes([0, len(LP), 20], [0, LP.max() * 1.1, 0.5], 4.6, 2.8, RIGHT * 3.4 + DOWN * 0.9, nums=False)
        a2l = VGroup(VT('vòng lặp', 18, LIGHT).next_to(a2, DOWN, buff=0.1), VT('entropy chéo (TB)', 18, LIGHT).next_to(a2, UP, buff=0.1).align_to(a2, LEFT))
        crv = always_redraw(lambda: VMobject(color=O, stroke_width=4).set_points_as_corners([a2.c2p(j, LP[j]) for j in range(int(it.get_value()) + 1)] if it.get_value() >= 1 else [a2.c2p(0, LP[0]), a2.c2p(0.01, LP[0])]))
        info = always_redraw(lambda: VGroup(VT(f'vòng lặp {int(it.get_value())}', 24), VT(f'độ chính xác huấn luyện: {vn(100 * np.mean((XA1 @ WP[int(it.get_value())] > 0) == (YA == 1)), 0)}%', 22, T))
                             .arrange(DOWN, buff=0.15).move_to(RIGHT * 3.4 + UP * 2.05))
        self.play(Create(ax), FadeIn(bd), FadeIn(pts), FadeIn(leg), Create(a2), FadeIn(a2l), FadeIn(crv), FadeIn(info), run_time=1.2)
        self.play(it.animate.set_value(len(LP) - 1), run_time=self.slots[13] - 2.2, rate_func=smooth)
        for m_ in (bd, crv, info): m_.clear_updaters()
        self.finish(13); self.clear_body()

        self.section('Tóm tắt'); self.line(14)
        lst = bullets(['Hồi quy tuyến tính: tuyến tính theo tham số w', 'Mở rộng đặc trưng ϕ(x): mô hình hóa quan hệ phi tuyến', 'Bậc thấp: dưới khớp · bậc cao: quá khớp',
                       'Ridge: nghiệm dạng đóng, hệ số nhỏ lại · LASSO: nghiệm thưa', 'Logistic: sigmoid + entropy chéo (lồi), giải bằng giảm gradient'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(14); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
