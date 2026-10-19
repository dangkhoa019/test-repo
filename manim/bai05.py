"""Bài 5 - Tập lồi, hàm lồi và bài toán tối ưu lồi (Manim)."""
from common import *

FC = lambda x: 0.35 * (x - 0.5) ** 2 + 0.6
RB = lambda th: 1 + 0.5 * np.cos(3 * th)          # biên tập không lồi (dạng cánh hoa)


def clip_poly(P, a, b):
    """Cắt đa giác P bởi nửa mặt phẳng a·x ≤ b (Sutherland–Hodgman)."""
    out = []
    for k in range(len(P)):
        p, q = P[k], P[(k + 1) % len(P)]; fp, fq = a @ p - b, a @ q - b
        if fp <= 0: out.append(p)
        if fp * fq < 0: out.append(p + (q - p) * fp / (fp - fq))
    return out


class Bai(Lesson):
    LESSON = 'video_bai05'; LABEL = 'BÀI 5 · TẬP LỒI, HÀM LỒI VÀ BÀI TOÁN TỐI ƯU LỒI'; TEXTS = load_texts('video_bai05')

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 5. Tập lồi, hàm lồi và tối ưu lồi', 44, WHITE, BOLD),
                   M(r'f(t\mathbf{x}+(1-t)\mathbf{y})\leq t f(\mathbf{x})+(1-t)f(\mathbf{y})', 46, O), VT('Chương 2 · Một số bài toán tối ưu', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1 — định nghĩa tập lồi
        self.section('Tập lồi: chứa trọn mọi đoạn thẳng'); self.line(1)
        S = 1.4; c1, c2 = LEFT * 3.4 + DOWN * 0.45, RIGHT * 3.4 + DOWN * 0.45
        ell = Ellipse(width=2.6 * S, height=1.8 * S, color=B, fill_opacity=0.15, stroke_width=3).move_to(c1)
        blob = ParametricFunction(lambda th: np.array([RB(th) * np.cos(th) * S, RB(th) * np.sin(th) * S, 0]), t_range=[0, TAU], color=B, stroke_width=3)
        blob.set_fill(B, opacity=0.15).shift(c2)
        P_ = panel(M(r'\mathbf{x},\mathbf{y}\in C,\ t\in[0,1]\ \Rightarrow\ t\mathbf{x}+(1-t)\mathbf{y}\in C', 34)).move_to(UP * 2.15 + RIGHT * 1.6)
        self.play(FadeIn(P_), Create(ell), Create(blob), run_time=1.5)
        u = ValueTracker(0)

        def seg_ell():
            x = np.array([-0.9, -0.4]); y = np.array([0.6 + 0.4 * np.cos(4 * u.get_value()), 0.5 * np.sin(4 * u.get_value())])
            return VGroup(Line(c1 + S * np.r_[x, 0], c1 + S * np.r_[y, 0], color=T, stroke_width=4),
                          Dot(c1 + S * np.r_[x, 0], color=WHITE), Dot(c1 + S * np.r_[y, 0], color=WHITE))

        def seg_blob():
            a2 = 2.0944 + 0.12 * np.sin(4 * u.get_value()); x = np.array([1.38, 0.0]); y = 1.38 * np.array([np.cos(a2), np.sin(a2)])
            g = VGroup()
            for s in np.linspace(0, 1, 40):
                p = s * x + (1 - s) * y; ok = np.hypot(*p) <= RB(np.arctan2(p[1], p[0])) + 1e-9
                g.add(Dot(c2 + S * np.r_[p, 0], radius=0.035, color=T if ok else R))
            return g.add(Dot(c2 + S * np.r_[x, 0], color=WHITE), Dot(c2 + S * np.r_[y, 0], color=WHITE))
        s1, s2 = always_redraw(seg_ell), always_redraw(seg_blob)
        self.play(FadeIn(s1), FadeIn(s2), FadeIn(VT('(a) tập lồi', 24, T).next_to(ell, DOWN, buff=0.45)),
                  FadeIn(VT('(b) không lồi: đoạn thẳng ra ngoài', 24, R).move_to(c2 + DOWN * 2.45)), run_time=1)
        self.play(u.animate.set_value(TAU / 2), run_time=5.5, rate_func=linear)
        s1.clear_updaters(); s2.clear_updaters(); self.finish(1); self.clear_body()

        # 2 — các tập lồi thường gặp
        self.section('Một số tập lồi thường gặp'); self.line(2)
        ax = axes([-2, 2, 1], [-2, 2, 1], 4.6, 4.6, LEFT * 3.6 + DOWN * 0.45, nums=False)
        hs = [(np.array([1, 1]), 1.2), (np.array([-1, 0.6]), 1.2), (np.array([0.3, -1]), 1.1)]
        self.play(Create(ax), run_time=0.8)
        for a, b in hs:
            xs = [x for x in np.linspace(-2, 2, 400) if -2 <= (b - a[0] * x) / a[1] <= 2]
            self.play(Create(Line(ax.c2p(xs[0], (b - a[0] * xs[0]) / a[1]), ax.c2p(xs[-1], (b - a[0] * xs[-1]) / a[1]), color=LIGHT, stroke_width=2.5)), run_time=0.6)
        P = [np.array(p, float) for p in [(-2, -2), (2, -2), (2, 2), (-2, 2)]]
        for a, b in hs: P = clip_poly(P, a, b)
        reg = Polygon(*[ax.c2p(*p) for p in P], color=T, fill_opacity=0.35, stroke_width=3)
        items = ['ℝᵈ', 'nửa không gian {x : aᵀx ≤ b}', 'hình cầu {x : ‖x − c‖ ≤ r}\n    (theo mọi chuẩn)', 'mọi không gian con', 'giao của các tập lồi']
        lst = VGroup(*[VT('•  ' + s_, 26, T if k == 4 else INK) for k, s_ in enumerate(items)]).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(RIGHT * 2.9 + DOWN * 0.3)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.2) for l_ in lst[:4]], lag_ratio=0.6), run_time=2.5)
        self.play(FadeIn(reg), FadeIn(lst[4]), FadeIn(VT('giao các nửa\nkhông gian', 20, T).move_to(ax.c2p(*np.mean(P, 0)))), run_time=1)
        self.finish(2); self.clear_body()

        # 3 — hàm lồi: dây cung trên đồ thị
        self.section('Hàm lồi: dây cung nằm trên đồ thị'); self.line(3)
        ax = axes([-2.5, 3.5, 1], [0, 5, 1], 6.4, 4.8, LEFT * 3.1 + DOWN * 0.45)
        a, b = -1.8, 2.8; t = ValueTracker(0.5)
        P_ = panel(M(r'f(t\mathbf{x}+(1-t)\mathbf{y})\leq t f(\mathbf{x})+(1-t)f(\mathbf{y})', 30)).move_to(RIGHT * 3.6 + UP * 1.9)
        self.play(Create(ax), Create(ax.plot(FC, x_range=[-2.5, 3.5], color=B, stroke_width=4)), FadeIn(P_), run_time=1.3)
        self.play(Create(Line(ax.c2p(a, FC(a)), ax.c2p(b, FC(b)), color=O, stroke_width=4)), FadeIn(Dot(ax.c2p(a, FC(a)), color=O)), FadeIn(Dot(ax.c2p(b, FC(b)), color=O)), run_time=0.8)
        xm = lambda: t.get_value() * a + (1 - t.get_value()) * b
        ch = lambda: t.get_value() * FC(a) + (1 - t.get_value()) * FC(b)
        seg = always_redraw(lambda: VGroup(Line(ax.c2p(xm(), FC(xm())), ax.c2p(xm(), ch()), color=T, stroke_width=5),
                                           Dot(ax.c2p(xm(), FC(xm())), color=B, radius=0.09), Dot(ax.c2p(xm(), ch()), color=O, radius=0.09)))
        info = always_redraw(lambda: VGroup(VT(f't = {vn(t.get_value())}', 28), VT(f'f(tx + (1−t)y) = {vn(FC(xm()))}', 22, B),
                                            VT(f't f(x) + (1−t) f(y) = {vn(ch())}', 22, O), VT('luôn ≤  ✓', 24, T)).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.6 + DOWN * 0.6))
        self.play(FadeIn(seg), FadeIn(info), run_time=0.6)
        self.play(t.animate.set_value(0.92), run_time=2, rate_func=smooth)
        self.play(t.animate.set_value(0.1), run_time=3, rate_func=smooth)
        seg.clear_updaters(); info.clear_updaters(); self.finish(3); self.clear_body()

        # 4 — lồi ngặt, lồi mạnh
        self.section('Lồi, lồi ngặt, lồi mạnh'); self.line(4)
        cases = [(np.abs, 'f = |x|: lồi,\nkhông lồi ngặt', INK), (lambda x: x ** 4, 'f = x⁴: lồi ngặt,\nkhông lồi mạnh', B), (lambda x: x ** 2, 'f = x²: lồi mạnh\n(m = 2)', T)]
        top = row('Lồi mạnh tham số m > 0:', '$f(\\mathbf{x})-\\tfrac{m}{2}\\|\\mathbf{x}\\|_2^2$', 'vẫn lồi', size=26).move_to(UP * 2.0)
        self.play(FadeIn(top), run_time=0.8)
        for k, (f, lab, c) in enumerate(cases):
            a_ = axes([-1.5, 1.5, 0.5], [-0.2, 2.3, 1], 3.6, 2.9, RIGHT * (4.2 * (k - 1)) + DOWN * 0.45, nums=False)
            self.play(Create(a_), Create(a_.plot(f, x_range=[-1.5, 1.5] if k == 0 else [-1.22, 1.22] if k == 1 else [-1.5, 1.5], color=c, stroke_width=4)),
                      FadeIn(VT(lab, 22, c).next_to(a_, DOWN, buff=0.25)), run_time=1.5)
        self.finish(4); self.clear_body()

        # 5 — quan hệ các mức độ lồi
        self.section('Quan hệ giữa các mức độ lồi'); self.line(5)
        lev = [('lồi mạnh', 'hội tụ tuyến tính của giảm gradient\n(khi gradient Lipschitz)', T), ('lồi ngặt', 'nghiệm duy nhất (nếu tồn tại)', B), ('lồi', 'không có cực tiểu địa phương giả', INK)]
        for k, (a_, b_, c) in enumerate(lev):
            y = 1.5 - 1.6 * k
            bx = panel(VT(a_, 30, c, BOLD), color=c).move_to(LEFT * 4.3 + UP * y)
            g = VGroup(bx, VT(b_, 24).next_to(bx, RIGHT, buff=0.6))
            if k < 2: g.add(MathTex(r'\Downarrow', font_size=44, color=INK).move_to(LEFT * 4.3 + UP * (y - 0.8)))
            self.play(FadeIn(g, shift=RIGHT * 0.2), run_time=1.2); self.wait(0.6)
        self.finish(5); self.clear_body()

        # 6 — tiêu chuẩn bậc nhất
        self.section('Tiêu chuẩn bậc nhất: tiếp tuyến nằm dưới đồ thị'); self.line(6)
        ax = axes([-2.5, 3.5, 1], [-0.5, 5, 1], 6.4, 4.8, LEFT * 3.1 + DOWN * 0.45)
        x0 = ValueTracker(-2)
        tl_ = lambda x: FC(x0.get_value()) + 0.7 * (x0.get_value() - 0.5) * (x - x0.get_value())
        tan = always_redraw(lambda: VGroup(ax.plot(tl_, x_range=[x0.get_value() - 1.8 / np.hypot(1, 0.7 * (x0.get_value() - 0.5)), x0.get_value() + 1.8 / np.hypot(1, 0.7 * (x0.get_value() - 0.5))], color=O, stroke_width=3.5),
                                           Dot(ax.c2p(x0.get_value(), FC(x0.get_value())), color=O, radius=0.09)))
        P_ = panel(M(r'f(\mathbf{y})\geq f(\mathbf{x})+\nabla f(\mathbf{x})^{\top}(\mathbf{y}-\mathbf{x})', 32)).move_to(RIGHT * 3.6 + UP * 1.2)
        self.play(Create(ax), Create(ax.plot(FC, x_range=[-2.5, 3.5], color=B, stroke_width=4)), FadeIn(P_), FadeIn(VT('với mọi x, y', 24).next_to(P_, DOWN, buff=0.35)), run_time=1.2)
        self.add(tan)
        self.play(x0.animate.set_value(3), run_time=self.slots[6] - 2.2, rate_func=smooth)
        tan.clear_updaters(); self.finish(6); self.clear_body()

        # 7 — tiêu chuẩn bậc hai
        self.section('Tiêu chuẩn bậc hai'); self.line(7)
        rows_ = VGroup(M(r'f\ \text{lồi}\ \ \Leftrightarrow\ \ \nabla^2 f(\mathbf{x})\succeq 0\quad\forall\mathbf{x}', 40, INK),
                       M(r'\nabla^2 f(\mathbf{x})\succ 0\quad\forall\mathbf{x}\ \ \Rightarrow\ \ f\ \text{lồi ngặt}', 40, B),
                       M(r'f\ \text{lồi mạnh tham số}\ m\ \ \Leftrightarrow\ \ \nabla^2 f(\mathbf{x})\succeq m\mathbf{I}\quad\forall\mathbf{x}', 40, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 1.1)
        for r_ in rows_:
            self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=1); self.wait(1.4)
        a_ = axes([-1.5, 1.5, 0.5], [-1, 28, 10], 4.0, 2.4, LEFT * 3.3 + DOWN * 2.05, nums=False)
        self.play(Create(a_), Create(a_.plot(lambda x: 12 * x ** 2, x_range=[-1.5, 1.5], color=B, stroke_width=4)),
                  FadeIn(VGroup(VT('Phản ví dụ: f = x⁴', 24, B), VT("f″ = 12x² ≥ 0 nhưng bằng 0 tại x = 0", 22), VT('→ lồi ngặt, không lồi mạnh', 22, O))
                                .arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(a_, RIGHT, buff=0.7)), run_time=1.5)
        self.finish(7); self.clear_body()

        # 8 — phép toán bảo toàn tính lồi
        self.section('Các phép toán bảo toàn tính lồi'); self.line(8)
        rows = [('Phép toán', 'Phát biểu', 'Ví dụ trong học máy'), ('Nhân với số α ≥ 0', 'αf lồi', 'hệ số điều chuẩn λ ≥ 0'), ('Tổng', 'f + g lồi', 'mất mát + điều chuẩn'),
                ('Hợp với ánh xạ afin', 'f(Ax + b) lồi', '‖Xw − y‖₂²'), ('Lấy cực đại', 'max(f, g) lồi', 'mất mát bản lề (SVM)'), ('Mọi chuẩn', '‖·‖ lồi', 'điều chuẩn ℓ₁, ℓ₂')]
        cols = [-5.9, -1.6, 1.9]; tb = VGroup()
        for k, r_ in enumerate(rows):
            y = 1.9 - 0.82 * k
            tb.add(VGroup(*[VT(s_, 25, B if k == 0 else INK, BOLD if k == 0 else NORMAL).move_to([x, y, 0], aligned_edge=LEFT) for x, s_ in zip(cols, r_)]))
        tb.add(Line([-6.0, 1.5, 0], [6.3, 1.5, 0], color=GRIDC, stroke_width=2))
        self.play(FadeIn(tb[0]), Create(tb[-1]), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in tb[1:6]], lag_ratio=0.75), run_time=5.2)
        self.finish(8); self.clear_body()

        # 9 — Ví dụ 2.3: ridge lồi mạnh
        self.section('Ví dụ 2.3: hàm mất mát ridge là lồi mạnh'); self.line(9)
        r = np.random.default_rng(1); x = r.normal(size=30); X = np.c_[x, x]; y = 1.5 * x + r.normal(0, 0.3, 30)
        A0, bb, cc = X.T @ X, X.T @ y, y @ y
        ax = axes([-1, 3, 1], [-1, 3, 1], 4.9, 4.9, LEFT * 3.6 + DOWN * 0.45)

        def J(w1, w2, lam):
            w = np.array([w1, w2]); return w @ (A0 + lam * np.eye(2)) @ w - 2 * bb @ w + cc

        def level_set(lam):
            jmin = cc - bb @ np.linalg.pinv(A0 + lam * np.eye(2)) @ bb
            return VGroup(*[ax.plot_implicit_curve(lambda a_, b_, l=l: J(a_, b_, lam) - jmin - l, color=B, stroke_width=1.8) for l in (1.5, 5, 12, 25, 45)])
        cur = level_set(0)
        txt = VGroup(VT('X có hai cột trùng nhau ⇒ XᵀX suy biến', 24), M(r'\nabla^2 J=2\mathbf{X}^{\top}\mathbf{X}+2\lambda\mathbf{I}\succeq 2\lambda\mathbf{I}\succ 0', 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 2.9 + UP * 1.4)
        self.play(Create(ax), Create(cur), FadeIn(txt[0]), run_time=1.5)
        lamt = VT('λ = 0', 30, O).move_to(RIGHT * 2.0 + DOWN * 0.4, aligned_edge=LEFT)
        note = VT('λ = 0: thung lũng phẳng, vô số nghiệm', 24, R).move_to(RIGHT * 0.5 + DOWN * 1.3, aligned_edge=LEFT)
        self.play(FadeIn(txt[1]), FadeIn(lamt), FadeIn(note), run_time=1.2); self.wait(1.3)
        star = None
        for lam in (0.5, 1.5, 3.0):
            w = np.linalg.solve(A0 + lam * np.eye(2), bb); new = level_set(lam)
            nl = VT(f'λ = {vn(lam, 1)}', 30, O).move_to(lamt, aligned_edge=LEFT)
            ns = Star(5, outer_radius=0.17, color=T, fill_opacity=1).move_to(ax.c2p(*w))
            anims = [Transform(cur, new), Transform(lamt, nl), Transform(star, ns) if star else FadeIn(ns)]
            if lam == 0.5: anims.append(Transform(note, VT('λ > 0: lồi mạnh, nghiệm duy nhất ★', 24, T).move_to(note, aligned_edge=LEFT)))
            self.play(*anims, run_time=1.6)
            if star is None: star = ns
            self.wait(0.6)
        self.finish(9); self.clear_body()

        # 10 — bài toán tối ưu lồi
        self.section('Bài toán tối ưu lồi'); self.line(10)
        P_ = panel(row('$\\min\\ f_0(\\mathbf{x})$', 'v.đ.k.', '$f_i(\\mathbf{x})\\leq 0$', '(lồi),', '$h_j(\\mathbf{x})=0$', '(afin)', size=30, buff=0.25)).move_to(UP * 1.5)
        self.play(FadeIn(P_), run_time=1)
        self.wait(2.5)
        th = panel(VT('Định lý: mọi cực tiểu địa phương đều là cực tiểu toàn cục', 30, T, BOLD), color=T).move_to(DOWN * 0.1)
        self.play(FadeIn(th, scale=0.95), run_time=1); self.wait(2)
        self.play(FadeIn(VT('f₀ lồi ngặt ⇒ nghiệm tối ưu (nếu tồn tại) là duy nhất', 26).move_to(DOWN * 1.5)), run_time=1)
        self.finish(10); self.clear_body()

        # 11 — ý chứng minh
        self.section('Ý chứng minh'); self.line(11)
        f = lambda x: 0.25 * (x - 2.5) ** 2 + 0.5; xs_, xb = 0.0, 3.0
        ax = axes([-1, 4.5, 1], [0, 4, 1], 6.0, 4.6, LEFT * 3.1 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(f, x_range=[-1, 4.5], color=B, stroke_width=4)), run_time=1.2)
        self.play(Create(Line(ax.c2p(xs_, f(xs_)), ax.c2p(xb, f(xb)), color=O, stroke_width=3)), Create(DashedLine(ax.c2p(-1, f(xs_)), ax.c2p(4.5, f(xs_)), color=R, stroke_width=2)),
                  FadeIn(Dot(ax.c2p(xs_, f(xs_)), color=R, radius=0.1)), FadeIn(VT('x* (giả sử cực tiểu địa phương)', 18, R).next_to(ax.c2p(xs_, f(xs_)), UR, buff=0.15)),
                  FadeIn(Dot(ax.c2p(xb, f(xb)), color=T, radius=0.1)), FadeIn(VT('x: f(x) < f(x*)', 18, T).next_to(ax.c2p(xb, f(xb)), DOWN, buff=0.3)), run_time=1.2)
        tv = ValueTracker(0.15)
        xt = lambda: tv.get_value() * xs_ + (1 - tv.get_value()) * xb
        pt = always_redraw(lambda: Dot(ax.c2p(xt(), f(xt())), color=O, radius=0.1))
        tl = always_redraw(lambda: VT(f't = {vn(tv.get_value())}: xₜ tiến sát x*', 24, O).move_to(RIGHT * 0.6 + DOWN * 0.3, aligned_edge=LEFT))
        rt = VGroup(M(r'\mathbf{x}_t=t\mathbf{x}^*+(1-t)\mathbf{x}', 34), M(r'f(\mathbf{x}_t)\leq t f(\mathbf{x}^*)+(1-t)f(\mathbf{x})<f(\mathbf{x}^*)', 32)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(RIGHT * 0.6 + UP * 1.2, aligned_edge=LEFT)
        self.play(FadeIn(rt), FadeIn(pt), FadeIn(tl), run_time=1)
        self.play(tv.animate.set_value(0.95), run_time=4.5, rate_func=smooth)
        pt.clear_updaters(); tl.clear_updaters()
        self.play(FadeIn(VT('→ mâu thuẫn với tính\n   cực tiểu địa phương  ◻', 24, T).move_to(RIGHT * 0.6 + DOWN * 1.4, aligned_edge=LEFT)), run_time=0.8)
        self.finish(11); self.clear_body()

        # 12 — lồi vs phi lồi trong học máy
        self.section('Vì sao học máy ưa chuộng hàm mất mát lồi'); self.line(12)
        for k, (fn, lab, c) in enumerate([(lambda x: 0.4 * x ** 2, 'Lồi: hồi quy tuyến tính, logistic, SVM', T),
                                          (lambda x: 0.25 * x ** 2 + np.sin(3 * x) + 0.4 * np.cos(7 * x), 'Phi lồi: mạng nơ-ron sâu', O)]):
            a_ = axes([-3, 3, 1], [-2, 4, 1], 5.6, 3.8, RIGHT * (3.3 * (2 * k - 1)) + DOWN * 0.1, nums=False)
            self.play(Create(a_), Create(a_.plot(fn, x_range=[-3, 3], color=c, stroke_width=4)), FadeIn(VT(lab, 22, c).next_to(a_, UP, buff=0.2)), run_time=1.6)
            self.wait(1.4)
        self.play(FadeIn(VT('Lồi: tìm được điểm dừng là có nghiệm tốt nhất', 26).move_to(DOWN * 2.6)), run_time=1)
        self.finish(12); self.clear_body()

        # 13 — LP, QP
        self.section('Quy hoạch tuyến tính và quy hoạch toàn phương'); self.line(13)
        ax = axes([-0.5, 4, 1], [-0.5, 4, 1], 4.9, 4.9, LEFT * 3.6 + DOWN * 0.45)
        V = np.array([[0, 0], [3, 0], [3, 1.2], [1.6, 3], [0, 2.5]]); cvec = np.array([-1.0, -1.4]); vals = V @ cvec
        poly = Polygon(*[ax.c2p(*p) for p in V], color=B, fill_opacity=0.2, stroke_width=3)
        lp = VGroup(panel(row('LP:', '$\\min\\ \\mathbf{c}^{\\top}\\mathbf{x}$', 'v.đ.k.', '$\\mathbf{Ax}\\leq\\mathbf{b}$', size=26)),
                    panel(row('QP:', '$\\min\\ \\tfrac{1}{2}\\mathbf{x}^{\\top}\\mathbf{Px}+\\mathbf{q}^{\\top}\\mathbf{x}$,', '$\\mathbf{P}\\succeq 0$', size=26)),
                    VT('SVM lề cứng là một QP (Bài 6)', 24, T)).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.1 + UP * 1.1)
        self.play(Create(ax), FadeIn(poly), FadeIn(lp[0]), run_time=1)
        lv = ValueTracker(-0.5)

        def lvl():
            xs = np.array([-0.5, 4]); ys = (lv.get_value() - cvec[0] * xs) / cvec[1]
            if ys[1] < -0.5: xs[1] = (lv.get_value() - cvec[1] * -0.5) / cvec[0]; ys[1] = -0.5
            if ys[0] > 4: xs[0] = (lv.get_value() - cvec[1] * 4) / cvec[0]; ys[0] = 4
            return DashedLine(ax.c2p(xs[0], ys[0]), ax.c2p(xs[1], ys[1]), color=O, stroke_width=3)
        ll = always_redraw(lvl)
        self.play(FadeIn(ll), FadeIn(lp[1:]), FadeIn(VT('đường mức cᵀx = hằng số trượt\ntới đỉnh tối ưu của đa giác', 22).move_to(RIGHT * 3.1 + DOWN * 1.4)), run_time=1)
        self.play(lv.animate.set_value(vals.min()), run_time=3.5, rate_func=smooth)
        ll.clear_updaters(); best = V[np.argmin(vals)]
        self.play(FadeIn(Star(5, outer_radius=0.2, color=T, fill_opacity=1).move_to(ax.c2p(*best))), FadeIn(VT('nghiệm tại một đỉnh', 20, T).next_to(ax.c2p(*best), UR, buff=0.15)), run_time=0.8)
        self.finish(13); self.clear_body()

        self.section('Tóm tắt'); self.line(14)
        lst = bullets(['Tập lồi chứa trọn đoạn thẳng; giao các tập lồi vẫn lồi', 'Hàm lồi: dây cung trên đồ thị, tiếp tuyến dưới đồ thị',
                       'Kiểm tra: ∇²f ⪰ 0, hoặc dùng phép toán bảo toàn tính lồi', 'Bài toán lồi: cực tiểu địa phương = toàn cục', 'LP và QP là hai lớp bài toán lồi chuẩn'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(14); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
