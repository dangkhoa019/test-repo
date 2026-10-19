"""Bài 2 - Không gian véc tơ, ánh xạ tuyến tính và chuẩn (Manim)."""
from common import *


def plane(xr, yr, w, h, pos):
    return NumberPlane(x_range=xr, y_range=yr, x_length=w, y_length=h, background_line_style={'stroke_color': GRIDC}).move_to(pos)


def unit_ball(pl, p, color, width=4):
    t = np.linspace(0, 2 * np.pi, 400); c, s = np.cos(t), np.sin(t)
    r = 1 / np.maximum(abs(c), abs(s)) if np.isinf(p) else 1 / (abs(c) ** p + abs(s) ** p) ** (1 / p)
    return VMobject(color=color, stroke_width=width).set_points_smoothly([pl.c2p(a, b) for a, b in zip(r * c, r * s)])


class Bai(Lesson):
    LESSON = 'video_bai02'; LABEL = 'BÀI 2 · KHÔNG GIAN VÉC TƠ, ÁNH XẠ TUYẾN TÍNH VÀ CHUẨN'; TEXTS = load_texts('video_bai02')

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 2. Không gian véc tơ và chuẩn', 46, WHITE, BOLD),
                   M(r'\|\mathbf{x}\|_p=\Big(\sum_i |x_i|^p\Big)^{1/p}', 54, O), VT('Chương 1 · Một số kiến thức cơ bản', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1 — không gian véc tơ
        self.section('Không gian véc tơ'); self.line(1)
        ax_ = VGroup(VT('Tám tiên đề: giao hoán, kết hợp, phần tử 0, phần tử đối,', 22, LIGHT), VT('1·x = x, (αβ)x = α(βx), hai luật phân phối', 22, LIGHT)).arrange(DOWN).shift(UP * 1.9)
        ex = VGroup(row('•', '$\\mathbb{R}^n$'), row('•', 'tập ma trận cùng cỡ', '$\\mathbb{R}^{m\\times n}$'), row('•', 'tập đa thức bậc ≤ k'),
                    row('•', 'tập hàm liên tục trên một đoạn')).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.4 + LEFT * 2)
        self.play(FadeIn(ax_)); self.play(LaggedStart(*[FadeIn(e, shift=RIGHT * 0.3) for e in ex], lag_ratio=0.7), run_time=5)
        self.finish(1); self.clear_body()

        # 2–3 — không gian con
        self.section('Không gian con'); self.line(2)
        pl = plane([-3, 3, 1], [-2.5, 3.5, 1], 5.6, 5.6, LEFT * 3.3 + DOWN * 0.45)
        S1 = pl.plot_line_graph([-1.5, 1.75], [-3, 3.5], add_vertex_dots=False, line_color=T, stroke_width=5)
        lab1 = M(r'S_1:\ x_2=2x_1', 32, T).move_to(pl.c2p(1.6, -1.8))
        self.play(Create(pl), Create(S1), FadeIn(lab1), FadeIn(Dot(pl.c2p(0, 0), color=WHITE)))
        u, v = np.array([0.5, 1.0]), np.array([0.8, 1.6])
        au, av = Arrow(pl.c2p(0, 0), pl.c2p(*u), buff=0, color=B), Arrow(pl.c2p(0, 0), pl.c2p(*v), buff=0, color=O)
        self.play(GrowArrow(au), GrowArrow(av))
        sm = Arrow(pl.c2p(0, 0), pl.c2p(*(u + v)), buff=0, color=WHITE); self.play(GrowArrow(sm), FadeIn(M(r'\mathbf{u}+\mathbf{v}\in S_1', 28).next_to(sm.get_end(), RIGHT)))
        neg = Arrow(pl.c2p(0, 0), pl.c2p(*(-1.6 * u)), buff=0, color=LIGHT); self.play(GrowArrow(neg), FadeIn(M(r'-1{,}6\,\mathbf{u}\in S_1', 26, LIGHT).next_to(neg.get_end(), LEFT)))
        ch = VGroup(row('$\\mathbf{0}\\in S_1$', '✓', color=T), VT('khép kín với phép cộng  ✓', 26, T), VT('khép kín với nhân vô hướng  ✓', 26, T),
                    VT('→ đường thẳng qua gốc', 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 3.4 + UP * 0.6)
        self.play(LaggedStart(*[FadeIn(c) for c in ch], lag_ratio=0.5), run_time=2.5); self.finish(2)
        self.line(3)
        self.play(FadeOut(ch), FadeOut(sm), FadeOut(neg), FadeOut(au), FadeOut(av), *[FadeOut(m) for m in self.mobjects if isinstance(m, MathTex) and m is not lab1])
        S2 = pl.plot_line_graph([-1.75, 1.25], [-2.5, 3.5], add_vertex_dots=False, line_color=O, stroke_width=5)
        self.play(Create(S2), FadeIn(M(r'S_2:\ x_2=2x_1+1', 30, O).move_to(pl.c2p(-1.9, -0.9))))
        p1, p2 = np.array([0.0, 1.0]), np.array([0.5, 2.0])
        self.play(FadeIn(Dot(pl.c2p(*p1), color=O)), FadeIn(Dot(pl.c2p(*p2), color=O)))
        bad = Arrow(pl.c2p(0, 0), pl.c2p(*(p1 + p2)), buff=0, color=R)
        self.play(GrowArrow(bad), FadeIn(M(r'\mathbf{u}+\mathbf{v}\notin S_2', 28, R).next_to(bad.get_end(), RIGHT)))
        ch2 = VGroup(row('$\\mathbf{0}\\notin S_2$', '✗', color=R), VT('Trong ℝ², không gian con chỉ có thể là:', 24), VT('{0}, một đường thẳng qua gốc, hoặc ℝ²', 24, B)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 3.4 + UP * 0.5)
        self.play(FadeIn(ch2)); self.finish(3); self.clear_body()

        # 4 — độc lập tuyến tính và cơ sở
        self.section('Độc lập tuyến tính và cơ sở'); self.line(4)
        v1 = np.array([1.0, 0.4])
        pls, dots = VGroup(), []
        for k, (w2, title, col) in enumerate([(np.array([0.3, 1.0]), 'v₁, v₂ độc lập → sinh cả ℝ²', T), (2 * v1, 'v₂ = 2v₁: phụ thuộc → một đường', O)]):
            pl = plane([-3, 3, 1], [-3, 3, 1], 4.2, 4.2, (LEFT if k == 0 else RIGHT) * 3.4 + DOWN * 0.95)
            pts = [a * v1 + b * w2 for a in np.linspace(-2, 2, 9) for b in np.linspace(-2, 2, 9)]
            g = VGroup(*[Dot(pl.c2p(*p_), radius=0.04, color=col) for p_ in pts if abs(p_[0]) <= 3 and abs(p_[1]) <= 3])
            pls.add(VGroup(pl, VT(title, 21, col).next_to(pl, UP, buff=0.1))); dots.append((pl, g, w2))
        self.play(FadeIn(pls))
        for pl, g, w2 in dots: self.play(GrowArrow(Arrow(pl.c2p(0, 0), pl.c2p(*v1), buff=0, color=B)), GrowArrow(Arrow(pl.c2p(0, 0), pl.c2p(*w2), buff=0, color=WHITE)), run_time=0.6)
        self.play(*[LaggedStart(*[FadeIn(d) for d in g], lag_ratio=0.01) for _, g, _ in dots], run_time=3)
        self.play(FadeIn(panel(M(r'\alpha_1\mathbf{v}_1+\dots+\alpha_k\mathbf{v}_k=\mathbf{0}\ \Rightarrow\ \alpha_i=0', 30), buff=0.15).move_to(UP * 2.3 + RIGHT * 2.6)))
        self.finish(4); self.clear_body()

        # 5 — số chiều, đa cộng tuyến
        self.section('Số chiều và đa cộng tuyến'); self.line(5)
        r = np.random.default_rng(4); h = r.normal(1.65, 0.08, 40); hc = 100 * h + r.normal(0, 0.3, 40)
        ax = Axes(x_range=[1.4, 1.9, 0.1], y_range=[140, 190, 10], x_length=5.5, y_length=4.4, axis_config={'color': LIGHT, 'include_numbers': True, 'font_size': 18}).shift(LEFT * 3.4 + DOWN * 0.5)
        labs = VGroup(VT('chiều cao (m)', 18, LIGHT).next_to(ax, DOWN, buff=0.1), VT('chiều cao (cm)', 18, LIGHT).rotate(PI / 2).next_to(ax, LEFT, buff=0.1))
        self.play(Create(ax), FadeIn(labs), LaggedStart(*[FadeIn(Dot(ax.c2p(a, b), radius=0.05, color=B)) for a, b in zip(h, hc)], lag_ratio=0.03), run_time=2.5)
        X = np.c_[np.ones(40), h, hc]; c = np.linalg.cond(X.T @ X); e = int(np.floor(np.log10(c)))
        txt = VGroup(row('$\\dim\\mathbb{R}^n=n$', '(cơ sở chính tắc', '$\\mathbf{e}_1,\\dots,\\mathbf{e}_n$', ')'), VT('Hai cột gần như tỉ lệ (m và cm):', 24),
                     row('số điều kiện của', '$\\mathbf{X}^\\top\\mathbf{X}\\approx ' + vn(c / 10 ** e, 1) + r'\cdot 10^{' + str(e) + '}$', color=O),
                     VT('→ XᵀX gần suy biến, nghiệm nhạy với nhiễu', 22, LIGHT), VT('→ khắc phục: điều chuẩn (Bài 8)', 22, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.33).scale(0.92).shift(RIGHT * 3.1 + UP * 0.2)
        self.play(LaggedStart(*[FadeIn(x_) for x_ in txt], lag_ratio=0.6), run_time=4); self.finish(5); self.clear_body()

        # 6 — ánh xạ tuyến tính: lưới biến dạng
        self.section('Ánh xạ tuyến tính = ma trận'); self.line(6)
        A = np.array([[1.2, 0.6], [0.3, 1.1]])
        bg = plane([-4, 4, 1], [-3, 3, 1], 6.4, 4.8, LEFT * 3.1 + DOWN * 0.45).set_opacity(0.35)
        gr = NumberPlane(x_range=[-4, 4, 1], y_range=[-3, 3, 1], x_length=6.4, y_length=4.8, background_line_style={'stroke_color': B, 'stroke_opacity': 0.6}, axis_config={'stroke_color': B}).move_to(bg)
        e1 = Arrow(gr.c2p(0, 0), gr.c2p(1, 0), buff=0, color=O); e2 = Arrow(gr.c2p(0, 0), gr.c2p(0, 1), buff=0, color=T)
        self.add(bg); self.play(Create(gr), GrowArrow(e1), GrowArrow(e2), run_time=1.2)
        side = VGroup(panel(M(r'\mathbf{A}=\big[\,T(\mathbf{e}_1)\ \ T(\mathbf{e}_2)\,\big]', 36)), M(r'\mathbf{A}=\begin{bmatrix}1{,}2&0{,}6\\0{,}3&1{,}1\end{bmatrix}', 36),
                      VT('đường thẳng → đường thẳng', 24), VT('gốc tọa độ giữ nguyên', 24)).arrange(DOWN, buff=0.35).shift(RIGHT * 3.6 + UP * 0.2)
        self.play(FadeIn(side[:2]))
        o = gr.c2p(0, 0); M3 = np.eye(3); M3[:2, :2] = A
        self.play(ApplyMatrix(M3, VGroup(gr, e1, e2), about_point=o), run_time=3)
        self.play(FadeIn(side[2:])); self.finish(6); self.clear_body()

        # 7 — hạng và không gian nghiệm
        self.section('Không gian nghiệm và định lý hạng – số chiều'); self.line(7)
        A = np.array([[1.0, 2.0], [0.5, 1.0]])
        gr = plane([-3, 3, 1], [-2.5, 2.5, 1], 5.8, 4.8, LEFT * 3.3 + DOWN * 0.45)
        tt = np.linspace(-1.2, 1.2, 9); nd = VGroup(*[Dot(gr.c2p(2 * t_, -t_), color=O, radius=0.07) for t_ in tt])
        nl = DashedLine(gr.c2p(-2.4, 1.2), gr.c2p(2.4, -1.2), color=O)
        self.play(Create(gr), Create(nl), FadeIn(nd))
        info = VGroup(M(r'\mathbf{A}=\begin{bmatrix}1&2\\0{,}5&1\end{bmatrix},\ \det\mathbf{A}=0', 34), row('null(A) = span{(2, −1)} → bị ép về 0', size=24, color=O),
                      row('col(A): một đường thẳng', size=24, color=T), panel(M(r'\dim\mathrm{null}(\mathbf{A})+\operatorname{rank}\mathbf{A}=n', 36)), M('1+1=2', 36)).arrange(DOWN, buff=0.33).shift(RIGHT * 3.5 + UP * 0.1)
        self.play(FadeIn(info[0]))
        M3 = np.eye(3); M3[:2, :2] = A
        col = Line(gr.c2p(-3, -1.5), gr.c2p(3, 1.5), color=T, stroke_width=5)
        self.play(ApplyMatrix(M3, VGroup(nd, nl), about_point=gr.c2p(0, 0)), Create(col), run_time=3)
        self.play(LaggedStart(*[FadeIn(i_) for i_ in info[1:]], lag_ratio=0.6), run_time=3); self.finish(7); self.clear_body()

        # 8 — tích vô hướng, góc
        self.section('Tích vô hướng, độ dài và góc'); self.line(8)
        gr = plane([-2, 3, 1], [-0.5, 2.5, 1], 6, 3.6, LEFT * 3.2 + DOWN * 0.3)
        th = ValueTracker(np.radians(25)); x = np.array([2.1, 0.65])
        yv = lambda: 1.8 * np.array([np.cos(th.get_value()), np.sin(th.get_value())])
        ax_ = Arrow(gr.c2p(0, 0), gr.c2p(*x), buff=0, color=B)
        ay = always_redraw(lambda: Arrow(gr.c2p(0, 0), gr.c2p(*yv()), buff=0, color=O))
        arc = always_redraw(lambda: Arc(radius=0.6, start_angle=np.arctan2(x[1], x[0]), angle=th.get_value() - np.arctan2(x[1], x[0]), arc_center=gr.c2p(0, 0), color=WHITE))
        cosv = always_redraw(lambda: VT(f'cos θ = {vn(x @ yv() / np.linalg.norm(x) / np.linalg.norm(yv()))}', 30, O).shift(RIGHT * 3.6 + UP * 0.1))
        f = VGroup(panel(M(r'\cos\theta=\frac{\langle\mathbf{x},\mathbf{y}\rangle}{\|\mathbf{x}\|_2\,\|\mathbf{y}\|_2}', 40)).shift(RIGHT * 3.6 + UP * 1.5),
                   VT('cos θ = 0 ⇔ x vuông góc y', 22, LIGHT).shift(RIGHT * 3.6 + DOWN * 0.8), M(r'|\langle\mathbf{x},\mathbf{y}\rangle|\leq\|\mathbf{x}\|_2\|\mathbf{y}\|_2', 32, LIGHT).shift(RIGHT * 3.6 + DOWN * 1.5))
        self.play(Create(gr), GrowArrow(ax_), FadeIn(ay), FadeIn(arc), FadeIn(f), FadeIn(cosv))
        self.play(th.animate.set_value(np.radians(120)), run_time=5, rate_func=there_and_back_with_pause)
        self.finish(8); self.remove(ay, arc, cosv); self.clear_body()

        # 9 — hình chiếu trực giao
        self.section('Hình chiếu trực giao'); self.line(9)
        gr = plane([-0.5, 3.2, 1], [-0.4, 2.4, 1], 6.2, 4.6, LEFT * 3.1 + DOWN * 0.4)
        u, y = np.array([2.6, 0.9]), np.array([1.2, 2.0]); p = (y @ u) / (u @ u) * u
        self.play(Create(gr), GrowArrow(Arrow(gr.c2p(0, 0), gr.c2p(*u), buff=0, color=B)), GrowArrow(Arrow(gr.c2p(0, 0), gr.c2p(*y), buff=0, color=WHITE)),
                  FadeIn(M(r'\mathbf{u}', 32, B).move_to(gr.c2p(*(u + [0.15, -0.25])))), FadeIn(M(r'\mathbf{y}', 32).move_to(gr.c2p(*(y + [0.1, 0.15])))))
        self.play(FadeIn(panel(M(r'\mathrm{proj}_{\mathbf{u}}\mathbf{y}=\frac{\langle\mathbf{y},\mathbf{u}\rangle}{\langle\mathbf{u},\mathbf{u}\rangle}\,\mathbf{u}', 40)).shift(RIGHT * 3.6 + UP * 1.2)))
        dl = DashedLine(gr.c2p(*y), gr.c2p(*p), color=O); self.play(Create(dl), run_time=1.5)
        pa = Arrow(gr.c2p(0, 0), gr.c2p(*p), buff=0, color=O, stroke_width=7)
        ra = RightAngle(Line(gr.c2p(*p), gr.c2p(*y)), Line(gr.c2p(*p), gr.c2p(*(p + u))), length=0.22, color=WHITE)
        self.play(GrowArrow(pa), Create(ra), FadeIn(M(r'\mathrm{proj}_{\mathbf{u}}\mathbf{y}', 30, O).move_to(gr.c2p(*(p + [0.1, -0.35])))))
        self.play(FadeIn(VGroup(VT('phần dư y − proj vuông góc với u', 24), VT('→ điểm gần y nhất trên đường thẳng', 24, T)).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.6 + DOWN * 0.6)))
        self.finish(9); self.clear_body()

        # 10–11 — chuẩn lp
        self.section('Các chuẩn ℓ₁, ℓ₂, ℓ∞ và hình cầu đơn vị'); self.line(10)
        gr = plane([-1.6, 1.6, 0.5], [-1.3, 1.3, 0.5], 5.6, 4.55, LEFT * 3.3 + DOWN * 0.45)
        pt = ValueTracker(1.0)
        ghost = VGroup(*[unit_ball(gr, q, c, 1.5).set_stroke(opacity=0.35) for q, c in [(1, B), (2, O), (np.inf, T)]])
        ball = always_redraw(lambda: unit_ball(gr, pt.get_value() if pt.get_value() < 30 else np.inf, WHITE, 5))
        ptxt = always_redraw(lambda: VT('p = ∞' if pt.get_value() >= 30 else f'p = {vn(pt.get_value(), 1)}', 40).shift(RIGHT * 3.5 + UP * 0.1))
        self.play(Create(gr), FadeIn(ghost), FadeIn(ball), FadeIn(ptxt), FadeIn(panel(M(r'\|\mathbf{x}\|_p=\Big(\sum_i|x_i|^p\Big)^{1/p}', 38)).shift(RIGHT * 3.5 + UP * 1.6)),
                  FadeIn(M(r'\|\mathbf{x}\|_\infty=\max_i|x_i|', 36, T).shift(RIGHT * 3.5 + DOWN * 1.2)))
        self.play(pt.animate.set_value(2), run_time=2.5); self.play(pt.animate.set_value(8), run_time=2.5); self.play(pt.animate.set_value(40), run_time=1)
        self.finish(10); self.remove(ball, ptxt)
        self.line(11)
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (self.header, gr, ghost)], run_time=0.5)
        self.play(*[g.animate.set_stroke(opacity=1, width=4) for g in ghost])
        vals = VGroup(M(r'\mathbf{x}=(3,-4)', 40), M(r'\|\mathbf{x}\|_1=|3|+|-4|=7', 36, B), M(r'\|\mathbf{x}\|_2=\sqrt{9+16}=5', 36, O), M(r'\|\mathbf{x}\|_\infty=\max(3,4)=4', 36, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 3.4 + UP * 0.3)
        self.play(LaggedStart(*[FadeIn(v_, shift=LEFT * 0.2) for v_ in vals], lag_ratio=0.8), run_time=4); self.finish(11); self.clear_body()

        # 12 — vì sao ℓ1 cho nghiệm thưa
        self.section('Vì sao ℓ₁ cho nghiệm thưa?'); self.line(12)
        SIG, CEN = np.array([[1.5, 0.3], [0.3, 1.0]]), np.array([1.8, 0.8])
        loss = lambda w: (w - CEN) @ SIG @ (w - CEN)
        def bmin(p):
            t = np.linspace(0, 2 * np.pi, 4000); c, s = np.cos(t), np.sin(t)
            r_ = 1 / (abs(c) ** p + abs(s) ** p) ** (1 / p); P_ = np.c_[r_ * c, r_ * s]; return P_[np.argmin([loss(q) for q in P_])]
        for k, (p, col, title) in enumerate([(1, B, 'Ràng buộc ℓ₁ (LASSO)'), (2, O, 'Ràng buộc ℓ₂ (ridge)')]):
            gr = plane([-1.5, 2.5, 1], [-1.3, 1.9, 1], 5.2, 4.2, (LEFT if k == 0 else RIGHT) * 3.3 + DOWN * 0.7)
            w = bmin(p); lv = loss(w)
            curves = VGroup(*[gr.plot_implicit_curve(lambda a, b, f=f: loss(np.array([a, b])) - lv * f, color=WHITE if f == 1 else LIGHT, stroke_width=2.5 if f == 1 else 1.2) for f in (0.3, 0.6, 1, 1.8)])
            ball = unit_ball(gr, p, col).set_fill(col, 0.25)
            self.play(Create(gr), FadeIn(VT(title, 24, col).next_to(gr, UP, buff=0.1)), Create(ball), run_time=0.8)
            self.play(Create(curves), FadeIn(Cross(stroke_color=WHITE, stroke_width=3).scale(0.1).move_to(gr.c2p(*CEN))), run_time=1.2)
            self.play(FadeIn(Dot(gr.c2p(*w), color=R, radius=0.11)), FadeIn(VT(f'w* = ({vn(w[0])}; {vn(w[1])})', 20, R).next_to(gr.c2p(*w), UR, buff=0.08)))
        self.finish(12); self.clear_body()

        # 13 — khoảng cách, kNN
        self.section('Khoảng cách và k láng giềng gần nhất'); self.line(13)
        r = np.random.default_rng(5); P_ = r.uniform(-3, 3, (40, 2)); q = np.array([0.4, 0.2]); d = np.linalg.norm(P_ - q, axis=1); idx = np.argsort(d)[:5]
        gr = plane([-3.2, 3.2, 1], [-3.2, 3.2, 1], 5.2, 5.2, LEFT * 3.3 + DOWN * 0.45)
        self.play(Create(gr), *[FadeIn(Dot(gr.c2p(*p_), color=LIGHT, radius=0.05)) for p_ in P_], FadeIn(Star(color=O, fill_opacity=1).scale(0.14).move_to(gr.c2p(*q))))
        circ = Circle(radius=(gr.c2p(d[idx[-1]], 0) - gr.c2p(0, 0))[0], color=O).move_to(gr.c2p(*q))
        self.play(Create(circ), run_time=1.5)
        self.play(*[Create(Line(gr.c2p(*q), gr.c2p(*P_[i]), color=B)) for i in idx], *[FadeIn(Dot(gr.c2p(*P_[i]), color=B, radius=0.08)) for i in idx])
        self.play(FadeIn(VGroup(panel(M(r'd(\mathbf{x},\mathbf{y})=\|\mathbf{x}-\mathbf{y}\|', 40)), VT('5 láng giềng gần nhất (ℓ₂)', 26, B), VT('đổi chuẩn → đổi láng giềng', 22, LIGHT)).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)))
        self.finish(13); self.clear_body()

        # 14 — chuẩn hóa z-score
        self.section('Chuẩn hóa dữ liệu z-score'); self.line(14)
        yrs = r.uniform(0, 10, 50); inc = 5 + 2.5 * yrs + r.normal(0, 6, 50); X = np.c_[yrs, inc]; Z = (X - X.mean(0)) / X.std(0)
        ax = Axes(x_range=[-3, 45, 10], y_range=[-3, 45, 10], x_length=5, y_length=5, axis_config={'color': LIGHT, 'include_numbers': True, 'font_size': 18}).shift(LEFT * 3.3 + DOWN * 0.45)
        dots = VGroup(*[Dot(ax.c2p(*p_), color=B, radius=0.05) for p_ in X])
        self.play(Create(ax), FadeIn(dots), FadeIn(VT('năm kinh nghiệm (trục ngang) vs thu nhập (trục dọc)', 18, LIGHT).next_to(ax, DOWN, buff=0.1)))
        self.play(FadeIn(VGroup(panel(M(r'z_{ij}=\frac{x_{ij}-\mu_j}{\sigma_j}', 46)), VT('mỗi cột: trung bình 0, độ lệch chuẩn 1', 24), VT('→ các đặc trưng đóng góp cân bằng', 24, T)).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)))
        ax2 = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1], x_length=5, y_length=5, axis_config={'color': T, 'include_numbers': True, 'font_size': 18}).move_to(ax)
        self.play(ReplacementTransform(ax, ax2), *[d_.animate.move_to(ax2.c2p(*z)) for d_, z in zip(dots, Z)], run_time=3)
        self.play(FadeIn(VT('sau chuẩn hóa: cùng thang đo (z)', 20, T).next_to(ax2, UP, buff=0.1)))
        self.finish(14); self.clear_body()

        self.section('Tóm tắt'); self.line(15)
        items = ['Không gian con chứa gốc, khép kín với cộng và nhân vô hướng', 'Cơ sở: độc lập tuyến tính + sinh; số phần tử = số chiều',
                 'Ánh xạ tuyến tính ↔ ma trận; dim null(A) + rank A = n', 'Tích vô hướng cho độ dài, góc, hình chiếu trực giao', 'ℓ₁ khuyến khích nghiệm thưa, ℓ₂ nghiệm nhỏ; cần chuẩn hóa dữ liệu']
        lst = VGroup(*[VT('✓  ' + s_, 27) for s_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(15); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
