import tkinter as tk
from tkinter import messagebox
from SAP.sap_interface import SAPSession
from SAP.IA11 import IA11Transaction  # 🔥 引入新的 IA11模块
from DataLoader.excel_loader import load_excel
from GUI.ui_main import SAPUploaderApp

class SAPController:
    def __init__(self, ui):
        self.ui = ui

    def start_import(self):
        try:
            # 1. Connect to SAP
            sap = SAPSession()
            self.ui.log("✅ Connected to SAP")

            technischer_platz = self.ui.get_tplnr().strip()
            if not technischer_platz:
                messagebox.showwarning("Input Required", "Please enter Technischen Platz.")
                return

            # 2. Create IA11 transaction handler
            ia11 = IA11Transaction(sap.session)

            # 3. Open IA11 transaction
            ia11.open(technischer_platz)
            self.ui.log(f"✅ IA11 opened for {technischer_platz}")

            # 4. Load Excel
            df = load_excel(self.ui.get_file_path(), mode=self.ui.get_mode())
            self.ui.log(f"✅ Loaded Excel with {len(df)} entries")

            # 5. Execute batch operation creation
            ia11.fill_operations(df, self.ui.log)
            self.ui.log("🎉 All lines completed successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.ui.log(f"❌ {e}")

            
#################### Example Usage ####################
if __name__ == "__main__":
    root = tk.Tk()
    root.title("SAP IA11 Batch Operation Import Tool")
    root.geometry("700x500")

    controller = None  
    def start_import():
        controller.start_import()
    app_ui = SAPUploaderApp(root, start_callback=start_import)
    controller = SAPController(app_ui)
    app_ui.pack(fill="both", expand=True)

    root.mainloop()
