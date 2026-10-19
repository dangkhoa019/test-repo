"""Bài 6 - Nhân tử Lagrange, tính đối ngẫu và điều kiện KKT (Manim)."""
import itertools
from common import *

# ---------- SVM lề cứng: nghiệm chính xác bằng cách duyệt tập véc tơ hỗ trợ ----------
r = np.random.default_rng(11)
XP = r.normal([2.0, 2.2], 0.55, (14, 2)); XN = r.normal([-0.2, 0.0], 0.55, (14, 2))
XS = np.vstack([XP, XN]); YS = np.r_[np.ones(14), -np.ones(14)]


def svm_hard(X, y):
    best = None; P, N = X[y > 0], X[y < 0]; cands = []
    for p, q in itertools.product(P, N): cands.append((p - q, (p + q) / 2))
    for A, Bc in [(P, N), (N, P)]:
        for (a1, a2), c in itertools.product(itertools.combinations(A, 2), Bc):
            d = a2 - a1; n = np.array([-d[1], d[0]])
            if (c - a1) @ n > 0: n = -n
            n = n if (A is P) else -n
            off = ((c - a1) @ n) / 2; cands.append((n, a1 + n / np.linalg.norm(n) ** 2 * off))
    for n, x0 in cands:
        u = n / np.linalg.norm(n); s = y * ((X - x0) @ u)
        if s.min() > 1e-9 and (best is None or s.min() > best[0]): best = (s.min(), u, x0)
    m, u, x0 = best; w = u / m
    return w, -w @ x0


W, B0 = svm_hard(XS, YS); SV = np.abs(YS * (XS @ W + B0) - 1) < 1e-6


