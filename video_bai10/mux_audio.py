"""Ghép giọng đọc (tts/NN.wav) vào đúng mốc phụ đề rồi trộn vào video.  Chạy sau make_video.py."""
import os, shutil, subprocess, wave, numpy as np
from make_video import SUBS, DUR
SR, LEAD = 48000, 0.3
track = np.zeros(int((DUR + 1) * SR), dtype=np.float32)
for i, (a, b, _) in enumerate(SUBS):
    with wave.open(f'tts/{i:02d}.wav') as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    assert LEAD + len(x) / SR <= b - a + 1e-6, f'câu {i} dài hơn khung'
    s = int((a + LEAD) * SR); track[s:s + len(x)] += x
track /= max(1.0, np.abs(track).max() / 0.95)
with wave.open('tts/narration.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track[:int(DUR * SR)] * 32767).astype(np.int16).tobytes())
src = 'bai10_pca_silent.mp4'
if not os.path.exists(src):  # dùng lại hình của video đã ghép trước đó
    src = 'tts/_video_only.mp4'; shutil.copy('bai10_pca.mp4', src)
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', src, '-i', 'tts/narration.wav', '-map', '0:v',
                '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest', '-movflags', '+faststart',
                'bai10_pca.mp4'], check=True)
ts = lambda x: f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)):03d}'
with open('bai10_pca.srt', 'w', encoding='utf-8') as f:
    for i, (a, b, s) in enumerate(SUBS, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n')
print('ok')
