import win32com.client
import pandas as pd
import time
import tkinter as tk
from tkinter import messagebox

###############################################################
# @ Test SAP GUI Scripting Connection  (SAP GUI must be open and logged in)
def connect_to_sap_gui():
    try:
        SapGuiAuto = win32com.client.GetObject("SAPGUI")
        application = SapGuiAuto.GetScriptingEngine
        connection = application.Children(0)
        session = connection.Children(0)
        print("✅ Connected to SAP GUI successfully!")
        return session
    except Exception as e:
        print("❌ Failed to connect to SAP GUI. PLease check if Scripting is activated and SAP GUI is logged in.")
        print(str(e))

# @ Open IA11 window based on input Technischen Platz
def open_ia11_window(session, technischer_platz):
        session.StartTransaction("IA11")
        # Input Technischen Platz
        session.findById("wnd[0]/usr/ctxtRC27E-TPLNR").text = technischer_platz
        # Press 'Plan'
        session.findById("wnd[0]/tbar[1]/btn[5]").press()
        # Press 'Neue Einträge'
        session.findById("wnd[0]/tbar[1]/btn[6]").press()
        # Input 'Status Plan'
        session.findById("wnd[0]/usr/ctxtPLKOD-STATU").text = "4"
        # Input 'Wartungsstrategie'
        session.findById("wnd[0]/usr/ctxtPLKOD-STRAT").text = "Z7"
        # Press 'Vorgang'
        session.findById("wnd[0]/tbar[1]/btn[16]").press()

# @ Load Data from Excel File
def load_data_from_excel(file_path):
    import pandas as pd
    try:
        df = pd.read_excel(file_path, header=None)
        print("✅ Data loaded from Excel successfully!")
        return df
    except Exception as e:
        print("❌ Failed to load data from Excel.")
        print(str(e))

###############################################################
# ------------------------------------------------------------#
###############################################################
if __name__ == "__main__":
    # Testing SAP GUI Scripting Connection
    session = connect_to_sap_gui()

    # Open IA11 window with Technischen Platz
    open_ia11_window(session, "6200-PR-H20-GR00-SEXT-0006")   

    # Load Data from Excel File
    df = load_data_from_excel(r"GUI\Arbeitsplan.xlsx")
    print(df.head())  # Display the first few rows of the DataFrame

    # -------------------------------------------------------------
    # Put each line from DataFrame into SAP 'Vorgangsbeschreibung'
    # -------------------------------------------------------------
    for index, row in df.iterrows():
        vorgangsnummer_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-VORNR[0,{min(index, 15)}]"
        vorgangsnummer = str((index + 1) * 10).zfill(4)
        beschreibung_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-LTXA1[5,{min(index, 15)}]"
        beschreibung_text = str(row[0][:40])  # Limit to 40 characters
        
        # Deal with scolling issue for index >= 16
        if index >= 16:
            try:
                # Try to scroll to the target row
                scroll_position = max(0, index - 15)  # Ensure not less than 0
                session.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position
                # print(f"🔃 Try to scroll to line {scroll_position}")
                time.sleep(2)  # Add wait time for the scroll to take effect

                # Check if the target row is visible by trying to set focus
                try:
                    test_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3400/txtPLPOD-VORNR[0,{min(index, 15)}]"
                    test_field = session.findById(test_id)
                    test_field.setFocus()
                except Exception as e:
                    print(e)
                    session.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position + 2
                    time.sleep(1.5)
                
                # check if the target row is visible
                try:
                    session.findById(vorgangsnummer_id).setFocus()
                except:
                    # if not visible, try to adjust the scroll position
                    session.findById("wnd[0]/usr/tblSAPLCPDITCTRL_3400").verticalScrollbar.position = scroll_position + 1
                    time.sleep(1)
                    print(f"🔃 Adject scolling position")
            except Exception as e:
                print(f"⚠️ 滚动失败：{e}")
                # 尝试继续处理，不直接退出
                continue

        try:
            # Input 'Vorgangsnummer' and 'Beschreibung'
            session.findById(vorgangsnummer_id).setFocus()
            time.sleep(0.5)
            session.findById(vorgangsnummer_id).text = vorgangsnummer        
            session.findById(beschreibung_id).setFocus()
            time.sleep(0.5)
            session.findById(beschreibung_id).text = beschreibung_text
            session.findById(beschreibung_id).caretPosition = len(beschreibung_text)
        except Exception as e:
            print(f"⚠️ Fail to deal with line {index}: {e}")
            # Keep going to the next line
            continue

        # Open 'Wartungspaket' and select the first one
        try:
            session.findById("wnd[0]/usr/btnTEXT_DRUCKTASTE_WP").press()
            time.sleep(2)
            
            wartungspaket_id = f"wnd[0]/usr/tblSAPLCPDITCTRL_3600/chkRIHSTRAT-MARK01[3,{min(index, 15)}]"
            session.findById(wartungspaket_id).selected = True
            session.findById(wartungspaket_id).setFocus()
            time.sleep(0.5)
        except Exception as e:
            print(f"⚠️ Fail to select 'Wartungspaket': {e}")
        
        # Go back to the previous screen
        try:
            session.findById("wnd[0]/tbar[1]/btn[26]").press()
            time.sleep(2)
        except:
            print("⚠️ Fail to go back to the previous screen")
            # Try to use F12 as a backup
            session.findById("wnd[0]").sendVKey(12)  # F12 is usually the key for 'Back' in SAP GUI
            time.sleep(2)

