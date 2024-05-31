import tkinter as tk
from tkinter import ttk

# 기본 창 생성
root = tk.Tk()
root.title("Treeview Example")
root.geometry("400x300")

# 프레임 생성 (Treeview와 Scrollbar를 담기 위해)
frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

# Treeview 위젯 생성
tree = ttk.Treeview(frame, columns=("one", "two"), show='headings')

# 열 정의
tree.column("one", width=100, minwidth=100)
tree.column("two", width=100, minwidth=100)

# 헤더 정의
tree.heading("one", text="Column 1", anchor=tk.W)
tree.heading("two", text="Column 2", anchor=tk.W)

# 데이터 삽입
for i in range(30):
    tree.insert("", "end", values=(f"Value {i+1}", f"Value2 {i+1}"))

# Scrollbar 생성
scrollbar = tk.Scrollbar(frame, orient="vertical", command=tree.yview)
scrollbar.pack(side="right", fill="y")

# Treeview와 Scrollbar 연결
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side="left", fill="both", expand=True)

# 이벤트 루프 실행
root.mainloop()
