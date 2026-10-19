"""Bài 4 - Đạo hàm và bài toán cực trị không ràng buộc (Manim)."""
from common import *

F1 = lambda x: 0.3 * x ** 3 - x ** 2 + 0.4 * x + 2.2; D1 = lambda x: 0.9 * x ** 2 - 2 * x + 0.4; D2 = lambda x: 1.8 * x - 2
F3 = lambda x: 0.25 * x ** 4 - 0.5 * x ** 3 - 1.6 * x ** 2 + 1.2 * x + 3; D3 = lambda x: x ** 3 - 1.5 * x ** 2 - 3.2 * x + 1.2
CR = np.sort(np.roots([1, -1.5, -3.2, 1.2]).real)


def axes(xr, yr, w, h, pos, nums=True):
    return Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, axis_config={'color': LIGHT, 'include_numbers': nums, 'font_size': 18}).move_to(pos)


class Bai(Lesson):
    LESSON = 'video_bai04'; LABEL = 'BÀI 4 · ĐẠO HÀM VÀ BÀI TOÁN CỰC TRỊ KHÔNG RÀNG BUỘC'; TEXTS = load_texts('video_bai04')
    MINS = {1: 8.5, 8: 9}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 4. Đạo hàm và cực trị', 46, WHITE, BOLD),
                   M(r'\nabla f(\mathbf{x}^*)=\mathbf{0},\qquad\nabla^2 f(\mathbf{x}^*)\succ 0', 54, O), VT('Chương 2 · Một số bài toán tối ưu', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1 — đạo hàm = hệ số góc tiếp tuyến
        self.section('Đạo hàm: hệ số góc của tiếp tuyến'); self.line(1)
        ax = axes([-1.5, 4, 1], [-1.5, 4.5, 1], 6.6, 5.0, LEFT * 3 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(F1, x_range=[-1.3, 3.6], color=B, stroke_width=4)), run_time=1.2)
        x0 = ValueTracker(-1.0)
        tan = always_redraw(lambda: ax.plot(lambda x: F1(x0.get_value()) + D1(x0.get_value()) * (x - x0.get_value()), x_range=[x0.get_value() - 1, x0.get_value() + 1], color=O, stroke_width=4))
        dot = always_redraw(lambda: Dot(ax.c2p(x0.get_value(), F1(x0.get_value())), color=O, radius=0.09))
        arr = always_redraw(lambda: Arrow(ax.c2p(x0.get_value(), F1(x0.get_value()) - 0.7), ax.c2p(x0.get_value() - 0.7 * np.sign(D1(x0.get_value())), F1(x0.get_value()) - 0.7), buff=0, color=T))
        val = always_redraw(lambda: VT(f"f′(x) = {vn(D1(x0.get_value()))}", 34, O).shift(RIGHT * 3.6 + UP * 0.2))
        self.play(FadeIn(tan), FadeIn(dot), FadeIn(arr), FadeIn(val), FadeIn(panel(M(r"f'(x)=\lim_{h\to 0}\frac{f(x+h)-f(x)}{h}", 38)).shift(RIGHT * 3.6 + UP * 1.7)),
                  FadeIn(VT('mũi tên xanh: hướng làm f giảm (ngược dấu đạo hàm)', 20, T).shift(RIGHT * 3.6 + DOWN * 0.7)))
        self.play(x0.animate.set_value(3.5), run_time=self.slots[1] - 2.5, rate_func=smooth); self.finish(1); self.remove(tan, dot, arr, val); self.clear_body()

        # 2–3 — Taylor
        self.section('Khai triển Taylor'); self.line(2)
        ax = axes([-1.5, 4, 1], [-1.5, 4.5, 1], 6.6, 5.0, LEFT * 3 + DOWN * 0.45); x0 = 0.5
        self.play(Create(ax), Create(ax.plot(F1, x_range=[-1.3, 3.6], color=B, stroke_width=4)), FadeIn(Dot(ax.c2p(x0, F1(x0)), color=WHITE)))
        self.play(FadeIn(panel(M(r"f(x+h)\approx f(x)+f'(x)h+\tfrac{1}{2}f''(x)h^2", 34)).shift(RIGHT * 3.6 + UP * 1.6)))
        l1 = ax.plot(lambda x: F1(x0) + D1(x0) * (x - x0), x_range=[-1.5, 4], color=O, stroke_width=4)
        l2 = ax.plot(lambda x: F1(x0) + D1(x0) * (x - x0) + 0.5 * D2(x0) * (x - x0) ** 2, x_range=[-1.3, 2.7], color=T, stroke_width=4)
        self.play(Create(l1), FadeIn(VT('bậc nhất', 22, O).shift(RIGHT * 3.6 + UP * 0.4)), run_time=1.5)
        self.play(Create(l2), FadeIn(VT('bậc hai', 22, T).shift(RIGHT * 3.6 + UP * 0.0)), run_time=1.5); self.finish(2)
        self.line(3)
        self.play(FadeIn(panel(M(r'f(\mathbf{x}+\mathbf{h})\approx f(\mathbf{x})+\nabla f(\mathbf{x})^{\top}\mathbf{h}+\tfrac{1}{2}\mathbf{h}^{\top}\nabla^2 f(\mathbf{x})\,\mathbf{h}', 30), color=O).shift(RIGHT * 3.4 + DOWN * 1.3)))
        self.finish(3); self.clear_body()

        # 4–5 — đạo hàm theo hướng (Ví dụ 2.1)
        self.section('Đạo hàm theo hướng'); self.line(4)
        F = lambda x, y: x * x + 3 * x * y + 2 * y * y; x0 = np.array([1.0, 2.0]); g = np.array([8.0, 11.0])
        ax = axes([-0.5, 2.5, 0.5], [0.5, 3.5, 0.5], 5.4, 5.0, LEFT * 3.4 + DOWN * 0.45)
        lv = VGroup(*[ax.plot_implicit_curve(lambda x, y, c=c: F(x, y) - c, color=B, stroke_width=1.5) for c in np.arange(4, 60, 5)])
        self.play(Create(ax), Create(lv), FadeIn(Dot(ax.c2p(*x0), color=WHITE)), run_time=1.5)
        gn = g / np.linalg.norm(g)
        self.play(GrowArrow(Arrow(ax.c2p(*x0), ax.c2p(*(x0 + gn)), buff=0, color=O)), FadeIn(M(r'\nabla f', 32, O).move_to(ax.c2p(*(x0 + gn * 1.15)))))
        th = ValueTracker(np.radians(-30)); uu = lambda: np.array([np.cos(th.get_value()), np.sin(th.get_value())])
        ua = always_redraw(lambda: Arrow(ax.c2p(*x0), ax.c2p(*(x0 + 0.8 * uu())), buff=0, color=T))
        dv = always_redraw(lambda: VT(f'D_u f = {vn(g @ uu())}', 34, T).shift(RIGHT * 3.6 + UP * 0.4))
        self.play(FadeIn(ua), FadeIn(dv), FadeIn(panel(M(r'D_{\mathbf{u}}f(\mathbf{x})=\nabla f(\mathbf{x})^{\top}\mathbf{u}\leq\|\nabla f(\mathbf{x})\|_2', 34)).shift(RIGHT * 3.6 + UP * 1.6)),
                  FadeIn(VT(f'‖∇f‖₂ = √185 ≈ {vn(np.linalg.norm(g))}', 26, O).shift(RIGHT * 3.6 + DOWN * 0.3)))
        self.play(th.animate.set_value(np.radians(330)), run_time=self.slots[4] - 5.5, rate_func=linear); self.finish(4)
        self.line(5)
        self.play(th.animate.set_value(np.radians(360 + 53.13)), run_time=2)
        ex = VGroup(M(r'f=x_1^2+3x_1x_2+2x_2^2,\quad \mathbf{x}_0=(1,2)', 30), M(r'\nabla f=(2x_1+3x_2,\ 3x_1+4x_2)=(8,11)', 30),
                    M(r'\mathbf{u}=(3/5,\ 4/5):\ \ 8\cdot\tfrac35+11\cdot\tfrac45=\tfrac{68}{5}=13{,}6', 30, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 3.2 + DOWN * 1.5)
        self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.8), run_time=4); self.finish(5); self.remove(ua, dv); self.clear_body()

        # 6 — bài toán tối ưu tổng quát
        self.section('Bài toán tối ưu tổng quát'); self.line(6)
        P_ = panel(M(r'\min_{\mathbf{x}}\ f_0(\mathbf{x})\quad\text{v.đ.k.}\quad f_i(\mathbf{x})\leq 0,\ \ h_j(\mathbf{x})=0', 46)).shift(UP * 1.4)
        rows_ = VGroup(row('$f_0$', ': hàm mục tiêu (hàm mất mát)'), row('$f_i\\leq 0,\\ h_j=0$', ': các ràng buộc'),
                       row('$\\mathcal{X}=\\{\\mathbf{x}: f_i(\\mathbf{x})\\leq 0,\\ h_j(\\mathbf{x})=0\\}$', ': tập chấp nhận được'),
                       row('$\\max f\\ \\Leftrightarrow\\ \\min(-f)$', ': luôn phát biểu dạng cực tiểu', color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).shift(DOWN * 1.0)
        self.play(FadeIn(P_)); self.play(LaggedStart(*[FadeIn(r_) for r_ in rows_], lag_ratio=0.7), run_time=4); self.finish(6); self.clear_body()

        # 7–8 — cực tiểu địa phương / toàn cục
        self.section('Cực tiểu địa phương và toàn cục'); self.line(7)
        ax = axes([-2.7, 3.2, 1], [-3, 9.5, 2], 7.2, 5.0, LEFT * 2.6 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(F3, x_range=[-2.6, 3.1], color=B, stroke_width=4)), run_time=1.5)
        for x, lab, c, d in [(CR[0], 'cực tiểu địa phương', O, DOWN), (CR[1], 'cực đại địa phương', T, UP), (CR[2], 'cực tiểu toàn cục', R, DOWN)]:
            self.play(FadeIn(Dot(ax.c2p(x, F3(x)), color=c, radius=0.09)), FadeIn(VT(lab, 20, c).next_to(ax.c2p(x, F3(x)), d, buff=0.25)), run_time=0.8)
        self.play(FadeIn(M(r'f(x)=0{,}25x^4-0{,}5x^3-1{,}6x^2+1{,}2x+3', 28, LIGHT).shift(RIGHT * 4.2 + UP * 1.5)))
        self.finish(7)
        self.line(8)
        def gd(x0):
            P = [x0]
            for _ in range(60): P.append(P[-1] - 0.05 * D3(P[-1]))
            return P
        balls = VGroup()
        for x0, c in [(-2.5, O), (1.0, R)]:
            b = Dot(ax.c2p(x0, F3(x0)), color=c, radius=0.16).set_fill(opacity=0).set_stroke(c, 4); balls.add(b); self.add(b)
        paths = [gd(-2.5), gd(1.0)]
        k = ValueTracker(0)
        for b, P in zip(balls, paths): b.add_updater(lambda m, P=P: m.move_to(ax.c2p(P[int(k.get_value())], F3(P[int(k.get_value())]))))
        info = VGroup(VT('Giảm gradient từ hai điểm xuất phát:', 22), VT(f'x₀ = −2,5  →  {vn(CR[0])} (mắc kẹt)', 22, O), VT(f'x₀ = 1,0  →  {vn(CR[2])} (toàn cục)', 22, R),
                      VT('→ lý do bài toán lồi (Bài 5) quan trọng', 22, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 4.3 + DOWN * 0.5)
        self.play(k.animate.set_value(60), FadeIn(info[:3]), run_time=5, rate_func=linear)
        for b in balls: b.clear_updaters()
        self.play(FadeIn(info[3])); self.finish(8); self.clear_body()

        # 9–10 — điều kiện cần bậc nhất
        self.section('Điều kiện cần bậc nhất'); self.line(9)
        P_ = panel(M(r'\mathbf{x}^*\ \text{cực tiểu địa phương},\ f\in C^1\ \Rightarrow\ \nabla f(\mathbf{x}^*)=\mathbf{0}', 42)).shift(UP * 1.6)
        steps = VGroup(row('1. Giả sử', '$\\nabla f(\\mathbf{x}^*)\\neq\\mathbf{0}$', ', chọn hướng', '$\\mathbf{h}=-\\nabla f(\\mathbf{x}^*)$'),
                       row('2. Taylor:', '$f(\\mathbf{x}^*+t\\mathbf{h})\\approx f(\\mathbf{x}^*)-t\\|\\nabla f(\\mathbf{x}^*)\\|_2^2<f(\\mathbf{x}^*)$'),
                       row('3. Mâu thuẫn với giả thiết x* là cực tiểu địa phương  ◻', color=T)).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.7)
        self.play(FadeIn(P_)); self.play(LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.8), run_time=4.5); self.finish(9); self.clear_body()
        self.line(10)
        ax = axes([-1.6, 1.6, 0.5], [-3, 3, 1], 5.6, 4.8, LEFT * 3.2 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(lambda x: x ** 3, x_range=[-1.44, 1.44], color=B, stroke_width=4)))
        self.play(Create(Line(ax.c2p(-0.8, 0), ax.c2p(0.8, 0), color=O, stroke_width=5)), FadeIn(Dot(ax.c2p(0, 0), color=O, radius=0.1)))
        self.play(FadeIn(VGroup(row("$f(x)=x^3$:", "$f'(0)=0$", 'nhưng 0 không là cực trị', color=O), VT('∇f = 0 chỉ là điều kiện CẦN', 28), VT('→ cần kiểm tra thêm bằng đạo hàm bậc hai', 24, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(RIGHT * 3.0)))
        self.finish(10); self.clear_body()

        # 11–12 — điều kiện bậc hai
        self.section('Điều kiện bậc hai: phân loại điểm dừng'); self.line(11)
        P_ = panel(M(r'f(\mathbf{x}^*+\mathbf{h})\approx f(\mathbf{x}^*)+\tfrac{1}{2}\,\mathbf{h}^{\top}\nabla^2 f(\mathbf{x}^*)\,\mathbf{h}', 44)).shift(UP * 1.8)
        expl = VGroup(row('$\\mathbf{h}^\\top\\nabla^2 f\\,\\mathbf{h}>0$', 'với mọi h ≠ 0  ⇒  f tăng theo mọi hướng', color=T),
                      row('$\\mathbf{h}^\\top\\nabla^2 f\\,\\mathbf{h}<0$', 'với mọi h ≠ 0  ⇒  f giảm theo mọi hướng', color=B),
                      row('đổi dấu theo hướng  ⇒  vừa tăng vừa giảm', color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).shift(DOWN * 0.4)
        self.play(FadeIn(P_)); self.play(LaggedStart(*[FadeIn(e) for e in expl], lag_ratio=0.8), run_time=4); self.finish(11)
        self.line(12)
        self.play(FadeOut(expl))
        cases = [(lambda x, y: x * x + y * y, 'xác định dương\n→ cực tiểu ngặt', T), (lambda x, y: -x * x - y * y, 'xác định âm\n→ cực đại ngặt', B),
                 (lambda x, y: x * x - y * y, 'không xác định dấu\n→ yên ngựa', O), (lambda x, y: x * x + y ** 4, 'suy biến, vd x₁² + x₂⁴\n→ chưa kết luận', LIGHT)]
        grp = VGroup()
        for f_, lab, c in cases:
            ax = Axes(x_range=[-1.5, 1.5], y_range=[-1.5, 1.5], x_length=2.6, y_length=2.6, axis_config={'color': GRIDC})
            lvls = [0.15, 0.4, 0.8, 1.3, 1.9] if f_(1, 0) > 0 and f_(0, 1) > 0 else ([-0.15, -0.4, -0.8, -1.3, -1.9] if f_(1, 0) < 0 else [-1.2, -0.6, -0.2, 0.2, 0.6, 1.2])
            curves = VGroup(*[ax.plot_implicit_curve(lambda x, y, l=l: f_(x, y) - l, color=c, stroke_width=1.8) for l in lvls])
            grp.add(VGroup(VGroup(ax, curves, Dot(ax.c2p(0, 0), radius=0.05)), VT(lab, 18, c)).arrange(DOWN, buff=0.15))
        grp.arrange(RIGHT, buff=0.4).shift(DOWN * 1.1)
        self.play(LaggedStart(*[FadeIn(g_, shift=UP * 0.2) for g_ in grp], lag_ratio=0.6), run_time=5); self.finish(12); self.clear_body()

        # 13–15 — Ví dụ 2.2
        self.section('Ví dụ 2.2: tìm và phân loại điểm dừng'); self.line(13)
        F = lambda x, y: x * x + y ** 3 - 3 * y
        ax = Axes(x_range=[-2, 2, 1], y_range=[-2.2, 2.2, 1], x_length=4.8, y_length=5.2, axis_config={'color': LIGHT, 'include_numbers': True, 'font_size': 18}).shift(LEFT * 3.6 + DOWN * 0.4)
        lv = VGroup(*[ax.plot_implicit_curve(lambda x, y, c=c: F(x, y) - c, color=B, stroke_width=1.5) for c in np.linspace(-3, 5, 17)])
        self.play(Create(ax), Create(lv), run_time=2)
        ex = VGroup(M(r'f=x_1^2+x_2^3-3x_2', 40), M(r'\nabla f=(2x_1,\ 3x_2^2-3)=\mathbf{0}', 36), M(r'\Rightarrow (0,1)\ \text{và}\ (0,-1)', 36)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 2.8 + UP * 1.3)
        self.play(LaggedStart(*[FadeIn(e) for e in ex], lag_ratio=0.8), run_time=3.5)
        self.play(FadeIn(Dot(ax.c2p(0, 1), color=T, radius=0.11)), FadeIn(Dot(ax.c2p(0, -1), color=O, radius=0.11))); self.finish(13)
        self.line(14)
        cl = VGroup(M(r'\nabla^2 f=\mathrm{diag}(2,\ 6x_2)', 36), M(r'(0,1):\ \mathrm{diag}(2,6)\succ 0\ \to\ \text{cực tiểu ngặt}', 32, T), M(r'(0,-1):\ \mathrm{diag}(2,-6)\ \to\ \text{yên ngựa}', 32, O)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ex, DOWN, buff=0.45, aligned_edge=LEFT)
        self.play(FadeIn(cl[0])); self.wait(1.5); self.play(FadeIn(cl[1]), Flash(ax.c2p(0, 1), color=T)); self.wait(2.5); self.play(FadeIn(cl[2]), Flash(ax.c2p(0, -1), color=O))
        self.finish(14); self.clear_body()
        self.line(15)
        ax = axes([-3, 2.5, 1], [-15, 8, 5], 6.0, 5.0, LEFT * 3.2 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(lambda x: x ** 3 - 3 * x, x_range=[-2.85, 2.4], color=B, stroke_width=4)), FadeIn(Dot(ax.c2p(1, -2), color=T)), FadeIn(Dot(ax.c2p(-1, 2), color=O)))
        self.play(GrowArrow(Arrow(ax.c2p(-2.2, -4), ax.c2p(-2.8, -11), buff=0, color=R)))
        self.play(FadeIn(VGroup(M(r'f(0,x_2)=x_2^3-3x_2\to-\infty', 36, R), M(r'\text{khi}\ x_2\to-\infty', 34, R), VT('→ không có cực tiểu toàn cục', 26), VT('(0, 1) chỉ là cực tiểu địa phương', 22, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.35).shift(RIGHT * 3.4)))
        self.finish(15); self.clear_body()

        self.section('Tóm tắt'); self.line(16)
        items = ['Taylor bậc hai: công cụ phân tích hàm quanh một điểm', 'D_u f = ∇fᵀu; gradient chỉ hướng tăng nhanh nhất', '∇f(x*) = 0 là điều kiện cần (điểm dừng)',
                 'Hessian: ≻ 0 cực tiểu, ≺ 0 cực đại, không xác định dấu: yên ngựa', 'Phi lồi: có thể mắc kẹt ở cực tiểu địa phương']
        lst = VGroup(*[VT('✓  ' + s_, 28) for s_ in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.42).shift(DOWN * 0.2)
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(16); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
