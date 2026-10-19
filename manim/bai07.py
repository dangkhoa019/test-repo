"""Bài 7 - Phương pháp bình phương nhỏ nhất (Manim)."""
from common import *

r = np.random.default_rng(8); XD = np.sort(r.uniform(0, 10, 14)); YD = 1.2 + 0.55 * XD + r.normal(0, 0.7, 14)
WLS = np.polyfit(XD, YD, 1)[::-1]; CX, CY = XD.mean(), YD.mean(); TH0 = np.arctan(WLS[1])
sse = lambda w0, w1, x=XD, y=YD: ((y - w0 - w1 * x) ** 2).sum()

PX = np.array([[1, 0], [1, 1], [1, 2]], float); PY = np.array([1.0, 3.0, 4.0]); PW = np.linalg.solve(PX.T @ PX, PX.T @ PY)
GY = np.array([1.0, 4.0, 2.0])  # véc tơ minh họa riêng để thấy rõ phần dư trong ℝ³
YH = PX @ np.linalg.solve(PX.T @ PX, PX.T @ GY); E = GY - YH; PM = PX @ np.linalg.inv(PX.T @ PX) @ PX.T

r2 = np.random.default_rng(21); XT = np.sort(r2.uniform(0, 1, 10)); YT = np.sin(2 * np.pi * XT) + r2.normal(0, 0.2, 10)
XV = r2.uniform(0, 1, 40); YV = np.sin(2 * np.pi * XV) + r2.normal(0, 0.2, 40)
r2s = lambda y, yh: 1 - ((y - yh) ** 2).sum() / ((y - y.mean()) ** 2).sum()


def mat(A, fmt=lambda v: vn(v, 0), size=34, color=INK):
    return Matrix([[fmt(v) for v in row_] for row_ in np.atleast_2d(A)], element_to_mobject=lambda s: M(s.replace('−', '-').replace(',', '{,}'), size, color),
                  h_buff=1.1, v_buff=0.7, bracket_h_buff=0.12).set_color(color)


