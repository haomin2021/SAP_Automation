import tkinter as tk
from tkinter import filedialog, messagebox, ttk, scrolledtext

class SAP_IA11UploaderApp(tk.Tk):
    def __init__(self, start_callback):
        """
            Initialize the SAP IA11 Batch Uploader interface.

            Args:
                start_callback (function): A callback function to execute when "Start Import" is clicked.

            Creates:
                - A scrollable block area for batch Excel input.
                - Buttons for adding blocks, starting, and stopping the import.
                - A scrollable log output area.
                - Adds one initial input block on startup.
        """

        super().__init__()
        self.title("SAP IA11 Batch Uploader")
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

        # Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="+ Add Block", command=self.add_block).pack(side="left", padx=5)
        tk.Button(button_frame, text="Start Import", bg="green", fg="white", command=self.start_all).pack(side="left", padx=5)
        tk.Button(button_frame, text="Stop Import", bg="red", fg="white", command=self.stop_import).pack(side="left", padx=5)

        # Log Area
        self.log_area = scrolledtext.ScrolledText(self, width=100, height=15)
        self.log_area.pack(pady=10)

        # Initially one block is added
        self.add_block()

    def add_block(self):
        '''
            Create and display a new input block for SAP batch uploading configuration.

            Each block includes:
                - An input for the Excel file path with a "Browse" button
                - A dropdown menu to choose the read mode ("raw" or "structured")
                - An input for the "Technischer Platz" (technical location)
                - A "Remove" button to delete the block

            The created block's UI components are stored in a dictionary for later access or removal,
            and the block is appended to self.blocks for management.
        '''

        block = {} # Create a dictionary to hold block components

        # Create a external frame for each block
        frame = tk.Frame(self.scroll_frame, relief="groove", borderwidth=2, padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        block["frame"] = frame

        # Set column weights for resizing
        frame.columnconfigure(1, weight=3) # File Entry
        frame.columnconfigure(2, weight=0) # Browse button
        frame.columnconfigure(3, weight=0) # Remove button 
        frame.columnconfigure(4, weight=1) # Add Block button

        # ===== Row 0 - Left：Excel File =====
        tk.Label(frame, text="Excel File:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
        file_entry = tk.Entry(frame)
        file_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        browse_btn = tk.Button(frame, text="Browse", command=lambda: self.browse_file(file_entry))
        browse_btn.grid(row=0, column=2, padx=5, pady=2)
        block["file_entry"] = file_entry

        # ===== Row 0 - Right：Excel Read Mode =====
        tk.Label(frame, text="Excel Read Mode:").grid(row=0, column=3, sticky="e", padx=5, pady=2)
        read_mode = tk.StringVar(value="Raw")
        mode_combo = ttk.Combobox(frame, textvariable=read_mode, values=["Raw", "Structured"], state="readonly", width=10)
        mode_combo.grid(row=0, column=4, sticky="ew", padx=5, pady=2)
        block["mode_var"] = read_mode

        # ===== Row 1 - Left：Technischer Platz =====
        tk.Label(frame, text="Technischer Platz:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
        platz_entry = tk.Entry(frame)
        platz_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=2)
        tplnr_browse_btn = tk.Button(frame, text="Browse", command=lambda: self.browse_tplnr(platz_entry))
        tplnr_browse_btn.grid(row=1, column=2, padx=5, pady=2)
        block["tplnr_entry"] = platz_entry

        # ===== Row 1 - Right：Remove Button =====
        remove_btn = tk.Button(frame, text="Remove", command=lambda: self.remove_block(block))
        remove_btn.grid(row=1, column=4, sticky="e", padx=5, pady=2)

        self.blocks.append(block)

    def remove_block(self, block):
        '''
            Remove a block from the UI and the internal list of blocks.

            Args:
                block (dict): The block dictionary containing UI components to be removed.
        '''
        block["frame"].destroy()
        self.blocks.remove(block)

    def stop_import(self):
        # Placeholder for stopping import logic
        messagebox.showinfo("Info", "Import stopped.")
        self.log("Import stopped.")

    def browse_file(self, entry_widget):
        '''
            Open a file dialog to select an Excel file and insert the selected path into the entry widget.

            Args:
                entry_widget (tk.Entry): The entry widget where the selected file path will be inserted.
        '''
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)

    def browse_tplnr(self, entry_widget):
        '''
            Open a file dialog to select a Technischer Platz and insert the selected path into the entry widget.

            Args:
                entry_widget (tk.Entry): The entry widget where the selected Technischer Platz will be inserted.
        '''
        tplnr = filedialog.askopenfilename(filetypes=[("TPLNR files", "*.tplnr")])
        if tplnr:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, tplnr)

    def start_all(self):
        '''
            Iterate through all blocks and execute the start callback with the provided parameters.

            Each block's file path, Technischer Platz, and read mode are retrieved and passed to the start callback.
            If any required field is missing, a log message is generated.
        '''
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
        '''
            Append a message to the log area and ensure it is visible.

            Args:
                message (str): The message to be logged.
        '''
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.update_idletasks()

#################### Example Usage ####################

def dummy_start(file, tplnr, mode):
    print(f"Simulating SAP upload for: {file}, {tplnr}, Mode: {mode}")

if __name__ == "__main__":
    app = SAP_IA11UploaderApp(start_callback=dummy_start)
    app.mainloop()










