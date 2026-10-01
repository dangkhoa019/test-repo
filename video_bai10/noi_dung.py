"""Lời thoại Bài 10 - Phân tích thành phần chính.
TEXTS: phụ đề hiển thị (giữ ký hiệu toán). SPOKEN: câu đọc cho TTS (ký hiệu viết theo cách đọc).
Hai danh sách phải cùng độ dài và cùng thứ tự.
"""
TEXTS = [
 'Bài 10: Phân tích thành phần chính (PCA).',
 'Dữ liệu thực tế thường có số chiều rất lớn: một ảnh xám 100×100 đã là véc tơ 10 000 chiều.',
 'Số chiều cao gây tốn chi phí tính toán, khó trực quan hóa, và dữ liệu thưa thớt khiến mô hình dễ quá khớp.',
 'PCA tìm một không gian con k chiều sao cho khi chiếu dữ liệu lên đó, phương sai giữ lại là lớn nhất.',
 'Trước hết, trừ trung bình để đưa tâm dữ liệu về gốc tọa độ.',
 'Chiếu dữ liệu lên hướng đơn vị u, các giá trị chiếu zᵢ = uᵀxᵢ có phương sai bằng uᵀSu.',
 'Xoay hướng u: phương sai thay đổi, lớn nhất ở một hướng và nhỏ nhất ở hướng vuông góc với nó.',
 'Bài toán: cực đại uᵀSu với ràng buộc ‖u‖₂ = 1 — chính là thương Rayleigh ở Bài 3.',
 'Dùng nhân tử Lagrange, điều kiện dừng cho Su = λu: u là véc tơ riêng của S và phương sai đạt được bằng λ.',
 'Vậy hướng giữ nhiều phương sai nhất là véc tơ riêng ứng với giá trị riêng lớn nhất: thành phần chính thứ nhất.',
 'Thuật toán: trừ trung bình, tính S = XcᵀXc/n, phân rã phổ S = QΛQᵀ và sắp các giá trị riêng giảm dần.',
 'Chọn k véc tơ riêng đầu tiên Uₖ, chiếu Z = XcUₖ; khôi phục xấp xỉ bằng ZUₖᵀ.',
 'Với k = 1, mỗi điểm được thay bằng hình chiếu của nó lên trục thành phần chính thứ nhất.',
 'Trong thực hành nên tính PCA qua SVD của Xc = UΣVᵀ: các cột của V là thành phần chính và λᵢ = σᵢ²/n.',
 'Tỉ lệ phương sai giải thích bởi k thành phần đầu: ρₖ = (λ₁ + … + λₖ) / (λ₁ + … + λ_d).',
 'Chọn k nhỏ nhất để ρₖ vượt một ngưỡng, thường là 90% hoặc 95%, hoặc tìm điểm gãy trên đồ thị giá trị riêng.',
 'Ở ví dụ này, bốn thành phần đầu giữ khoảng 88% phương sai, nên cần năm thành phần để vượt ngưỡng 90%.',
 'Lưu ý: PCA là phương pháp không giám sát, không dùng nhãn y — hướng phương sai lớn nhất chưa chắc phân biệt lớp tốt nhất.',
 'PCA nhạy với thang đo nên cần chuẩn hóa; phép chuẩn hóa và phép chiếu chỉ ước lượng trên tập huấn luyện để tránh rò rỉ dữ liệu.',
 'Tóm lại: PCA tìm các hướng giữ nhiều phương sai nhất — chính là các véc tơ riêng của ma trận hiệp phương sai.',
]
SPOKEN = [
 'Bài mười: Phân tích thành phần chính, hay pê xê a.',
 'Dữ liệu thực tế thường có số chiều rất lớn: một bức ảnh xám một trăm nhân một trăm điểm ảnh đã là một véc tơ mười nghìn chiều.',
 'Số chiều cao làm tốn chi phí tính toán, khó trực quan hóa, và dữ liệu thưa thớt khiến mô hình dễ bị quá khớp.',
 'Pê xê a tìm một không gian con ca chiều, sao cho khi chiếu dữ liệu lên đó, phương sai được giữ lại là lớn nhất.',
 'Trước hết, ta trừ đi giá trị trung bình, để đưa tâm của dữ liệu về gốc tọa độ.',
 'Chiếu dữ liệu lên một hướng đơn vị u, các giá trị chiếu có phương sai bằng u chuyển vị, nhân S, nhân u, với S là ma trận hiệp phương sai.',
 'Khi xoay hướng u, phương sai thay đổi: lớn nhất ở một hướng, và nhỏ nhất ở hướng vuông góc với nó.',
 'Bài toán đặt ra là cực đại u chuyển vị S u, với ràng buộc độ dài của u bằng một. Đây chính là thương Rây-li đã học ở bài ba.',
 'Dùng nhân tử La-gơ-răng, điều kiện dừng cho S u bằng lam-đa u. Vậy u là véc tơ riêng của S, và phương sai đạt được bằng chính giá trị riêng lam-đa.',
 'Vậy hướng giữ được nhiều phương sai nhất là véc tơ riêng ứng với giá trị riêng lớn nhất. Đó là thành phần chính thứ nhất.',
 'Thuật toán gồm các bước: trừ trung bình, tính ma trận hiệp phương sai S, phân rã phổ, rồi sắp các giá trị riêng theo thứ tự giảm dần.',
 'Chọn ca véc tơ riêng đầu tiên, rồi chiếu dữ liệu lên chúng. Muốn khôi phục xấp xỉ, ta nhân ngược lại với ma trận chuyển vị của chúng.',
 'Với ca bằng một, mỗi điểm dữ liệu được thay bằng hình chiếu của nó lên trục thành phần chính thứ nhất.',
 'Trong thực hành, nên tính pê xê a qua phân rã giá trị suy biến của dữ liệu đã trừ trung bình. Các cột của ma trận V là các thành phần chính, và lam-đa i bằng xích-ma i bình phương chia cho en.',
 'Tỉ lệ phương sai giải thích bởi ca thành phần đầu, bằng tổng ca giá trị riêng lớn nhất, chia cho tổng tất cả các giá trị riêng.',
 'Ta chọn ca nhỏ nhất để tỉ lệ này vượt một ngưỡng, thường là chín mươi hoặc chín mươi lăm phần trăm, hoặc tìm điểm gãy trên đồ thị giá trị riêng.',
 'Ở ví dụ này, bốn thành phần đầu giữ khoảng tám mươi tám phần trăm phương sai, nên cần năm thành phần để vượt ngưỡng chín mươi phần trăm.',
 'Lưu ý: pê xê a là phương pháp không giám sát, không dùng tới nhãn. Hướng có phương sai lớn nhất chưa chắc là hướng phân biệt các lớp tốt nhất.',
 'Pê xê a nhạy với thang đo nên cần chuẩn hóa dữ liệu. Phép chuẩn hóa và phép chiếu chỉ được ước lượng trên tập huấn luyện, để tránh rò rỉ dữ liệu.',
 'Tóm lại, pê xê a tìm các hướng giữ được nhiều phương sai nhất, và đó chính là các véc tơ riêng của ma trận hiệp phương sai.',
]
assert len(TEXTS) == len(SPOKEN)
