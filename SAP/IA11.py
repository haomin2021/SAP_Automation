# SAP/IA11.py

import time

class IA11Transaction:
    def __init__(self, session):
        self.session = session

    def open(self, technischer_platz):
        session = self.session
        session.StartTransaction("IA11")
        session.findById("wnd[0]/usr/ctxtRC27E-TPLNR").text = technischer_platz
        session.findById("wnd[0]/tbar[1]/btn[5]").press()  # "Plan"
        session.findById("wnd[0]/tbar[1]/btn[6]").press()  # "New Entry"
        session.findById("wnd[0]/usr/ctxtPLKOD-STATU").text = "4"  # Status
        session.findById("wnd[0]/usr/ctxtPLKOD-STRAT").text = "Z7"  # Strategy
        session.findById("wnd[0]/tbar[1]/btn[16]").press()  # "Operation"

    def fill_operations(self, df, log_callback, should_cancel=lambda: False):
        for index, row in df.iterrows():
            # Check for cancellation
            if should_cancel():
                log_callback("🚫 Operation cancelled")
                break

            operation_number = str((index + 1) * 10).zfill(4)
            description_text = str(row[0])[:40]

            if index >= 16:
                scroll_position = max(0, index - 15)
                self.session.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position
                time.sleep(1.5)

            try:
                self._input_operation(index, operation_number, description_text)
            except Exception as e:
                log_callback(f"❌ Line {index + 1} failed: {e}")
                continue

            try:
                # Check for cancellation
                if should_cancel():
                    log_callback("🚫 Operation cancelled")
                    break
                self._select_maintenance_package(index)
            except Exception as e:
                log_callback(f"⚠️ Wartungspaket select failed on line {index + 1}: {e}")

            log_callback(f"✅ Line {index + 1} completed")
    
    def fill_operation_step(self, df, row_idx, log):
        """
        执行“第 row_idx 行”的录入；成功或失败都返回 True 表示继续下一行；
        当 row_idx >= len(df) 时返回 False 表示本 block 完成。
        """
        if row_idx >= len(df):
            return False

        s = self.session
        row = df.iloc[row_idx]

        operation_number = str((row_idx + 1) * 10).zfill(4)
        description_text = str(row.iloc[0])[:40]

        # 滚动到可见区（0..15）
        if row_idx >= 16:
            scroll_position = max(0, row_idx - 15)
            s.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position
            time.sleep(0.05)  # VERY SHORT，避免卡 UI

        vis_idx = min(row_idx, 15)
        op_id   = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-VORNR[0,{vis_idx}]"
        desc_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-LTXA1[5,{vis_idx}]"

        try:
            s.findById(op_id).setFocus();   s.findById(op_id).text  = operation_number
            s.findById(desc_id).setFocus(); s.findById(desc_id).text = description_text
            s.findById(desc_id).caretPosition = len(description_text)
        except Exception as e:
            log(f"❌ Line {row_idx+1} failed to input: {e}")
            return True  # 本行失败但不中断

        # 维护包（允许失败）
        try:
            s.findById("wnd[0]/usr/btnTEXT_DRUCKTASTE_WP").press()
            time.sleep(0.05)
            wp_chk = f"wnd[0]/usr/tblSAPLCPDITCTRL_3600/chkRIHSTRAT-MARK01[3,{vis_idx}]"
            s.findById(wp_chk).selected = True
            s.findById(wp_chk).setFocus()
            try:
                s.findById("wnd[0]/tbar[1]/btn[26]").press()
            except:
                s.findById("wnd[0]").sendVKey(12)
        except Exception as e:
            log(f"⚠️ Wartungspaket select failed on line {row_idx+1}: {e}")

        log(f"✅ Line {row_idx+1} completed")
        return True

    def _input_operation(self, index, operation_number, description_text):
        session = self.session
        row_index = min(index, 15)

        operation_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-VORNR[0,{row_index}]"
        description_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-LTXA1[5,{row_index}]"

        session.findById(operation_id).setFocus()
        session.findById(operation_id).text = operation_number
        session.findById(description_id).setFocus()
        session.findById(description_id).text = description_text
        session.findById(description_id).caretPosition = len(description_text)

    def _select_maintenance_package(self, index):
        session = self.session
        session.findById("wnd[0]/usr/btnTEXT_DRUCKTASTE_WP").press()
        time.sleep(1)

        wp_row_index = min(index, 15)
        wp_checkbox_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3600/chkRIHSTRAT-MARK01[3,{wp_row_index}]"

        session.findById(wp_checkbox_id).selected = True
        session.findById(wp_checkbox_id).setFocus()

        try:
            session.findById("wnd[0]/tbar[1]/btn[26]").press()  # Back
        except:
            session.findById("wnd[0]").sendVKey(12)  # Alternative back
        time.sleep(1)
