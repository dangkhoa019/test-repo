"""Tạo giọng đọc lời thoại Bài 9 bằng VieNeu-TTS (v3 Turbo, CPU/ONNX).
Cài đặt: pip install vieneu.  Chạy: python make_voice.py [tên giọng]
Mỗi câu trong SPOKEN ứng với một dòng phụ đề trong make_video.SUBS (cùng thứ tự).
Ký hiệu toán được viết lại theo cách đọc để TTS phát âm đúng.
"""
import sys, json, wave, numpy as np
from vieneu import Vieneu

VOICE = sys.argv[1] if len(sys.argv) > 1 else 'Minh Triết'
SPOKEN = [
 'Bài chín: Giải thuật giảm gradient. Ý tưởng, tốc độ học, và các biến thể.',
 'Khi hàm mất mát không có nghiệm dạng đóng, ta tìm cực tiểu bằng phương pháp lặp.',
 'Gradient chỉ hướng hàm số tăng nhanh nhất, nên ta bước theo hướng ngược lại, tức là âm gradient.',
 'Công thức cập nhật: vê kép mới bằng vê kép cũ, trừ ê-ta nhân gradient, trong đó ê-ta là tốc độ học.',
 'Với hàm J bằng vê kép trừ ba, bình phương, xuất phát từ không, và ê-ta bằng không phẩy một: ta lần lượt được không phẩy sáu, một phẩy không tám, rồi một phẩy bốn sáu bốn, tiến dần về ba.',
 'Với nhiều tham số, gradient luôn vuông góc với đường đồng mức.',
 'Mỗi bước đi ngược hướng gradient. Càng gần cực tiểu, gradient càng nhỏ, nên bước đi càng ngắn.',
 'Thuật toán tự giảm tốc khi tới gần đích, mà không cần can thiệp thêm.',
 'Tốc độ học ê-ta là siêu tham số quan trọng nhất. Ta xét ba cách chọn trên cùng một hàm số.',
 'Ê-ta quá nhỏ, bằng không phẩy không năm: thuật toán vẫn hội tụ, nhưng cần rất nhiều vòng lặp.',
 'Ê-ta hợp lý, bằng không phẩy ba: hàm mất mát giảm nhanh và đều đặn về giá trị tối ưu.',
 'Ê-ta quá lớn, bằng một phẩy không năm: mỗi bước vượt qua điểm cực tiểu, dao động ngày càng mạnh, và phân kỳ.',
 'Với hàm lồi mạnh tham số em, gradient liên tục Líp-sít hằng số e-lờ, và ê-ta bằng một chia e-lờ, sai số giảm theo cấp số nhân.',
 'Hệ số co, bằng một trừ em chia e-lờ, phụ thuộc số điều kiện. Đường đồng mức càng dẹt, thuật toán hội tụ càng chậm.',
 'Chuẩn hóa dữ liệu làm đường đồng mức tròn hơn, giảm số điều kiện, nên thuật toán hội tụ nhanh hơn rõ rệt.',
 'Khi hàm mất mát là trung bình trên en mẫu, cách ước lượng gradient ở mỗi bước sinh ra ba biến thể.',
 'Theo lô: dùng toàn bộ dữ liệu, quỹ đạo mượt nhưng chậm khi dữ liệu lớn. Ngẫu nhiên: dùng một mẫu, cập nhật nhanh nhưng nhiễu.',
 'Theo lô nhỏ, từ ba mươi hai đến năm trăm mười hai mẫu, cân bằng cả hai, và là lựa chọn mặc định trong học sâu hiện nay.',
 'Ta dừng khi chuẩn của gradient nhỏ hơn ngưỡng ép-xi-lon, khi mất mát gần như không đổi, hoặc khi đạt số vòng lặp tối đa.',
 'Hãy luôn vẽ đường cong mất mát. Đi ngang quá sớm gợi ý ê-ta quá nhỏ; răng cưa mạnh gợi ý ê-ta quá lớn.',
 'Tóm lại: đi ngược gradient, chọn ê-ta hợp lý, chuẩn hóa dữ liệu, và theo dõi đường cong mất mát.',
]

if __name__ == '__main__':
    only = [int(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 else range(len(SPOKEN))
    tts = Vieneu(); sr = 48000
    try: durs = json.load(open('tts/durations.json'))
    except FileNotFoundError: durs = [0.0] * len(SPOKEN)
    for i in only:
        text = SPOKEN[i]
        a = np.asarray(tts.infer(text, voice=VOICE), dtype=np.float32)
        tts.save(a, f'tts/{i:02d}.wav'); durs[i] = len(a) / sr
        print(f'{i:02d} {durs[i]:5.2f}s  {text[:60]}', flush=True)
    json.dump(durs, open('tts/durations.json', 'w'))
