BÁO CÁO TUẦN 1: THUẬT TOÁN AKT VÀ A*
I.	Tìm hiểu thuật toán
1.	AKT
- Mô tả bài toán: Bài toán xếp hình là một trò chơi xếp các ô vuông trên 1 bảng nxn sao cho các ô được xếp theo đúng vị trí ở trạng thái đúng.
+ VD: Có 1 ma trận 3x3 với 9 ô -> Bao gồm các ô đánh số từ 1-8 và 1 ô trống. Ở trạng thái ban đầu các ô được xếp 1 cách ngẫu nhiên và phải di chuyển các ô cho đến khi nào đạt được trạng thái đích.
Trạng thái ban đầu :    1 3	5                             Trạng thái đích:   1 2 3
                        4	8	6                                                8   4
	                        2	7                                                7 6 5                
- Các bước để giải quyết:
a) Đối tượng: 
- Các đối tượng trong bài toán;
**Đối tượng	                                                            Vai trò	                                                            Hình thức biểu diễn**
Trạng thái	                                                        Cấu hình cụ thể 	                                                          Ma trận nxn 
Ô trống 	                                                        Vị trí có thể di chuyển	                                                  Cặp tọa độ, 1 phần tử 
Toán tử	                                                    Những hành động có thể thực hiện: Up, Down, Left, Right	C                    ác hàm sinh trạng thái mới
Trạng thái đích 	                                          Cấu hình đúng thứ tự cần đạt	                                                  [1,2,3, …, n2 – 1, 0]
Node	                                                      Biểu diễn trạng thái trong cây tìm kiếm	                                      (state, parent, g, h, f)

* Input
Bao gồm: Trạng thái ban đầu, trạng thái đích, vị trí ô trống, heuristic 
- Trạng thái ban đầu: Là 1 ma trận với kích thước nxn (Cụ thể là 3x3 với bài toán 8 – puzzle) để lưu trữ các ô đánh số từ 1-8 và ô trống được sắp xếp ngẫu nhiên.
- Heuristic: Là 1 hàm kiểm tra các ô (vị trí) của bàn cờ với trạng thái đích. Khi vị trí của 1 ô không trùng với ô tương ứng ở vị trí trong ô đích thì heuristic tang lên 1.
- Trạng thái đích: Là 1 ma trận kích thước nxn (Cụ thể là 3x3 với bài toán 8 – puzzle) để lưu trữ các ô đánh số từ 1 – 8 đã được sắp xếp được sắp xếp và so sánh với trạng thái đích cho trước.* 
- g: số bước đi của bài toán, f: tổng của g và h để xác định trạng thái nhỏ nhất 

* Output 
- Trạng thái ban đầu khi này giống với trạng thái đích
- h(heuristic) = 0: Khi này các ô ở trạng thái ban đầu đã trùng với trạng thái đích
- g: số bước đi của bài toán
- f: tổng của g và h để xác định trạng thái nhỏ nhất
b) Giải pháp
- Bước 1: Khởi tạo ma trận nxn (Trạng thái đích và trạng thái ban đầu)
- Bước 2: Tạo node root (g, h, f)
- Bước 3: Tạo hàm tính Heuristic
- Bước 4: Sao chép ma trận cha, di chuyển ô trống sang vị trí mới, tính chi phí cho node con
- Bước 5: Lấy node có chi phí nhỏ nhất và tiếp tục di chuyển ô trống
- Bước 6: In ra ma trận đích
2. A*
- Mô tả bài toán: Thuật toán A* được sử dụng để tìm đường đi ngắn nhất từ đỉnh bắt đầu tới đỉnh kết thúc (đi từ A đến B) trên 1 đồ thị.
+ Đồ thị gồm các đỉnh và cạnh 
+ Mỗi cạnh có trọng số
+ Tìm đường đi sao cho có tổng chi phí nhỏ nhất

<img width="961" height="353" alt="image" src="https://github.com/user-attachments/assets/7c0ba874-3fb5-42f5-a453-9c2ffce874ca" />

	A	 B	 C	 D	 E	 F
A	0	1.5	N/A	N/A	N/A	0.7
B	1.5	0	1.0	N/A	N/A	2.0
C	N/A	1.0	0	2.5	N/A	N/A
D	N/A	N/A	2.5	0	1.8	1.2
E	N/A	N/A	N/A	1.8	0	3.0
F	0.7	2.0	N/A	1.2	3.0	0
a)	Đối tượng
* Input
- Ma trận trọng số 
* Output 
- Đường đi tối ưu và chi phí
b) Giải pháp
- Bước 1: Khởi tạo ma trận trọng số 
- Bước 2: Chạy vòng lặp và so sánh giá trị cost 
- Bước 3: Xuất ra 1 ma trận chứa đường đi tối ưu và trọng số
3. So sánh AKT và A*
**Tiêu chí	                                                                                AKT 	                                                                        A* **
Nguyên lý	                                                      Tìm kiếm có kiến thức, dựa trên thông tin sẵn có về môi trường	                    Tìm kiếm theo chi phí tổng hợp f(n) = g(n) + h(n)
Cách chọn node mở tiếp theo	                                       Dựa vào kiến thức hướng tới mục tiêu, không chắc tối ưu	              Dựa vào giá trị f(n) nhỏ nhất, đảm bảo tối ưu nếu heuristic admissible
Tối ưu đường đi	                                                                      Không đảm bảo tối ưu	                                            Đảm bảo tối ưu nếu heuristic là admissible
Số node mở ra	                                                        Có thể mở ít hơn BFS nhưng không chắc ít nhất	                    Mở ít node hơn thuật toán không heuristic, hướng tới mục tiêu hiệu quả
Thời gian thực thi	                                          Thường nhanh hơn uninformed search, phụ thuộc kiến thức	                    Nhanh nếu heuristic tốt, nhưng có thể mở nhiều node nếu heuristic kém
Dữ liệu cần	                                                                  Ma trận đồ thị + kiến thức bổ sung	                                            Ma trận đồ thị + hàm heuristic
Khi dùng	                                                          Khi có kiến thức về môi trường nhưng heuristic không rõ ràng                  	Khi có heuristic admissible và muốn tìm đường đi tối ưu

