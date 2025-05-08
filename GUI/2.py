import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext

class SAPBatchUploaderApp(tk.Tk):
    def __init__(self, start_callback):
        super().__init__()
        self.title("SAP Batch Uploader")
        self.geometry("900x700")
        self.start_callback = start_callback

        self.blocks = []

        # Block Container (Scrollable)
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        self.scroll_window = canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw", tags="frame_window")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig("frame_window", width=e.width - scrollbar.winfo_width()))
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons and Logs
        # 创建一个横向容器来装按钮
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        # 添加三个按钮并水平排列（side="left"）
        tk.Button(button_frame, text="+ Add Block", command=self.add_block).pack(side="left", padx=5)
        tk.Button(button_frame, text="Start Import", bg="green", fg="white", command=self.start_all).pack(side="left", padx=5)
        tk.Button(button_frame, text="Stop Import", bg="red", fg="white", command=self.stop_import).pack(side="left", padx=5)


        self.log_area = scrolledtext.ScrolledText(self, width=100, height=15)
        self.log_area.pack(pady=10)

        self.add_block()  # Add initial block

    def add_block(self):
        block = {}

        frame = tk.Frame(self.scroll_frame, relief="groove", borderwidth=2, padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        # 设置列比例：左列=3，右列=1
        # Set column weights for resizing
        frame.columnconfigure(1, weight=3) # File Entry
        frame.columnconfigure(2, weight=0) # Browse button
        frame.columnconfigure(3, weight=0) # Remove button 
        frame.columnconfigure(4, weight=1) # Add Block button

        # ===== Row 0 - 左：Excel File =====
        tk.Label(frame, text="Excel File:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        file_entry = tk.Entry(frame)
        file_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        browse_btn = tk.Button(frame, text="Browse", command=lambda: self.browse_file(file_entry))
        browse_btn.grid(row=0, column=2, padx=5, pady=2)
        block["file_entry"] = file_entry

        # ===== Row 0 - 右：Excel Read Mode =====
        tk.Label(frame, text="Excel Read Mode:").grid(row=0, column=3, sticky="e", padx=5, pady=2)
        read_mode = tk.StringVar(value="raw")
        mode_combo = ttk.Combobox(frame, textvariable=read_mode, values=["raw", "structured"], state="readonly", width=10)
        mode_combo.grid(row=0, column=4, sticky="ew", padx=5, pady=2)
        block["mode_var"] = read_mode

        # ===== Row 1 - 左：Technischer Platz =====
        tk.Label(frame, text="Technischer Platz:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        platz_entry = tk.Entry(frame)
        platz_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=2)
        block["tplnr_entry"] = platz_entry

        # ===== Row 1 - 右：Remove 按钮 =====
        remove_btn = tk.Button(frame, text="Remove", command=lambda: self.remove_block(block))
        remove_btn.grid(row=1, column=4, sticky="e", padx=5, pady=2)

        self.blocks.append(block)



    def remove_block(self, block):
        block["frame"].destroy()
        self.blocks.remove(block)

    def stop_import(self):
        # Placeholder for stopping import logic
        messagebox.showinfo("Info", "Import stopped.")
        self.log("Import stopped.")

    def browse_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    def start_all(self):
        for i, block in enumerate(self.blocks):
            file_path = block["file_entry"].get()
            tplnr = block["tplnr_entry"].get()
            mode = block["mode_var"].get()

            if not file_path or not tplnr:
                self.log(f"[Block {i+1}] Missing file or Technischer Platz.")
                continue

            self.log(f"--- Block {i+1} ---")
            self.log(f"File: {file_path}")
            self.log(f"TPLNR: {tplnr}")
            self.log(f"Mode: {mode}")
            self.start_callback(file_path, tplnr, mode)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

#################### Example Usage ####################

def dummy_start(file, tplnr, mode):
    print(f"Simulating SAP upload for: {file}, {tplnr}, Mode: {mode}")

if __name__ == "__main__":
    app = SAPBatchUploaderApp(start_callback=dummy_start)
    app.mainloop()
