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

    def fill_operations(self, df, log_callback):
        for index, row in df.iterrows():
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
                self._select_maintenance_package(index)
            except Exception as e:
                log_callback(f"⚠️ Wartungspaket select failed on line {index + 1}: {e}")

            log_callback(f"✅ Line {index + 1} completed")

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
