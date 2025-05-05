# sap/sap_interface.py

import win32com.client


class SAPSession:
    def __init__(self):
        self.session = self._connect_to_sap()

    def _connect_to_sap(self):
        """连接到正在运行的 SAP GUI 会话"""
        try:
            SapGuiAuto = win32com.client.GetObject("SAPGUI")
            application = SapGuiAuto.GetScriptingEngine
            connection = application.Children(0)
            session = connection.Children(0)
            return session
        except Exception as e:
            raise RuntimeError("Failed to connect to SAP GUI. Make sure SAP is running and scripting is enabled.\n" + str(e))

