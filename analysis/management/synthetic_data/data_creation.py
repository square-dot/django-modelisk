import datetime
import math
import random

from analysis.management.synthetic_data.insurance_name_generator import (
    test_insurance_data_generator,
)
from analysis.models.reference_value.Company import Company
from analysis.models.contract.Layer import Layer
from analysis.models.reference_value.Country import Country
from analysis.models.reference_value.Currency import Currency
from analysis.models.contract.Premium import Premium
from analysis.models.contract.Program import Program
from analysis.models.contract.Reinstatement import Reinstatement
from analysis.models.reference_value.Classification import Classification
from analysis.models.RiskProfile import RiskProfile
from analysis.models.Risk import Risk
from analysis.models.LossProfile import LossProfile
from analysis.models.Loss import Loss
from analysis.models.contract.Expenses import Expenses

class ContractsCreation:
    @staticmethod
    def populate_test_data():
        countries = ContractsCreation.create_countries()
        currencies = ContractsCreation.create_currencies()
        lobs = ContractsCreation.create_lobs()
        insureds = ContractsCreation.create_companies(countries)
        programs = ContractsCreation.create_programs(insureds, currencies, lobs)
        for program in programs:
            ContractsCreation.create_contracts(random.choice(currencies), program)
        for _ in programs:
            ContractsCreation.create_risk_profile()
        for _ in programs:
            ContractsCreation.create_loss_profile()

    @staticmethod
    def create_countries() -> list[Country]:
        for t in (
            ("USA", "United States"),
            ("ITA", "Italy"),
            ("FRA", "France"),
            ("GBR", "Great Britain"),
            ("GER", "Germany"),
            ("CHE", "Switzerland"),
            ("SWE", "Sweden"),
            ("BRA", "Brazil"),
            ("ESP", "Spain"),
            ("JPN", "Japan"),
        ):
            Country.objects.create(iso_code_3=t[0], name=t[1])
        return list(Country.objects.all())

    @staticmethod
    def create_currencies() -> list[Currency]:
        for t in (
            ("CHF", "Swiss Franc"),
            ("USD", "US Dollar"),
            ("GBP", "British Pound"),
            ("EUR", "Euro"),
        ):
            Currency.objects.create(iso_code_3=t[0], name=t[1])
        return list(Currency.objects.all())

    @staticmethod
    def create_lobs() -> list[Classification]:
        for t in (
            ("Agriculture"),
            ("Property"),
            ("Casualty"),
            ("Motor"),
        ):
            Classification.objects.create(name=t[0])
        return list(Classification.objects.all())

    @staticmethod
    def create_companies(countries: list[Country]):
        nr = 50
        for v in test_insurance_data_generator(nr, countries):
            Company.objects.create(
                country=next((c for c in countries if c.iso_code_3 == v[0])),
                name=v[1],
                email=v[2],
            )
        return Company.objects.all()

    @staticmethod
    def create_programs(insureds, currencies, lobs) -> list[Program]:
        nr = 100
        for _ in range(nr):
            currency = random.choice(currencies)
            insured = random.choice(insureds)
            lob = random.choice(lobs)
            Program.objects.create(
                insured=insured,
                currency=currency,
                start_date=datetime.date(2020, 1, 1),
                end_date=datetime.date(2020, 12, 31),
                line_of_business=lob,
            )
        return list(Program.objects.all())

    @staticmethod
    def create_premium(magnitude=1000) -> Premium:
        premium = max(
            round(random.normalvariate(mu=magnitude, sigma=magnitude / 4), 2), 0
        )
        return Premium.objects.create(upfront_premium=premium)

    @staticmethod
    def create_contracts(currency: Currency, program: Program):
        magnitude = random.choice([10_000 * (3**e) for e in range(10)])
        rounding = -1 * int(math.log10(magnitude) - 2)
        contract_type = random.choice(("QS", "XL_Risk", "XL_Event"))

        premium = ContractsCreation.create_premium(magnitude=magnitude)
        brokerage = max(
            round(random.normalvariate(mu=magnitude / 20, sigma=magnitude / 40), 2), 0
        )
        expenses = Expenses.objects.create(upfront_expenses=max(
            round(random.normalvariate(mu=magnitude / 30, sigma=magnitude / 60), 2), 0
        ))
        share = max(round(random.random(), 4), 0)
        participation = max(0, round(random.random(), 2))
        match contract_type:
            case "QS":
                Layer.objects.create(
                    program=program,
                    currency=currency,
                    premium=premium,
                    participation=participation,
                    share=share,
                    expenses=expenses,
                )
            case "XL_Risk":
                retention = max(round(random.normalvariate(mu=magnitude), rounding), 0)
                limit = max(round(random.normalvariate(mu=magnitude), rounding), 0)
                Layer.objects.create(
                    program=program,
                    currency=currency,
                    premium=premium,
                    participation=participation,
                    expenses=expenses,
                    risk_retention=retention,
                    risk_limit=limit,
                    aggregate_retention=None,
                    aggregate_limit=None,
                )
            case "XL_Event":
                retention = max(round(random.normalvariate(mu=magnitude), rounding), 0)
                limit = max(round(random.normalvariate(mu=magnitude), rounding), 0)
                c = Layer.objects.create(
                    program=program,
                    currency=currency,
                    premium=premium,
                    participation=participation,
                    expenses=expenses,
                    event_retention=retention,
                    event_limit=limit,
                    aggregate_retention=None,
                    aggregate_limit=None,
                )
                Reinstatement.objects.create(contract=c, nr=1, size=1, cost=0.5)

    @staticmethod
    def create_risk_profile():
        rp = RiskProfile.objects.create(name="test_risk_profile")
        for i in range(3):
            Risk.objects.create(
                risk_profile=rp,
                name=f"test_risk_{i}",
                quantity=random.randint(1, 4),
                expected_maximal_loss=10_000_000,
                expected_average_loss=1_000_000,
                tag_1=random.choice(("Europe", "Africa")),
                tag_2=random.choice(("private building", "public building")),
                tag_3=random.choice(("small", "big")),
            )

    @staticmethod
    def create_loss_profile():
        lp = LossProfile.objects.create(name="test_loss_profile")
        for i in range(30):
            Loss.objects.create(
                loss_profile=lp,
                name=f"test_loss_{i}",
                size=random.normalvariate(1_000, 300),
                period = random.randint(1, 30),
            )