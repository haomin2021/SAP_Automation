import tkinter as tk
from tkinter import filedialog, ttk

class BlockManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SAP Automation Module Blocks")
        self.geometry("800x600")

        # Scrollable frame
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scroll_frame = tk.Frame(canvas)

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.blocks = []
        self.add_block()

        self.add_btn = tk.Button(self, text="+ Add Block", command=self.add_block)
        self.add_btn.pack(pady=10)

    def add_block(self):
        block = tk.Frame(self.scroll_frame, relief="groove", borderwidth=2, padx=10, pady=10)
        block.pack(fill="x", pady=5)

        # Excel File
        tk.Label(block, text="Excel File:").grid(row=0, column=0, sticky="w")
        file_entry = tk.Entry(block, width=50)
        file_entry.grid(row=0, column=1)
        browse_btn = tk.Button(block, text="Browse", command=lambda: self.browse_file(file_entry))
        browse_btn.grid(row=0, column=2)

        # Technischer Platz
        tk.Label(block, text="Technischer Platz:").grid(row=1, column=0, sticky="w")
        platz_entry = tk.Entry(block)
        platz_entry.grid(row=1, column=1)

        # Sample Parameter
        tk.Label(block, text="Wartungspaket Priority:").grid(row=2, column=0, sticky="w")
        param_entry = tk.Entry(block)
        param_entry.grid(row=2, column=1)

        # Remove block button
        remove_btn = tk.Button(block, text="Remove", command=lambda: self.remove_block(block))
        remove_btn.grid(row=0, column=3, rowspan=2)

        self.blocks.append(block)

    def remove_block(self, block):
        block.destroy()
        self.blocks.remove(block)

    def browse_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)


#################### Example Usage ####################
if __name__ == "__main__":
    app = BlockManager()
    app.mainloop()