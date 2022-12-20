class TransactionFetcher:

    def __init__(self, acc_num: int):
        self.acc_num = acc_num

    def fetch(self) -> None:
        """
        - podivat se u uctu na "last_fetched", to je datum, kdy byly transakce naposled stazeny
        - stahnout transakce ode dne "last_fetched" + 1 do dne "today" - 1
        :return:
        """
        pass

