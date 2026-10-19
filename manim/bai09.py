"""Bài 9 - Giải thuật giảm gradient (Manim)."""
from common import *

J1 = lambda w: (w - 3) ** 2; dJ1 = lambda w: 2 * (w - 3)


def gd1(w0, eta, n):
    ws = [w0]
    for _ in range(n): ws.append(ws[-1] - eta * dJ1(ws[-1]))
    return np.array(ws)


WS = gd1(0.0, 0.1, 12)
A2 = np.array([1.0, 4.0]); C2 = np.array([2.4, 1.1])


def path2(w0, eta, n, a=A2, c=C2):
    P = [np.array(w0, float)]
    for _ in range(n): P.append(P[-1] - eta * a * (P[-1] - c))
    return np.array(P)


P2 = path2([-0.5, 2.9], 0.22, 18)
ETAS = [(0.05, 'η = 0,05 — quá nhỏ', T), (0.3, 'η = 0,3 — hợp lý', B), (1.05, 'η = 1,05 — quá lớn', O)]

rng = np.random.default_rng(0); NS = 1000
Xs = rng.normal(size=NS); Ys = 1.5 - 2.0 * Xs + rng.normal(scale=0.8, size=NS)
Xd = np.c_[np.ones(NS), Xs]; WSTAR = np.linalg.lstsq(Xd, Ys, rcond=None)[0]
SXX, SXY, SYY = Xd.T @ Xd / NS, Xd.T @ Ys / NS, Ys @ Ys / NS


def gd_var(bs, steps=45, eta=0.08, seed=1):
    r = np.random.default_rng(seed); w = np.array([-1.5, 1.0]); P = [w.copy()]
    for _ in range(steps):
        idx = np.arange(NS) if bs is None else r.choice(NS, bs, replace=False)
        g = 2 / len(idx) * Xd[idx].T @ (Xd[idx] @ w - Ys[idx]); w = w - eta * g; P.append(w.copy())
    return np.array(P)


VARS = [(gd_var(None), 'Theo lô (n mẫu)', B), (gd_var(1), 'Ngẫu nhiên — SGD (1 mẫu)', O), (gd_var(32), 'Lô nhỏ (32 mẫu)', T)]


def ellipses(ax, a, c, levels, color=B, sw=2):
    ux = ax.c2p(1, 0)[0] - ax.c2p(0, 0)[0]; uy = ax.c2p(0, 1)[1] - ax.c2p(0, 0)[1]
    return VGroup(*[Ellipse(width=2 * np.sqrt(2 * l / a[0]) * ux, height=2 * np.sqrt(2 * l / a[1]) * uy, color=color, stroke_width=sw).move_to(ax.c2p(*c)) for l in levels])


def trail(ax, P, u, color):
    """Quỹ đạo tới 'thời điểm' u (số bước, có thể lẻ)."""
    i = int(min(u, len(P) - 2)); f = min(1.0, u - i); cur = P[i] + (P[i + 1] - P[i]) * f
    pts = [ax.c2p(*p) for p in P[:i + 1]] + [ax.c2p(*cur)]
    g = VGroup(VMobject(color=color, stroke_width=3).set_points_as_corners(pts if len(pts) > 1 else pts * 2))
    g.add(*[Dot(ax.c2p(*p), color=color, radius=0.045) for p in P[:i + 1]], Dot(ax.c2p(*cur), color=color, radius=0.1))
    return g, cur


