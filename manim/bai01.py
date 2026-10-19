"""Bài 1 - Ma trận và các phép toán trên ma trận (Manim)."""
from common import *


class Bai(Lesson):
    LESSON = 'video_bai01'; LABEL = 'BÀI 1 · MA TRẬN VÀ CÁC PHÉP TOÁN'; TEXTS = load_texts('video_bai01')
    MINS = {5: 12, 10: 9, 11: 9}

    def construct(self):
        # 0 — tiêu đề
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 1. Ma trận và các phép toán', 46, WHITE, BOLD),
                   M(r'(\mathbf{AB})_{ij}=\sum_k a_{ik}\,b_{kj}', 54, O), VT('Chương 1 · Một số kiến thức cơ bản', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–2 — véc tơ
        self.section('Véc tơ trong không gian thực'); self.line(1)
        ex = VGroup(row('Ảnh xám 28×28', '→', '$\\mathbf{x}\\in\\mathbb{R}^{784}$', color=INK),
                    row('Khách hàng', '→', '(tuổi, thu nhập, số lần mua, …)'),
                    row('Câu văn', '→', 'véc tơ tần suất từ')).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(UP * 0.4)
        for r_ in ex: r_[-1].set_color(B)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.3) for r_ in ex], lag_ratio=0.6), run_time=4)
        self.finish(1); self.play(ex.animate.scale(0.75).to_corner(UL).shift(DOWN * 1.3), run_time=0.8)
        self.line(2)
        pl = NumberPlane(x_range=[-1, 5, 1], y_range=[-1, 4, 1], x_length=6, y_length=5, background_line_style={'stroke_color': GRIDC}).shift(RIGHT * 3.2 + DOWN * 0.3)
        u, v = np.array([3, 1]), np.array([1, 2.2])
        au = Arrow(pl.c2p(0, 0), pl.c2p(*u), buff=0, color=B); av = Arrow(pl.c2p(0, 0), pl.c2p(*v), buff=0, color=T)
        lu = M(r'\mathbf{u}', 34, B).next_to(au.get_end(), DR, buff=0.1); lv = M(r'\mathbf{v}', 34, T).next_to(av.get_end(), UL, buff=0.1)
        self.play(Create(pl), run_time=1); self.play(GrowArrow(au), GrowArrow(av), FadeIn(lu, lv))
        d1 = DashedLine(pl.c2p(*u), pl.c2p(*(u + v)), color=T); d2 = DashedLine(pl.c2p(*v), pl.c2p(*(u + v)), color=B)
        self.play(Create(d1), Create(d2), run_time=1.2)
        s = Arrow(pl.c2p(0, 0), pl.c2p(*(u + v)), buff=0, color=O, stroke_width=7)
        self.play(GrowArrow(s), FadeIn(M(r'\mathbf{u}+\mathbf{v}', 34, O).next_to(s.get_end(), UR, buff=0.1)))
        f = panel(M(r'\mathbf{x}+\mathbf{y}=\begin{bmatrix}x_1+y_1\\ \vdots\\ x_n+y_n\end{bmatrix}', 36)).to_edge(LEFT, buff=0.8).shift(DOWN * 1.6)
        self.play(FadeIn(f)); self.finish(2); self.clear_body()

        # 3 — ba cách nhìn ma trận
        self.section('Ma trận và ba cách nhìn'); self.line(3)
        A = Matrix([[3, 1, 4, 1], [5, 9, 2, 6], [5, 3, 5, 8]], h_buff=1.0).scale(1.1).shift(LEFT * 3)
        lab = M(r'\mathbf{A}\in\mathbb{R}^{3\times 4}', 40).next_to(A, UP)
        self.play(Write(A), FadeIn(lab), run_time=1.5)
        views = VGroup(VT('Theo phần tử: bảng số a_ij', 26), VT('Theo cột: A = [a₁ a₂ … aₙ]', 26), VT('Theo hàng: mỗi hàng là một quan sát', 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.5).shift(RIGHT * 3.2)
        boxes = [SurroundingRectangle(A.get_entries(), color=B), SurroundingRectangle(A.get_columns()[1], color=O), SurroundingRectangle(A.get_rows()[1], color=T)]
        for k, (vw, bx, c) in enumerate(zip(views, boxes, [B, O, T])):
            vw.set_color(c); self.play(FadeIn(vw, shift=LEFT * 0.2), Create(bx), *( [FadeOut(boxes[k - 1])] if k else []), run_time=1)
            self.wait(0.5)
        self.finish(3); self.clear_body()

        # 4–6 — nhân ma trận (Ví dụ 1.1)
        self.section('Phép nhân hai ma trận'); self.line(4)
        A1 = Matrix([[1, 2, 0], [3, -1, 4]]); B1 = Matrix([[2, 1], [0, -3], [5, 2]]); C1 = Matrix([[2, -5], [26, 14]])
        eq = VGroup(A1, M(r'\times', 40), B1, M('=', 40), C1).arrange(RIGHT, buff=0.35).shift(UP * 0.8)
        for e in C1.get_entries(): e.set_opacity(0)
        la = VGroup(M(r'\mathbf{A}\ (2\times 3)', 30).next_to(A1, UP), M(r'\mathbf{B}\ (3\times 2)', 30).next_to(B1, UP), M(r'\mathbf{AB}\ (2\times 2)', 30, T).next_to(C1, UP))
        self.play(FadeIn(eq), FadeIn(la), run_time=1.2)
        rule = M(r'c_{ij}=\sum_{k=1}^{n} a_{ik}\,b_{kj}', 42, O).shift(DOWN * 1.6)
        self.play(Write(rule)); self.wait(1)
        r0 = SurroundingRectangle(A1.get_rows()[0], color=B); c0 = SurroundingRectangle(B1.get_columns()[0], color=O)
        self.play(Create(r0), Create(c0)); self.finish(4)
        self.line(5)
        self.play(FadeOut(rule), run_time=0.4)
        Av, Bv = [[1, 2, 0], [3, -1, 4]], [[2, 1], [0, -3], [5, 2]]
        p = lambda x: str(x) if x >= 0 else f'({x})'
        calc = None
        for i in range(2):
            for j in range(2):
                nr = SurroundingRectangle(A1.get_rows()[i], color=B); nc = SurroundingRectangle(B1.get_columns()[j], color=O)
                txt = M(f'c_{{{i+1}{j+1}}}=' + ' + '.join(f'{p(Av[i][k])}\\cdot {p(Bv[k][j])}' for k in range(3)) + f'={Av[i][0]*Bv[0][j]+Av[i][1]*Bv[1][j]+Av[i][2]*Bv[2][j]}', 40).shift(DOWN * 1.6)
                anims = [Transform(r0, nr), Transform(c0, nc)]
                anims.append(Transform(calc, txt) if calc else FadeIn(txt)); 
                self.play(*anims, run_time=0.8)
                if calc is None: calc = txt
                e = C1.get_entries()[2 * i + j]; e.set_color(T)
                self.play(e.animate.set_opacity(1), run_time=0.5); self.play(Indicate(e, color=T, scale_factor=1.3), run_time=0.6); self.wait(0.3)
        self.finish(5)
        self.line(6)
        self.play(FadeOut(r0, c0, calc), run_time=0.5)
        note = row('$\\mathbf{BA}$', 'có cỡ 3×3', '$\\Rightarrow\\ \\mathbf{AB}\\neq\\mathbf{BA}$', color=O).shift(DOWN * 1.6)
        self.play(Circumscribe(C1, color=T), FadeIn(note)); self.finish(6); self.clear_body()

        # 7 — Ax là tổ hợp tuyến tính các cột
        self.section('Ax là tổ hợp tuyến tính các cột'); self.line(7)
        pl = NumberPlane(x_range=[-2, 4, 1], y_range=[-1, 3.5, 1], x_length=6.5, y_length=4.9, background_line_style={'stroke_color': GRIDC}).shift(LEFT * 3 + DOWN * 0.4)
        a1, a2, x = np.array([2, 0.6]), np.array([-0.8, 1.5]), np.array([1.5, 1.2])
        A1v = Arrow(pl.c2p(0, 0), pl.c2p(*a1), buff=0, color=LIGHT); A2v = Arrow(pl.c2p(0, 0), pl.c2p(*a2), buff=0, color=LIGHT)
        self.play(Create(pl), GrowArrow(A1v), GrowArrow(A2v), FadeIn(M(r'\mathbf{a}_1', 30).next_to(A1v.get_end(), DOWN), M(r'\mathbf{a}_2', 30).next_to(A2v.get_end(), LEFT)))
        s1 = Arrow(pl.c2p(0, 0), pl.c2p(*(x[0] * a1)), buff=0, color=B); s2 = Arrow(pl.c2p(*(x[0] * a1)), pl.c2p(*(x[0] * a1 + x[1] * a2)), buff=0, color=T)
        s3 = Arrow(pl.c2p(0, 0), pl.c2p(*(x[0] * a1 + x[1] * a2)), buff=0, color=O, stroke_width=7)
        self.play(GrowArrow(s1)); self.play(GrowArrow(s2)); self.play(GrowArrow(s3), FadeIn(M(r'\mathbf{Ax}', 34, O).next_to(s3.get_end(), UP)))
        f = VGroup(M(r'\mathbf{Ax}=x_1\mathbf{a}_1+x_2\mathbf{a}_2+\cdots+x_n\mathbf{a}_n', 38), M(r'x_1=1{,}5,\quad x_2=1{,}2', 34, LIGHT),
                   VT('tập mọi tích Ax = không gian cột', 24)).arrange(DOWN, buff=0.4).shift(RIGHT * 3.6 + UP * 0.5)
        self.play(FadeIn(f, shift=LEFT * 0.2)); self.finish(7); self.clear_body()

        # 8 — tính chất
        self.section('Tính chất của phép nhân và chuyển vị'); self.line(8)
        props = [('Kết hợp', r'(\mathbf{AB})\mathbf{C}=\mathbf{A}(\mathbf{BC})', INK), ('Phân phối', r'\mathbf{A}(\mathbf{B}+\mathbf{C})=\mathbf{AB}+\mathbf{AC}', INK),
                 ('Phần tử đơn vị', r'\mathbf{I}_m\mathbf{A}=\mathbf{A}\mathbf{I}_n=\mathbf{A}', INK), ('Không giao hoán', r'\mathbf{AB}\neq\mathbf{BA}\ \text{(nói chung)}', O),
                 ('Chuyển vị của tích', r'(\mathbf{AB})^{\top}=\mathbf{B}^{\top}\mathbf{A}^{\top}', O)]
        rows_ = VGroup(*[VGroup(VT(a, 28, c), M(b, 40, c)) for a, b, c in props])
        for r_ in rows_: r_[1].next_to(r_[0], RIGHT, buff=0).align_to(ORIGIN, LEFT).shift(RIGHT * 0.2)
        rows_.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(ORIGIN + DOWN * 0.2)
        for r_ in rows_: r_[0].shift(LEFT * 0.5); r_[1].set_x(1.6, LEFT) if hasattr(r_[1], 'set_x') else None
        for r_ in rows_: r_[1].move_to([1.6 + r_[1].width / 2 - 0.5, r_[0].get_y(), 0])
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows_], lag_ratio=0.5), run_time=4.5)
        self.finish(8); self.clear_body()

        # 9 — ma trận trực giao
        self.section('Ma trận trực giao: quay hoặc phản xạ'); self.line(9)
        pl = NumberPlane(x_range=[-2, 2.5, 1], y_range=[-0.5, 2.5, 1], x_length=6, y_length=4, background_line_style={'stroke_color': GRIDC}).shift(LEFT * 3 + DOWN * 0.4)
        th = ValueTracker(0)
        Qm = lambda: np.array([[np.cos(th.get_value()), -np.sin(th.get_value())], [np.sin(th.get_value()), np.cos(th.get_value())]])
        sq = always_redraw(lambda: Polygon(*[pl.c2p(*(Qm() @ p_)) for p_ in [(0, 0), (1, 0), (1, 1), (0, 1)]], color=B, fill_opacity=0.3))
        xv = np.array([1.6, 0.6]); xa = always_redraw(lambda: Arrow(pl.c2p(0, 0), pl.c2p(*(Qm() @ xv)), buff=0, color=O))
        ghost = Polygon(*[pl.c2p(*p_) for p_ in [(0, 0), (1, 0), (1, 1), (0, 1)]], color=LIGHT, stroke_opacity=0.6)
        info = always_redraw(lambda: VGroup(M(r'\mathbf{Q}^{\top}\mathbf{Q}=\mathbf{I}', 44), M(r'(\mathbf{Qx})^{\top}(\mathbf{Qy})=\mathbf{x}^{\top}\mathbf{y}', 38),
                                            VT(f'‖x‖ = {vn(np.linalg.norm(xv))}    ‖Qx‖ = {vn(np.linalg.norm(Qm() @ xv))}', 24, O),
                                            VT(f'góc quay {vn(np.degrees(th.get_value()), 0)}°', 22, LIGHT), M(r'\mathbf{Q}^{-1}=\mathbf{Q}^{\top}', 40, T)).arrange(DOWN, buff=0.35).shift(RIGHT * 3.4))
        self.play(Create(pl), FadeIn(ghost), FadeIn(sq), FadeIn(xa), FadeIn(info))
        self.play(th.animate.set_value(np.radians(50)), run_time=4, rate_func=smooth); self.finish(9)
        self.remove(info, sq, xa); self.clear_body()

        # 10–11 — định thức
        self.section('Định thức: hệ số co giãn diện tích'); self.line(10)
        pl = NumberPlane(x_range=[-0.5, 2.6, 0.5], y_range=[-0.5, 1.9, 0.5], x_length=6.2, y_length=4.8, background_line_style={'stroke_color': GRIDC}).shift(LEFT * 3 + DOWN * 0.4)
        k = ValueTracker(0); Am = np.array([[1.5, 0.5], [0.3, 1.2]]); Zm = np.array([[1.5, 0.75], [0.6, 0.3]])
        cur = lambda: (np.eye(2) + (Am - np.eye(2)) * min(k.get_value(), 1)) if k.get_value() <= 1 else Am + (Zm - Am) * (k.get_value() - 1)
        par = always_redraw(lambda: Polygon(*[pl.c2p(*(cur() @ p_)) for p_ in [(0, 0), (1, 0), (1, 1), (0, 1)]], color=O if k.get_value() > 1 else B, fill_opacity=0.35))
        det = always_redraw(lambda: VT(f'diện tích = |det A| = {vn(abs(np.linalg.det(cur())))}', 28, O if abs(np.linalg.det(cur())) < 0.03 else B).shift(RIGHT * 3.4 + UP * 0.2))
        self.play(Create(pl), FadeIn(par), FadeIn(det), FadeIn(panel(M(r'\det\begin{pmatrix}a&b\\ c&d\end{pmatrix}=ad-bc', 40)).shift(RIGHT * 3.4 + UP * 1.6)))
        self.play(k.animate.set_value(1), run_time=3); self.finish(10)
        self.line(11)
        inv = M(r'\det\mathbf{A}\neq 0\ \Longleftrightarrow\ \mathbf{A}\ \text{khả nghịch}', 38).shift(RIGHT * 3.4 + DOWN * 1.0)
        self.play(FadeIn(inv)); self.play(k.animate.set_value(2), run_time=3.5)
        self.play(FadeIn(VT('det A = 0: ép dẹt, không đảo ngược được', 22, O).shift(RIGHT * 3.4 + DOWN * 1.8)))
        self.finish(11); self.remove(par, det); self.clear_body()

        # 12 — giải hệ trong thực hành
        self.section('Giải hệ Ax = b trong thực hành'); self.line(12)
        code = Code(code_string='import numpy as np\n\n# không nên\nx = np.linalg.inv(A) @ b\n\n# nên dùng\nx = np.linalg.solve(A, b)',
                    language='python', background='rectangle', formatter_style='monokai', add_line_numbers=False).scale(1.1).shift(LEFT * 2)
        side = VGroup(VT('Phân rã LU / Cholesky / QR', 28), VT('→ chính xác hơn, nhanh hơn', 28, T)).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.6)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=1.2); self.play(FadeIn(side)); self.finish(12); self.clear_body()

        # 13 — hạng và số nghiệm
        self.section('Hạng và số nghiệm của hệ Ax = b'); self.line(13)
        cases = [('Nghiệm duy nhất', [(1, 1, 3), (1, -1, 0)], T, r'\operatorname{rank}\mathbf{A}=n'), ('Vô nghiệm', [(1, 1, 3), (1, 1, 1.5)], O, r'\operatorname{rank}[\mathbf{A}|\mathbf{b}]>\operatorname{rank}\mathbf{A}'),
                 ('Vô số nghiệm', [(1, 1, 3), (2, 2, 6)], B, r'\operatorname{rank}\mathbf{A}<n,\ \text{tương thích}')]
        grp = VGroup()
        for kk, (lab_, eqs, c, cond) in enumerate(cases):
            ax = Axes(x_range=[-1, 4, 1], y_range=[-1, 4, 1], x_length=3.4, y_length=3.4, axis_config={'color': LIGHT})
            lines = VGroup(*[ax.plot(lambda x, a=a, b_=b_, c_=c_: (c_ - a * x) / b_, x_range=[-1, 4], color=[INK, c][j], stroke_width=[3, 5][j]) for j, (a, b_, c_) in enumerate(eqs)])
            if kk == 2: lines[1].set_stroke(opacity=0.8).set_style(stroke_width=6); lines[1] = DashedVMobject(lines[1])
            g = VGroup(VT(lab_, 26, c), VGroup(ax, lines), M(cond, 30, LIGHT)).arrange(DOWN, buff=0.25)
            if kk == 0: g[1].add(Dot(ax.c2p(1.5, 1.5), color=T, radius=0.09))
            grp.add(g)
        grp.arrange(RIGHT, buff=0.6, aligned_edge=UP).shift(DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in grp], lag_ratio=0.7), run_time=4.5); self.finish(13); self.clear_body()

        # 14 — hệ quá xác định
        self.section('Hệ quá xác định trong học máy'); self.line(14)
        rng = np.random.default_rng(2); xs = np.sort(rng.uniform(0, 10, 25)); ys = 1 + 0.6 * xs + rng.normal(0, 0.8, 25)
        ax = Axes(x_range=[0, 10, 2], y_range=[0, 9, 2], x_length=6.5, y_length=4.8, axis_config={'color': LIGHT, 'include_numbers': True, 'font_size': 20}).shift(LEFT * 3 + DOWN * 0.4)
        dots = VGroup(*[Dot(ax.c2p(a, b_), color=B, radius=0.06) for a, b_ in zip(xs, ys)])
        self.play(Create(ax), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.05), run_time=2)
        txt = VGroup(VT('25 phương trình, 2 ẩn', 30), VT('không đường thẳng nào đi qua mọi điểm', 22, LIGHT)).arrange(DOWN, aligned_edge=LEFT).shift(RIGHT * 3.6 + UP * 0.8)
        self.play(FadeIn(txt)); w = np.polyfit(xs, ys, 1)
        self.play(Create(ax.plot(lambda x: np.polyval(w, x), x_range=[0, 10], color=O, stroke_width=5)), FadeIn(VT('→ nghiệm bình phương nhỏ nhất (Bài 7)', 24, O).shift(RIGHT * 3.6 + DOWN * 0.6)))
        self.finish(14); self.clear_body()

        # 15–16 — ma trận thiết kế
        self.section('Biểu diễn dữ liệu bằng ma trận thiết kế'); self.line(15)
        X = Matrix([['1', '2'], ['2', '1{,}5'], ['3', '4{,}2']], h_buff=1.3).shift(LEFT * 4 + UP * 0.4)
        lx = M(r'\mathbf{X}\in\mathbb{R}^{3\times 2}', 36).next_to(X, UP)
        self.play(Write(X), FadeIn(lx))
        hr = SurroundingRectangle(X.get_rows()[0], color=T); hc = SurroundingRectangle(X.get_columns()[1], color=O)
        self.play(Create(hr), FadeIn(VT('hàng = một mẫu', 24, T).next_to(X, DOWN, buff=0.5)))
        for i in (1, 2): self.play(hr.animate.become(SurroundingRectangle(X.get_rows()[i], color=T)), run_time=0.6)
        self.play(Create(hc), FadeIn(VT('cột = một đặc trưng', 24, O).next_to(X, DOWN, buff=1.0)))
        self.finish(15)
        self.line(16)
        Wm = Matrix([['0{,}5'], ['-1{,}2']]); Y = Matrix([['-1{,}9'], ['-0{,}8'], ['-3{,}54']]).set_color(O)
        eq = VGroup(M(r'\times', 40), Wm, M('=', 40), Y).arrange(RIGHT, buff=0.3).next_to(X, RIGHT, buff=0.3)
        self.play(FadeOut(hr, hc), FadeIn(eq[:3]), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(e) for e in Y], lag_ratio=0.4), FadeIn(M(r'\hat{\mathbf{y}}=\mathbf{Xw}', 36, O).next_to(Y, UP)), run_time=2)
        code = Code(code_string='X = np.array([[1.0, 2.0],\n              [2.0, 1.5],\n              [3.0, 4.2]])\nw = np.array([0.5, -1.2])\ny_hat = X @ w\n# [-1.9  -0.8  -3.54]',
                    language='python', background='rectangle', formatter_style='monokai', add_line_numbers=False).scale(0.82).to_edge(RIGHT, buff=0.5).shift(DOWN * 2.0)
        self.play(FadeIn(code)); self.finish(16); self.clear_body()

        # 17 — tóm tắt
        self.section('Tóm tắt'); self.line(17)
        items = ['Véc tơ là véc tơ cột; ma trận nhìn theo phần tử, cột hoặc hàng', 'Phép nhân: kết hợp, phân phối, KHÔNG giao hoán',
                 '(AB)ᵀ = BᵀAᵀ  ·  Q trực giao: Q⁻¹ = Qᵀ', 'det A ≠ 0 ⇔ A khả nghịch; hạng quyết định số nghiệm', 'Ma trận thiết kế X ∈ ℝⁿˣᵈ:  ŷ = Xw']
        lst = VGroup(*[VT('✓  ' + s_, 28) for s_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=6.5)
        self.finish(17); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
