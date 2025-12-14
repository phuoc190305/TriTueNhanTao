import heapq

# --- PHẦN 1: CORE THUẬT TOÁN (ĐÃ TỐI ƯU) ---
class Graph:
    def __init__(self):
        self.adjacency_list = {} # Lưu đồ thị dạng { 'A': [('B', 1), ('C', 2)] }

    def add_edge(self, u, v, weight):
        # Nếu đỉnh chưa tồn tại, tạo list rỗng cho nó
        if u not in self.adjacency_list:
            self.adjacency_list[u] = []
        if v not in self.adjacency_list:
            self.adjacency_list[v] = []
            
        # Thêm cạnh u -> v
        self.adjacency_list[u].append((v, weight))

    def get_neighbors(self, v):
        return self.adjacency_list.get(v, [])

    def a_star_algorithm(self, start_node, stop_node, heuristic_dict):
        # Hàm lấy heuristic an toàn (nếu không nhập thì bằng 0)
        def h(n):
            return heuristic_dict.get(n, 0)

        # Priority Queue: Lưu (f_score, node). f = g + h
        open_queue = [(h(start_node), start_node)]
        
        # Lưu chi phí thực tế g(n)
        g_score = {start_node: 0}
        
        # Lưu vết đường đi
        parents = {start_node: None}
        
        # Set các node đã đóng để tối ưu
        closed_set = set()

        while open_queue:
            # Lấy node có f thấp nhất
            current_f, current_node = heapq.heappop(open_queue)

            if current_node == stop_node:
                # Tìm thấy đích -> Truy vết ngược lại
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = parents[current_node]
                path.reverse()
                return path, g_score[stop_node]

            if current_node in closed_set:
                continue
            closed_set.add(current_node)

            # Duyệt hàng xóm
            for (neighbor, weight) in self.get_neighbors(current_node):
                tentative_g_score = g_score[current_node] + weight

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + h(neighbor)
                    parents[neighbor] = current_node
                    heapq.heappush(open_queue, (f_score, neighbor))

        return None, float('inf')

# --- PHẦN 2: GIAO DIỆN NHẬP LIỆU CHO USER ---

def get_user_input():
    g = Graph()
    heuristics = {}

    print("\n=== CHƯƠNG TRÌNH TÌM ĐƯỜNG A* (NHẬP TAY) ===")
    
    # 1. Nhập Đồ thị (Các cạnh)
    print("\n--- BƯỚC 1: NHẬP CÁC CẠNH (ĐƯỜNG ĐI) ---")
    print("Cú pháp: [Điểm đầu] [Điểm cuối] [Trọng số]")
    print("Ví dụ: A B 5 (Nghĩa là đi từ A đến B mất 5)")
    print("Gõ 'done' để kết thúc bước này.")
    
    while True:
        line = input(">> Nhập cạnh: ").strip()
        if line.lower() == 'done':
            break
        try:
            parts = line.split()
            if len(parts) != 3:
                print("⚠️  Lỗi: Vui lòng nhập đúng 3 phần. Ví dụ: A B 10")
                continue
            
            u, v, w = parts[0], parts[1], float(parts[2])
            g.add_edge(u, v, w)
            # Nếu là đồ thị vô hướng (2 chiều), bỏ comment dòng dưới:
            # g.add_edge(v, u, w) 
        except ValueError:
            print("⚠️  Lỗi: Trọng số phải là một con số.")

    # 2. Nhập Heuristic
    print("\n--- BƯỚC 2: NHẬP HEURISTIC (KHOẢNG CÁCH ƯỚC LƯỢNG) ---")
    print("Cú pháp: [Tên Đỉnh] [Giá trị]")
    print("Ví dụ: A 10 (Nghĩa là đoán từ A đến đích còn 10)")
    print("Gõ 'done' để kết thúc bước này.")
    
    # Tự động liệt kê các đỉnh đã nhập ở bước 1 để người dùng đỡ quên
    all_nodes = list(g.adjacency_list.keys())
    print(f"Các đỉnh hiện có: {', '.join(all_nodes)}")

    while True:
        line = input(">> Nhập Heuristic: ").strip()
        if line.lower() == 'done':
            break
        try:
            parts = line.split()
            if len(parts) != 2:
                print("⚠️  Lỗi: Nhập sai cú pháp. Ví dụ: A 5")
                continue
            
            node, h_val = parts[0], float(parts[1])
            heuristics[node] = h_val
        except ValueError:
            print("⚠️  Lỗi: Giá trị heuristic phải là số.")

    # 3. Nhập Điểm đầu và Đích
    print("\n--- BƯỚC 3: CẤU HÌNH TÌM KIẾM ---")
    start = input("Nhập điểm BẮT ĐẦU: ").strip()
    end = input("Nhập điểm ĐÍCH: ").strip()

    return g, heuristics, start, end

# --- PHẦN 3: MAIN ---
if __name__ == "__main__":
    # Gọi hàm nhập liệu
    try:
        my_graph, my_heuristics, start_node, end_node = get_user_input()
        
        print("\n" + "="*30)
        print(f"🚀 Đang tìm đường từ {start_node} đến {end_node}...")
        
        path, cost = my_graph.a_star_algorithm(start_node, end_node, my_heuristics)
        
        if path:
            print(f"✅ KẾT QUẢ: Đã tìm thấy đường đi!")
            print(f"🗺️  Lộ trình: {' -> '.join(path)}")
            print(f"💰 Tổng chi phí thực tế: {cost}")
        else:
            print(f"❌ KẾT QUẢ: Không có đường đi nào từ {start_node} đến {end_node}.")
            
    except Exception as e:
        print(f"\nCó lỗi xảy ra: {e}")