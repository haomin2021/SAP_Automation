import win32com.client
import pandas as pd
import time
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# ----------------------------- SAP Connection & Logic -----------------------------
def connect_to_sap_gui():
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        return session
    except Exception as e:
        raise RuntimeError("Failed to connect to SAP GUI. Make sure SAP is running and scripting is enabled.\n" + str(e))

def open_ia11_window(session, technischer_platz):
    session.StartTransaction("IA11")
    session.findById("wnd[0]/usr/ctxtRC27E-TPLNR").text = technischer_platz
    session.findById("wnd[0]/tbar[1]/btn[5]").press()  # "Plan"
    session.findById("wnd[0]/tbar[1]/btn[6]").press()  # "New Entry"
    session.findById("wnd[0]/usr/ctxtPLKOD-STATU").text = "4"  # Status
    session.findById("wnd[0]/usr/ctxtPLKOD-STRAT").text = "Z7"  # Strategy
    session.findById("wnd[0]/tbar[1]/btn[16]").press()  # "Operation"

def load_data_from_excel(file_path):
    try:
        df = pd.read_excel(file_path, header=None)
        return df
    except Exception as e:
        raise RuntimeError("Failed to load Excel file:\n" + str(e))

def fill_data_into_sap(session, df, log_callback):
    for index, row in df.iterrows():
        operation_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-VORNR[0,{min(index, 15)}]"
        operation_number = str((index + 1) * 10).zfill(4)
        description_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-LTXA1[5,{min(index, 15)}]"
        description_text = str(row[0][:40])

        if index >= 16:
            scroll_position = max(0, index - 15)
            session.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position
            time.sleep(1.5)

        try:
            session.findById(operation_id).setFocus()
            session.findById(operation_id).text = operation_number        
            session.findById(description_id).setFocus()
            session.findById(description_id).text = description_text
            session.findById(description_id).caretPosition = len(description_text)
        except Exception as e:
            log_callback(f"❌ Line {index + 1} failed to input: {e}")
            continue

        # Select Wartungspaket
        try:
            session.findById("wnd[0]/usr/btnTEXT_DRUCKTASTE_WP").press()
            time.sleep(1)
            wp_checkbox_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3600/chkRIHSTRAT-MARK01[3,{min(index, 15)}]"
            session.findById(wp_checkbox_id).selected = True
            session.findById(wp_checkbox_id).setFocus()
        except Exception as e:
            log_callback(f"⚠️ Failed to select Wartungspaket on line {index + 1}: {e}")
        finally:
            try:
                session.findById("wnd[0]/tbar[1]/btn[26]").press()  # Back
            except:
                session.findById("wnd[0]").sendVKey(12)  # F12 backup
            time.sleep(1)

        log_callback(f"✅ Line {index + 1} completed")

# ----------------------------- GUI Application -----------------------------
class SAPUploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SAP IA11 Batch Operation Import Tool")
        self.root.geometry("700x500")

        self.file_path = tk.StringVar()
        self.tplnr = tk.StringVar()

        # Excel file input
        tk.Label(root, text="Select Excel File:").pack()
        tk.Entry(root, textvariable=self.file_path, width=70).pack(pady=2)
        tk.Button(root, text="Browse", command=self.browse_file).pack()

        # Technischen Platz input
        tk.Label(root, text="Technischen Platz:").pack(pady=(10, 0))
        tk.Entry(root, textvariable=self.tplnr, width=50).pack()

        # Start button
        tk.Button(root, text="Start Import", bg="green", fg="white", command=self.run_process).pack(pady=10)

        # Log area
        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20)
        self.log_area.pack()

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if path:
            self.file_path.set(path)

    def log(self, message):
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.root.update_idletasks()

    def run_process(self):
        try:
            session = connect_to_sap_gui()
            self.log("✅ Connected to SAP GUI successfully")

            technischer_platz = self.tplnr.get().strip()
            if not technischer_platz:
                messagebox.showwarning("Input Required", "Please enter Technischen Platz.")
                return
            
            open_ia11_window(session, technischer_platz)
            self.log(f"✅ Opened IA11 for: {technischer_platz}")

            df = load_data_from_excel(self.file_path.get())
            self.log(f"✅ Excel loaded successfully with {len(df)} lines")

            fill_data_into_sap(session, df, self.log)
            self.log("🎉 All lines completed successfully")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.log(f"❌ Error occurred: {str(e)}")

# ----------------------------- Launch Application -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SAPUploaderApp(root)
    root.mainloop()
