from insurance_contract.models import (Country, Insured, AdministrativeInformation,
                                        Premium, Expenses, Contract, QuotaShare)
import datetime

class ContractCreation():

    def __init__(self):
        countries = self.create_countries()
        insureds = self.create_insureds(countries)
        self.create_contracts(insureds)


    @staticmethod
    def create_countries():
        for t in (("USA", "United States"), ("ITA", "Italy"), ("FRA", "France"), ("GBR", "Great Britain"),
                    ("GER", "Germany"), ("CHE", "Switzerland"), ("JPN", "Japan")):
            Country.objects.create(iso_code_3=t[0], name=t[1])

    def create_insureds(self, countries):
        for t in zip(countries, ("AAA", "BBB", "CCC", "DDD", "EEE", "FFF", "GGG", "HHH", "III", "JJJ", "KKK")):
            Insured.objects.create(country=t[0], name=t[1])


    def create_contracts(self, insureds):
        for t in zip(insureds, ((150, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (200, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (300, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (350, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (400, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (500, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),),
                                (650, 20, 15, (1, 1, 0.5), (datetime.date(2020, 1, 1), datetime.date(2020, 12, 31), 1, 10000, 1000, 0.5),))):
            a = AdministrativeInformation.objects.create(insured=t[0])
            p = Premium.objects.create(premium=t[1][0])
            e = Expenses.objects.create(commission=t[1][1], brokerage=t[1][2])
            c = QuotaShare(start_date=t[1][4][0], end_date=t[1][4][1], participation=t[1][4][2], share=t[1][4][5])
            Contract.objects.create(administrative_information=a, premium=p, expenses=e, coverage=c)



