"""Bài 10 - Phân tích thành phần chính (Manim)."""
from common import *

rng = np.random.default_rng(3); N = 150
ang = np.deg2rad(32); RM = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
MU = np.array([3.2, 2.2])
X = (rng.normal(size=(N, 2)) * [1.7, 0.55]) @ RM.T + MU
Xc = X - X.mean(0); S = Xc.T @ Xc / N
LAM, Q = np.linalg.eigh(S); LAM, Q = LAM[::-1], Q[:, ::-1]
U1, U2 = Q[:, 0] * np.sign(Q[0, 0]), Q[:, 1] * np.sign(Q[1, 1])
TH1 = np.degrees(np.arctan2(U1[1], U1[0])) % 180
ud = lambda th: np.array([np.cos(np.radians(th)), np.sin(np.radians(th))])
var_th = lambda th: ud(th) @ S @ ud(th)
_, SIG, VTm = np.linalg.svd(Xc, full_matrices=False)
V1 = VTm[0] * np.sign(VTm[0, 0])
yy, xx = np.mgrid[0:10, 0:10]
IMG = np.clip(1.2 - np.abs(np.hypot(xx - 4.5, yy - 4.5) - 3.0), 0, 1)
RATIO = np.array([42, 24.5, 13.5, 8, 5, 3.5, 2, 1.5]); CUM = np.cumsum(RATIO)
r2 = np.random.default_rng(7); MM = 120
CA = np.c_[r2.normal(0, 2.0, MM), r2.normal(0.6, 0.25, MM)]; CB = np.c_[r2.normal(0, 2.0, MM), r2.normal(-0.6, 0.25, MM)]


