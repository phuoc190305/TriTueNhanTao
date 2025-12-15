-- Graph-Coloring
I. Giới thiệu thuật toán
- Tô màu đồ thị là một phép gán màu sắc đến các phần tử của đồ thị để thỏa mãn điều kiện cho trước
- Một số bài toán tô màu phổ biến:
+ Tô màu sao cho 2 đỉnh kề nhau không cùng màu gọi là tô màu đỉnh (vertex coloring).
+ Tô màu sao cho 2 cạnh kề nhau không cùng màu gọi là tô màu cạnh (edge coloring).
+ Tô màu bề mặt (face coloring) của một đồ thị phẳng là phép tô mỗi mặt hay miền sao cho hai mặt có cùng đường biên không có cùng màu.
II. Ứng dụng
- Lập lịch: một tập các công việc cần được gán khoảng thời gian. Một số công việc không được làm trong cùng thời điểm.
- Cấp phát thanh ghi: những chương trình thường xuyên sử dụng được giữ trong thanh ghi xử lý nhanh.
- Giải Sudoku với 9-màu và 81 đỉnh.
III. Đi sâu vào thuật toán
1. Input
- Đầu vào có thể là 1 ma trận vuông cấp n với số dòng và số cột là các đỉnh của đồ thị. Bậc của đỉnh được xác định bằng tổng số các cạnh liền kề của đỉnh đó. Và trong đồ thị từ đỉnh x tới đỉnh y nếu có kề thì đánh số 1, còn lại là 0.
- Ví dụ về ma trận với 6 đỉnh (A-F).
+ Đỉnh A (bậc 3), B (bậc 3), C (bậc 4), D (bậc 3), E (bậc 1), F (bậc 2).
+ Matran của đồ thị trên:
- 0 1 1 0 0 1  
- 1 0 1 1 0 0
- 1 1 0 1 0 1
- 0 1 1 0 1 0
- 0 0 0 1 0 0
- 1 0 1 0 0 0
2. Output
- Đầu ra ở phiên bản Graph-Coloring.py sẽ là tên các đỉnh kèm theo đó là tên màu đã được tô.
- Đầu ra ở phiên bản Graph-Coloring(File).py Graph-Coloring(View Graphic).py và  sẽ là đồ thị gồm các đỉnh và cạnh tương ứng với bậc và đã được tô màu các đỉnh.
3. Các bước chạy
B1: Xác định bậc của đỉnh.
B2: Tô màu đỉnh có bậc lớn nhất.
B4: Khi tô màu thì bậc của đỉnh về 0, các đỉnh liền kề với đỉnh trước đó bậc := bậc -1.
B5: Quay lại bước 1.
-> Chạy đến khi nào các đỉnh được tô màu và bậc của các đỉnh khi này bằng 0.
III. Code
1. Thư viện sử dụng
- tkinter: Thư viện tiêu chuẩn để tạo cửa sổ ứng dụng, nút bấm, bảng...
- turtle: Thư viện đồ họa.
- math: Dùng để tính toán.
2. Các hàm sử dụng
- def doc_ma_tran(ten_file):
+ Chức năng: Đọc file văn bản chứa ma trận.
+ Hoạt động:
          Mở file, đọc từng dòng.
          replace(',', ' '): Xử lý trường hợp file dùng dấu phẩy hoặc dấu cách để ngăn cách số.
          [int(x) for x in parts]: Chuyển đổi các ký tự số (string) thành số nguyên (integer).
          Trả về một mảng 2 chiều (list of lists) biểu diễn đồ thị.
- thuat_toan_welsh_powell(G, nodes, degrees):
+ Chức năng: Thực hiện thuật toán tô màu.
+ Quy trình:
          Chuẩn bị màu: Tạo danh sách các màu cơ bản (đỏ, xanh, vàng...).
          Sắp xếp: sorted_nodes = sorted(...). Xếp các đỉnh có bậc từ cao xuống thấp. Đỉnh nào có bậc lớn nhất sẽ được tô trước.
          Duyệt và Tô màu:
                    Duyệt qua từng đỉnh trong danh sách đã sắp xếp.
                    Lấy màu đầu tiên trong danh sách màu khả dụng của đỉnh đó.
                    Sau khi tô màu cho đỉnh A (ví dụ màu Đỏ), thuật toán sẽ đi tìm tất cả hàng xóm của A và xóa màu Đỏ khỏi danh sách màu khả dụng của hàng xóm (để hàng xóm không bị tô trùng màu).
                    Trả về: Danh sách đỉnh đã sắp xếp và hiển thị kết quả tô màu.
