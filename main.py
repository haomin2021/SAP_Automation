import tkinter as tk
from tkinter import messagebox
from SAP.sap_interface import SAPSession
from SAP.IA11 import IA11Transaction  # 🔥 引入新的 IA11模块
from DataLoader.excel_loader import load_excel
from GUI.ui_main import SAP_IA11UploaderApp

class SAPController:
    def __init__(self, ui):
        self.ui = ui
        self._cancelled = False

    def start_import(self):
        self._cancelled = False

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
                if self._cancelled:
                    self.ui.log("❌ Import cancelled.")
                    break

                file_path = block["file"]
                tplnr = block["tplnr"]
                mode = block["mode"]

                self.ui.log(f"\n🔄 Processing Block {i+1}")
                self.ui.log(f"📁 File: {file_path}")
                self.ui.log(f"🏷️ TPLNR: {tplnr}")
                self.ui.log(f"📊 Mode: {mode}")

                # 3. Open IA11 transaction for the current block
                try:
                    ia11.open(tplnr)
                    self.ui.log(f"✅ IA11 opened for {tplnr}")
                except Exception as e_open:
                    self.ui.log(f"❌ Fail to open IA11(block {i}): {e_open}")
                    continue

                # 4. Load Excel file
                try:
                    df = load_excel(file_path, mode=mode)                    
                except Exception as e_load:
                    self.ui.log(f"❌ Fail to load Excel(block {i}): {e_load}")
                    continue

                self.ui.log(f"✅ Loaded Excel with {len(df)} entries")

                # 5. Execute batch operation creation
                try:
                    ia11.fill_operations(df, self.ui.log, should_cancel=lambda: self._cancelled)
                except Exception as e_fill:
                    self.ui.log(f"❌ Fail to fill operations(block {i}): {e_fill}")
                    continue

            if not self._cancelled:
                self.ui.log("\n🎉 All lines completed successfully")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.ui.log(f"❌ {e}")

    def cancel_import(self):
        self._cancelled = True
        self.ui.log("⏹️ Stop requested by user.")
            
#################### Example Usage ####################
if __name__ == "__main__":
    controller = SAPController(ui=None)

    app_ui = SAP_IA11UploaderApp(
        start_callback=controller.start_import,   # Start Button → Controller
        cancel_callback=controller.cancel_import    # Stop  Button → Controller
    )

    controller.ui = app_ui   # Fill back UI reference
    app_ui.mainloop()

