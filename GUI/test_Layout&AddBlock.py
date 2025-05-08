import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext

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
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
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
        block = {} # Create a dictionary to hold block components

        # Create a external frame for each block
        frame = tk.Frame(self.scroll_frame, relief="groove", borderwidth=2, padx=10, pady=10)
        frame.pack(fill="x", pady=5)

        # Set column weights for resizing
        frame.columnconfigure(1, weight=3) # File Entry
        frame.columnconfigure(2, weight=0) # Browse button
        frame.columnconfigure(3, weight=0) # Remove button 
        frame.columnconfigure(4, weight=1) # Add Block button





