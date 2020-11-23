import numpy as np
import pandas as pd
from .models import Transaction, Account, User


class Stats:
    transactions = np.zeros((0, 1))

    def __init__(self, user: User):
        user_accounts = Account.objects.filter(user_id=user.email).values()[0]
        self.transactions = Transaction.objects.filter(account_id__in=user_accounts).values()
        print(self.transactions)

    def get_median(self):
        return np.median(self.transactions)

    def get_mean(self):
        return np.mean(self.transactions)

    def get_total_by_mcc(self):
        df = pd.DataFrame(self.transactions)
        return df.groupby(['mcc']).apply(lambda x: np.mean(x))
