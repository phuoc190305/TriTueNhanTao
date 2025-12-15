Báo cáo tuần 3: GIẢI THUẬT TÌM KIẾM ĐỐI KHÁNG
Thuật toán Minimax & Alpha – Beta
I.	Thuật toán Minimax
1.	Giới thiệu
-	Minimax là giải thuật là một thuật toán đệ quy lựa chọn bước đi kế tiếp trong một trò chơi có hai người bằng cách định giá trị cho các Node trên cây trò chơi sau đó tìm Node có giá trị phù hợp để đi bước tiếp theo.
2.	Các thành phần
-	Trạng thái ban đầu (initial state): Trạng thái của trò chơi + Người chơi nào được đi nước đầu tiên.
-	Trạng thái kết thúc (terminal state): Kiểm tra kết thúc trò chơi.
-	Hàm chuyển trạng thái (Sucessor): Trả về thông tin (nước đi, trạng thái). Nghĩa là, các nước đi hợp lệ từ trạng thái hiện tại, trạng thái mới được chọn.
-	Hàm lợi ích (utility function): đánh giá trạng thái và kết thúc.
3.	Áp dụng vào bài toán TicTacToe (3x3)
a.	Giá trị đầu vào
-	1 ma trận 3x3. 
-	Người chơi chọn đối tượng X hoặc O (Chọn 1 đối tượng thì đối tượng còn lại sẽ do máy điều khiển).
-	Người chơi sẽ chọn vị trí đánh dấu X hoặc O dựa vào vị trí ma trận rows và cols.
b.	Giá trị đầu ra
-	Sẽ có 3 kết quả là thắng thua hoặc hòa: 
+ Kết quả thắng khi người chơi có 3 đối tượng X hoặc O ở hàng ngang dọc hoặc chéo
+ Kết quả thua khi máy có 3 đối tượng X hoặc O ở hàng ngang dọc hoặc chéo
+ Kết quả hòa khi 2 đối tượng X và O đều đã được đánh dấu hết bàn cờ và không đáp ứng kết quả thắng hoặc thua bên trên.
c.	Các giá trị hình thành
-	Max sẽ tương ứng với người chơi đi trước sao cho tối đa hóa hàm lợi ích
-	Min sẽ tương ứng với người chơi đi sau sao cho tối tiểu hàm lợi ích
Ví dụ:
-	Ở bước đầu tiên thì giá trị Max(X) sẽ có 9 giá trị làm sao để các bước tiếp theo tối đa hóa cơ hội chiến thắng. Còn giá trị Min(O) sẽ có 8 giá trị để làm sao tối thiểu hóa cơ hội chiến thắng của giá trị Max(X) ở từng khả năng của X mà vẫn mang lại cơ hội thắng cho bản thân. Ví dụ như có (n+1)Max(X) thì mỗi Max(X) sẽ có (n+1)Min(O) miễn sao còn nằm trong giá trị 3x3 mà ko trùng giá trị của Max(X)
-	Khi kết thúc sẽ sinh ra 3 lợi ích [-1, 1] tương ứng thua, hòa, thắng.


II.	Thuật toán cắt tỉa Alpha – Beta
1.	Giới thiệu
-	Giải thuật cắt tỉa Alpha-beta từng được nhiều nhà khoa học máy tính đề xuất ý tưởng và không ngừng được cải tiến cho đến ngày nay. Giải thuật này thường sử dụng chung với thuật toán tìm kiếm Minimax nhằm hỗ trợ giảm bớt các không gian trạng thái trong cây trò chơi, giúp thuật toán Minimax có thể tìm kiếm sâu và nhanh hơn. Giải thuật cắt tỉa Alpha-beta có nguyên tắc đơn giản "Nếu biết là trường hợp xáu thì không cần phải xét thêm".
=> Tất cả các dữ liệu đều giống Minimax nhưng thay vì người dùng phải chọn vị trí ma trận theo rows và cols thì chỉ cần chọn số được đánh dấu trên mỗi ô từ 1 đến 9. Điểm lưu ý là ở đây đối tượng X sẽ auto được đi trước.
- Khi sử dụng kỹ thuật cắt tỉa thì giá trị Max sẽ tương ứng với Alpha(α) và Min sẽ tương ứng với Beta(β) và khi α ≥ β thì các nút con còn lại của nút đó có thể bị bỏ qua (cắt tỉa), vì đối thủ sẽ không cho phép ta chọn các giá trị đó.
Tiêu chí	Minimax thuần	Alpha–Beta
Kết quả	Cùng nước đi tối ưu (khỏi lo)	Cùng nước đi tối ưu
Khả năng duyệt toàn bộ trạng thái	Có thể (khả thi trên máy thường)	Cũng được, ít tối ưu cần thiết hơn
Chi phí (upper bound)	Duyệt theo hoán vị nước đi: (9!;=;362{,}880) trình tự nước đi (upper bound). Thực tế còn ít vì trò chơi kết thúc sớm.	Cắt tỉa một số nhánh nhưng với cây nhỏ như 3×3 không khác biệt lớn về thời gian
Khi nên dùng	Mặc định — dễ cài, đủ nhanh cho 3×3	Dùng nếu muốn tối ưu thêm hoặc chuẩn hóa cho mở rộng (5×5 trở lên)
Phức tạp cài đặt	Rất đơn giản	Thêm 2 tham số alpha, beta + kiểm tra điều kiện cắt tỉa
Lợi ích thực tế	Tốt cho học/giải bài tập, demo AI	Ít lợi cho 3×3; hữu ích khi nâng lên bàn lớn hoặc muốn giảm thời gian thực thi tối đa

--Output kết quả chạy
+ Thuật giải Akt với bài toán (8 puzzle) n = 3
<img width="118" height="322" alt="image" src="https://github.com/user-attachments/assets/066afb23-e290-4530-a1a3-dc4c91655aff" />

+ Thuật giải A* với bài toán đồ thị
<img width="352" height="49" alt="image" src="https://github.com/user-attachments/assets/2cf9eabc-ccdb-43fe-857f-30547afc2f33" />


+ Thuật giải A* với bài toán đồ thị (Update)
<img width="353" height="139" alt="image" src="https://github.com/user-attachments/assets/ea537782-bf0b-43b4-829e-1ee2f038ba8c" />

