1. Tổng quan
- K-Nearest Neighbors (K-NN): Một thuật toán Học có giám sát (Supervised Learning) dùng để phân loại.
- K-Means: Một thuật toán Học không giám sát (Unsupervised Learning) dùng để gom nhóm dữ liệu.
2. Phân tích thuật toán K-Nearest Neighbors (K-NN)
2.1. Lý thuyết cơ bản
- K-NN là thuật toán dựa trên nguyên lý: "Gần mực thì đen, gần đèn thì rạng". Để xác định nhãn (label) của một điểm dữ liệu mới, thuật toán sẽ:
  + Tính khoảng cách từ điểm đó đến tất cả các điểm trong tập dữ liệu huấn luyện (Training set).
  + Chọn ra K điểm gần nhất (Neighbors).
  + Lấy nhãn chiếm đa số trong K điểm đó để gán cho điểm mới.
2.2. Phân tích mã nguồn (K-NN.py)
- Mã nguồn của bạn chia làm 2 phần chính: Sử dụng thư viện scikit-learn và Tự cài đặt thuật toán (From scratch).
* Thư viện scikit-learn
- Tạo dữ liệu: Sử dụng make_blobs để tạo 100 điểm dữ liệu giả lập với 4 tâm cụm.
- Huấn luyện:
  + Mã thử nghiệm với K=5 và K=1.
  + knn.fit(X_train, y_train): Quá trình "học" (thực chất K-NN chỉ lưu dữ liệu lại).
  + knn.predict(X_test): Dự đoán nhãn cho tập kiểm tra.
- Tối ưu hóa tham số (Hyperparameter Tuning):
  + Sử dụng GridSearchCV để chạy thử các giá trị K từ 1 đến 9.
  + Mục đích: Tìm ra giá trị K tốt nhất giúp mô hình dự đoán chính xác nhất (Kết quả in ra bằng knn_grid.best_params_).
* Hàm KNN
- Tính khoảng cách: Sử dụng công thức khoảng cách Euclidean: d(p, q) = sqrt{sum (p_i - q_i)^2}
- Sắp xếp: sorted(zipped, key=lambda x:x[0]) giúp sắp xếp các điểm theo thứ tự khoảng cách tăng dần.
- Lấy K điểm gần nhất: res[:k].
- Bầu chọn (Voting): Đếm số lượng label trong K điểm đó (classes[j] = classes[j] + 1) và trả về label xuất hiện nhiều nhất (max(classes, key=classes.get)).
3. Phân tích thuật toán K-Means Clustering
3.1. Lý thuyết cơ bản
- K-Means là thuật toán gom nhóm dữ liệu chưa được gán nhãn. Mục tiêu là chia dữ liệu thành K cụm (clusters) sao cho các điểm trong cùng một cụm có tính chất tương đồng nhau nhất.
- Quy trình lặp lại (Iterative):
  + Chọn ngẫu nhiên K tâm cụm (centroids).
  + Gán mỗi điểm dữ liệu vào cụm có tâm gần nhất.
  + Cập nhật lại vị trí tâm cụm bằng cách lấy trung bình cộng (mean) tọa độ các điểm trong cụm đó.
  + Lặp lại bước 2 và 3 cho đến khi tâm cụm không thay đổi nữa (hội tụ).
3.2. Phân tích mã nguồn (K-Means.py)
- Mã nguồn này được viết hoàn toàn từ đầu (from scratch), rất tốt cho việc hiểu sâu thuật toán.
4. Các hàm thành phần
- kmeans_init_centers: Chọn ngẫu nhiên n_cluster điểm dữ liệu ban đầu làm tâm cụm.
- kmeans_predict_labels:
  + Sử dụng thư viện scipy.spatial.distance.cdist để tính khoảng cách từ mọi điểm đến các tâm cụm.
  + np.argmin(D, axis=1): Tìm chỉ số (index) của tâm cụm gần nhất cho mỗi điểm.
- kmeans_update_centers:
  + Tính trung bình cộng vị trí các điểm thuộc về một cụm (np.mean(Xk, axis=0)) để dời tâm cụm về vị trí chính xác hơn.
- kmeans_has_converged: Kiểm tra xem tập hợp các tâm cụm mới có giống hệt tâm cụm cũ không. Nếu giống, thuật toán dừng lại.
