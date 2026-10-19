# Video bài giảng Toán cho học máy — phiên bản Manim

Mười bài giảng (Bài 1–10) dựng lại bằng [Manim Community](https://www.manim.community/), dùng lại lời thoại
(giọng Adam, VieNeu-TTS) và phụ đề của phiên bản trước trong các thư mục `video_bai01` … `video_bai10`.

## Cấu trúc

- `common.py` — bảng màu, hàm tiện ích (chữ tiếng Việt, công thức LaTeX, trục, khung…) và lớp `Lesson`
  đồng bộ hình với âm thanh: mỗi câu thoại `i` có một khung thời gian, `self.line(i)` phát âm thanh,
  `self.finish(i)` chờ hết khung; khi dựng xong sẽ ghi file phụ đề `.srt` khớp đúng thời điểm.
- `bai01.py` … `bai10.py` — cảnh `Bai` của từng bài.
- `render.py` — dựng một bài và in phụ đề vào bản có phụ đề.

## Cách dựng

Cần: Python 3.10+, `manim` 0.22 (đã thử với 0.22.0), TeX Live (gói `latex-extra`, `lang-other` cho tiếng Việt), `dvisvgm`, `ffmpeg`.

```bash
cd manim
python render.py bai01            # 720p30, kết quả trong manim/output/
python render.py bai01 --preview  # bản xem nhanh chất lượng thấp
```

Kết quả cho mỗi bài:

- `baiXX_<ten>_khong_phu_de.mp4` — video không phụ đề (để biên tập, ví dụ trong CapCut);
- `baiXX_<ten>.mp4` — video có phụ đề in sẵn;
- `baiXX_<ten>.srt` — phụ đề rời.