3. Class giao diện (GraphColoringApp)
- __init__(self, root):
+ Thiết lập cửa sổ chính 1100x700 pixel.
+ Chia Layout:
          Trái (left_frame): Chứa các nút bấm (Đọc file, Xuất file, Chạy...), và bảng Treeview (hiển thị danh sách đỉnh, bậc, màu).
          Phải (right_frame): Chứa Canvas. Đây sẽ là nơi hiển thị đồ thị và quá trình được tô màu.
- Các hàm xử lý dữ liệu:
+ load_file: Mở hộp thoại chọn file .txt từ máy tính, sau đó gọi hàm đọc ma trận.          
+ update_graph_data:
          Nhận ma trận, tính toán danh sách đỉnh (A, B, C...) và bậc của từng đỉnh (tổng các số 1 trong hàng).
          Xóa dữ liệu cũ trên bảng và màn hình vẽ.
          Gọi draw_initial_graph để vẽ đồ thị chưa tô màu.
- Các hàm vẽ đồ thị
+ draw_initial_graph: (tính tọa độ hình tròn)
          angle = (2 * math.pi * i) / total
          x = radius * math.cos(angle)
          y = radius * math.sin(angle) + offset_y
          Đoạn code này chia đều 360 độ cho số lượng đỉnh để xếp chúng thành vòng tròn. offset_y dùng để dời toàn bộ hình xuống dưới một chút cho cân đối.
          Vẽ cạnh trước: Dùng vòng lặp lồng nhau để nối dây giữa các đỉnh có liên kết (giá trị 1 trong ma trận).
          Vẽ đỉnh sau: Gọi draw_node để vẽ hình tròn đại diện cho đỉnh đè lên các dây nối.
+ draw_node(node_name, fill_color):
          Dùng bút Turtle (self.t) di chuyển đến tọa độ (x, y).
          Vẽ một chấm tròn (dot) với màu sắc được chỉ định. Nếu chưa tô màu thì vẽ viền đen ruột trắng.
          Viết tên đỉnh (A, B, C...) vào giữa chấm tròn.
- Chức năng chỉnh sửa (open_editor):
+ Tạo một cửa sổ phụ (Toplevel).
+ Hiển thị ma trận hiện tại vào một ô nhập văn bản (Text widget).
+ Khi người dùng sửa số và bấm "Cập nhật", chương trình sẽ đọc lại văn bản đó, chuyển thành ma trận mới và vẽ lại đồ thị.
- Chức năng hoạt hình (start_coloring & animate_step)
+ start_coloring: Chạy thuật toán logic để lấy kết quả trước, sau đó khóa các nút bấm và bắt đầu hoạt hình.
+ animate_step(index): Đây là hàm đệ quy gián tiếp dùng root.after.
          Lấy đỉnh thứ index trong danh sách đã sắp xếp.
          Tô màu đỉnh đó trên màn hình Turtle (draw_node).
          Cập nhật màu và bôi đen dòng tương ứng trên bảng bên trái (self.tree).
IV. Tóm tắt luồng chạy của chương trình:
Bước 1: Khởi động: Hiện giao diện trống.
Bước 2: Đọc File: Người dùng chọn file -> Chương trình vẽ các đỉnh trắng và dây nối đen.
Nước 3: Chạy Tô màu:
          Thuật toán tính toán ngầm bên dưới.
          Giao diện bắt đầu "chiếu phim": Đỉnh có bậc cao nhất sáng lên màu đầu tiên -> Cập nhật bảng -> Chờ 0.8s -> Đỉnh tiếp theo...
Bước 4: Kết thúc: Thông báo "Đã tô màu xong".

--Kết quả chạy 
+ Thuật giải tô màu đồ thị
<img width="209" height="149" alt="image" src="https://github.com/user-attachments/assets/b4fb0031-b0ca-43ed-94a9-95e4aaa4db73" />
+ Thuật giải tô màu đồ thị (Update 1) - Đọc file txt
<img width="932" height="657" alt="image" src="https://github.com/user-attachments/assets/bbdc5b14-7499-400a-85f8-f482b3afdf4c" />
+ Thuật giải tô màu đồ thị (Update 2) - Đọc/xuất file txt, có thể chỉnh sửa ma trận trực tiếp
<img width="994" height="658" alt="image" src="https://github.com/user-attachments/assets/2ef160f6-f0d8-4a8c-87a9-56c0e9db6fa0" />
<img width="677" height="758" alt="image" src="https://github.com/user-attachments/assets/e9eca4a2-47c6-4ad5-aeab-c7ef648cb6c3" />
+ TSP
<img width="1015" height="671" alt="image" src="https://github.com/user-attachments/assets/1846461e-86cd-4a9c-8115-25aea52a2048" />

  
