"""Tạo giọng đọc bằng VieNeu-TTS (v3 Turbo).  Chạy: python make_voice.py [giọng] [các câu, vd 3,7]"""
import sys, json, numpy as np
from vieneu import Vieneu
from noi_dung import SPOKEN

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'Adam'
if __name__ == '__main__':
    only = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else range(len(SPOKEN))
    try: durs = json.load(open('tts/durations.json'))
    except FileNotFoundError: durs = [0.0] * len(SPOKEN)
    tts = Vieneu()
    for i in only:
        a = np.asarray(tts.infer(SPOKEN[i], voice=VOICE), dtype=np.float32)
        tts.save(a, f'tts/{i:02d}.wav'); durs[i] = len(a) / 48000
        print(f'{i:02d} {durs[i]:5.2f}s  {SPOKEN[i][:60]}', flush=True)
    json.dump(durs, open('tts/durations.json', 'w'))
