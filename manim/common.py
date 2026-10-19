"""Khung dùng chung cho các bài giảng 'Toán cho học máy' dựng bằng Manim Community.

Mỗi bài là một Scene kế thừa Lesson. Lời thoại và giọng đọc (VieNeu-TTS, giọng Adam) lấy từ thư mục
video_baiXX/tts của phiên bản trước; phụ đề lấy từ TEXTS tương ứng.

Mẫu dùng trong construct():
    self.line(3)            # bắt đầu câu thoại 3: phát âm thanh, ghi mốc phụ đề
    self.play(...)          # các hoạt hình minh họa cho câu đó
    self.finish(3)          # chờ đến hết khung thời gian của câu 3

Dựng:  python render.py bai01   (xem render.py)
"""
import json, os, wave
import numpy as np
from manim import *

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = '#14161e'
B, O, T, R, INK, LIGHT, GRIDC, P = '#7b90f0', '#f5a524', '#2dd4bf', '#f26d6d', '#d6d9e3', '#8a90a3', '#2c3040', '#c084fc'
config.background_color = BG
TEX = TexTemplate(); TEX.preamble = r'\usepackage[T5]{fontenc}\usepackage[utf8]{inputenc}\usepackage{amsmath}\usepackage{amssymb}'
config.tex_template = TEX
FONT = 'DejaVu Sans'


def vn(x, d=2):
    return f'{x:.{d}f}'.replace('.', ',').replace('-', '−')


def VT(s, size=28, color=INK, weight=NORMAL):
    """Chữ tiếng Việt (Pango)."""
    return Text(s, font=FONT, font_size=size, color=color, weight=weight)


def M(s, size=40, color=INK):
    """Công thức LaTeX."""
    return MathTex(s, tex_template=TEX, font_size=size, color=color)


def row(*parts, size=28, color=INK, buff=0.15):
    """Ghép chữ và công thức trên một dòng: chuỗi bắt đầu bằng '$' là công thức."""
    mobs = []
    for p in parts:
        if p.startswith('$') and p.count('$') >= 2:
            j = p.rindex('$'); mobs.append(M(p[1:j], size * 1.35, color))
            if p[j + 1:]: mobs.append(VT(p[j + 1:], size, color))
        else:
            mobs.append(VT(p, size, color))
    return VGroup(*mobs).arrange(RIGHT, buff=buff, aligned_edge=DOWN)


def panel(mob, color=GRIDC, buff=0.25):
    box = SurroundingRectangle(mob, color=color, buff=buff, corner_radius=0.12, fill_color='#1d2030', fill_opacity=1, stroke_width=1.5)
    return VGroup(box, mob)


class Lesson(Scene):
    LESSON = 'video_bai01'        # thư mục chứa tts/NN.wav và tts/durations.json
    LABEL = 'BÀI 1 · ...'
    TEXTS = []                    # phụ đề (để xuất .srt)
    MINS = {}                     # độ dài tối thiểu (giây) của một số câu
    PAD = 1.1                     # khoảng nghỉ sau mỗi câu

    def setup(self):
        tts = os.path.join(ROOT, self.LESSON, 'tts')
        self.durs = json.load(open(os.path.join(tts, 'durations.json')))
        self.tts = tts
        self.slots = [max(np.ceil((d + self.PAD) * 2) / 2, self.MINS.get(i, 0)) for i, d in enumerate(self.durs)]
        self.starts, self.ends = {}, {}
        self.header = VGroup()

    @property
    def now(self):
        return self.renderer.time

    def line(self, i):
        if self.starts:  # không bắt đầu câu mới trước khi câu trước đọc xong
            last = max(self.starts); lag = self.starts[last] + 0.3 + self.durs[last] + 0.4 - self.now
            if lag > 0: self.wait(lag)
        self.starts[i] = self.now
        self.add_sound(os.path.join(self.tts, f'{i:02d}.wav'), time_offset=0.3)

    def finish(self, i):
        rest = self.starts[i] + self.slots[i] - self.now
        if rest > 0.02: self.wait(rest)
        self.ends[i] = self.now

    def section(self, title):
        new = VGroup(VT(self.LABEL, 16, B, BOLD), VT(title, 30, WHITE, BOLD)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        new.to_corner(UL, buff=0.35)
        if len(self.header): self.play(FadeOut(self.header, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), run_time=0.6)
        else: self.play(FadeIn(new), run_time=0.6)
        self.header = new

    def clear_body(self, run_time=0.6):
        rest = [m for m in self.mobjects if m is not self.header]
        if rest: self.play(*[FadeOut(m) for m in rest], run_time=run_time)

    def tear_down(self):
        def ts(x):
            ms = int(round(x * 1000)); return f'{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}'
        out = os.environ.get('SRT_OUT')
        if out:
            with open(out, 'w', encoding='utf-8') as f:
                for k, i in enumerate(sorted(self.starts), 1):
                    f.write(f'{k}\n{ts(self.starts[i])} --> {ts(self.ends.get(i, self.now))}\n{self.TEXTS[i]}\n\n')
        over = [i for i in self.starts if i in self.ends and self.ends[i] - self.starts[i] > self.slots[i] + 0.05]
        print('TIMING tổng', round(self.now, 1), 's; câu vượt khung:', over)


def load_texts(lesson):
    """Đọc TEXTS (phụ đề) của một bài từ phiên bản trước."""
    import importlib.util
    p = os.path.join(ROOT, lesson, 'noi_dung.py')
    if not os.path.exists(p): p = os.path.join(ROOT, lesson, 'make_video.py')
    spec = importlib.util.spec_from_file_location('nd_' + lesson, p); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.TEXTS
