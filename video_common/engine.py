"""Khung dùng chung để dựng video bài giảng 'Toán cho học máy' (ĐH Trà Vinh).

Mỗi bài có thư mục riêng gồm:
  noi_dung.py   : TEXTS (phụ đề hiển thị) và SPOKEN (câu cho TTS đọc), cùng độ dài
  make_video.py : các cảnh hoạt hình, gọi Lesson(...) và lesson.main()
Chạy trong thư mục bài:  python make_video.py voice | render | mux | all  [--voice Adam] [--only 3,7]
  voice  : tạo giọng đọc VieNeu-TTS cho từng câu (tts/NN.wav, tts/durations.json)
  render : dựng hình (độ dài mỗi câu = giọng đọc + 1,2 s, lưu cố định trong tts/slots.json)
  mux    : ghép giọng vào video, xuất <tên>.mp4 và <tên>.srt
"""
import json, os, shutil, subprocess, sys, textwrap, wave
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

W, H, FPS, SR, LEAD = 1280, 720, 24, 48000, 0.3
B, O, T, INK, GRID, DARK, LIGHT, RED = '#4a5fc1', '#d97706', '#0e8f7e', '#3a4050', '#dde0ea', '#1c1f2a', '#9aa0b4', '#c2410c'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'axes.edgecolor': INK, 'axes.labelcolor': DARK,
                     'xtick.color': INK, 'ytick.color': INK, 'axes.grid': True, 'grid.color': GRID,
                     'axes.spines.top': False, 'axes.spines.right': False, 'mathtext.fontset': 'dejavusans'})
ease = lambda u: 0.5 - 0.5 * np.cos(np.pi * np.clip(u, 0, 1))
vn = lambda x, d=2: f'{x:.{d}f}'.replace('.', ',').replace('-', '−')


