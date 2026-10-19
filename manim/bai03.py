"""Bài 3 - Giá trị riêng, phân rã ma trận, gradient và Hessian (Manim)."""
from common import *


def plane(xr, yr, w, h, pos, **kw):
    return NumberPlane(x_range=xr, y_range=yr, x_length=w, y_length=h, background_line_style={'stroke_color': GRIDC}, **kw).move_to(pos)


class Bai(Lesson):
    LESSON = 'video_bai03'; LABEL = 'BÀI 3 · GIÁ TRỊ RIÊNG, PHÂN RÃ MA TRẬN, GRADIENT VÀ HESSIAN'; TEXTS = load_texts('video_bai03')
    MINS = {2: 9}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 3. Giá trị riêng, gradient và Hessian', 44, WHITE, BOLD),
                   M(r'\mathbf{Av}=\lambda\mathbf{v},\qquad \mathbf{A}=\mathbf{U}\Sigma\mathbf{V}^{\top}', 54, O), VT('Chương 1 · Một số kiến thức cơ bản', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–2 — véc tơ riêng: xoay v, quan sát Av
        A = np.array([[4.0, 1.0], [2.0, 3.0]])
        self.section('Giá trị riêng và véc tơ riêng'); self.line(1)
        gr = plane([-6, 6, 1], [-4.5, 4.5, 1], 6.6, 5.0, LEFT * 3.0 + DOWN * 0.45)
        for d in [(1, 1), (1, -2)]:
            d = np.array(d) / np.linalg.norm(d); self.add(DashedLine(gr.c2p(*(-6 * d)), gr.c2p(*(6 * d)), color=T, stroke_opacity=0.5))
        th = ValueTracker(np.radians(20))
        vv = lambda: np.array([np.cos(th.get_value()), np.sin(th.get_value())])
        av = always_redraw(lambda: Arrow(gr.c2p(0, 0), gr.c2p(*vv()), buff=0, color=B, stroke_width=6))
        aA = always_redraw(lambda: Arrow(gr.c2p(0, 0), gr.c2p(*(A @ vv())), buff=0, color=O, stroke_width=6))
        def status():
            v = vv(); w = A @ v; cr = abs(v[0] * w[1] - v[1] * w[0]) / np.linalg.norm(w)
            return (VT(f'cùng phương!  λ = {vn(w @ v, 1)}', 30, T, BOLD) if cr < 0.04 else VT('Av đổi phương so với v', 26, LIGHT)).shift(RIGHT * 3.6 + DOWN * 0.4)
        st = always_redraw(status)
        side = VGroup(panel(M(r'\mathbf{Av}=\lambda\mathbf{v},\quad\mathbf{v}\neq\mathbf{0}', 42)), M(r'\mathbf{A}=\begin{bmatrix}4&1\\2&3\end{bmatrix}', 40)).arrange(DOWN, buff=0.4).shift(RIGHT * 3.6 + UP * 1.4)
        self.play(Create(gr), FadeIn(av), FadeIn(aA), FadeIn(side), FadeIn(st))
        self.play(th.animate.set_value(np.radians(45)), run_time=3); self.wait(1.5); self.finish(1)
        self.line(2)
        self.play(th.animate.set_value(np.radians(45 + 360)), run_time=self.slots[2] - 0.8, rate_func=linear)
        self.finish(2); self.remove(av, aA, st); self.clear_body()

        # 3–4 — Ví dụ 1.3
        self.section('Ví dụ 1.3: tính giá trị riêng'); self.line(3)
        gr = plane([-6, 6, 1], [-4.5, 4.5, 1], 6.0, 4.6, LEFT * 3.3 + DOWN * 0.6)
        steps = VGroup(M(r'\det(\mathbf{A}-\lambda\mathbf{I})=(4-\lambda)(3-\lambda)-2', 36), M(r'=\lambda^2-7\lambda+10=0', 36), M(r'\lambda_1=5,\qquad\lambda_2=2', 40, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 3.4 + UP * 1.4)
        self.play(Create(gr)); self.play(LaggedStart(*[Write(s_) for s_ in steps], lag_ratio=0.8), run_time=5); self.finish(3)
        self.line(4)
        for v, lam, c in [((1, 1), 5, B), ((1, -2), 2, O)]:
            v = np.array(v, float); a0 = Arrow(gr.c2p(0, 0), gr.c2p(*v), buff=0, color=c)
            self.play(GrowArrow(a0), run_time=0.6); self.play(a0.animate.put_start_and_end_on(gr.c2p(0, 0), gr.c2p(*(lam * v))), run_time=1.2)
        chk = VGroup(M(r'\mathbf{v}_1=(1,1),\ \mathbf{Av}_1=5\mathbf{v}_1', 34, B), M(r'\mathbf{v}_2=(1,-2),\ \mathbf{Av}_2=2\mathbf{v}_2', 34, O),
                     M(r'\lambda_1+\lambda_2=7=\operatorname{tr}\mathbf{A},\quad \lambda_1\lambda_2=10=\det\mathbf{A}', 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(steps, DOWN, buff=0.5, aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(c_) for c_ in chk], lag_ratio=0.6), run_time=2.5); self.finish(4); self.clear_body()

        # 5–7 — ma trận đối xứng, ellipse, Rayleigh
        S = np.array([[2.0, 1.0], [1.0, 1.5]]); L_, Q = np.linalg.eigh(S)
        self.section('Ma trận đối xứng và phân rã phổ'); self.line(5)
        gr = plane([-3, 3, 1], [-2.4, 2.4, 1], 6.2, 5.0, LEFT * 3.1 + DOWN * 0.45)
        side = VGroup(panel(M(r'\mathbf{A}=\mathbf{Q}\Lambda\mathbf{Q}^{\top}=\sum_i\lambda_i\,\mathbf{q}_i\mathbf{q}_i^{\top}', 38)), M(r'\mathbf{A}=\begin{bmatrix}2&1\\1&1{,}5\end{bmatrix}', 38),
                      VT(f'λ₁ = {vn(L_[1])},  λ₂ = {vn(L_[0])}', 26), VT('λ thực, Q trực giao', 24, T)).arrange(DOWN, buff=0.35).shift(RIGHT * 3.5 + UP * 0.6)
        self.play(Create(gr), LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.6), run_time=3.5); self.finish(5)
        self.line(6)
        circ = Circle(radius=(gr.c2p(1, 0) - gr.c2p(0, 0))[0], color=B).move_to(gr.c2p(0, 0))
        q1 = Arrow(gr.c2p(0, 0), gr.c2p(*Q[:, 1]), buff=0, color=O); q2 = Arrow(gr.c2p(0, 0), gr.c2p(*Q[:, 0]), buff=0, color=T)
        self.play(Create(circ), GrowArrow(q1), GrowArrow(q2))
        M3 = np.eye(3); M3[:2, :2] = S
        self.play(ApplyMatrix(M3, VGroup(circ, q1, q2), about_point=gr.c2p(0, 0)), run_time=3); self.finish(6)
        self.line(7)
        ph = ValueTracker(0)
        xr = always_redraw(lambda: Arrow(gr.c2p(0, 0), gr.c2p(np.cos(ph.get_value()), np.sin(ph.get_value())), buff=0, color=WHITE))
        rq = always_redraw(lambda: VT(f'R(x) = {vn(np.array([np.cos(ph.get_value()), np.sin(ph.get_value())]) @ S @ np.array([np.cos(ph.get_value()), np.sin(ph.get_value())]))}', 30, O).shift(RIGHT * 3.5 + DOWN * 2.0))
        self.play(FadeOut(side[2:]), FadeIn(panel(M(r'\lambda_{\min}\leq\frac{\mathbf{x}^{\top}\mathbf{A}\mathbf{x}}{\mathbf{x}^{\top}\mathbf{x}}\leq\lambda_{\max}', 40)).shift(RIGHT * 3.5 + DOWN * 0.7)), FadeIn(xr), FadeIn(rq))
        self.play(ph.animate.set_value(2 * PI), run_time=5, rate_func=linear); self.finish(7); self.remove(xr, rq); self.clear_body()

        # 8 — xác định dương
        self.section('Ma trận xác định dương'); self.line(8)
        rows_ = VGroup(row('$\\mathbf{A}\\succ 0$:', '$\\mathbf{x}^\\top\\mathbf{A}\\mathbf{x}>0\\ \\ \\forall\\mathbf{x}\\neq\\mathbf{0}$', '⇔ mọi λᵢ > 0'),
                       row('$\\mathbf{A}\\succeq 0$:', '$\\mathbf{x}^\\top\\mathbf{A}\\mathbf{x}\\geq 0\\ \\ \\forall\\mathbf{x}$', '⇔ mọi λᵢ ≥ 0'),
                       row('$\\mathbf{x}^\\top\\mathbf{X}^\\top\\mathbf{X}\\mathbf{x}=\\|\\mathbf{X}\\mathbf{x}\\|_2^2\\geq 0$', '⇒ XᵀX ⪰ 0 với mọi X', color=T),
                       row('Cột của X độc lập tuyến tính', '⇒ XᵀX ≻ 0, khả nghịch', color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.3) for r_ in rows_], lag_ratio=0.8), run_time=6); self.finish(8); self.clear_body()

        # 9 — chén và yên ngựa (3D)
        self.section('Dạng toàn phương: chén và yên ngựa'); self.line(9)
        az = ValueTracker(-30)
        def surf(k):
            a, b, col, lab = [(1, 2, B, 'A ≻ 0: cực tiểu tại gốc'), (1.5, -1.5, O, 'A không xác định dấu: yên ngựa')][k]
            ax = ThreeDAxes(x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], z_range=[-3.5, 7], x_length=3.4, y_length=3.4, z_length=3.0)
            sf = Surface(lambda u, v: ax.c2p(u, v, a * u * u + b * v * v), u_range=[-1.4, 1.4], v_range=[-1.4, 1.4], resolution=(14, 14),
                         fill_opacity=0.88, checkerboard_colors=[col, interpolate_color(ManimColor(col), ManimColor(BG), 0.45)], stroke_width=0.3)
            g = VGroup(ax, sf).rotate(az.get_value() * DEGREES, axis=OUT).rotate(-60 * DEGREES, axis=RIGHT)
            return g.move_to((LEFT if k == 0 else RIGHT) * 3.3 + DOWN * 0.8)
        s0, s1 = always_redraw(lambda: surf(0)), always_redraw(lambda: surf(1))
        labs = VGroup(VT('A ≻ 0: cực tiểu tại gốc', 24, B).move_to(LEFT * 3.3 + UP * 2.0), VT('A không xác định dấu: yên ngựa', 24, O).move_to(RIGHT * 3.3 + UP * 2.0))
        self.play(FadeIn(s0), FadeIn(s1), FadeIn(labs), run_time=1.5)
        self.play(az.animate.set_value(15), run_time=self.slots[9] - 3, rate_func=smooth)
        self.remove(s0, s1)
        self.finish(9); self.clear_body()

        # 10–11 — SVD
        self.section('Phân rã giá trị suy biến (SVD)'); self.line(10)
        A = np.array([[1.6, 0.9], [0.3, 1.1]]); U, s, Vt = np.linalg.svd(A)
        gr = plane([-2.6, 2.6, 1], [-2, 2, 1], 6.2, 4.8, LEFT * 3.1 + DOWN * 0.45)
        circ = Circle(radius=(gr.c2p(1, 0) - gr.c2p(0, 0))[0], color=B).move_to(gr.c2p(0, 0))
        v1 = Arrow(gr.c2p(0, 0), gr.c2p(*Vt[0]), buff=0, color=O); v2 = Arrow(gr.c2p(0, 0), gr.c2p(*Vt[1]), buff=0, color=T)
        stp = VGroup(VT('1. Vᵀ: quay', 26), VT(f'2. Σ: co giãn σ₁ = {vn(s[0])}, σ₂ = {vn(s[1])}', 26), VT('3. U: quay (hoặc phản xạ)', 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 3.4 + DOWN * 0.2)
        self.play(Create(gr), Create(circ), GrowArrow(v1), GrowArrow(v2), FadeIn(panel(M(r'\mathbf{A}=\mathbf{U}\,\Sigma\,\mathbf{V}^{\top}', 52)).shift(RIGHT * 3.4 + UP * 1.7)), FadeIn(stp.set_opacity(0.35)))
        o = gr.c2p(0, 0)
        for k_, Mk in enumerate([Vt, np.diag(s), U]):
            M3 = np.eye(3); M3[:2, :2] = Mk; stp[k_].set_opacity(1).set_color(O)
            self.play(ApplyMatrix(M3, VGroup(circ, v1, v2), about_point=o), run_time=1.6); stp[k_].set_color(INK)
        self.play(FadeIn(VT('số σᵢ khác 0 = hạng của A', 24, T).next_to(stp, DOWN, buff=0.4, aligned_edge=LEFT)))
        self.finish(10); self.clear_body()
        self.section('Xấp xỉ hạng thấp bằng SVD'); self.line(11)
        img = self.make_img(); IU, IS, IVt = np.linalg.svd(img)
        pics = Group()
        for k in [1, 5, 20, None]:
            Ak = img if k is None else (IU[:, :k] * IS[:k]) @ IVt[:k]
            err = 0 if k is None else np.linalg.norm(img - Ak) / np.linalg.norm(img)
            im = ImageMobject(np.uint8(np.clip(Ak, 0, 1) * 255)).set_height(2.6); im.set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest'])
            cap = VT(f'ảnh gốc (hạng {np.linalg.matrix_rank(img)})' if k is None else f'k = {k}   sai số {vn(100 * err, 1)}%', 20)
            pics.add(Group(im, cap.next_to(im, DOWN, buff=0.15)))
        pics.arrange(RIGHT, buff=0.35).shift(UP * 0.1)
        for p_ in pics: self.play(FadeIn(p_, shift=UP * 0.2), run_time=0.9)
        self.play(FadeIn(VT('Giữ k giá trị suy biến lớn nhất: xấp xỉ hạng k tốt nhất theo chuẩn Frobenius', 22, T).next_to(pics, DOWN, buff=0.45)))
        self.finish(11); self.clear_body()

        # 12 — gradient
        self.section('Gradient'); self.line(12)
        f = lambda x, y: x * x + 3 * y * y + 0.6 * x * y
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[-1.6, 1.6, 1], x_length=6.6, y_length=4.8, axis_config={'color': LIGHT}).shift(LEFT * 3 + DOWN * 0.45)
        lv = VGroup(*[ax.plot_implicit_curve(lambda x, y, c=c: f(x, y) - c, color=B, stroke_width=2) for c in (0.3, 0.8, 1.6, 2.8, 4.4)])
        self.play(Create(ax), Create(lv), run_time=1.5)
        for (x, y) in [(1.2, 0.5), (-1.0, 0.6), (0.4, -0.8), (-1.5, -0.3), (1.6, -0.4)]:
            g = np.array([2 * x + 0.6 * y, 6 * y + 0.6 * x]); g = g / np.linalg.norm(g) * 0.55
            self.play(FadeIn(Dot(ax.c2p(x, y), color=O, radius=0.06)), GrowArrow(Arrow(ax.c2p(x, y), ax.c2p(x + g[0], y + g[1]), buff=0, color=O, max_tip_length_to_length_ratio=0.35)), run_time=0.5)
        side = VGroup(panel(M(r'\nabla f(\mathbf{x})=\Big(\frac{\partial f}{\partial x_1},\dots,\frac{\partial f}{\partial x_d}\Big)^{\!\top}', 36)), VT('vuông góc với đường đồng mức', 24),
                      row('$\\nabla f$:', 'hướng tăng nhanh nhất', color=O), row('$-\\nabla f$:', 'hướng giảm nhanh nhất', color=T)).arrange(DOWN, buff=0.35).shift(RIGHT * 3.6 + UP * 0.2)
        self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.5), run_time=2); self.finish(12); self.clear_body()

        # 13 — Jacobian và quy tắc chuỗi
        self.section('Ma trận Jacobian và quy tắc chuỗi'); self.line(13)
        J = panel(M(r'\mathbf{J}_{\mathbf{f}}=\Big[\frac{\partial f_i}{\partial x_j}\Big]\in\mathbb{R}^{m\times n}', 44)).shift(UP * 1.6)
        nodes = VGroup(*[panel(M(s_, 38), color=B) for s_ in [r'\mathbf{x}\in\mathbb{R}^{n}', r'\mathbf{g}(\mathbf{x})\in\mathbb{R}^{p}', r'\mathbf{f}(\mathbf{g}(\mathbf{x}))\in\mathbb{R}^{m}']]).arrange(RIGHT, buff=1.2)
        arrs = VGroup(*[Arrow(nodes[i].get_right(), nodes[i + 1].get_left(), color=LIGHT) for i in range(2)])
        chain = M(r'\mathbf{J}_{\mathbf{f}\circ\mathbf{g}}(\mathbf{x})=\mathbf{J}_{\mathbf{f}}(\mathbf{g}(\mathbf{x}))\,\mathbf{J}_{\mathbf{g}}(\mathbf{x})', 44, O).shift(DOWN * 1.4)
        self.play(FadeIn(J)); self.play(LaggedStart(FadeIn(nodes[0]), GrowArrow(arrs[0]), FadeIn(nodes[1]), GrowArrow(arrs[1]), FadeIn(nodes[2]), lag_ratio=0.4), run_time=2)
        self.play(Write(chain)); self.play(FadeIn(VT('(m×p)·(p×n) = m×n  —  lan truyền ngược trong mạng nơ-ron', 22, LIGHT).next_to(chain, DOWN, buff=0.35)))
        self.finish(13); self.clear_body()

        # 14 — Hessian
        self.section('Ma trận Hessian'); self.line(14)
        H = VGroup(panel(M(r'\nabla^2 f(\mathbf{x})=\Big[\frac{\partial^2 f}{\partial x_i\,\partial x_j}\Big]_{d\times d}', 46)), row('Ví dụ', '$f=x_1^2+3x_2^2+0{,}6\\,x_1x_2$', ':'),
                   row('$\\nabla^2 f=\\begin{bmatrix}2&0{,}6\\\\0{,}6&6\\end{bmatrix}$', 'đối xứng', color=O),
                   VT('Clairaut: đạo hàm cấp hai liên tục ⇒ ∂²f/∂x₁∂x₂ = ∂²f/∂x₂∂x₁', 24, T)).arrange(DOWN, buff=0.45).shift(DOWN * 0.1)
        self.play(LaggedStart(*[FadeIn(h_, shift=UP * 0.2) for h_ in H], lag_ratio=0.8), run_time=5.5); self.finish(14); self.clear_body()

        # 15 — bảng quy tắc
        self.section('Một số quy tắc giải tích ma trận'); self.line(15)
        tb = MathTable([[r'\mathbf{a}^{\top}\mathbf{x}', r'\mathbf{a}', r'\text{—}'], [r'\mathbf{x}^{\top}\mathbf{A}\mathbf{x}', r'(\mathbf{A}+\mathbf{A}^{\top})\mathbf{x}', r'\mathbf{A}\ \text{vuông}'],
                        [r'\mathbf{x}^{\top}\mathbf{A}\mathbf{x}', r'2\mathbf{A}\mathbf{x}', r'\mathbf{A}\ \text{đối xứng}'], [r'\|\mathbf{x}\|_2^2', r'2\mathbf{x}', r'\text{—}'],
                        [r'\|\mathbf{A}\mathbf{x}-\mathbf{b}\|_2^2', r'2\mathbf{A}^{\top}(\mathbf{A}\mathbf{x}-\mathbf{b})', r'\text{bình phương nhỏ nhất}']],
                       col_labels=[M(r'f(\mathbf{x})', 36, B), M(r'\nabla f(\mathbf{x})', 36, B), M(r'\text{Điều kiện}', 36, B)], include_outer_lines=False,
                       line_config={'stroke_color': GRIDC}, element_to_mobject_config={'font_size': 36}).scale(0.85).shift(DOWN * 0.3)
        self.play(FadeIn(tb.get_col_labels()), Create(tb.get_horizontal_lines()), Create(tb.get_vertical_lines()))
        for r_ in tb.get_rows()[1:]: self.play(FadeIn(r_), run_time=0.6); self.wait(1.2)
        self.finish(15); self.clear_body()

        # 16 — Ví dụ 1.4
        self.section('Ví dụ 1.4: hàm toàn phương'); self.line(16)
        A = np.array([[3.0, 1.0], [1.0, 2.0]]); b = np.array([1.0, 1.0]); xs = np.linalg.solve(A, b)
        F = lambda x, y: 0.5 * (3 * x * x + 2 * x * y + 2 * y * y) - x - y
        ax = Axes(x_range=[-1.3, 1.7, 0.5], y_range=[-1.0, 1.6, 0.5], x_length=6.0, y_length=5.0, axis_config={'color': LIGHT}).shift(LEFT * 3.3 + DOWN * 0.4)
        lv = VGroup(*[ax.plot_implicit_curve(lambda x, y, c=c: F(x, y) - F(*xs) - c, color=B, stroke_width=2) for c in (0.05, 0.25, 0.6, 1.2, 2.0, 3.0)])
        self.play(Create(ax), Create(lv), run_time=1.5)
        st_ = VGroup(M(r'f(\mathbf{x})=\tfrac{1}{2}\mathbf{x}^{\top}\mathbf{A}\mathbf{x}-\mathbf{b}^{\top}\mathbf{x}', 38), M(r'\nabla f=\mathbf{A}\mathbf{x}-\mathbf{b},\qquad\nabla^2 f=\mathbf{A}', 38, O),
                     M(r'\mathbf{A}=\begin{bmatrix}3&1\\1&2\end{bmatrix}\succ 0,\ \ \mathbf{b}=(1,1)', 34), M(r'\mathbf{x}^*=\mathbf{A}^{-1}\mathbf{b}=(0{,}2;\ 0{,}4)', 38, T),
                     VT('cực tiểu toàn cục duy nhất', 24, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).shift(RIGHT * 3.2 + UP * 0.1)
        self.play(LaggedStart(*[FadeIn(s_) for s_ in st_[:3]], lag_ratio=0.8), run_time=4)
        self.play(FadeIn(Star(color=T, fill_opacity=1).scale(0.16).move_to(ax.c2p(*xs))), FadeIn(st_[3:]))
        self.finish(16); self.clear_body()

        self.section('Tóm tắt'); self.line(17)
        items = ['Véc tơ riêng: hướng không đổi phương, co giãn hệ số λ', 'A đối xứng: A = QΛQᵀ, λ thực, Q trực giao', 'XᵀX ⪰ 0; ≻ 0 khi các cột của X độc lập tuyến tính',
                 'SVD A = UΣVᵀ cho mọi ma trận; số σᵢ ≠ 0 = hạng', 'Gradient: hướng tăng nhanh nhất · Hessian: độ cong']
        lst = VGroup(*[VT('✓  ' + s_, 28) for s_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7.5)
        self.finish(17); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)

    @staticmethod
    def make_img():  # ảnh tổng hợp 120×120 (chữ TVU) để minh họa nén SVD
        import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
        f = plt.figure(figsize=(1.2, 1.2), dpi=100); a = f.add_axes([0, 0, 1, 1]); a.set_xlim(0, 1); a.set_ylim(0, 1); a.axis('off')
        yy, xx = np.mgrid[0:1:120j, 0:1:120j]; a.imshow(0.35 + 0.3 * xx * yy, cmap='gray', vmin=0, vmax=1, extent=(0, 1, 0, 1))
        a.add_patch(plt.Circle((0.3, 0.68), 0.18, color='0.9')); a.add_patch(plt.Rectangle((0.55, 0.15), 0.32, 0.3, color='0.1', angle=12))
        a.text(0.5, 0.3, 'TVU', fontsize=22, ha='center', color='white', weight='bold'); f.canvas.draw()
        im = np.asarray(f.canvas.buffer_rgba())[..., :3].mean(-1) / 255; plt.close(f); return im
