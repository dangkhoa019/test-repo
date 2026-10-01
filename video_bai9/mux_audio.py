"""Ghép các câu giọng đọc (tts/NN.wav) vào đúng mốc phụ đề rồi trộn vào video.
Chạy sau make_video.py và make_voice.py:  python mux_audio.py
"""
import subprocess, wave, numpy as np
from make_video import SUBS, DUR
SR, LEAD = 48000, 0.3  # mỗi câu bắt đầu sau mốc phụ đề 0,3 giây
track = np.zeros(int((DUR + 1) * SR), dtype=np.float32)
for i, (a, b, _) in enumerate(SUBS):
    with wave.open(f'tts/{i:02d}.wav') as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    assert LEAD + len(x) / SR <= b - a + 1e-6, f'câu {i} dài {len(x)/SR:.2f}s vượt khung {b-a}s'
    s = int((a + LEAD) * SR); track[s:s + len(x)] += x
track /= max(1.0, np.abs(track).max() / 0.95)
with wave.open('tts/narration.wav', 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((track[:int(DUR * SR)] * 32767).astype(np.int16).tobytes())
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', 'bai9_giam_gradient_silent.mp4', '-i', 'tts/narration.wav',
                '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '160k', '-shortest',
                '-movflags', '+faststart', 'bai9_giam_gradient.mp4'], check=True)
with open('bai9_giam_gradient.srt', 'w', encoding='utf-8') as f:
    ts = lambda x: f'{int(x//3600):02d}:{int(x%3600//60):02d}:{int(x%60):02d},{int(round(x%1*1000)):03d}'
    for i, (a, b, s) in enumerate(SUBS, 1): f.write(f'{i}\n{ts(a)} --> {ts(b)}\n{s}\n\n')
print('ok')
