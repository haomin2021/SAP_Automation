# SAP/IH01.py

import time
import os

class IH01Transaction:
    def __init__(self, session):
        self.session = session

    def export_html(self, save_dir: str, tplnr: str = "6200", filename: str = "TP_data.html"):
        session = self.session
        session.StartTransaction("IH01")
        if not save_dir:
            # Get the current file directory (i.e., SAP/)
            current_dir = os.path.dirname(__file__)
            # Relative path to Resources/Technischer Platz
            save_dir = os.path.abspath(os.path.join(current_dir, "..", "Resources", "TechnischerPlatz"))

        # input Technischer Platz
        session.findById("wnd[0]/usr/ctxtDY_TPLNR").text = tplnr
        # Press 'Ausführen' button
        session.findById("wnd[0]/tbar[1]/btn[8]").press()
        # Press 'Aufreißen Gesamt' button
        session.findById("wnd[0]/tbar[1]/btn[16]").press()
        # Press 'Sichern als lokale Datei' button
        session.findById("wnd[0]/tbar[1]/btn[45]").press()
        # Select 'HTML Format'
        session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").select()
        session.findById("wnd[1]/usr/subSUBSCREEN_STEPLOOP:SAPLSPO5:0150/sub:SAPLSPO5:0150/radSPOPLI-SELFLAG[3,0]").setFocus()
        # Press 'Continue' button
        session.findById("wnd[1]/tbar[0]/btn[0]").press()
        time.sleep(2)
        # Input File path
        session.findById("wnd[1]/usr/ctxtDY_PATH").text = save_dir
        # Input File name
        session.findById("wnd[1]/usr/ctxtDY_FILENAME").text = "TP_data.html"
        session.findById("wnd[1]/tbar[0]/btn[11]").press()
        # Wait for the file to be saved
        time.sleep(2)
        # Close the transaction
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        session.findById("wnd[0]/tbar[0]/btn[15]").press()
        

#################### Example Usage ####################
if __name__ == "__main__":
    from sap_interface import SAPSession
    import os

    sap = SAPSession()
    ih01 = IH01Transaction(sap.session)

    # Use default save directory
    ih01.export_html(
        save_dir="",  # Leave blank to use default path
        tplnr="6200",
        filename="TP_6200.html"
    )