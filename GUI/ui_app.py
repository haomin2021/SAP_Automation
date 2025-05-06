import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

class SAPUploaderApp(tk.Frame):
    def __init__(self, master, start_callback):
        super().__init__(master)
        self.master = master
        self.start_callback = start_callback  # 外部传入启动方法

        self.file_path = tk.StringVar()
        self.tplnr = tk.StringVar()
        self.read_mode = tk.StringVar(value="raw")  # 默认模式

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Select Excel File:").pack()
        tk.Entry(self, textvariable=self.file_path, width=70).pack(pady=2)
        tk.Button(self, text="Browse", command=self.browse_file).pack()

        tk.Label(self, text="Technischen Platz:").pack(pady=(10, 0))
        tk.Entry(self, textvariable=self.tplnr, width=50).pack()

        # 添加读取模式选项
        tk.Label(self, text="Excel Read Mode:").pack(pady=(10, 0))
        tk.OptionMenu(self, self.read_mode, "raw", "structured").pack()

        tk.Button(self, text="Start Import", bg="green", fg="white", command=self.start_callback).pack(pady=10)

        self.log_area = scrolledtext.ScrolledText(self, width=80, height=20)
        self.log_area.pack()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.file_path.set(path)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

    def get_file_path(self):
        return self.file_path.get()

    def get_tplnr(self):
        return self.tplnr.get()

    def get_mode(self):
        return self.read_mode.get()


#################### Example Usage ####################
if __name__ == "__main__":
    def dummy_start():
        file = app.get_file_path()
        tplnr = app.get_tplnr()
        mode = app.get_mode()

        app.log(f"Test Start:\nFile: {file}\nTPLNR: {tplnr}\nMode: {mode}")

    root = tk.Tk()
    root.title("SAP Uploader UI Test")
    app = SAPUploaderApp(master=root, start_callback=dummy_start)
    app.pack(padx=10, pady=10)
    root.mainloop()