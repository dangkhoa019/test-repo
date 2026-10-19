"""Dựng một bài:  python render.py bai01 [--preview]
Kết quả trong manim/output/: baiXX_<ten>_khong_phu_de.mp4, baiXX_<ten>.mp4 (phụ đề in sẵn), baiXX_<ten>.srt
--preview: dựng nhanh chất lượng thấp để xem thử."""
import os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
NAMES = {'bai01': 'ma_tran', 'bai02': 'khong_gian_vec_to', 'bai03': 'gia_tri_rieng', 'bai04': 'cuc_tri', 'bai05': 'toi_uu_loi',
         'bai06': 'lagrange_kkt', 'bai07': 'binh_phuong_nho_nhat', 'bai08': 'hoi_quy', 'bai09': 'giam_gradient', 'bai10': 'pca'}
key = sys.argv[1]; prev = '--preview' in sys.argv
out = os.path.join(HERE, 'output'); os.makedirs(out, exist_ok=True)
base = f'{key}_{NAMES[key]}'; media = os.environ.get('MEDIA_DIR', os.path.join(HERE, '.media'))
srt = os.path.join(out, base + '.srt')
env = dict(os.environ, SRT_OUT=srt)
q = ['-ql'] if prev else ['-qm']
subprocess.run(['manim', *q, '--disable_caching', '--media_dir', os.path.join(media, key), '-o', base + '_khong_phu_de',
                os.path.join(HERE, key + '.py'), 'Bai'], check=True, env=env, cwd=HERE)
vid = subprocess.run(['find', os.path.join(media, key), '-name', base + '_khong_phu_de.mp4'], capture_output=True, text=True).stdout.split()[0]
nosub = os.path.join(out, base + ('_preview' if prev else '') + '_khong_phu_de.mp4'); os.replace(vid, nosub)
if not prev:
    style = "FontName=DejaVu Sans,FontSize=17,PrimaryColour=&H00FFFFFF,BackColour=&H90141018,BorderStyle=3,Outline=6,Shadow=0,MarginV=22"
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', nosub, '-vf', f"subtitles={srt}:force_style='{style}'",
                    '-c:a', 'copy', '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', '-movflags', '+faststart',
                    os.path.join(out, base + '.mp4')], check=True)
print('xong', base)