class Bai(Lesson):
    LESSON = 'video_bai10'; LABEL = 'BÀI 10 · PHÂN TÍCH THÀNH PHẦN CHÍNH'; TEXTS = load_texts('video_bai10')
    MINS = {0: 5, 3: 8, 4: 5.5, 6: 10, 12: 7, 16: 7, 17: 9}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 10. Phân tích thành phần chính', 44, WHITE, BOLD),
                   M(r'\max_{\mathbf{u}}\ \mathbf{u}^{\top}\mathbf{S}\,\mathbf{u}\quad \text{v.đ.k.}\ \ \|\mathbf{u}\|_2=1', 50, O), VT('Chương 3 · Ứng dụng toán trong học máy', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–2 — vì sao giảm chiều
        self.section('Vì sao cần giảm chiều?'); self.line(1)
        c = 0.2; px = VGroup(*[Square(c, stroke_width=0.5, stroke_color=GRIDC, fill_color=interpolate_color(ManimColor(BG), ManimColor(WHITE), IMG[i, j] / 1.2), fill_opacity=1)
                               .move_to(LEFT * 4.3 + UP * 0.9 + RIGHT * c * (j - 4.5) + DOWN * c * (i - 4.5)) for i in range(10) for j in range(10)])
        self.play(FadeIn(px), FadeIn(VT('ảnh xám (minh họa 10×10)', 20, LIGHT).next_to(px, UP, buff=0.2)), run_time=1)
        tgt = VGroup(*[p.copy().scale(0.45).move_to(LEFT * 2.2 + UP * 1.15 + RIGHT * 0.088 * k) for k, p in enumerate(px)])
        self.play(FadeIn(VT('trải phẳng thành véc tơ', 20, LIGHT).move_to(RIGHT * 2.5 + UP * 1.65)), run_time=0.5)
        self.play(*[Transform(p.copy(), q) for p, q in zip(px, tgt)], run_time=2.5)
        self.play(FadeIn(row('ảnh', '$100\\times100$', '→', '$\\mathbf{x}\\in\\mathbb{R}^{10\\,000}$', size=28, color=O).move_to(RIGHT * 2.5 + UP * 0.3)), run_time=1)
        self.finish(1)
        self.line(2)
        probs = ['Chi phí tính toán lớn', 'Khó trực quan hóa', 'Dữ liệu thưa thớt → dễ quá khớp']
        bx = VGroup(*[panel(VT(p_, 22, O if k == 2 else INK), color=O if k == 2 else GRIDC) for k, p_ in enumerate(probs)]).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.9)
        self.play(LaggedStart(*[FadeIn(b_, shift=UP * 0.2) for b_ in bx], lag_ratio=0.8), run_time=4)
        self.finish(2); self.clear_body()

        # 3–7 — cực đại phương sai
        self.section('Tìm hướng giữ nhiều phương sai nhất'); self.line(3)
        XR, YR = [-5, 8], [-3.5, 5.5]
        ax = axes([*XR, 1], [*YR, 1], 6.5, 4.5, LEFT * 3.1 + DOWN * 0.4, nums=False)
        sc = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]
        dots = VGroup(*[Dot(ax.c2p(*p), color=LIGHT, radius=0.045) for p in X])
        ctr = Dot(ax.c2p(*X.mean(0)), color=B, radius=0.09)
        self.play(Create(ax), FadeIn(dots), FadeIn(ctr), FadeIn(VGroup(M('x_1', 26, LIGHT).next_to(ax.x_axis, RIGHT, buff=0.1), M('x_2', 26, LIGHT).next_to(ax.y_axis, UP, buff=0.1))), run_time=1.2)
        m0 = X.mean(0); pl = Line(ax.c2p(*(m0 - 4.5 * U1)), ax.c2p(*(m0 + 4.5 * U1)), color=O, stroke_width=3)
        proj = m0 + ((X - m0) @ U1)[:, None] * U1
        segs = VGroup(*[Line(ax.c2p(*p), ax.c2p(*q), color=O, stroke_width=1, stroke_opacity=0.5) for p, q in zip(X[::2], proj[::2])])
        pd = VGroup(*[Dot(ax.c2p(*q), color=O, radius=0.035) for q in proj])
        rt = VGroup(VT('Chiếu dữ liệu xuống', 28), VT('không gian con k chiều', 28), VT('→ giữ lại nhiều phương sai nhất', 24, O)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.6 + UP * 0.8)
        self.play(Create(pl), FadeIn(rt), run_time=1)
        self.play(Create(segs), FadeIn(pd), run_time=2.5)
        self.finish(3)
        self.line(4)
        self.play(FadeOut(VGroup(pl, segs, pd, rt)), run_time=0.5)
        self.play(dots.animate.shift(ax.c2p(0, 0) - ax.c2p(*m0)), ctr.animate.move_to(ax.c2p(0, 0)), run_time=2)
        cen = VGroup(M(r'\mathbf{x}_i\leftarrow\mathbf{x}_i-\bar{\mathbf{x}}', 40, B), VT('đưa tâm dữ liệu về gốc tọa độ', 24)).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.6 + UP * 0.8)
        self.play(FadeIn(cen), run_time=0.8)
        self.finish(4)

        self.line(5)
        self.play(FadeOut(cen), run_time=0.5)
        th = ValueTracker(0)

        def proj_view():
            u = ud(th.get_value()); z = Xc @ u; P = z[:, None] * u; g = VGroup()
            g.add(Line(ax.c2p(*(-5 * u)), ax.c2p(*(5 * u)), color=O, stroke_width=3))
            g.add(*[Line(ax.c2p(*p), ax.c2p(*q), color=O, stroke_width=0.8, stroke_opacity=0.4) for p, q in zip(Xc[::3], P[::3])])
            g.add(*[Dot(ax.c2p(*q), color=O, radius=0.03) for q in P])
            g.add(Arrow(ax.c2p(0, 0), ax.c2p(*(1.8 * u)), buff=0, color=WHITE, stroke_width=5), M(r'\mathbf{u}', 30, WHITE).move_to(ax.c2p(*(2.4 * u))))
            return g
        pv = always_redraw(proj_view)
        ia = axes([0, 180, 45], [0, LAM[0] * 1.15, 1], 4.6, 2.6, RIGHT * 3.6 + UP * 0.9, nums=True, fs=16)
        il = VGroup(VT('góc của u (độ)', 16, LIGHT).next_to(ia, DOWN, buff=0.08), M(r'\mathbf{u}^{\top}\mathbf{S}\mathbf{u}', 24, LIGHT).next_to(ia, UP, buff=0.05).align_to(ia, LEFT))
        tracer = always_redraw(lambda: VGroup(ia.plot(var_th, x_range=[0, max(0.5, min(th.get_value(), 180))], color=B, stroke_width=3),
                                              Dot(ia.c2p(th.get_value() % 180, var_th(th.get_value())), color=O, radius=0.08)))
        vt = always_redraw(lambda: VT(f'phương sai = {vn(var_th(th.get_value()))}', 26, O).move_to(RIGHT * 3.6 + DOWN * 1.1))
        self.play(FadeIn(pv), Create(ia), FadeIn(il), FadeIn(tracer), FadeIn(vt), run_time=1.2)
        self.play(Indicate(vt, color=O, scale_factor=1.05), run_time=1)
        self.finish(5)
        self.line(6)
        self.play(th.animate.set_value(180), run_time=self.slots[6] - 1.5, rate_func=smooth)
        self.finish(6)
        self.line(7)
        tracer.clear_updaters(); self.remove(tracer); full = VGroup(ia.plot(var_th, x_range=[0, 180], color=B, stroke_width=3)); self.add(full)
        dt = always_redraw(lambda: Dot(ia.c2p(th.get_value() % 180 if th.get_value() < 180 else th.get_value() - 180, var_th(th.get_value())), color=O, radius=0.08)); self.add(dt)
        self.play(th.animate.set_value(180 + TH1), Create(DashedLine(ia.c2p(0, LAM[0]), ia.c2p(180, LAM[0]), color=T, stroke_width=1.5)),
                  Create(DashedLine(ia.c2p(0, LAM[1]), ia.c2p(180, LAM[1]), color=LIGHT, stroke_width=1.5)), run_time=2.5)
        self.play(FadeIn(M(r'\lambda_{\max}', 24, T).next_to(ia.c2p(180, LAM[0]), RIGHT, buff=0.1)), FadeIn(M(r'\lambda_{\min}', 24, LIGHT).next_to(ia.c2p(180, LAM[1]), RIGHT, buff=0.1)),
                  FadeIn(panel(M(r'\max_{\mathbf{u}}\ \mathbf{u}^{\top}\mathbf{S}\mathbf{u}\ \ \text{v.đ.k.}\ \|\mathbf{u}\|_2=1', 30)).move_to(RIGHT * 3.6 + DOWN * 2.1)), run_time=1)
        for m_ in (pv, dt, vt): m_.clear_updaters()
        self.finish(7); self.clear_body()

        # 8–9 — véc tơ riêng
        self.section('Lời giải: véc tơ riêng của ma trận hiệp phương sai'); self.line(8)
        ax = axes([-4.6, 4.6, 1], [-3, 3, 1], 6.4, 4.2, LEFT * 3.3 + DOWN * 0.45, nums=False)
        self.play(Create(ax), FadeIn(VGroup(*[Dot(ax.c2p(*p), color=LIGHT, radius=0.045) for p in Xc])), run_time=1)
        a1 = Arrow(ax.c2p(0, 0), ax.c2p(*(2 * np.sqrt(LAM[0]) * U1)), buff=0, color=O, stroke_width=6); a2_ = Arrow(ax.c2p(0, 0), ax.c2p(*(2 * np.sqrt(LAM[1]) * U2)), buff=0, color=T, stroke_width=6)
        self.play(GrowArrow(a1), GrowArrow(a2_), FadeIn(M(r'\mathbf{u}_1', 32, O).next_to(a1.get_end(), RIGHT, buff=0.1)), FadeIn(M(r'\mathbf{u}_2', 32, T).next_to(a2_.get_end(), UP, buff=0.1)), run_time=1.5)
        rr = VGroup(panel(M(r'L=\mathbf{u}^{\top}\mathbf{S}\mathbf{u}-\lambda(\mathbf{u}^{\top}\mathbf{u}-1)', 32)), M(r'\nabla_{\mathbf{u}}L=0\ \ \Rightarrow\ \ \mathbf{S}\mathbf{u}=\lambda\mathbf{u}', 36),
                    M(r'\mathbf{u}^{\top}\mathbf{S}\mathbf{u}=\lambda\,\mathbf{u}^{\top}\mathbf{u}=\lambda', 34), VT(f'λ₁ = {vn(LAM[0])}     λ₂ = {vn(LAM[1])}', 24, LIGHT)).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.5 + UP * 0.7)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rr], lag_ratio=0.7), run_time=5)
        self.finish(8)
        self.line(9)
        self.play(FadeIn(VGroup(VT('Thành phần chính thứ nhất:', 26, O, BOLD), VT('véc tơ riêng của λ lớn nhất', 26, O, BOLD)).arrange(DOWN, buff=0.15).move_to(RIGHT * 3.5 + DOWN * 1.8)), Indicate(a1, color=O), run_time=1.5)
        self.finish(9); self.clear_body()

        # 10–12 — thuật toán
        self.section('Thuật toán PCA'); self.line(10)
        ax = axes([-4.6, 4.6, 1], [-3, 3, 1], 5.6, 3.7, LEFT * 3.7 + DOWN * 0.45, nums=False)
        dd = VGroup(*[Dot(ax.c2p(*p), color=B, radius=0.04) for p in Xc])
        self.play(Create(ax), FadeIn(dd), Create(Line(ax.c2p(*(-4.5 * U1)), ax.c2p(*(4.5 * U1)), color=O, stroke_width=2, stroke_opacity=0.7)),
                  GrowArrow(Arrow(ax.c2p(0, 0), ax.c2p(*(2 * np.sqrt(LAM[0]) * U1)), buff=0, color=O, stroke_width=5)), GrowArrow(Arrow(ax.c2p(0, 0), ax.c2p(*(2 * np.sqrt(LAM[1]) * U2)), buff=0, color=T, stroke_width=5)), run_time=1)
        steps = [row('1. Trừ trung bình (chuẩn hóa nếu khác đơn vị)', size=22), row('2.', '$\\mathbf{S}=\\frac{1}{n}\\mathbf{X}_c^{\\top}\\mathbf{X}_c$', '(d×d, đối xứng, nửa xđd)', size=22),
                 row('3.', '$\\mathbf{S}=\\mathbf{Q}\\Lambda\\mathbf{Q}^{\\top}$,', 'sắp', '$\\lambda_1\\geq\\dots\\geq\\lambda_d$', size=22), row('4. Lấy', '$\\mathbf{U}_k=[\\mathbf{u}_1\\cdots\\mathbf{u}_k]$', size=22),
                 row('5. Chiếu', '$\\mathbf{Z}=\\mathbf{X}_c\\mathbf{U}_k$;', 'khôi phục', '$\\hat{\\mathbf{X}}_c=\\mathbf{Z}\\mathbf{U}_k^{\\top}$', size=22)]
        G = VGroup(*steps).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(LEFT * 0.5 + UP * 0.5, aligned_edge=LEFT)
        for s_ in G: s_.set_opacity(0.3)
        self.add(G)
        cur = [None]

        def hl(i, rt=0.6):
            anims = [G[i].animate.set_opacity(1).set_color(O)]
            if cur[0] is not None: anims.append(G[cur[0]].animate.set_color(INK))
            cur[0] = i; self.play(*anims, run_time=rt)
        for i in range(3): hl(i); self.wait(self.slots[10] / 3 - 1.0)
        self.finish(10)
        self.line(11)
        for i in range(3, 5): hl(i); self.wait(self.slots[11] / 2 - 1.0)
        self.finish(11)
        self.line(12)
        G[cur[0]].set_color(INK)
        rec = (Xc @ U1)[:, None] * U1
        self.play(*[d_.animate.move_to(ax.c2p(*q)).set_color(O) for d_, q in zip(dd, rec)], run_time=3)
        self.play(FadeIn(VT(f'k = 1: giữ {vn(100 * LAM[0] / LAM.sum(), 1)}% phương sai', 26, O).move_to(RIGHT * 2.9 + DOWN * 2.3)), run_time=0.8)
        self.finish(12); self.clear_body()

        # 13 — SVD
        self.section('Tính PCA qua phân rã SVD'); self.line(13)
        P1 = panel(M(r'\mathbf{X}_c=\mathbf{U}\Sigma\mathbf{V}^{\top}\ \Rightarrow\ \mathbf{S}=\frac{1}{n}\mathbf{X}_c^{\top}\mathbf{X}_c=\mathbf{V}\,\frac{\Sigma^2}{n}\,\mathbf{V}^{\top}', 42)).move_to(UP * 1.9)
        self.play(FadeIn(P1), run_time=1)
        rows = [('', 'Phân rã phổ của S', 'SVD của Xc'), ('λ₁', vn(LAM[0], 4), vn(SIG[0] ** 2 / N, 4)), ('λ₂', vn(LAM[1], 4), vn(SIG[1] ** 2 / N, 4)),
                ('u₁', f'({vn(U1[0], 3)}; {vn(U1[1], 3)})', f'({vn(V1[0], 3)}; {vn(V1[1], 3)})')]
        tb = VGroup(VT('Kiểm tra trên dữ liệu minh họa (n = 150):', 22, LIGHT).move_to(UP * 0.75))
        for r_, rw in enumerate(rows):
            tb.add(VGroup(*[VT(s_, 24, B if r_ == 0 else INK, BOLD if r_ == 0 else NORMAL).move_to([x, 0.05 - 0.55 * r_, 0]) for x, s_ in zip([-3.4, -0.6, 2.8], rw)]))
        self.play(FadeIn(tb[0]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(r_) for r_ in tb[1:]], lag_ratio=0.7), run_time=4)
        self.play(FadeIn(VT('Không cần lập S tường minh → chính xác hơn về số học, nhanh hơn khi d lớn', 22, T).move_to(DOWN * 2.35)), run_time=0.8)
        self.finish(13); self.clear_body()

        # 14–16 — chọn k
        self.section('Chọn số thành phần chính k'); self.line(14)
        ax = axes([0, 9, 1], [0, 108, 20], 6.6, 4.4, LEFT * 3.0 + DOWN * 0.4, nums=True, fs=16)
        lab = VGroup(VT('thành phần chính', 18, LIGHT).next_to(ax, DOWN, buff=0.1), VT('% phương sai', 18, LIGHT).next_to(ax, UP, buff=0.05).align_to(ax, LEFT))
        bars = VGroup(*[Rectangle(width=0.6 * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), height=ax.c2p(0, v)[1] - ax.c2p(0, 0)[1], color=B, fill_opacity=0.85, stroke_width=0)
                        .move_to(ax.c2p(k + 1, 0), aligned_edge=DOWN) for k, v in enumerate(RATIO)])
        cum = VMobject(color=O, stroke_width=4).set_points_as_corners([ax.c2p(k + 1, v) for k, v in enumerate(CUM)])
        cdots = VGroup(*[Dot(ax.c2p(k + 1, v), color=O, radius=0.06) for k, v in enumerate(CUM)])
        P1 = panel(M(r'\rho_k=\frac{\lambda_1+\cdots+\lambda_k}{\lambda_1+\cdots+\lambda_d}', 42)).move_to(RIGHT * 3.7 + UP * 1.7)
        leg = VGroup(row('■', 'từng thành phần', size=20, color=B), row('●', 'tích lũy ρₖ', size=20, color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ax.c2p(6.8, 45))
        self.play(Create(ax), FadeIn(lab), FadeIn(P1), run_time=1)
        self.play(LaggedStart(*[GrowFromEdge(b_, DOWN) for b_ in bars], lag_ratio=0.25), Create(cum), LaggedStart(*[FadeIn(d_) for d_ in cdots], lag_ratio=0.25), FadeIn(leg), run_time=3.5)
        self.finish(14)
        self.line(15)
        self.play(Create(DashedLine(ax.c2p(0, 90), ax.c2p(9, 90), color=WHITE, stroke_width=2)), Create(DashedLine(ax.c2p(0, 95), ax.c2p(9, 95), color=LIGHT, stroke_width=1.5)),
                  FadeIn(VT('ngưỡng 90%', 16).next_to(ax.c2p(0.1, 90), DR, buff=0.05)), FadeIn(VT('95%', 15, LIGHT).next_to(ax.c2p(0.1, 95), UR, buff=0.05)), run_time=1.2)
        self.play(FadeIn(VGroup(VT('k nhỏ nhất với ρₖ ≥ ngưỡng', 24), VT('hoặc điểm gãy của đồ thị', 24)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.7 + UP * 0.0)), run_time=1)
        self.finish(15)
        self.line(16)
        for kk, col in [(4, LIGHT), (5, T)]:
            self.play(Create(Circle(radius=0.2, color=col, stroke_width=4).move_to(ax.c2p(kk, CUM[kk - 1]))),
                      FadeIn(VT(f'k={kk}: {vn(CUM[kk - 1], 0)}%', 18, col, BOLD).next_to(ax.c2p(kk, CUM[kk - 1]), DR, buff=0.2)), run_time=1)
            self.wait(0.5)
        self.play(FadeIn(VT('Ngưỡng 90%  →  k = 5', 28, T, BOLD).move_to(RIGHT * 3.7 + DOWN * 1.4)), run_time=0.8)
        self.finish(16); self.clear_body()

        # 17–18 — lưu ý
        self.section('Lưu ý khi áp dụng PCA'); self.line(17)
        ax = axes([-6, 6, 2], [-3, 3, 1], 6.0, 3.0, LEFT * 3.4 + DOWN * 0.2, nums=False)
        pts = VGroup(*[Dot(ax.c2p(*p), color=B, radius=0.04) for p in CA], *[Dot(ax.c2p(*p), color=O, radius=0.04) for p in CB])
        leg = VGroup(row('●', 'lớp A', size=18, color=B), row('●', 'lớp B', size=18, color=O)).arrange(RIGHT, buff=0.4).next_to(ax, DOWN, buff=0.25)
        self.play(Create(ax), FadeIn(pts), FadeIn(leg), GrowArrow(Arrow(ax.c2p(0, 0), ax.c2p(4, 0), buff=0, color=WHITE, stroke_width=5)), GrowArrow(Arrow(ax.c2p(0, 0), ax.c2p(0, 1.6), buff=0, color=T, stroke_width=5)),
                  FadeIn(VT('PC1', 20).next_to(ax.c2p(4, 0), UP, buff=0.1)), FadeIn(VT('PC2', 20, T).next_to(ax.c2p(0, 1.6), RIGHT, buff=0.1)), run_time=1.5)
        for j, (dim, lab_, col) in enumerate([(0, 'chiếu lên PC1: hai lớp chồng lấn', WHITE), (1, 'chiếu lên PC2: hai lớp tách rời', T)]):
            bins = np.linspace(-6, 6, 31) if dim == 0 else np.linspace(-1.6, 1.6, 31)
            hA, _ = np.histogram(CA[:, dim], bins); hB, _ = np.histogram(CB[:, dim], bins); hm = max(hA.max(), hB.max())
            ha = axes([bins[0], bins[-1], (bins[-1] - bins[0]) / 4], [0, hm, hm], 4.6, 1.3, RIGHT * 3.6 + UP * (1.0 - 2.1 * j), nums=False)
            bw = (ha.c2p(bins[1], 0)[0] - ha.c2p(bins[0], 0)[0])
            hist = VGroup(*[Rectangle(width=bw, height=max(1e-3, ha.c2p(0, h)[1] - ha.c2p(0, 0)[1]), fill_color=c_, fill_opacity=0.55, stroke_width=0).move_to(ha.c2p((bins[i] + bins[i + 1]) / 2, 0), aligned_edge=DOWN)
                            for hh, c_ in [(hA, B), (hB, O)] for i, h in enumerate(hh)])
            self.play(Create(ha), FadeIn(hist), FadeIn(VT(lab_, 20, col).next_to(ha, UP, buff=0.1)), run_time=1.2); self.wait(0.6)
        self.finish(17); self.clear_body()
        self.line(18)
        items = [('•  Chuẩn hóa z-score khi các đặc trưng khác đơn vị đo', INK), ('•  Ước lượng trung bình, độ lệch chuẩn và Uₖ chỉ trên tập huấn luyện', INK),
                 ('•  Áp dụng đúng phép biến đổi đó cho tập kiểm tra', INK), ('⚠  Nếu ước lượng trên toàn bộ dữ liệu → rò rỉ dữ liệu', O)]
        lst = VGroup(*[VT(s_, 26, c_) for s_, c_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in lst], lag_ratio=0.8), run_time=5.5)
        self.finish(18); self.clear_body()

        self.section('Tóm tắt'); self.line(19)
        lst = bullets(['PCA tìm không gian con giữ nhiều phương sai nhất', 'Thành phần chính = véc tơ riêng của S, sắp theo λ giảm dần', 'Dẫn dắt từ thương Rayleigh và nhân tử Lagrange',
                       'Chọn k theo tỉ lệ phương sai tích lũy hoặc điểm gãy', 'Không giám sát, nhạy với thang đo, chỉ nắm bắt quan hệ tuyến tính'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=self.slots[19] - 1)
        self.finish(19); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