class Bai(Lesson):
    LESSON = 'video_bai07'; LABEL = 'BÀI 7 · PHƯƠNG PHÁP BÌNH PHƯƠNG NHỎ NHẤT'; TEXTS = load_texts('video_bai07')
    MINS = {0: 5, 2: 10, 9: 10}

    def construct(self):
        self.line(0)
        t = VGroup(VT('TOÁN CHO HỌC MÁY', 24, B, BOLD), VT('Bài 7. Bình phương nhỏ nhất', 46, WHITE, BOLD),
                   M(r'\mathbf{X}^{\top}\mathbf{X}\,\mathbf{w}=\mathbf{X}^{\top}\mathbf{y}', 56, O), VT('Chương 3 · Ứng dụng toán trong học máy', 22, LIGHT)).arrange(DOWN, buff=0.45)
        self.play(FadeIn(t[:2], shift=UP * 0.3), run_time=1.2); self.play(Write(t[2]), FadeIn(t[3]), run_time=1.5)
        self.finish(0); self.play(FadeOut(t), run_time=0.5)

        # 1–3 — đặt bài toán, xoay đường thẳng, vì sao bình phương
        self.section('Đặt bài toán bình phương nhỏ nhất'); self.line(1)
        ax = axes([0, 10.5, 2], [0, 9, 2], 6.4, 5.0, LEFT * 3.2 + DOWN * 0.45)
        th = ValueTracker(TH0 + 0.35); ok = ValueTracker(0); st = {'fit': False}

        def data():
            x, y = XD, YD
            if ok.get_value() > 0: x, y = np.r_[XD, 9.5], np.r_[YD, 6.4 - 5.5 * ok.get_value()]
            return x, y

        def coef():
            x, y = data()
            if st['fit']: w1, w0 = np.polyfit(x, y, 1)
            else: w1 = np.tan(th.get_value()); w0 = CY - w1 * CX
            return w0, w1

        def scene_():
            x, y = data(); w0, w1 = coef(); g = VGroup()
            for xi, yi in zip(x, y): g.add(Line(ax.c2p(xi, yi), ax.c2p(xi, np.clip(w0 + w1 * xi, 0, 9)), color=T, stroke_width=2.5))
            se = seg_in_box(np.array([-w1, 1]), w0, [0, 10.5], [0, 9])
            g.add(Line(ax.c2p(*se[0]), ax.c2p(*se[1]), color=O, stroke_width=4))
            g.add(*[Dot(ax.c2p(xi, yi), color=B, radius=0.07) for xi, yi in zip(x, y)])
            return g
        sc = always_redraw(scene_)
        P1 = panel(M(r'J(\mathbf{w})=\sum_i (y_i-\mathbf{w}^{\top}\mathbf{x}_i)^2=\|\mathbf{y}-\mathbf{Xw}\|_2^2', 30)).move_to(RIGHT * 3.5 + UP * 2.1)
        jt = always_redraw(lambda: VT(f'J = {vn(sse(*coef(), *data()))}', 34, O).move_to(RIGHT * 3.5 + UP * 1.0))
        self.play(Create(ax), FadeIn(sc), run_time=1.5); self.play(FadeIn(P1), FadeIn(jt), run_time=1); self.finish(1)

        self.line(2)
        Jt = lambda a: sse(CY - np.tan(np.radians(a)) * CX, np.tan(np.radians(a)))
        D0 = np.degrees(TH0); jm = max(Jt(D0 - 23.5), Jt(D0 + 23.5)) * 1.05
        ia = axes([D0 - 24, D0 + 24, 10], [0, jm, jm / 4], 4.6, 2.6, RIGHT * 3.6 + DOWN * 1.2, nums=False)
        ic = ia.plot(Jt, x_range=[D0 - 23.5, D0 + 23.5], color=B, stroke_width=3)
        idot = always_redraw(lambda: Dot(ia.c2p(np.degrees(th.get_value()), Jt(np.degrees(th.get_value()))), color=O, radius=0.09))
        ilab = VGroup(VT('góc của đường thẳng', 18, LIGHT).next_to(ia, DOWN, buff=0.1), VT('J', 20, LIGHT).next_to(ia, LEFT, buff=0.1))
        self.play(Create(ia), Create(ic), FadeIn(idot), FadeIn(ilab), run_time=1)
        self.play(th.animate.set_value(TH0 - 0.35), run_time=3.5, rate_func=smooth)
        self.play(th.animate.set_value(TH0), run_time=2.5, rate_func=smooth)
        self.finish(2)

        self.line(3)
        idot.clear_updaters(); self.play(FadeOut(VGroup(ia, ic, idot, ilab)), run_time=0.5)
        st['fit'] = True
        items = VGroup(*[VT('✓ ' + s_, 20) for s_ in ['khả vi mọi nơi', 'hàm toàn phương lồi → nghiệm dạng đóng', 'nhiễu chuẩn → trùng ước lượng\n    hợp lý cực đại']]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        items.move_to(RIGHT * 0.45 + DOWN * 0.5, aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(i_, shift=RIGHT * 0.2) for i_ in items], lag_ratio=0.8), run_time=4)
        self.wait(0.8)
        self.play(ok.animate.set_value(1), FadeIn(VT('✗ một điểm ngoại lai kéo lệch cả đường', 20, R).next_to(items, DOWN, aligned_edge=LEFT, buff=0.35)), run_time=2.5)
        sc.clear_updaters(); jt.clear_updaters(); self.finish(3); self.clear_body()

        # 4–6 — hệ phương trình chuẩn tắc
        self.section('Hệ phương trình chuẩn tắc'); self.line(4)
        rows = [M(r'J(\mathbf{w})=\mathbf{w}^{\top}\mathbf{X}^{\top}\mathbf{X}\mathbf{w}-2\mathbf{y}^{\top}\mathbf{X}\mathbf{w}+\mathbf{y}^{\top}\mathbf{y}', 40),
                M(r'\nabla J(\mathbf{w})=2\mathbf{X}^{\top}\mathbf{X}\mathbf{w}-2\mathbf{X}^{\top}\mathbf{y}', 40),
                panel(M(r'\mathbf{X}^{\top}\mathbf{X}\,\mathbf{w}=\mathbf{X}^{\top}\mathbf{y}', 48, O), color=O),
                row('$\\Rightarrow\\ \\mathbf{w}=(\\mathbf{X}^{\\top}\\mathbf{X})^{-1}\\mathbf{X}^{\\top}\\mathbf{y}$', '(khi khả nghịch)', size=28),
                row('$\\nabla^2 J=2\\mathbf{X}^{\\top}\\mathbf{X}\\succeq 0\\ \\Rightarrow\\ J$', 'lồi, điểm dừng = cực tiểu toàn cục', size=26, color=T),
                VT('cột của X độc lập tuyến tính ⇒ XᵀX ≻ 0 ⇒ nghiệm duy nhất', 26, T)]
        G = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(DOWN * 0.35 + LEFT * 0.2)
        self.play(FadeIn(G[0], shift=RIGHT * 0.2), run_time=1); self.wait(2.2); self.play(FadeIn(G[1], shift=RIGHT * 0.2), run_time=1); self.finish(4)
        self.line(5); self.play(FadeIn(G[2], scale=0.95), run_time=1); self.wait(2.4); self.play(FadeIn(G[3], shift=RIGHT * 0.2), run_time=1); self.finish(5)
        self.line(6); self.play(FadeIn(G[4], shift=RIGHT * 0.2), run_time=1); self.wait(3); self.play(FadeIn(G[5], shift=RIGHT * 0.2), run_time=1); self.finish(6); self.clear_body()

        # 7–8 — ví dụ ba điểm
        self.section('Ví dụ: đường hồi quy qua ba điểm'); self.line(7)
        ax = axes([-0.5, 2.6, 1], [0, 5, 1], 5.0, 5.0, LEFT * 4.0 + DOWN * 0.45)
        dots = VGroup(*[Dot(ax.c2p(x, y), color=B, radius=0.1) for x, y in zip(PX[:, 1], PY)])
        XM = VGroup(M(r'\mathbf{X}=', 36), mat(PX)).arrange(RIGHT, buff=0.15); YM = VGroup(M(r'\mathbf{y}=', 36), mat(PY.reshape(3, 1))).arrange(RIGHT, buff=0.15)
        top = VGroup(XM, YM).arrange(RIGHT, buff=0.8).move_to(RIGHT * 2.6 + UP * 1.3)
        self.play(Create(ax), LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.3), run_time=1.5)
        self.play(FadeIn(top), run_time=1); self.play(Indicate(XM[1].get_columns()[0], color=O), run_time=1.2); self.finish(7)
        self.line(8)
        A_ = VGroup(M(r'\mathbf{X}^{\top}\mathbf{X}=', 34), mat(PX.T @ PX)).arrange(RIGHT, buff=0.15)
        b_ = VGroup(M(r'\mathbf{X}^{\top}\mathbf{y}=', 34), mat((PX.T @ PY).reshape(2, 1))).arrange(RIGHT, buff=0.15)
        mid = VGroup(A_, b_).arrange(RIGHT, buff=0.8).move_to(RIGHT * 2.6 + DOWN * 0.75)
        self.play(FadeIn(A_), run_time=0.8); self.wait(1); self.play(FadeIn(b_), run_time=0.8); self.wait(1)
        res = M(r'w_0=7/6\approx 1{,}17,\quad w_1=3/2=1{,}5', 36, T).move_to(RIGHT * 2.6 + DOWN * 2.3)
        ln = ax.plot(lambda x: PW[0] + PW[1] * x, x_range=[-0.5, 2.6], color=O, stroke_width=4)
        rs = VGroup(*[Line(ax.c2p(x, y), ax.c2p(x, PW[0] + PW[1] * x), color=T, stroke_width=3) for x, y in zip(PX[:, 1], PY)])
        self.play(FadeIn(res), Create(ln), Create(rs), run_time=1.5)
        self.finish(8); self.clear_body()

        # 9–10 — ý nghĩa hình học
        self.section('Ý nghĩa hình học: phép chiếu trực giao'); self.line(9)
        a, b = PX[:, 0], PX[:, 1]; nrm = E / np.linalg.norm(E); sw = ValueTracker(-50)
        base_in = np.array([1, 1, 1]) / np.sqrt(3); ORG = LEFT * 2.0 + DOWN * 1.1; SC = 1.15

        def view():
            s_ = np.radians(sw.get_value()); inpl = np.cos(s_) * base_in + np.sin(s_) * np.cross(nrm, base_in)
            d = np.cos(np.radians(40)) * inpl + np.sin(np.radians(40)) * nrm
            rt = np.cross([0, 0, 1], d); rt /= np.linalg.norm(rt); up = np.cross(d, rt)
            return lambda p: ORG + SC * (rt @ p) * RIGHT + SC * (up @ p) * UP
        k = ValueTracker(0)

        def geo():
            P = view(); g = VGroup()
            cs = [P(s_ * a + t_ * b) for s_, t_ in [(-0.2, -0.6), (1.6, -0.6), (1.6, 1.4), (-0.2, 1.4)]]
            g.add(Polygon(*cs, color=B, fill_opacity=0.15, stroke_width=1))
            for v in np.eye(3) * 3.2: g.add(Line(P(0 * v), P(v), color=GRIDC, stroke_width=2))
            g.add(Line(P(0 * a), P(a), color=LIGHT, stroke_width=3), Line(P(0 * b), P(b), color=LIGHT, stroke_width=3))
            g.add(Arrow(P(0 * a), P(GY), buff=0, color=WHITE, stroke_width=5), M(r'\mathbf{y}', 32, WHITE).next_to(P(GY), LEFT, buff=0.15))
            kk = k.get_value()
            if kk > 0.01: g.add(Arrow(P(0 * a), P(YH * kk), buff=0, color=O, stroke_width=5))
            if kk > 0.3: g.add(Line(P(YH), P(YH + E * min(1, (kk - 0.3) / 0.7)), color=T, stroke_width=4))
            if kk > 0.99:
                u1, u2 = nrm * 0.25, -YH / np.linalg.norm(YH) * 0.25
                g.add(VMobject(color=WHITE, stroke_width=2).set_points_as_corners([P(YH + u1), P(YH + u1 + u2), P(YH + u2)]))
                g.add(M(r'\hat{\mathbf{y}}=\mathbf{Xw}', 28, O).next_to(P(YH), UP, buff=0.15), M(r'\mathbf{e}', 30, T).next_to(P(YH + E / 2), LEFT, buff=0.12))
            return g
        gg = always_redraw(geo)
        self.play(FadeIn(gg), FadeIn(VT('mặt phẳng col(X) ⊂ ℝ³ — minh họa với y = (1, 4, 2)', 18, B).move_to(LEFT * 3.4 + DOWN * 2.9)), run_time=1)
        info = VGroup(VT(f'ŷ = ({vn(YH[0])}; {vn(YH[1])}; {vn(YH[2])})', 24, O), VT(f'e = y − ŷ = ({vn(E[0])}; {vn(E[1])}; {vn(E[2])})', 24, T),
                      row(f'Xᵀe = ({vn(abs(PX[:, 0] @ E))}; {vn(abs(PX[:, 1] @ E))})  ⇒', '$\\mathbf{e}\\perp\\mathrm{col}(\\mathbf{X})$', size=24)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        info.move_to(RIGHT * 0.9 + UP * 1.6, aligned_edge=LEFT)
        self.play(k.animate.set_value(1), sw.animate.set_value(-46), run_time=3)
        self.play(LaggedStart(*[FadeIn(i_) for i_ in info], lag_ratio=0.6), sw.animate.set_value(-41), run_time=self.slots[9] - 5.2)
        self.finish(9)
        self.line(10)
        pm = VGroup(M(r'\mathbf{P}=\mathbf{X}(\mathbf{X}^{\top}\mathbf{X})^{-1}\mathbf{X}^{\top},\ \ \mathbf{P}^2=\mathbf{P}=\mathbf{P}^{\top}', 34),
                    VGroup(M(r'\mathbf{P}=', 32), mat(PM, fmt=lambda v: vn(v, 2), size=28), VT('đối xứng ✓', 22, T)).arrange(RIGHT, buff=0.25)).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        pm.move_to(RIGHT * 0.9 + DOWN * 1.0, aligned_edge=LEFT)
        self.play(FadeIn(pm[0]), sw.animate.set_value(-37), run_time=2); self.play(FadeIn(pm[1]), sw.animate.set_value(-32), run_time=self.slots[10] - 3.2)
        gg.clear_updaters(); self.finish(10); self.clear_body()

        # 11–12 — suy biến và giải số ổn định
        self.section('Khi ma trận chuẩn tắc suy biến'); self.line(11)
        hd = VT('Cột của X phụ thuộc tuyến tính ⇒ XᵀX suy biến ⇒ vô số nghiệm', 26, R).move_to(UP * 1.9)
        its = [('Giả nghịch đảo Moore – Penrose X⁺ (từ SVD)', 'nghiệm có chuẩn ℓ₂ nhỏ nhất'), ('Thêm điều chuẩn λ‖w‖₂²', 'XᵀX + λI luôn khả nghịch'), ('Loại bớt đặc trưng / giảm chiều bằng PCA', 'loại bỏ cột dư thừa')]
        G = VGroup(*[VGroup(VT(f'{k + 1}. ' + a_, 26), VT('→ ' + b_, 22, T)).arrange(DOWN, aligned_edge=LEFT, buff=0.12).shift(RIGHT * 0.3 * 0) for k, (a_, b_) in enumerate(its)])
        G.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.6)
        for g_ in G: g_[1].shift(RIGHT * 0.4)
        self.play(FadeIn(hd), run_time=1)
        self.play(LaggedStart(*[FadeIn(g_, shift=RIGHT * 0.2) for g_ in G], lag_ratio=0.8), run_time=5.5)
        self.finish(11); self.clear_body()
        self.section('Giải số học ổn định'); self.line(12)
        code = Code(code_string='rng = np.random.default_rng(0)\nX = np.c_[np.ones(100), rng.normal(size=(100, 2))]\nw_true = np.array([1.5, -2.0, 0.8])\n'
                                'y = X @ w_true + rng.normal(scale=0.3, size=100)\n\nw1 = np.linalg.inv(X.T @ X) @ X.T @ y     # không nên\n'
                                'w2 = np.linalg.solve(X.T @ X, X.T @ y)    # tốt hơn\nw3 = np.linalg.lstsq(X, y, rcond=None)[0] # ổn định nhất (SVD)\n'
                                'print(np.round(w3, 3))   # [ 1.451 -2.032  0.852]',
                    language='python', background='rectangle', formatter_style='monokai', add_line_numbers=False)
        code.scale_to_fit_width(11.5).move_to(DOWN * 0.4)
        self.play(FadeIn(code, shift=UP * 0.2), run_time=1.5)
        self.play(FadeIn(VT('Phân rã QR hoặc SVD của X — không tính nghịch đảo tường minh', 24, T).next_to(code, DOWN, buff=0.3)), run_time=1)
        self.finish(12); self.clear_body()

        # 13–14 — đánh giá
        self.section('Đánh giá chất lượng mô hình'); self.line(13)
        P_ = panel(M(r'\mathrm{MSE}=\frac{1}{n}\sum_i(y_i-\hat y_i)^2,\quad \mathrm{RMSE}=\sqrt{\mathrm{MSE}},\quad R^2=1-\frac{\sum_i(y_i-\hat y_i)^2}{\sum_i(y_i-\bar y)^2}', 36)).move_to(UP * 1.4)
        self.play(FadeIn(P_), run_time=1.2); self.wait(1)
        rr = VGroup(VT('•  R² = 1: khớp hoàn hảo', 26, T), VT('•  R² = 0: không tốt hơn luôn dự đoán ȳ', 26), VT('•  R² < 0: tệ hơn cả dự đoán trung bình', 26, R)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to(DOWN * 1.2)
        self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rr], lag_ratio=0.8), run_time=4)
        self.finish(13); self.clear_body()
        self.line(14)
        for k_, deg in enumerate([3, 9]):
            c = np.polyfit(XT, YT, deg); a_ = axes([0, 1, 0.25], [-2, 2, 1], 5.4, 3.4, RIGHT * 3.3 * (2 * k_ - 1) + DOWN * 0.1, nums=False)
            xs = np.linspace(0, 1, 600); ok_ = np.abs(np.polyval(c, xs)) <= 2; pieces = VGroup(); i = 0
            while i < len(xs):
                if ok_[i]:
                    j = i
                    while j + 1 < len(xs) and ok_[j + 1]: j += 1
                    if j > i: pieces.add(a_.plot(lambda x: np.polyval(c, x), x_range=[xs[i], xs[j]], color=WHITE, stroke_width=3))
                    i = j + 1
                else: i += 1
            pts = VGroup(*[Dot(a_.c2p(x, y), color=O, radius=0.045, fill_opacity=0.7) for x, y in zip(XV, YV)], *[Dot(a_.c2p(x, y), color=B, radius=0.08) for x, y in zip(XT, YT)])
            rv = r2s(YV, np.polyval(c, XV))
            lab = VGroup(VT(f'đa thức bậc {deg}', 24), VT(f'R² huấn luyện = {vn(r2s(YT, np.polyval(c, XT)))}', 20, T if deg == 3 else INK),
                         VT('R² kiểm tra = ' + (vn(rv) if rv > -10 else '≪ 0 (rất tệ)'), 20, T if deg == 3 else R))
            lab[0].next_to(a_, UP, buff=0.15); VGroup(lab[1], lab[2]).arrange(DOWN, buff=0.12).next_to(a_, DOWN, buff=0.2)
            self.play(Create(a_), FadeIn(pts), Create(pieces), FadeIn(lab), run_time=1.6); self.wait(0.8)
        self.add(VGroup(row('●', 'huấn luyện', size=18, color=B), row('●', 'kiểm tra', size=18, color=O)).arrange(RIGHT, buff=0.5).move_to(UP * 2.35))
        self.finish(14); self.clear_body()

        self.section('Tóm tắt'); self.line(15)
        lst = bullets(['Cực tiểu ‖y − Xw‖₂²: hàm toàn phương lồi', 'Hệ chuẩn tắc XᵀXw = Xᵀy', 'ŷ là hình chiếu trực giao của y lên col(X); e vuông góc col(X)',
                       'Nghiệm duy nhất ⇔ cột của X độc lập tuyến tính', 'Giải bằng QR/SVD; đánh giá trên tập kiểm tra'])
        self.play(LaggedStart(*[FadeIn(l_, shift=RIGHT * 0.3) for l_ in lst], lag_ratio=0.8), run_time=7)
        self.finish(15); self.play(FadeOut(lst), FadeOut(self.header), run_time=0.8)