class Lesson:
    def __init__(self, label, texts, spoken, outname, mins=None, chapter=''):
        assert len(texts) == len(spoken)
        self.label, self.texts, self.spoken, self.out, self.chapter = label, texts, spoken, outname, chapter
        self.mins = mins or {}
        self.now = 0.0
        os.makedirs('tts', exist_ok=True)
        self._timing()

    # ---------- thời gian ----------
    def _timing(self):
        if os.path.exists('tts/slots.json'):
            self.slots = json.load(open('tts/slots.json'))
        elif os.path.exists('tts/durations.json'):
            d = json.load(open('tts/durations.json'))
            self.slots = [float(max(np.ceil((x + 1.2) * 2) / 2, self.mins.get(i, 0))) for i, x in enumerate(d)]
        else:
            self.slots = [float(self.mins.get(i, 6)) for i in range(len(self.texts))]
        self.T = np.concatenate([[0], np.cumsum(self.slots)])
        self.subs = [(float(self.T[i]), float(self.T[i + 1]), self.texts[i]) for i in range(len(self.texts))]
        self.dur = float(self.T[-1])

    def st(self, i):  # số giây kể từ khi câu i bắt đầu
        return self.now - self.T[i]

    def pr(self, i, d=None):  # tiến độ 0..1 trong câu i (hoặc trong d giây đầu)
        return float(np.clip(self.st(i) / (d or self.slots[i]), 0, 1))

    def on(self, i):
        return self.now >= self.T[i]

    # ---------- vẽ ----------
    def base(self, fig, section):
        fig.clf(); fig.patch.set_facecolor('white')
        if section:
            fig.text(0.04, 0.945, self.label.upper(), fontsize=11, color=B, weight='bold')
            fig.text(0.04, 0.895, section, fontsize=19, color=DARK, weight='bold')
        sub = next((s for a, b, s in self.subs if a <= self.now < b), '')
        if sub:
            fig.patches.append(FancyBboxPatch((0.06, 0.018), 0.88, 0.085, boxstyle='round,pad=0.006',
                               transform=fig.transFigure, fc='#1c1f2aE6', ec='none'))
            fig.text(0.5, 0.06, '\n'.join(textwrap.wrap(sub, 98)), ha='center', va='center', fontsize=14.5,
                     color='white', linespacing=1.3)

    def title(self, fig, title, formula):
        self.base(fig, ''); a = self.pr(0, 1.2)
        fig.text(0.5, 0.68, 'TOÁN CHO HỌC MÁY', ha='center', fontsize=16, color=B, weight='bold', alpha=a)
        fig.text(0.5, 0.57, title, ha='center', fontsize=32, color=DARK, weight='bold', alpha=a)
        fig.text(0.5, 0.45, formula, ha='center', fontsize=26, color=O, alpha=a)
        fig.text(0.5, 0.33, self.chapter, ha='center', fontsize=14, color=INK, alpha=a)

    def bullets(self, fig, i, items, x=0.1, y0=0.74, dy=0.1, fs=18, gap=1.0, mark='✓ '):
        for k, s in enumerate(items):
            if self.st(i) > 0.3 + gap * k:
                fig.text(x, y0 - dy * k, mark + s, fontsize=fs, color=DARK)

    # ---------- giọng đọc ----------
    def voice(self, name='Adam', only=None):
        from vieneu import Vieneu
        try: durs = json.load(open('tts/durations.json'))
        except FileNotFoundError: durs = [0.0] * len(self.spoken)
        tts = Vieneu()
        for i in (only if only is not None else range(len(self.spoken))):
            a = np.asarray(tts.infer(self.spoken[i], voice=name), dtype=np.float32)
            tts.save(a, f'tts/{i:02d}.wav'); durs[i] = len(a) / SR
            print(f'{i:02d} {durs[i]:5.2f}s  {self.spoken[i][:70]}', flush=True)
        json.dump(durs, open('tts/durations.json', 'w'))
        self._timing()

    # ---------- dựng hình ----------
    def render(self, scenes):
        """scenes: danh sách (chỉ số câu mở đầu cảnh, hàm vẽ fn(fig))."""
        self._timing(); json.dump(self.slots, open('tts/slots.json', 'w'))
        starts = [s for s, _ in scenes] + [None]
        rng = [(float(self.T[a]), float(self.T[b]) if b is not None else self.dur, f) for (a, f), b in zip(scenes, starts[1:])]
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100)
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgba', '-s', f'{W}x{H}',
                               '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20',
                               '-movflags', '+faststart', f'{self.out}_silent.mp4'], stdin=subprocess.PIPE)
        for n in range(int(self.dur * FPS)):
            self.now = n / FPS
            fn = next(f for a, b, f in rng if a <= self.now < b)
            fn(fig); fig.canvas.draw(); ff.stdin.write(fig.canvas.buffer_rgba().tobytes())
            if n % (FPS * 30) == 0: print(f'{self.now:.0f}/{self.dur:.0f}s', flush=True)
        ff.stdin.close(); ff.wait()

    def still(self, scenes, times, path):
        """Ảnh xem trước: các khung tại những thời điểm cho trước ghép thành lưới 2 cột."""
        from PIL import Image
        starts = [s for s, _ in scenes] + [None]
        rng = [(float(self.T[a]), float(self.T[b]) if b is not None else self.dur, f) for (a, f), b in zip(scenes, starts[1:])]
        fig = plt.figure(figsize=(W / 100, H / 100), dpi=100); ims = []
        for t in times:
            self.now = t; fn = next(f for a, b, f in rng if a <= t < b); fn(fig); fig.canvas.draw()
            ims.append(Image.frombuffer('RGBA', fig.canvas.get_width_height(), fig.canvas.buffer_rgba()).convert('RGB'))
        rows = (len(ims) + 1) // 2; sh = Image.new('RGB', (2 * W, rows * H), 'white')
        for j, im in enumerate(ims): sh.paste(im, ((j % 2) * W, (j // 2) * H))
        sh.resize((1600, 450 * rows)).save(path)

    # ---------- ghép audio ----------
    def mux(self):
        self._timing()
        track = np.zeros(int((self.dur + 1) * SR), dtype=np.float32)
        for i, (a, b, _) in enumerate(self.subs):
            with wave.open(f'tts/{i:02d}.wav') as w:
                x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
            assert LEAD + len(x) / SR <= b - a + 1e-6, f'câu {i} dài {len(x)/SR:.2f}s, vượt khung {b-a}s'
            s = int((a + LEAD) * SR); track[s:s + len(x)] += x
        track /= max(1.0, np.abs(track).max() / 0.95)
        with wave.open('tts/narration.wav', 'wb') as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((track[:int(self.dur * SR)] * 32767).astype(np.int16).tobytes())
        src = f'{self.out}_silent.mp4'
        if not os.path.exists(src):
            src = 'tts/_video_only.mp4'; shutil.copy(f'{self.out}.mp4', src)
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-i', 'tts/narration.wav', '-map', '0:v', '-map', '1:a',
                        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart',
                        f'{self.out}.mp4'], check=True)
        for f in [f'{self.out}_silent.mp4', 'tts/_video_only.mp4']:
            if os.path.exists(f): os.remove(f)
        ts = lambda x: f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)):03d}'
        with open(f'{self.out}.srt', 'w', encoding='utf-8') as f:
            for i, (a, b, s) in enumerate(self.subs, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n')
        print('ok', self.out, self.dur)

    def main(self, scenes):
        args = sys.argv[1:] or ['all']
        name = args[args.index('--voice') + 1] if '--voice' in args else 'Adam'
        only = [int(x) for x in args[args.index('--only') + 1].split(',')] if '--only' in args else None
        if args[0] in ('voice', 'all'): self.voice(name, only)
        if args[0] in ('render', 'all'): self.render(scenes)
        if args[0] in ('mux', 'all'): self.mux()
        if args[0] == 'still':
            self.still(scenes, [float(x) for x in args[1].split(',')], args[2])


def ax_at(fig, rect, xlim, ylim, equal=True, xl=None, yl=None, fs=9):
    ax = fig.add_axes(rect); ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if equal: ax.set_aspect('equal')
    if xl: ax.set_xlabel(xl, fontsize=12)
    if yl: ax.set_ylabel(yl, fontsize=12)
    ax.tick_params(labelsize=fs); return ax


def arrow(ax, v, color, lw=3, origin=(0, 0), ms=18):
    ax.annotate('', xy=np.add(origin, v), xytext=origin,
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=ms, shrinkA=0, shrinkB=0))


def box(fig, x, y, s, fs=18, color=DARK, ha='center'):
    fig.text(x, y, s, fontsize=fs, color=color, ha=ha, va='center', bbox=dict(boxstyle='round,pad=0.5', fc='#f2f4fa', ec=GRID))
