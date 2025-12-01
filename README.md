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
* Input
- Đầu vào có thể là 1 ma trận vuông cấp n với số dòng và số cột là các đỉnh của đồ thị. Bậc của đỉnh được xác định bằng tổng số các cạnh liền kề của đỉnh đó. Và trong đồ thị từ đỉnh x tới đỉnh y nếu có kề thì đánh số 1, còn lại là 0.
- Ví dụ về ma trận với 6 đỉnh (A-F).
+ Đỉnh A (bậc 3), B (bậc 3), C (bậc 4), D (bậc 3), E (bậc 1), F (bậc 2).
+ Matran của đồ thị trên:
          0 1 1 0 0 1  
          1 0 1 1 0 0
          1 1 0 1 0 1
          0 1 1 0 1 0
          0 0 0 1 0 0
          1 0 1 0 0 0
* Output
- Đầu ra ở phiên bản Graph-Coloring.py sẽ là tên các đỉnh kèm theo đó là màu đã được tô.
- Đầu ra ở phiên bản Graph-Coloring(File).py Graph-Coloring(File).py và  sẽ là đồ thị gồm các đỉnh và cạnh tương ứng với bậc và đã được tô màu các đỉnh
