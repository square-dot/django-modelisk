from insurance_contract.models import (Country, Company, AdministrativeInformation,
                                        Premium, Expenses, Contract, QuotaShare, ExcessOfLoss)
from insurance_contract.models import ContractType
from insurance_name_generator import test_insurance_name_generator
import datetime
import random
import math

class ContractsCreation():

    @staticmethod
    def populate_test_data():
        countries = ContractsCreation.create_countries()
        insureds = ContractsCreation.create_companies(countries)
        ContractsCreation.create_contracts(insureds)

    @staticmethod
    def depopulate_and_repopulate_test_data():
        ContractsCreation.empty_database()
        ContractsCreation.populate_test_data()

    @staticmethod
    def create_countries():
        for t in (("USA", "United States"), ("ITA", "Italy"), ("FRA", "France"), ("GBR", "Great Britain"),
                    ("GER", "Germany"), ("CHE", "Switzerland"), ("JPN", "Japan")):
            Country.objects.create(iso_code_3=t[0], name=t[1])
        return Country.objects.all()

    @staticmethod
    def create_companies(countries):
        nr = 50
        for t in zip([countries[i % len(countries)] for i in range(nr)], [test_insurance_name_generator() for i in range(nr)]):
            q = Company.objects.filter(name=t[1])
            if q.count() > 0:
                Company.objects.create(country=t[0], name=(t[1] + f" ({q.count()})"))
            else:
                Company.objects.create(country=t[0], name=t[1])
        return Company.objects.all()


    @staticmethod
    def create_contracts(insureds):
        nr = 100
        for i in range(nr):
            magnitude = random.choice((1000, 4000, 10000, 38000, 100000))
            v = test_contract_number_generator(magnitude)
            c = test_coverage_generator(random.choice((ContractType("QS"), ContractType("XL_Risk"), ContractType("XL_Event"))), magnitude=magnitude)
            e = Expenses.objects.create(upfront_brokerage=v[1], upfront_commission=v[2])
            p = Premium.objects.create(upfront_premium=v[0])
            i = random.choice(insureds)
            a = AdministrativeInformation.objects.create(name = Contract.default_name(c, i.name), insured = i)
            Contract.objects.create(administrative_information = a,
                                    premium = p,
                                    expenses = e,
                                    coverage = c)   
        return Contract.objects.all()


    @staticmethod
    def empty_database():
        for c in (Country, Company, AdministrativeInformation, Premium, Expenses, Contract, QuotaShare, ExcessOfLoss):
            c.objects.all().delete()


def test_contract_number_generator(magnitude = 1000) -> tuple:
    premium = max(round(random.normalvariate(mu = magnitude, sigma = magnitude / 4), 2), 0)
    brokerage = max(round(random.normalvariate(mu = magnitude / 20, sigma = magnitude / 40), 2), 0)
    commission = max(round(random.normalvariate(mu = magnitude / 30, sigma = magnitude / 60), 2), 0)
    participation = max(round(random.random(), 4), 0)
    return (premium, brokerage, commission, participation)


def test_coverage_generator(contract_type:ContractType, magnitude=1000):
    if contract_type.is_quota_share():
        return QuotaShare.objects.create(start_date = datetime.date(2020,1,1),
                                        end_date = datetime.date(2020, 12,31), 
                                        participation = max(0, round(random.random(), 2)),
                                        share=max(round(random.random(),4),0))
    if contract_type.type == "XL_Risk":
        return ExcessOfLoss.objects.create(start_date = datetime.date(2020,1,1),
                                            end_date = datetime.date(2020, 12,31),
                                            participation = max(0, round(random.random(), 2)),
                                            risk_retention = max(round(random.normalvariate(mu=magnitude*3), -1 * int(math.log(magnitude) - 1)), 0),
                                            risk_limit=max(round(random.normalvariate(mu=magnitude*10), -1 * int(math.log(magnitude) - 1)), 0))
    if contract_type.type == "XL_Event":
        return ExcessOfLoss.objects.create(start_date = datetime.date(2020,1,1),
                                            end_date = datetime.date(2020, 12,31),
                                            participation = max(0, round(random.random(), 2)),
                                            event_retention = max(round(random.normalvariate(mu=magnitude*3), -1 * int(math.log(magnitude) - 1)), 0),
                                            event_limit=max(round(random.normalvariate(mu=magnitude*10), -1 * int(math.log(magnitude) - 1)), 0))




