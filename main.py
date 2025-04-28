import tkinter as tk
from SAP.sap_interface import SAPSession
from DataLoader.excel_loader import load_excel
from GUI.ui_app import SAPUploaderApp
from tkinter import messagebox

class SAPController:
    def __init__(self, ui):
        self.ui = ui

    def start_import(self):
        try:
            sap = SAPSession()
            self.ui.log("✅ Connected to SAP")

            technischer_platz = self.ui.get_tplnr().strip()
            if not technischer_platz:
                messagebox.showwarning("Input Required", "Please enter Technischen Platz.")
                return

            sap.open_ia11(technischer_platz)
            self.ui.log(f"✅ IA11 opened for {technischer_platz}")

            df = load_excel(self.ui.get_file_path())
            self.ui.log(f"✅ Loaded Excel with {len(df)} entries")

            sap.fill_operations(df, self.ui.log)
            self.ui.log("🎉 All lines completed successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.ui.log(f"❌ {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("SAP IA11 Batch Operation Import Tool")
    root.geometry("700x500")

    app_ui = SAPUploaderApp(root, start_callback=None)
    controller = SAPController(app_ui)
    app_ui.start_callback = controller.start_import
    app_ui.pack(fill="both", expand=True)

    root.mainloop()
