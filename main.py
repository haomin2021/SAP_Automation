import tkinter as tk
from tkinter import messagebox
from SAP.sap_interface import SAPSession
from SAP.IA11 import IA11Transaction  # 🔥 引入新的 IA11模块
from DataLoader.excel_loader import load_excel
from GUI.ui_main import SAP_IA11UploaderApp

class SAPController:
    def __init__(self, ui):
        self.ui = ui

    def start_import(self):
        try:
            block_info = self.ui.collect_block_info()
            if not block_info:
                messagebox.showwarning("No Valid Blocks", "No valid blocks found to process.")
                return

            # 1. Connect to SAP
            sap = SAPSession()
            self.ui.log("✅ Connected to SAP")
            # 2. Create IA11 transaction handler
            ia11 = IA11Transaction(sap.session)

            for i, block in enumerate(block_info):
                file_path = block["file"]
                tplnr = block["tplnr"]
                mode = block["mode"]

                self.ui.log(f"\n🔄 Processing Block {i+1}")
                self.ui.log(f"📁 File: {file_path}")
                self.ui.log(f"🏷️ TPLNR: {tplnr}")
                self.ui.log(f"📊 Mode: {mode}")

                # 3. Open IA11 transaction for the current block
                ia11.open(tplnr)
                self.ui.log(f"✅ IA11 opened for {tplnr}")

                # 4. Load Excel file
                df = load_excel(file_path, mode=mode)
                self.ui.log(f"✅ Loaded Excel with {len(df)} entries")

                # 5. Execute batch operation creation
                ia11.fill_operations(df, self.ui.log)

            self.ui.log("\n🎉 All lines completed successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.ui.log(f"❌ {e}")

            
#################### Example Usage ####################
if __name__ == "__main__":

    controller = None  
    def start_import():
        controller.start_import()
    app_ui = SAP_IA11UploaderApp(start_callback=start_import)
    controller = SAPController(app_ui)

    app_ui.mainloop()