class Bai(Lesson):
    LESSON = 'video_bai9'; LABEL = 'BÀI 9 · GIẢI THUẬT GIẢM GRADIENT'; TEXTS = load_texts('video_bai9')
    MINS = {1: 6, 2: 7, 5: 6, 7: 6.5, 13: 9, 14: 8, 16: 9, 17: 8}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 9. Giải thuật giảm gradient', 46, WHITE, BOLD),
                   M(r'\mathbf{w}_{t+1}=\mathbf{w}_t-\eta\,\nabla J(\mathbf{w}_t)', 56, O), VT('Chương 3 · Ứng dụng toán trong học máy', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–4 — ý tưởng
        self.section('Ý tưởng: đi ngược hướng gradient'); self.line(1)
        ax = axes([-1, 7, 1], [-1, 17, 4], 6.6, 5.0, LEFT * 3.0 + DOWN * 0.45)
        self.play(Create(ax), Create(ax.plot(J1, x_range=[-1, 7], color=B, stroke_width=4)), run_time=1.5)
        ball = Dot(ax.c2p(0, J1(0)), color=O, radius=0.13)
        self.play(FadeIn(Star(5, outer_radius=0.17, color=T, fill_opacity=1).move_to(ax.c2p(3, 0))), FadeIn(VT('cực tiểu w* = 3', 20, T).move_to(ax.c2p(5.4, 1.0))),
                  FadeIn(ball), FadeIn(VGroup(VT('w', 20, LIGHT).next_to(ax.x_axis, RIGHT, buff=0.1), VT('J(w)', 20, LIGHT).next_to(ax.y_axis, UP, buff=0.1))), run_time=1)
        self.finish(1)
        self.line(2)
        tg = DashedLine(ax.c2p(-0.9, J1(0) - 6 * -0.9), ax.c2p(1.2, J1(0) - 6 * 1.2), color=INK, stroke_width=2)
        sl = VT("độ dốc J'(0) = −6 < 0", 20).next_to(ax.c2p(0.5, 15), RIGHT, buff=0.1)
        self.play(Create(tg), FadeIn(sl), run_time=1)
        ar = Arrow(ax.c2p(0, 9), ax.c2p(1.7, 9), buff=0, color=O, stroke_width=6)
        al = VT('−∇J: hướng giảm nhanh nhất', 20, O).next_to(ar, RIGHT, buff=0.15)
        self.play(GrowArrow(ar), FadeIn(al), run_time=1.2)
        self.finish(2)
        self.line(3)
        P1 = panel(M(r'w_{t+1}=w_t-\eta\,\nabla J(w_t)', 40)).move_to(RIGHT * 3.5 + UP * 2.0)
        self.play(FadeIn(P1), run_time=1); self.play(Indicate(P1, color=O, scale_factor=1.03), run_time=1)
        self.finish(3)
        self.line(4)
        self.play(FadeOut(tg), FadeOut(ar), FadeOut(sl), FadeOut(al), run_time=0.5)
        rows = VGroup(M(r'J(w)=(w-3)^2,\ \ w_0=0,\ \ \eta=0{,}1', 30, LIGHT), M(r'w_1=0-0{,}1\cdot(-6)=0{,}6', 30), M(r'w_2=0{,}6-0{,}1\cdot(-4{,}8)=1{,}08', 30),
                      M(r'w_3=1{,}08-0{,}1\cdot(-3{,}84)=1{,}464', 30)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(RIGHT * 0.8 + UP * 0.2, aligned_edge=LEFT)
        self.play(FadeIn(rows[0]), run_time=0.6)
        for k in range(1, 4):
            self.play(FadeIn(rows[k]), ball.animate.move_to(ax.c2p(WS[k], J1(WS[k]))), FadeIn(Dot(ax.c2p(WS[k - 1], J1(WS[k - 1])), color=O, radius=0.06, fill_opacity=0.5)), run_time=1.1)
            self.wait(0.6)
        wl = always_redraw(lambda: VT(f'w = {vn(ax.p2c(ball.get_center())[0], 3)}', 22, O).next_to(ball, UP, buff=0.3))
        self.add(wl)
        for k in range(4, 9):
            self.play(ball.animate.move_to(ax.c2p(WS[k], J1(WS[k]))), run_time=0.4)
        wl.clear_updaters(); self.finish(4); self.clear_body()

        # 5–7 — đường đồng mức
        self.section('Quỹ đạo trên đường đồng mức'); self.line(5)
        ax = axes([-1.2, 5.6, 1], [-0.8, 3.4, 1], 6.8, 4.2, LEFT * 3.0 + DOWN * 0.3)
        el = ellipses(ax, A2, C2, [0.3, 1, 2.2, 4.5])
        self.play(Create(ax), Create(el), FadeIn(Star(5, outer_radius=0.17, color=T, fill_opacity=1).move_to(ax.c2p(*C2))), FadeIn(M(r'\mathbf{w}^*', 30, T).next_to(ax.c2p(*C2), DR, buff=0.1)), run_time=1.5)
        u = ValueTracker(0)

        def state():
            g, cur = trail(ax, P2, u.get_value(), O); gr = A2 * (cur - C2); nn = np.linalg.norm(gr)
            if nn > 0.05: g.add(Arrow(ax.c2p(*cur), ax.c2p(*(cur - gr / nn * min(1.2, 0.35 + 0.35 * nn))), buff=0, color=WHITE, stroke_width=4, max_tip_length_to_length_ratio=0.3))
            g.add(VT(f'‖∇J‖ = {vn(nn, 3)}', 30, O).move_to(RIGHT * 3.6 + UP * 0.6))
            return g
        st = always_redraw(state)
        P1 = panel(M(r'\mathbf{w}_{t+1}=\mathbf{w}_t-\eta\,\nabla J(\mathbf{w}_t)', 34)).move_to(RIGHT * 3.6 + UP * 2.0)
        self.play(FadeIn(st), FadeIn(P1), FadeIn(VGroup(VT('mũi tên trắng: hướng −∇J', 20, LIGHT), VT('gradient vuông góc với đường đồng mức', 20, LIGHT)).arrange(DOWN, buff=0.12).move_to(RIGHT * 3.6 + DOWN * 0.3)), run_time=1)
        self.finish(5)
        self.line(6); self.play(u.animate.set_value(6), run_time=self.slots[6] - 0.8, rate_func=linear); self.finish(6)
        self.line(7); self.play(u.animate.set_value(17), run_time=self.slots[7] - 2.0, rate_func=linear)
        st.clear_updaters(); self.play(FadeIn(VT('bước tự ngắn lại khi gần w*', 22, T).move_to(RIGHT * 3.6 + DOWN * 1.4)), run_time=0.6)
        self.finish(7); self.clear_body()

        # 8–11 — tốc độ học
        self.section('Tốc độ học η'); self.line(8)
        pans, tracks, losses = [], [], []
        la = axes([0, 10, 2], [0, 12, 3], 7.0, 1.9, DOWN * 2.05 + RIGHT * 0.3, nums=False)
        lal = VGroup(VT('vòng lặp', 16, LIGHT).next_to(la, DOWN, buff=0.05), VT('J', 18, LIGHT).next_to(la, LEFT, buff=0.1))
        for k, (eta, lab, col) in enumerate(ETAS):
            span = (-1, 7) if eta < 1 else (-11, 17)
            a_ = axes([span[0], span[1], 2 if eta < 1 else 7], [-1, J1(span[0]) * 1.02, 10 ** int(np.log10(J1(span[0])))], 3.8, 2.3, RIGHT * 4.25 * (k - 1) + UP * 0.75, nums=False)
            pans.append(VGroup(a_, a_.plot(J1, x_range=list(span), color=GRIDC, stroke_width=3), VT(lab, 20, col).next_to(a_, UP, buff=0.1)))
        self.play(*[FadeIn(p_) for p_ in pans], Create(la), FadeIn(lal), run_time=1.5)
        self.finish(8)
        for k, (eta, lab, col) in enumerate(ETAS):
            self.line(9 + k)
            a_ = pans[k][0]; ws = gd1(0.0, eta, 10); it = ValueTracker(0)

            def pth(a_=a_, ws=ws, col=col, it=it):
                i = int(min(it.get_value(), 9)); f = min(1.0, it.get_value() - i); cur = ws[i] + (ws[i + 1] - ws[i]) * f
                pts = [a_.c2p(w, J1(w)) for w in ws[:i + 1]] + [a_.c2p(cur, J1(cur))]
                return VGroup(VMobject(color=col, stroke_width=2.5).set_points_as_corners(pts), *[Dot(a_.c2p(w, J1(w)), color=col, radius=0.04) for w in ws[:i + 1]], Dot(a_.c2p(cur, J1(cur)), color=col, radius=0.08))
            lc = always_redraw(lambda eta=eta, col=col, it=it: plot_clipped(la, lambda t_: 9 * ((1 - 2 * eta) ** 2) ** t_, [0, max(it.get_value(), 0.05)], [0, 12], n=200, color=col, stroke_width=3.5))
            pg = always_redraw(pth)
            self.add(pg, lc)
            self.play(it.animate.set_value(10), run_time=self.slots[9 + k] - 1.2, rate_func=linear)
            pg.clear_updaters(); lc.clear_updaters(); self.finish(9 + k)
        self.clear_body()

        # 12–14 — số điều kiện
        self.section('Số điều kiện và chuẩn hóa dữ liệu'); self.line(12)
        P1 = panel(M(r'J(\mathbf{w}_t)-J^*\leq\left(1-\frac{m}{L}\right)^{t}(J(\mathbf{w}_0)-J^*)', 34)).move_to(RIGHT * 3.6 + UP * 1.9)
        cases = [(np.array([1.0, 10.0]), 'Chưa chuẩn hóa: L/m = 10', O), (np.array([1.0, 1.0]), 'Đã chuẩn hóa: L/m = 1', T)]
        A_ = []
        for k, (a, lab, col) in enumerate(cases):
            a_ = axes([-3.6, 3.6, 1], [-2.2, 2.2, 1], 3.4, 2.1, LEFT * 3.7 + UP * (0.85 - 2.7 * k), nums=False)
            A_.append(a_)
            self.play(Create(a_), Create(ellipses(a_, a, [0, 0], [0.1, 0.5, 1.2, 2.5, 4.5] if k == 0 else [0.5, 1.2, 2.5, 4.5])), FadeIn(VT(lab, 19, col).next_to(a_, UP, buff=0.08)), run_time=1)
        self.play(FadeIn(P1), FadeIn(VT('với η = 1/L', 22, LIGHT).next_to(P1, DOWN, buff=0.2)), run_time=1)
        self.finish(12)
        self.line(13)
        u = ValueTracker(0); Ps = [path2([-3.0, 1.2], 1 / a.max(), 25, a, np.zeros(2)) for a, _, _ in cases]
        trs = [always_redraw(lambda k=k: trail(A_[k], Ps[k], u.get_value(), cases[k][2])[0]) for k in range(2)]
        tc = always_redraw(lambda: VT(f't = {int(u.get_value())}', 22).move_to(LEFT * 1.0 + DOWN * 2.6))
        self.add(*trs, tc)
        self.play(u.animate.set_value(25), FadeIn(VGroup(VT('L/m = 10  →  hệ số co 0,9', 24, O), VT('L/m = 1  →  hệ số co 0', 24, T)).arrange(DOWN, buff=0.2).move_to(RIGHT * 3.6 + UP * 0.1)),
                  run_time=self.slots[13] - 1.0, rate_func=linear)
        for m_ in (*trs, tc): m_.clear_updaters()
        self.finish(13)
        self.line(14)
        self.play(FadeIn(VGroup(VT('Chuẩn hóa z-score (mục 2.6)', 24), VT('→ đường đồng mức tròn hơn', 24, T), VT('→ số điều kiện nhỏ, hội tụ nhanh', 24, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(RIGHT * 3.6 + DOWN * 1.6)), run_time=1)
        self.finish(14); self.clear_body()

        # 15–17 — biến thể
        self.section('Ba biến thể theo cách lấy mẫu'); self.line(15)
        XR, YR = [-2.2, 3.2], [-3.2, 1.6]
        ax = axes([*XR, 1], [*YR, 1], 5.4, 4.8, LEFT * 3.6 + DOWN * 0.45, nums=False)
        Z = lambda a, b: np.array([a, b]) @ SXX @ np.array([a, b]) - 2 * SXY @ np.array([a, b]) + SYY
        lv = VGroup(*[ax.plot_implicit_curve(lambda a, b, l=l: Z(a, b) - l, color=GRIDC, stroke_width=2) for l in [0.8, 1.2, 2, 3.5, 6, 10]])
        axl = VGroup(M(r'w_0', 26, LIGHT).next_to(ax.x_axis, RIGHT, buff=0.1), M(r'w_1', 26, LIGHT).next_to(ax.y_axis, UP, buff=0.1))
        self.play(Create(ax), Create(lv), FadeIn(axl), FadeIn(Star(5, outer_radius=0.17, color=WHITE, fill_opacity=1).move_to(ax.c2p(*WSTAR))), run_time=1.5)
        tb = [('Biến thể', 'Mẫu/bước', 'Ưu điểm', INK), ('Theo lô', 'n', 'mượt, chính xác', B), ('SGD', '1', 'cập nhật rất nhanh', O), ('Lô nhỏ', '32–512', 'cân bằng, tận dụng GPU', T)]
        rowsT = VGroup(*[VGroup(*[VT(s_, 19, c, BOLD if i == 0 else NORMAL).move_to([x, 1.9 - 0.55 * i, 0], aligned_edge=LEFT) for x, s_ in zip([0.2, 1.75, 3.35], r_[:3])]) for i, (*r_, c) in enumerate(tb)])
        self.play(FadeIn(rowsT[0]), FadeIn(VT('Hồi quy tuyến tính, n = 1000, cùng η = 0,08\nvà 45 bước cập nhật', 18, LIGHT).move_to(RIGHT * 3.0 + DOWN * 1.9)), run_time=1)
        self.finish(15)
        u = ValueTracker(0); trs = []
        self.line(16)
        for k in (0, 1):
            trs.append(always_redraw(lambda k=k: trail(ax, VARS[k][0], u.get_value(), VARS[k][2])[0]))
        self.add(trs[0]); self.play(FadeIn(rowsT[1]), u.animate.set_value(20), run_time=self.slots[16] / 2 - 0.2, rate_func=linear)
        self.add(trs[1]); self.play(FadeIn(rowsT[2]), u.animate.set_value(45), run_time=self.slots[16] / 2 - 0.2, rate_func=linear)
        for m_ in trs: m_.clear_updaters()
        self.finish(16)
        self.line(17)
        u3 = ValueTracker(0); t3 = always_redraw(lambda: trail(ax, VARS[2][0], u3.get_value(), VARS[2][2])[0]); self.add(t3)
        self.play(FadeIn(rowsT[3]), u3.animate.set_value(45), run_time=self.slots[17] - 1.0, rate_func=linear)
        t3.clear_updaters(); self.finish(17); self.clear_body()

        # 18–19 — tiêu chuẩn dừng
        self.section('Tiêu chuẩn dừng và đường cong mất mát'); self.line(18)
        its = VGroup(VT('•  Dừng khi ‖∇J(wₜ)‖₂ < ε', 26), VT('•  hoặc khi J thay đổi rất ít giữa hai vòng lặp', 26), VT('•  hoặc khi đạt số vòng lặp tối đa', 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(UP * 1.4)
        self.play(LaggedStart(*[FadeIn(i_, shift=RIGHT * 0.2) for i_ in its], lag_ratio=0.8), run_time=3.5)
        self.finish(18)
        self.line(19)
        self.play(its.animate.scale(0.75).to_edge(RIGHT, buff=0.4).shift(UP * 0.6), run_time=0.6)
        it = np.arange(0, 60)
        a_ = axes([0, 60, 10], [0, 5, 1], 6.4, 3.6, LEFT * 2.9 + DOWN * 0.7, nums=False)
        crv = [(np.log10(9 * 0.995 ** it), 'đi ngang quá sớm → η quá nhỏ', T), (np.log10(9 * 0.9 ** it * (1 + 0.6 * (-1) ** it) + 2e-3), 'răng cưa mạnh → η quá lớn', O),
               (np.log10(9 * 0.8 ** it + 1e-3), 'giảm đều → η hợp lý', B)]
        lab = VGroup(VT('số vòng lặp', 18, LIGHT).next_to(a_, DOWN, buff=0.1), VT('log J', 18, LIGHT).next_to(a_, LEFT, buff=0.1))
        self.play(Create(a_), FadeIn(lab), run_time=0.8)
        leg = VGroup()
        for y, s_, c in crv:
            self.play(Create(VMobject(color=c, stroke_width=3).set_points_as_corners([a_.c2p(x, v + 3) for x, v in zip(it, y)])), run_time=1.2)
            leg.add(row('—', s_, size=20, color=c))
        self.play(FadeIn(leg.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 3.7 + DOWN * 1.3)), run_time=0.6)
        self.finish(19); self.clear_body()

        self.section('Tóm tắt'); self.line(20)
        lst = bullets(['Đi ngược gradient một bước η', 'η quá nhỏ: chậm · quá lớn: phân kỳ', 'Chuẩn hóa dữ liệu → hội tụ nhanh hơn', 'Lô nhỏ là mặc định trong học sâu',
                       'Luôn theo dõi đường cong mất mát'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=self.slots[20] - 1)
        self.finish(20); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
