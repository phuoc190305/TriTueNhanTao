import copy
from heapq import heappush, heappop
import sys

N = 3 
ROWS = [1, 0, -1, 0]
COLS = [0, -1, 0, 1]


class Node:
    def __init__(self, parent, mat, empty_pos, cost_h, cost_g):
        self.parent = parent
        self.mat = mat             
        self.empty_pos = empty_pos 
        self.cost_h = cost_h       
        self.cost_g = cost_g       
        self.f = cost_g + cost_h   

    def __lt__(self, other):
        return self.f < other.f

def get_manhattan_distance(mat, final_coords):
    """Hàm Heuristic: Tính tổng khoảng cách Manhattan(Khoảng cách taxi) các ô về đúng vị trí"""
    distance = 0
    for r in range(N):
        for c in range(N):
            val = mat[r][c]
            if val != 0: # Không tính ô trống
                target_r, target_c = final_coords[val]
                distance += abs(r - target_r) + abs(c - target_c)
    return distance

def is_safe(x, y):
    return 0 <= x < N and 0 <= y < N

# --- PHẦN 2: CÁC HÀM XỬ LÝ NHẬP LIỆU VÀ KIỂM TRA ---

def print_matrix_pretty(mat, label=""):
    if label: print(f"--- {label} ---")
    print("-" * 13)
    for row in mat:
        print("|", end=" ")
        for val in row:
            if val == 0:
                print(" ", end=" | ") # In khoảng trắng cho dễ nhìn
            else:
                print(val, end=" | ")
        print("\n" + "-" * 13)

def input_3x3_matrix(prompt_name):
    """Hàm nhập liệu an toàn: Bắt buộc nhập đúng 3x3 và đủ số 0-8"""
    print(f"\n>> Mời nhập MA TRẬN {prompt_name} (3 dòng):")
    print("(Nhập 3 số cách nhau bởi dấu cách. Ví dụ: 1 2 3)")
    
    while True:
        mat = []
        try:
            for i in range(N):
                line = input(f"   Dòng {i+1}: ").strip()
                row = list(map(int, line.split()))
                if len(row) != N:
                    raise ValueError(f"Vui lòng nhập đúng {N} số.")
                mat.append(row)
            
            # Kiểm tra tính hợp lệ (đủ các số từ 0-8)
            flat = [x for r in mat for x in r]
            if sorted(flat) != list(range(9)):
                print("LỖI: Ma trận phải chứa các số từ 0 đến 8 không trùng lặp!")
                print("Vui lòng nhập lại.")
                continue
            
            return mat
        except ValueError:
            print("LỖI: Định dạng nhập không đúng (phải là số nguyên). Nhập lại!")

def count_inversions(mat):
    """Đếm số cặp nghịch thế để kiểm tra tính giải được"""
    flat = [x for row in mat for x in row if x != 0]
    inv_count = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inv_count += 1
    return inv_count

def check_solvable(initial, final):
    """
    Quy tắc giải được:
    Số cặp nghịch thế của TRẠNG THÁI ĐẦU và TRẠNG THÁI ĐÍCH phải CÙNG TÍNH CHẴN LẺ.
    """
    inv_init = count_inversions(initial)
    inv_final = count_inversions(final)
    
    return (inv_init % 2) == (inv_final % 2)

# --- PHẦN 3: THUẬT TOÁN GIẢI ---

def solve(initial, final):
    # 1. Kiểm tra tính giải được
    if not check_solvable(initial, final):
        print("\n=============================================")
        print("❌ CẢNH BÁO: KHÔNG THỂ GIẢI ĐƯỢC!")
        print("Lý do: Tính chẵn lẻ của trạng thái Đầu và Đích không khớp.")
        print("Bạn vui lòng kiểm tra lại đề bài.")
        print("=============================================")
        return

    # 2. Chuẩn bị dữ liệu
    # Tìm tọa độ các số trong ma trận đích để tra cứu nhanh cho hàm Heuristic
    final_coords = {}
    for r in range(N):
        for c in range(N):
            final_coords[final[r][c]] = (r, c)

    # Tìm vị trí ô trống (số 0) ban đầu
    start_pos = None
    for r in range(N):
        for c in range(N):
            if initial[r][c] == 0:
                start_pos = [r, c]

    pq = [] # Priority Queue
    visited = set()
    
    # Tính chi phí ban đầu
    h = get_manhattan_distance(initial, final_coords)
    root = Node(None, initial, start_pos, h, 0)
    heappush(pq, root)
    
    print("\n🚀 Đang tìm kiếm lời giải... (Vui lòng đợi)")
    
    # 4. Vòng lặp chính
    nodes_explored = 0
    while pq:
        current = heappop(pq)
        nodes_explored += 1
        
        # Kiểm tra đích (h = 0 nghĩa là giống hệt đích)
        if current.cost_h == 0:
            print(f"✅ ĐÃ TÌM THẤY! (Duyệt qua {nodes_explored} trạng thái)")
            
            # Truy vết đường đi
            path = []
            curr = current
            while curr:
                path.append(curr.mat)
                curr = curr.parent
            path.reverse()
            
            print(f"Tổng số bước di chuyển: {len(path) - 1}")
            input("👉 Nhấn Enter để xem từng bước...")
            
            for step, mat in enumerate(path):
                print_matrix_pretty(mat, label=f"BƯỚC {step}")
            return

        # Lưu trạng thái vào visited
        state_tuple = tuple(tuple(row) for row in current.mat)
        if state_tuple in visited:
            continue
        visited.add(state_tuple)

        # Sinh trạng thái con
        x, y = current.empty_pos
        for i in range(4):
            nx, ny = x + ROWS[i], y + COLS[i]
            
            if is_safe(nx, ny):
                # Tạo ma trận mới
                new_mat = [r[:] for r in current.mat]
                # Hoán đổi ô trống
                new_mat[x][y], new_mat[nx][ny] = new_mat[nx][ny], new_mat[x][y]
                
                if tuple(tuple(r) for r in new_mat) not in visited:
                    # Tính toán chi phí mới
                    new_g = current.cost_g + 1
                    new_h = get_manhattan_distance(new_mat, final_coords)
                    
                    child = Node(current, new_mat, [nx, ny], new_h, new_g)
                    heappush(pq, child)
    
    print("Không tìm thấy đường đi (Lỗi không xác định).")

# --- PHẦN 4: CHƯƠNG TRÌNH CHÍNH (MAIN) ---
if __name__ == "__main__":
    print("========================================")
    print("   CHƯƠNG TRÌNH GIẢI 8-PUZZLE (AKT)   ")
    print("========================================")
    
    # Nhập Đầu
    start_matrix = input_3x3_matrix("BẮT ĐẦU")
    print_matrix_pretty(start_matrix, "Trạng thái BẮT ĐẦU của bạn")
    
    # Nhập Đích
    target_matrix = input_3x3_matrix("ĐÍCH (MONG MUỐN)")
    print_matrix_pretty(target_matrix, "Trạng thái ĐÍCH mong muốn")
    
    # Xác nhận chạy
    input("\nNhấn Enter để bắt đầu giải...")
    solve(start_matrix, target_matrix)