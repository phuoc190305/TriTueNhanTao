import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import turtle
import math

# --- PHẦN 1: XỬ LÝ LOGIC (GIỮ NGUYÊN) ---
def doc_ma_tran(ten_file):
    matrix = []
    try:
        with open(ten_file, 'r') as f:
            for line in f:
                parts = line.strip().replace(',', ' ').split()
                row = [int(x) for x in parts]
                if row:
                    matrix.append(row)
        return matrix
    except Exception as e:
        print(f"Lỗi đọc file: {e}")
        return None

def thuat_toan_welsh_powell(G, nodes, degrees):
    colorDict = {}
    base_colors = ["red", "green", "blue", "yellow", "orange", "purple", "pink", "brown", "cyan", "magenta", "gold", "lightgray"]
    t_ = {n: i for i, n in enumerate(nodes)}
    for n in nodes:
        colorDict[n] = base_colors.copy()
        
    sorted_nodes = sorted(nodes, key=lambda x: degrees[t_[x]], reverse=True)
    final_solution = {}
    
    for n in sorted_nodes:
        if not colorDict[n]:
            final_solution[n] = "white"
            continue
        assigned = colorDict[n][0]
        final_solution[n] = assigned
        row_idx = t_[n]
        adj = G[row_idx]
        for j in range(len(adj)):
            neighbor = nodes[j]
            if adj[j] == 1 and (assigned in colorDict[neighbor]):
                colorDict[neighbor].remove(assigned)
    return sorted_nodes, final_solution

