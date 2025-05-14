from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QComboBox, QTextEdit,
    QScrollArea, QFrame, QMessageBox
)
import sys

class SAPBlock(QFrame):
    def __init__(self, remove_callback):
        super().__init__()

        self.remove_callback = remove_callback
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Frame styling
        self.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.setStyleSheet("border: 1px solid gray; padding: 10px;")

        # First row: File + Mode
        row1 = QHBoxLayout()
        self.file_input = QLineEdit()
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.browse_file)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Raw", "Structured"])

        row1.addWidget(QLabel("Excel File:"))
        row1.addWidget(self.file_input)
        row1.addWidget(browse_btn)
        row1.addSpacing(20)
        row1.addWidget(QLabel("Read Mode:"))
        row1.addWidget(self.mode_combo)

        # Second row: Technischer Platz + Remove
        row2 = QHBoxLayout()
        self.tplnr_input = QLineEdit()
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_self)

        row2.addWidget(QLabel("Technischer Platz:"))
        row2.addWidget(self.tplnr_input)
        row2.addStretch()
        row2.addWidget(remove_btn)

        self.layout.addLayout(row1)
        self.layout.addLayout(row2)

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.file_input.setText(file_path)

    def remove_self(self):
        self.remove_callback(self)

    def get_data(self):
        return {
            "file": self.file_input.text(),
            "tplnr": self.tplnr_input.text(),
            "mode": self.mode_combo.currentText()
        }


class SAPUploaderApp(QWidget):
    def __init__(self, start_callback):
        super().__init__()
        self.setWindowTitle("SAP IA11 Batch Uploader (PyQt5)")
        self.setMinimumSize(900, 700)
        self.start_callback = start_callback
        self.blocks = []

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # Scrollable block area
        self.scroll_area = QScrollArea()
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_widget)
        self.scroll_area.setWidgetResizable(True)

        self.main_layout.addWidget(self.scroll_area)

        # Buttons
        btn_layout = QHBoxLayout()
        add_btn = QPushButton("+ Add Block")
        start_btn = QPushButton("Start Import")
        stop_btn = QPushButton("Stop Import")

        add_btn.clicked.connect(self.add_block)
        start_btn.clicked.connect(self.start_all)
        stop_btn.clicked.connect(self.stop_import)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(start_btn)
        btn_layout.addWidget(stop_btn)

        self.main_layout.addLayout(btn_layout)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.main_layout.addWidget(self.log_area)

        self.add_block()  # Add initial block

    def add_block(self):
        block = SAPBlock(remove_callback=self.remove_block)
        self.scroll_layout.addWidget(block)
        self.blocks.append(block)

    def remove_block(self, block):
        self.scroll_layout.removeWidget(block)
        block.setParent(None)
        self.blocks.remove(block)

    def start_all(self):
        for i, block in enumerate(self.blocks):
            data = block.get_data()
            if not data["file"] or not data["tplnr"]:
                self.log(f"[Block {i+1}] Missing file or Technischer Platz.")
                continue

            self.log(f"--- Block {i+1} ---")
            self.log(f"File: {data['file']}")
            self.log(f"TPLNR: {data['tplnr']}")
            self.log(f"Mode: {data['mode']}")
            self.start_callback(data["file"], data["tplnr"], data["mode"])

    def stop_import(self):
        QMessageBox.information(self, "Info", "Import stopped.")
        self.log("Import stopped.")

    def log(self, message):
        self.log_area.append(message)

#################### Example Usage ####################

def dummy_start(file, tplnr, mode):
    print(f"Simulating SAP upload for: {file}, {tplnr}, Mode: {mode}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SAPUploaderApp(start_callback=dummy_start)
    window.show()
    sys.exit(app.exec_())
