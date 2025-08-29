import tkinter as tk
from tkinter import messagebox
from SAP.sap_interface import SAPSession
from SAP.IA11 import IA11Transaction  # 🔥 引入新的 IA11模块
from DataLoader.excel_loader import load_excel
from GUI.ui_main import SAP_IA11UploaderApp

# controller.py
class SAPController:
    def __init__(self, ui):
        self.ui = ui
        self._cancelled = False
        self._ctx = None

    def start_import(self):
        self._cancelled = False

        blocks = self.ui.collect_block_info()
        if not blocks:
            messagebox.showwarning("No Valid Blocks", "No valid blocks found to process.")
            return

        sap = SAPSession()
        ia11 = IA11Transaction(sap.session)
        self.ui.log("✅ Connected to SAP")

        self._ctx = {"blocks": blocks, "bi": 0, "ia11": ia11, "df": None, "ri": 0}
        self.ui.after(0, self._step_block_begin)

    def cancel_import(self):
        self._cancelled = True
        self.ui.log("⏹️ Stop requested by user.")

    def _step_block_begin(self):
        if self._cancelled:
            return self.ui.log("⏹️ 导入已被用户中断")

        ctx = self._ctx
        blocks, bi, ia11 = ctx["blocks"], ctx["bi"], ctx["ia11"]
        if bi >= len(blocks):
            return self.ui.log("\n🎉 All blocks completed successfully")

        b = blocks[bi]
        file_path, tplnr = b["file"], b["tplnr"]
        mode = (b["mode"] or "").strip().lower()

        self.ui.log(f"\n🔄 Processing Block {bi+1}")
        self.ui.log(f"📁 File: {file_path}")
        self.ui.log(f"🏷️ TPLNR: {tplnr}")
        self.ui.log(f"📊 Mode: {mode}")

        try:
            ia11.open(tplnr)
            self.ui.log(f"✅ IA11 opened for {tplnr}")
        except Exception as e_open:
            self.ui.log(f"❌ open IA11 failed (block {bi+1}): {e_open}")
            ctx["bi"] += 1
            return self.ui.after(0, self._step_block_begin)

        try:
            df = load_excel(file_path, mode=mode)
        except Exception as e_load:
            self.ui.log(f"❌ load excel failed (block {bi+1}): {e_load}")
            ctx["bi"] += 1
            return self.ui.after(0, self._step_block_begin)

        if df is None or len(df) == 0:
            self.ui.log(f"⚠️ Empty/invalid Excel (block {bi+1}) — skipped")
            ctx["bi"] += 1
            return self.ui.after(0, self._step_block_begin)

        self.ui.log(f"✅ Loaded Excel with {len(df)} entries")
        self.ui.log(f"[DEBUG] df len={len(df)}")     # ← 调试

        ctx["df"] = df
        ctx["ri"] = 0
        return self.ui.after(0, self._step_row)

    def _step_row(self):
        if self._cancelled:
            return self.ui.log("⏹️ 导入已被用户中断")

        ctx = self._ctx
        ia11, df, ri = ctx["ia11"], ctx["df"], ctx["ri"]
        if df is None:
            self.ui.log("⚠️ df is None — skip block")
            ctx["bi"] += 1
            return self.ui.after(0, self._step_block_begin)

        if ri >= len(df):
            try:
                ia11.save(self.ui.log)   # 可选：每块保存
            except Exception as e:
                self.ui.log(f"⚠️ save failed: {e}")
            ctx["bi"] += 1
            return self.ui.after(0, self._step_block_begin)

        self.ui.log(f"[DEBUG] step row ri={ri+1}/{len(df)}")  # ← 调试

        try:
            keep = ia11.fill_operation_step(df, ri, self.ui.log)  # ← 参数顺序对
        except Exception as e_line:
            self.ui.log(f"❌ line {ri+1} failed: {e_line}")
            keep = True

        if keep:
            ctx["ri"] = ri + 1

        return self.ui.after(0, self._step_row)

            
#################### Example Usage ####################
if __name__ == "__main__":
    controller = SAPController(ui=None)

    app_ui = SAP_IA11UploaderApp(
        start_callback=controller.start_import,   # Start Button → Controller
        cancel_callback=controller.cancel_import    # Stop  Button → Controller
    )

    controller.ui = app_ui   # Fill back UI reference
    app_ui.mainloop()