# --- PHẦN 2: GIAO DIỆN GUI & TURTLE (ĐÃ SỬA LỖI CANH CHỈNH) ---
class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minh Họa Tô Màu Đồ Thị - Welsh Powell")
        self.root.geometry("1000x650") # Tăng chiều cao cửa sổ lên chút

        # --- Layout ---
        left_frame = tk.Frame(root, width=320, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Frame chứa Canvas Turtle (thêm padding để không bị sát viền)
        right_frame = tk.Frame(root, bg="white", padx=20, pady=20)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. Các Widget bên Trái
        tk.Label(left_frame, text="BẢNG ĐIỀU KHIỂN", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(20, 10))
        
        self.btn_load = tk.Button(left_frame, text="📂 Chọn File Ma trận", command=self.load_file, font=("Arial", 11), bg="#4CAF50", fg="white", cursor="hand2")
        self.btn_load.pack(pady=5, ipadx=15, ipady=5)

        self.btn_run = tk.Button(left_frame, text="▶ Chạy Tô Màu", command=self.start_coloring, state=tk.DISABLED, font=("Arial", 11), bg="#2196F3", fg="white", cursor="hand2")
        self.btn_run.pack(pady=5, ipadx=25, ipady=5)

        # Bảng (Treeview)
        columns = ("node", "degree", "color")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        self.tree.heading("node", text="Đỉnh")
        self.tree.heading("degree", text="Bậc")
        self.tree.heading("color", text="Màu (Kết quả)")
        
        self.tree.column("node", width=60, anchor="center")
        self.tree.column("degree", width=60, anchor="center")
        self.tree.column("color", width=120, anchor="center")
        self.tree.pack(pady=20, padx=15, fill=tk.BOTH, expand=True)

        # 2. Setup Turtle bên Phải
        self.canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.bgcolor("white")
        # Khởi tạo con rùa vẽ NGAY TẠI ĐÂY
        self.t = turtle.RawTurtle(self.turtle_screen) 
        self.t.speed(0)
        self.t.hideturtle()

        # Biến lưu trữ dữ liệu
        self.G = []
        self.nodes = []
        self.degrees = []
        self.positions = {}
        self.sorted_nodes = []
        self.final_colors = {}
        self.is_running = False

    def load_file(self):
        if self.is_running: return
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if not file_path: return

        matrix = doc_ma_tran(file_path)
        if matrix is None or len(matrix) == 0:
            messagebox.showerror("Lỗi", "File không hợp lệ hoặc rỗng!")
            return
        
        # Kiểm tra ma trận vuông
        num_rows = len(matrix)
        if any(len(row) != num_rows for row in matrix):
             messagebox.showerror("Lỗi", "Ma trận kề phải là ma trận vuông!")
             return

        self.G = matrix
        num_nodes = len(self.G)
        self.nodes = [chr(65 + i) for i in range(num_nodes)]
        self.degrees = [sum(row) for row in self.G]

        self.tree.delete(*self.tree.get_children())
        self.t.clear() # self.t đã được khởi tạo trong __init__, không bị lỗi nữa
        
        for i, n in enumerate(self.nodes):
            self.tree.insert("", tk.END, iid=n, values=(n, self.degrees[i], "Chờ..."))

        self.draw_initial_graph()
        self.btn_run.config(state=tk.NORMAL)

    def draw_initial_graph(self):
        self.t.clear()
        self.positions = {}
        # --- SỬA LỖI CANH CHỈNH TẠI ĐÂY ---
        radius = 160  # Giảm bán kính một chút
        offset_y = -50 # Dời tâm vòng tròn xuống 50 đơn vị
        total = len(self.nodes)
        
        if total == 0: return

        # Tính tọa độ với offset
        for i, n in enumerate(self.nodes):
            angle = (2 * math.pi * i) / total
            # Dời trục y xuống
            x = radius * math.cos(angle)
            y = radius * math.sin(angle) + offset_y 
            self.positions[n] = (x, y)

        # Vẽ cạnh
        self.t.pencolor("#555555")
        self.t.pensize(2)
        for i in range(total):
            for j in range(i+1, total):
                if self.G[i][j] == 1:
                    u, v = self.nodes[i], self.nodes[j]
                    self.t.penup()
                    self.t.goto(self.positions[u])
                    self.t.pendown()
                    self.t.goto(self.positions[v])

        # Vẽ đỉnh trắng
        for n in self.nodes:
            self.draw_node(n, "white")

    def draw_node(self, node_name, fill_color):
        x, y = self.positions[node_name]
        self.t.penup()
        # Điều chỉnh vị trí vẽ chấm tròn
        self.t.goto(x, y + 5) 
        self.t.pendown()
        
        text_color = "black"
        if fill_color == "white":
            self.t.dot(44, "black") # Viền
            self.t.dot(40, "white") # Nền trắng
        else:
            self.t.dot(42, fill_color) # Màu tô
            # Chọn màu chữ tương phản
            if fill_color in ["red", "blue", "green", "purple", "brown", "magenta"]:
                text_color = "white"

        # Viết tên đỉnh
        self.t.penup()
        # Điều chỉnh vị trí text cho cân giữa chấm tròn
        self.t.goto(x, y - 7) 
        self.t.color(text_color)
        # Dùng font nhỏ hơn xíu để gọn
        self.t.write(node_name, align="center", font=("Arial", 11, "bold"))

    def start_coloring(self):
        self.sorted_nodes, self.final_colors = thuat_toan_welsh_powell(self.G, self.nodes, self.degrees)
        self.btn_run.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self.is_running = True
        self.animate_step(0)

    def animate_step(self, index):
        if index >= len(self.sorted_nodes):
            messagebox.showinfo("Hoàn tất", "Đã tô màu xong!")
            self.btn_run.config(state=tk.DISABLED)
            self.btn_load.config(state=tk.NORMAL)
            self.is_running = False
            return

        current_node = self.sorted_nodes[index]
        color = self.final_colors[current_node]

        # 1. Cập nhật hình vẽ
        self.draw_node(current_node, color)

        # 2. Cập nhật bảng
        d = self.degrees[self.nodes.index(current_node)]
        self.tree.item(current_node, values=(current_node, d, color))
        
        self.tree.selection_set(current_node)
        self.tree.focus(current_node)

        # Chạy bước tiếp theo sau 1s
        self.root.after(1000, lambda: self.animate_step(index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringApp(root)
    root.mainloop()