class Bai(Lesson):
    LESSON = 'video_bai06'; LABEL = 'BÀI 6 · NHÂN TỬ LAGRANGE, TÍNH ĐỐI NGẪU VÀ ĐIỀU KIỆN KKT'; TEXTS = load_texts('video_bai06')
    MINS = {0: 5}

    def circles(self, ax, lv=(0.5, 1, 2, 3, 4.5, 6.5)):
        return VGroup(*[ax.plot_implicit_curve(lambda x, y, r2=r2: x * x + y * y - r2, color=GRIDC, stroke_width=2) for r2 in lv])

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 6. Lagrange, đối ngẫu và KKT', 44, WHITE, BOLD),
                   M(r'\nabla f(\mathbf{x}^*)+\lambda\,\nabla h(\mathbf{x}^*)=\mathbf{0}', 50, O), VT('Chương 2 · Một số bài toán tối ưu', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–4 — ràng buộc đẳng thức, nhân tử Lagrange, Ví dụ 2.4
        self.section('Ràng buộc đẳng thức và nhân tử Lagrange'); self.line(1)
        XR, YR = [-1.5, 3], [-1.5, 3]
        ax = axes([*XR, 1], [*YR, 1], 5.0, 5.0, LEFT * 3.7 + DOWN * 0.45)
        circ = self.circles(ax)
        p1, p2 = seg_in_box(np.array([1, 1]), 2, XR, YR)
        cons = Line(ax.c2p(*p1), ax.c2p(*p2), color=O, stroke_width=4)
        self.play(Create(ax), FadeIn(circ), Create(cons), FadeIn(M('x_1+x_2=2', 28, O).next_to(ax.c2p(2.6, -0.6), RIGHT, buff=0.1).shift(UP * 0.3)), run_time=1.3)
        A_, B_ = np.array([2.6, -0.6]), np.array([-0.4, 2.4]); s = ValueTracker(0.5)
        pp = lambda: A_ + (B_ - A_) * s.get_value()
        mov = always_redraw(lambda: VGroup(Dot(ax.c2p(*pp()), color=B, radius=0.11),
                                           Arrow(ax.c2p(*pp()), ax.c2p(*(pp() - pp() / np.linalg.norm(pp()) * 0.7)), buff=0, color=R, stroke_width=5, max_tip_length_to_length_ratio=0.35)))
        txt = VGroup(VT('−∇f chỉ về gốc, nhưng điểm phải', 24), VT('nằm trên đường ràng buộc', 24)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 0.3 + UP * 1.6, aligned_edge=LEFT)
        fv = always_redraw(lambda: VT(f'f = x₁² + x₂² = {vn(pp() @ pp())}', 26, B).move_to(RIGHT * 0.3 + UP * 0.5, aligned_edge=LEFT))
        self.play(FadeIn(mov), FadeIn(txt), FadeIn(fv), run_time=0.8)
        self.play(s.animate.set_value(0.0), run_time=2, rate_func=smooth)
        self.play(s.animate.set_value(0.95), run_time=3.2, rate_func=smooth)
        mov.clear_updaters(); fv.clear_updaters(); self.finish(1)

        self.line(2)
        tangent = Circle(radius=np.sqrt(2) * (ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]), color=B, stroke_width=4).move_to(ax.c2p(0, 0))
        self.play(FadeOut(mov), FadeOut(txt), FadeOut(fv), Create(tangent), run_time=1.5)
        g1 = Arrow(ax.c2p(1, 1), ax.c2p(1.8, 1.8), buff=0, color=B, stroke_width=6); g2 = Arrow(ax.c2p(1, 1), ax.c2p(1.4, 1.4), buff=0, color=O, stroke_width=6)
        self.play(FadeIn(Dot(ax.c2p(1, 1), color=T, radius=0.12)), GrowArrow(g1), GrowArrow(g2),
                  FadeIn(M(r'\nabla f', 30, B).next_to(g1.get_end(), UR, buff=0.05)), FadeIn(M(r'\nabla h', 28, O).next_to(g2.get_end(), RIGHT, buff=0.15).shift(DOWN * 0.25)), run_time=1.2)
        P1 = panel(M(r'\nabla f(\mathbf{x}^*)+\lambda\nabla h(\mathbf{x}^*)=\mathbf{0},\ \ h(\mathbf{x}^*)=0', 32)).move_to(RIGHT * 3.0 + UP * 2.1)
        self.play(FadeIn(P1), run_time=0.8); self.finish(2)

        self.line(3)
        self.play(FadeIn(M(r'L(\mathbf{x},\lambda)=f(\mathbf{x})+\lambda h(\mathbf{x})', 40, INK).move_to(RIGHT * 3.0 + UP * 1.0)), run_time=1)
        self.play(Indicate(P1, color=T, scale_factor=1.04), run_time=1.2); self.finish(3)

        self.line(4)
        rows = VGroup(M(r'L=x_1^2+x_2^2+\lambda(x_1+x_2-2)', 34), M(r'2x_1+\lambda=0,\ \ 2x_2+\lambda=0', 34), M(r'x_1=x_2=-\lambda/2\ \Rightarrow\ -\lambda=2', 34),
                      M(r'\lambda=-2,\ \ \mathbf{x}^*=(1,1),\ \ f^*=2', 36, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 0.6 + DOWN * 1.35, aligned_edge=LEFT)
        self.play(FadeIn(VT('Ví dụ 2.4: min x₁² + x₂²,  x₁ + x₂ = 2', 22, O).move_to(RIGHT * 0.6 + UP * 0.35, aligned_edge=LEFT)), run_time=0.8)
        for r_ in rows:
            self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.9); self.wait(1.9)
        self.finish(4); self.clear_body()

        # 5 — hàm Lagrange tổng quát và hàm đối ngẫu
        self.section('Hàm Lagrange tổng quát và hàm đối ngẫu'); self.line(5)
        a_ = panel(M(r'L(\mathbf{x},\lambda,\nu)=f_0(\mathbf{x})+\sum_i\lambda_i f_i(\mathbf{x})+\sum_j\nu_j h_j(\mathbf{x}),\quad \lambda_i\geq 0', 40)).move_to(UP * 1.4)
        b_ = panel(M(r'g(\lambda,\nu)=\inf_{\mathbf{x}}\ L(\mathbf{x},\lambda,\nu)', 44), color=B).move_to(DOWN * 0.3)
        c_ = VT('cận dưới đúng của một họ hàm afin  ⇒  g luôn lõm  ⇒  bài toán đối ngẫu luôn lồi', 24, T).move_to(DOWN * 1.8)
        self.play(FadeIn(a_), run_time=1); self.wait(2.5); self.play(FadeIn(b_), run_time=1); self.wait(2.5); self.play(FadeIn(c_), run_time=1)
        self.finish(5); self.clear_body()

        # 6 — đối ngẫu yếu / mạnh
        self.section('Đối ngẫu yếu và đối ngẫu mạnh'); self.line(6)
        top = VT('d* ≤ p*  (luôn đúng)', 30).move_to(UP * 2.1); self.play(FadeIn(top), run_time=0.6)
        g = lambda l: 3.2 - 0.55 * (l - 2.3) ** 2
        for k, (p, title, c) in enumerate([(3.2, '(a) Đối ngẫu mạnh: p* − d* = 0', T), (4.1, '(b) Có khoảng trống: p* − d* > 0', O)]):
            a_ = axes([-0.2, 4.2, 1], [-1, 5, 1], 5.2, 3.6, RIGHT * 3.3 * (2 * k - 1) + DOWN * 0.6, nums=False)
            self.play(Create(a_), Create(a_.plot(g, x_range=[0, 4], color=B, stroke_width=4)), Create(DashedLine(a_.c2p(-0.2, p), a_.c2p(4.2, p), color=O)),
                      FadeIn(Dot(a_.c2p(2.3, 3.2), color=T)), FadeIn(M('p^*', 30, O).next_to(a_.c2p(4.2, p), UP, buff=0.1)),
                      FadeIn(M(r'd^*=g(\lambda^*)', 26, T).next_to(a_.c2p(2.3, 3.2), DOWN, buff=0.3)), FadeIn(VT(title, 22, c).next_to(a_, UP, buff=0.15)), run_time=1.5)
            self.wait(0.6)
        self.finish(6); self.clear_body()

        # 7 — điều kiện Slater
        self.section('Điều kiện Slater'); self.line(7)
        ax = axes([-2, 2, 1], [-2, 2, 1], 4.6, 4.6, LEFT * 4.0 + DOWN * 0.45, nums=False)
        reg = Ellipse(width=2.6 * 1.2, height=2.0 * 1.2, color=B, fill_opacity=0.2, stroke_width=3).move_to(ax.c2p(0, 0))
        self.play(Create(ax), FadeIn(reg), run_time=1)
        self.play(FadeIn(Star(5, outer_radius=0.18, color=T, fill_opacity=1).move_to(ax.c2p(0.2, 0.1))), FadeIn(VT('điểm trong chặt: fᵢ(x) < 0', 20, T).next_to(ax.c2p(0.2, -1.2), DOWN, buff=0.2)), run_time=1)
        sl = VGroup(VT('Bài toán lồi', 28), VT('+ tồn tại x chấp nhận được\n   với fᵢ(x) < 0', 26), VT('⇒ đối ngẫu mạnh: d* = p*', 30, T, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 0.4 + UP * 0.2, aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(x_, shift=RIGHT * 0.2) for x_ in sl], lag_ratio=0.7), run_time=3)
        self.finish(7); self.clear_body()

        # 8–9 — KKT
        self.section('Điều kiện Karush – Kuhn – Tucker'); self.line(8)
        kk = [('1. Chấp nhận được (gốc)', r'f_i(\mathbf{x}^*)\leq 0,\ \ h_j(\mathbf{x}^*)=0', INK), ('2. Chấp nhận được (đối ngẫu)', r'\lambda_i^*\geq 0', INK),
              ('3. Điều kiện bù', r'\lambda_i^* f_i(\mathbf{x}^*)=0', O),
              ('4. Điều kiện dừng', r'\nabla f_0(\mathbf{x}^*)+\sum_i\lambda_i^*\nabla f_i(\mathbf{x}^*)+\sum_j\nu_j^*\nabla h_j(\mathbf{x}^*)=\mathbf{0}', INK)]
        G = VGroup()
        for k, (a_, b_, c) in enumerate(kk):
            y = 1.9 - 0.95 * k
            G.add(VGroup(VT(a_, 24, c, BOLD if c == O else NORMAL).move_to([-6.3, y, 0], aligned_edge=LEFT), M(b_, 34, c).move_to([-1.0, y, 0], aligned_edge=LEFT)))
        self.play(LaggedStart(*[FadeIn(g_, shift=RIGHT * 0.2) for g_ in G], lag_ratio=0.8), run_time=5); self.finish(8)
        self.line(9)
        self.play(Create(SurroundingRectangle(G[2], color=O, buff=0.15, corner_radius=0.1)), run_time=0.8)
        cs = VGroup(row('$\\lambda_i^*>0\\ \\Rightarrow\\ f_i(\\mathbf{x}^*)=0$', '(ràng buộc hoạt động)', color=O), row('$f_i(\\mathbf{x}^*)<0\\ \\Rightarrow\\ \\lambda_i^*=0$', '(ràng buộc không hoạt động)', color=T)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(DOWN * 2.2 + LEFT * 0.8)
        self.play(FadeIn(cs[0], shift=RIGHT * 0.2), run_time=1); self.wait(1.8); self.play(FadeIn(cs[1], shift=RIGHT * 0.2), run_time=1)
        self.finish(9); self.clear_body()

        # 10–11 — Ví dụ 2.5
        self.section('Ví dụ 2.5: ràng buộc hoạt động và không hoạt động'); self.line(10)
        XR, YR = [-2, 3], [-2, 3]
        sq = [(-2, -2), (3, -2), (3, 3), (-2, 3)]

        def case(c, pos, col, lab, xs, lam):
            a_ = axes([*XR, 1], [*YR, 1], 4.3, 4.3, pos, nums=False)
            R_ = Polygon(*[a_.c2p(*p) for p in clip_poly(sq, np.array([-1, -1]), -c)], color=col, fill_opacity=0.15, stroke_width=0)
            p1, p2 = seg_in_box(np.array([1, 1]), c, XR, YR)
            cc = self.circles(a_, (0.5, 1, 2, 3, 4.5))
            return VGroup(a_, cc, R_, Line(a_.c2p(*p1), a_.c2p(*p2), color=col, stroke_width=4), Star(5, outer_radius=0.17, color=R, fill_opacity=1).move_to(a_.c2p(*xs)),
                          VT(lab, 22, col).next_to(a_, UP, buff=0.12), M(rf'\mathbf{{x}}^*={xs},\ \ \lambda^*={lam}', 30).next_to(a_, DOWN, buff=0.2))
        L1 = case(2, LEFT * 3.4 + DOWN * 0.3, O, 'x₁ + x₂ ≥ 2: hoạt động', (1, 1), 2)
        self.play(FadeIn(L1[:4]), FadeIn(L1[5]), run_time=1.2)
        rr = VGroup(M(r'f_1(\mathbf{x})=2-x_1-x_2\leq 0', 32), M(r'L=x_1^2+x_2^2+\lambda(2-x_1-x_2)', 32), row('$\\lambda=0\\Rightarrow\\mathbf{x}=\\mathbf{0}$:', 'vi phạm ràng buộc ✗', color=R, size=24),
                    row('$\\lambda>0\\Rightarrow x_1+x_2=2\\Rightarrow\\lambda=2,\\ \\mathbf{x}^*=(1,1)$', '✓', color=T, size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(RIGHT * 0.4 + UP * 0.6, aligned_edge=LEFT)
        for r_ in rr:
            self.play(FadeIn(r_, shift=RIGHT * 0.2), run_time=0.9); self.wait(1.6)
        self.play(FadeIn(L1[4]), FadeIn(L1[6]), run_time=0.8)
        self.finish(10)
        self.line(11)
        L2 = case(-1, RIGHT * 3.4 + DOWN * 0.3, T, 'x₁ + x₂ ≥ −1: không hoạt động', (0, 0), 0)
        self.play(FadeOut(rr), run_time=0.5)
        self.play(FadeIn(L2[:4]), FadeIn(L2[5]), run_time=1.2); self.wait(1.5); self.play(FadeIn(L2[4]), FadeIn(L2[6]), run_time=0.8)
        self.finish(11); self.clear_body()

        # 12 — KKT đủ
        self.section('KKT: cần và đủ cho bài toán lồi'); self.line(12)
        g = VGroup(VT('Bài toán lồi  +  điều kiện Slater', 34), MathTex(r'\Downarrow', font_size=60, color=INK), VT('x* tối ưu  ⇔  (x*, λ*, ν*) thỏa KKT', 34, T, BOLD)).arrange(DOWN, buff=0.4).shift(DOWN * 0.2)
        self.play(FadeIn(g[0]), run_time=1); self.play(FadeIn(g[1]), run_time=0.6); self.play(FadeIn(g[2], scale=0.95), run_time=1)
        self.finish(12); self.clear_body()

        # 13–15 — SVM
        self.section('Ứng dụng: máy véc tơ hỗ trợ (SVM) lề cứng'); self.line(13)
        XR, YR = [-2, 4], [-1.8, 4]
        ax = axes([*XR, 1], [-2, 4, 1], 5.4, 5.4, LEFT * 3.6 + DOWN * 0.45, nums=False)
        pts = VGroup(*[Dot(ax.c2p(*p), color=B, radius=0.07) for p in XP], *[Dot(ax.c2p(*p), color=O, radius=0.07) for p in XN])
        leg = VGroup(row('●', 'yᵢ = +1', size=20, color=B), row('●', 'yᵢ = −1', size=20, color=O)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(ax.c2p(-1.0, 3.4))
        self.play(Create(ax), LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.03), FadeIn(leg), run_time=1.5)
        k = ValueTracker(0)

        def hyp():
            gg = VGroup()
            for off in (0, 1, -1):
                se = seg_in_box(W, off * k.get_value() - B0, XR, YR)
                if se is None: continue
                L_ = Line(ax.c2p(*se[0]), ax.c2p(*se[1]), color=WHITE, stroke_width=3 if off == 0 else 2)
                gg.add(L_ if off == 0 else DashedLine(L_.get_start(), L_.get_end(), color=LIGHT, stroke_width=2))
            return gg
        hp = always_redraw(hyp)
        P1 = panel(M(r'\min_{\mathbf{w},b}\ \tfrac{1}{2}\|\mathbf{w}\|_2^2\ \ \text{v.đ.k.}\ \ y_i(\mathbf{w}^{\top}\mathbf{x}_i+b)\geq 1', 32)).move_to(RIGHT * 3.2 + UP * 2.1)
        self.play(FadeIn(hp), FadeIn(P1), run_time=1)
        self.play(k.animate.set_value(1), run_time=4)
        hp.clear_updaters()
        self.play(FadeIn(M(rf'\text{{lề}}=2/\|\mathbf{{w}}\|_2={vn(2 / np.linalg.norm(W))}', 34).move_to(RIGHT * 3.2 + UP * 1.05)), run_time=0.8)
        self.finish(13)
        self.line(14)
        dual = MathTex(r'\max_{\alpha\succeq 0}\ \sum_i\alpha_i-\tfrac{1}{2}\sum_{i,j}\alpha_i\alpha_j y_i y_j\,', r'\mathbf{x}_i^{\top}\mathbf{x}_j', font_size=32, color=INK)
        P2 = panel(VGroup(dual,
                          M(r'\text{v.đ.k.}\ \ \sum_i\alpha_i y_i=0', 28)).arrange(DOWN, buff=0.2), color=B).move_to(RIGHT * 3.2 + DOWN * 0.3)
        self.play(FadeIn(P2), run_time=1)
        hl = SurroundingRectangle(dual[1], color=T, buff=0.06)
        self.play(Create(hl), run_time=0.8); self.finish(14)
        self.line(15)
        rings = VGroup(*[Circle(radius=0.2, color=R, stroke_width=4).move_to(ax.c2p(*p)) for p in XS[SV]])
        self.play(LaggedStart(*[Create(c_) for c_ in rings], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(VGroup(VT(f'{SV.sum()} véc tơ hỗ trợ (αᵢ > 0)', 26, R), row('$\\mathbf{w}^*=\\sum_i\\alpha_i^* y_i\\mathbf{x}_i$', 'chỉ gồm các điểm này', size=22))
                         .arrange(DOWN, buff=0.25).move_to(RIGHT * 3.2 + DOWN * 2.1)), run_time=1)
        self.finish(15); self.clear_body()

        self.section('Tóm tắt'); self.line(16)
        lst = bullets(['Lagrange: ràng buộc đẳng thức → điểm dừng của L(x, λ)', 'Hàm đối ngẫu luôn lõm; đối ngẫu yếu d* ≤ p*',
                       'Lồi + Slater ⇒ đối ngẫu mạnh; KKT vừa cần vừa đủ', 'Điều kiện bù: chỉ ràng buộc hoạt động có λ > 0', 'SVM: véc tơ hỗ trợ là các điểm có αᵢ > 0'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(16); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
