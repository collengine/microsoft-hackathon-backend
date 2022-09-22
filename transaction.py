class Transaction:
    def __init__(self,created_at, guid, amount, milliliters, timestamp, status, receipt):
        self.created_at = created_at
        self.guid = guid
        self.amount = amount
        self.milliliters = milliliters
        self.timestamp = timestamp
        self.status = status
        self.receipt = receipt

    def  __repr__(self):
        return "Transaction('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(self.created_at, self.guid, self.amount, self.milliliters, self.timestamp, self.status, self.receipt)


        