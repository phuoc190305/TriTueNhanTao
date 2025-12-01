import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
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

# --- PHẦN 2: GIAO DIỆN GUI & TURTLE ---
class GraphColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minh Họa Tô Màu Đồ Thị - Welsh Powell Pro")
        self.root.geometry("1100x700")

        # --- Layout ---
        left_frame = tk.Frame(root, width=350, bg="#f0f0f0")
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Frame phải chứa Canvas (Thêm padding để canvas nằm gọn bên trong)
        right_frame = tk.Frame(root, bg="white", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 1. BẢNG ĐIỀU KHIỂN
        tk.Label(left_frame, text="BẢNG ĐIỀU KHIỂN", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=(20, 10))
        
        btn_frame = tk.Frame(left_frame, bg="#f0f0f0")
        btn_frame.pack(pady=5, fill=tk.X, padx=20)

        self.btn_load = tk.Button(btn_frame, text="📂 Đọc File", command=self.load_file, font=("Arial", 10), bg="#4CAF50", fg="white", width=12)
        self.btn_load.grid(row=0, column=0, padx=5, pady=5)

        self.btn_save = tk.Button(btn_frame, text="💾 Xuất File", command=self.save_to_file, state=tk.DISABLED, font=("Arial", 10), bg="#FF9800", fg="white", width=12)
        self.btn_save.grid(row=0, column=1, padx=5, pady=5)

        self.btn_edit = tk.Button(left_frame, text="✏️ Chỉnh sửa Ma trận / Đỉnh", command=self.open_editor, state=tk.DISABLED, font=("Arial", 11, "bold"), bg="#607D8B", fg="white")
        self.btn_edit.pack(pady=5, ipadx=10, fill=tk.X, padx=25)

        self.btn_run = tk.Button(left_frame, text="▶ CHẠY TÔ MÀU", command=self.start_coloring, state=tk.DISABLED, font=("Arial", 12, "bold"), bg="#2196F3", fg="white")
        self.btn_run.pack(pady=15, ipadx=20, ipady=5, fill=tk.X, padx=25)

        # Treeview
        columns = ("node", "degree", "color")
        self.tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=20)
        self.tree.heading("node", text="Đỉnh")
        self.tree.heading("degree", text="Bậc")
        self.tree.heading("color", text="Màu")
        self.tree.column("node", width=60, anchor="center")
        self.tree.column("degree", width=60, anchor="center")
        self.tree.column("color", width=100, anchor="center")
        self.tree.pack(pady=10, padx=15, fill=tk.BOTH, expand=True)

        # 2. Setup Turtle
        self.canvas = tk.Canvas(right_frame, bg="white", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.turtle_screen = turtle.TurtleScreen(self.canvas)
        self.turtle_screen.bgcolor("white")
        self.t = turtle.RawTurtle(self.turtle_screen) 
        self.t.speed(0)
        self.t.hideturtle()

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
        if matrix:
            self.update_graph_data(matrix)

    def update_graph_data(self, matrix):
        if not matrix: return
        num_rows = len(matrix)
        if any(len(row) != num_rows for row in matrix):
             messagebox.showerror("Lỗi", "Ma trận không vuông.")
             return

        self.G = matrix
        num_nodes = len(self.G)
        self.nodes = [chr(65 + i) for i in range(num_nodes)]
        self.degrees = [sum(row) for row in self.G]

        self.tree.delete(*self.tree.get_children())
        self.t.clear()
        
        for i, n in enumerate(self.nodes):
            self.tree.insert("", tk.END, iid=n, values=(n, self.degrees[i], "Chờ..."))

        self.draw_initial_graph()
        
        self.btn_run.config(state=tk.NORMAL)
        self.btn_edit.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.NORMAL)

    # --- ĐOẠN CODE SỬA LỖI LỆCH HÌNH ---
    def draw_initial_graph(self):
        self.t.clear()
        self.positions = {}
        total = len(self.nodes)
        
        if total == 0: return

        # --- TÙY CHỈNH TỌA ĐỘ MỚI Ở ĐÂY ---
        # 1. Giảm radius: Lúc trước là 180-220, giờ giảm xuống cố định 150 cho gọn
        radius = 150 
        
        # 2. Dời tâm xuống thấp hơn nữa: 
        # Trong turtle: Y dương là lên trên, Y âm là xuống dưới.
        # Ta đặt -80 để kéo hẳn đồ thị xuống dưới tâm màn hình.
        offset_y = -80 

        for i, n in enumerate(self.nodes):
            angle = (2 * math.pi * i) / total
            # Tính tọa độ
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

        # Vẽ đỉnh
        for n in self.nodes:
            self.draw_node(n, "white")
    # -----------------------------------

    def draw_node(self, node_name, fill_color):
        x, y = self.positions[node_name]
        self.t.penup()
        self.t.goto(x, y + 5) 
        self.t.pendown()
        
        text_color = "black"
        if fill_color == "white":
            self.t.dot(44, "black")
            self.t.dot(40, "white")
        else:
            self.t.dot(42, fill_color)
            if fill_color in ["red", "blue", "green", "purple", "brown", "magenta"]:
                text_color = "white"

        self.t.penup()
        self.t.goto(x, y - 7) 
        self.t.color(text_color)
        self.t.write(node_name, align="center", font=("Arial", 11, "bold"))

    def open_editor(self):
        if self.is_running: return
        editor_win = tk.Toplevel(self.root)
        editor_win.title("Chỉnh sửa Ma trận")
        editor_win.geometry("500x500")

        tk.Label(editor_win, text="Chỉnh sửa ma trận kề bên dưới:", font=("Arial", 10, "bold")).pack(pady=5)
        txt_editor = tk.Text(editor_win, font=("Consolas", 12), width=40, height=15)
        txt_editor.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        content = ""
        for row in self.G:
            line = " ".join(str(x) for x in row)
            content += line + "\n"
        txt_editor.insert(tk.END, content)

        def apply_changes():
            raw_text = txt_editor.get("1.0", tk.END).strip()
            if not raw_text: return
            new_matrix = []
            try:
                lines = raw_text.split('\n')
                for line in lines:
                    parts = line.strip().replace(',', ' ').split()
                    if not parts: continue
                    row = [int(x) for x in parts]
                    new_matrix.append(row)
                self.update_graph_data(new_matrix)
                editor_win.destroy()
                messagebox.showinfo("Thành công", "Đã cập nhật đồ thị mới!")
            except Exception:
                messagebox.showerror("Lỗi", "Dữ liệu không hợp lệ")

        tk.Button(editor_win, text="Cập nhật & Vẽ lại", command=apply_changes, bg="#2196F3", fg="white").pack(pady=10)

    def save_to_file(self):
        if not self.G: return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path: return
        try:
            with open(file_path, 'w') as f:
                for row in self.G:
                    line = " ".join(str(x) for x in row)
                    f.write(line + "\n")
            messagebox.showinfo("Thành công", "Đã lưu file!")
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))

    def start_coloring(self):
        self.sorted_nodes, self.final_colors = thuat_toan_welsh_powell(self.G, self.nodes, self.degrees)
        self.btn_run.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self.btn_edit.config(state=tk.DISABLED)
        self.is_running = True
        self.animate_step(0)

    def animate_step(self, index):
        if index >= len(self.sorted_nodes):
            messagebox.showinfo("Hoàn tất", "Đã tô màu xong!")
            self.btn_run.config(state=tk.DISABLED)
            self.btn_load.config(state=tk.NORMAL)
            self.btn_edit.config(state=tk.NORMAL)
            self.is_running = False
            return

        current_node = self.sorted_nodes[index]
        color = self.final_colors[current_node]

        self.draw_node(current_node, color)

        d = self.degrees[self.nodes.index(current_node)]
        self.tree.item(current_node, values=(current_node, d, color))
        self.tree.selection_set(current_node)
        self.tree.focus(current_node)

        self.root.after(800, lambda: self.animate_step(index + 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphColoringApp(root)
    root.mainloop()