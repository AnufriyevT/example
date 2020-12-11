import datetime as dt


class Calculator:
    def __init__(self, limit: int):
        self.limit = limit  # Defining the day limit
        self.records = []  # List where all records saved

    def add_record(self, record):
        """
        This function adds record to record list and saves
        record to the dictionary by date
        :param record to be added to the record list and dictionary
        :type record: Record
        """
        self.records.append(record)  # Adds new record to records list

    def get_stats(self, days) -> int:
        """
        This function calculates total of money/calories spent
        for the last n days
        :return amount of money spent or the whole week
        """
        today = dt.datetime.today().date()
        days_before = today - dt.timedelta(days=days)
        total = sum(r.amount for r in self.records
                    if days_before <= r.date <= today)
        return total

    def get_today_stats(self) -> int:
        """
        This function returns total amount of
        calories/cash that was used today
        :return amount of money spent today
        """
        return self.get_stats(0)

    def get_week_stats(self) -> int:
        """
        This function calculates total of money/calories spent
        for the last 7 days
        :return amount of money spent or the whole week
        """
        return self.get_stats(6)

    def get_remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 60.0  # defining a USD rate to RUB rate at 60
    EURO_RATE = 70.0  # defining a EURO rate to RUB rate at 70
    currency_dict = {  # Keeps name of the currency and it's rate
        'rub': ('руб', 1),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE)
    }


    def get_today_cash_remained(self, currency):
        """
        This function returns amount of money left for today

        :param currency: currency in which amount of money left returns
        :type currency: str
        :return: prepared phrases depending on the remainder
        :rtype: str
        """
        remainder = self.get_remained()
        if remainder == 0:
            return 'Денег нет, держись'
        currency, rate = self.currency_dict[currency]
        remainder /= rate
        if remainder < 0:
            remainder = -remainder
            return (f'Денег нет, держись: твой долг - {remainder:.2f} '
                    f'{currency}')
        return (f'На сегодня осталось {remainder:.2f} '
                f'{currency}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        """
        This function returns amount of calories left for today

        :return: prepared phrases depending on the remainder
        :rtype: str
        """
        remainder = self.get_remained()
        if remainder > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более {remainder} кКал')
        return 'Хватит есть!'


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:  # if user does not specify the date
            self.date = dt.date.today()  # Then take today's date
        else:
            date_format = '%d.%m.%Y'
            self.date = dt.datetime.strptime(date, date_format).date()