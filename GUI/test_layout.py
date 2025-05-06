import tkinter as tk
from tkinter import filedialog, StringVar, OptionMenu, Text

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
    excel_file_var.set(filename)

# 初始化主窗口
root = tk.Tk()
root.title("SAP Automation GUI")

# 变量
excel_file_var = StringVar()
tech_platz_var = StringVar()
sap_transaction_var = StringVar(value="IA05")
read_mode_var = StringVar(value="Row by Row")

# === 第一行: Excel File 与 Technischer Platz ===
frame_top = tk.Frame(root, pady=5)
frame_top.pack(fill="x")

tk.Label(frame_top, text="Excel File:").grid(row=0, column=0, sticky="w", padx=5)
tk.Entry(frame_top, textvariable=excel_file_var, width=40).grid(row=1, column=0, padx=5, pady=2)
tk.Button(frame_top, text="Button", command=browse_file, width=6).grid(row=1, column=1, padx=5)

tk.Label(frame_top, text="Technischer Platz:").grid(row=0, column=2, sticky="w", padx=10)
tk.Entry(frame_top, textvariable=tech_platz_var, width=30).grid(row=1, column=2, padx=5)

# === 第二行: SAP-Transaction 与 Excel Read Mode ===
frame_middle = tk.Frame(root, pady=5)
frame_middle.pack(fill="x", padx=10)

# 设置列权重，使 OptionMenu 可拉伸
frame_middle.grid_columnconfigure(1, weight=5)  # SAP-Transaction OptionMenu（加长）
frame_middle.grid_columnconfigure(3, weight=1)  # Excel Read Mode OptionMenu（缩短）
frame_middle.grid_columnconfigure(4, weight=0)  # Add Block 按钮不拉伸

tk.Label(frame_middle, text="SAP-Transaction:").grid(row=0, column=0, sticky="w", padx=5)
tk.OptionMenu(frame_middle, sap_transaction_var, "IA05", "IA06", "IA07")\
    .grid(row=0, column=1, padx=5, sticky="we")

tk.Label(frame_middle, text="Excel Read Mode:").grid(row=0, column=2, sticky="w", padx=10)
tk.OptionMenu(frame_middle, read_mode_var, "Row by Row", "Full Sheet")\
    .grid(row=0, column=3, padx=5, sticky="we")

tk.Button(frame_middle, text="Add Block").grid(row=0, column=4, padx=5, sticky="e")

# === 第三行: 控制按钮 ===
frame_controls = tk.Frame(root, pady=10)
frame_controls.pack()

tk.Button(frame_controls, text="Reset", width=20).grid(row=0, column=0, padx=15)
tk.Button(frame_controls, text="Start", width=20).grid(row=0, column=1, padx=15)
tk.Button(frame_controls, text="Stop", width=20).grid(row=0, column=2, padx=15)

# === 第四行: 日志区域 ===
frame_log = tk.LabelFrame(root, text="Log Area", padx=10, pady=10)
frame_log.pack(fill="both", expand=True, padx=10, pady=5)

log_text = Text(frame_log, height=12)
log_text.pack(fill="both", expand=True)

root.mainloop()