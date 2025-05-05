# SAP/CC04.py

class CC04Transaction:
    def __init__(self, session):
        self.session = session

    def open(self, technischer_platz):
        session = self.session
        session.StartTransaction("CC04")

######################################################################

if __name__ == "__main__":
    # Example usage
    from SAP.sap_interface import SAPSession

    sap = SAPSession()
    cc04 = CC04Transaction(sap.session)
    cc04.open("6200")