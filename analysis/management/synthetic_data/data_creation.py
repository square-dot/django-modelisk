from analysis.models import (
    Country,
    Company,
    Premium,
    Expenses,
    Currency,
    Contract,
    QuotaShare,
    ExcessOfLoss,
    Program,
)
from analysis.management.synthetic_data.insurance_name_generator import (
    test_insurance_data_generator,
)
import datetime
import random
import math


class ContractsCreation:
    @staticmethod
    def populate_test_data():
        countries = ContractsCreation.create_countries()
        currencies = ContractsCreation.create_currencies()
        insureds = ContractsCreation.create_companies(countries)
        ContractsCreation.create_programs(insureds, currencies)

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
    def create_currencies():
        for t in (
            ("CHF", "Swiss Franc"),
            ("USD", "US Dollar"),
            ("GBP", "British Pound"),
            ("EUR", "Euro"),
        ):
            Currency.objects.create(iso_code_3=t[0], name=t[1])
        return Currency.objects.all()

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
    def create_premium(magnitude=1000) -> Premium:
        premium = max(
            round(random.normalvariate(mu=magnitude, sigma=magnitude / 4), 2), 0
        )
        return Premium.objects.create(upfront_premium=premium)

    @staticmethod
    def create_expenses(magnitude=1000) -> Expenses:
        brokerage = max(
            round(random.normalvariate(mu=magnitude / 20, sigma=magnitude / 40), 2), 0
        )
        commission = max(
            round(random.normalvariate(mu=magnitude / 30, sigma=magnitude / 60), 2), 0
        )
        return Expenses.objects.create(
            upfront_brokerage=brokerage, upfront_commission=commission
        )

    @staticmethod
    def create_coverages(contract_type: str, magnitude=1000) -> list:
        c = []
        if contract_type == "QS":
            c.append(
                QuotaShare.objects.create(
                    participation=max(0, round(random.random(), 2)),
                    share=max(round(random.random(), 4), 0),
                )
            )
        if contract_type == "XL_Risk":
            rounding = -1 * int(math.log10(magnitude) - 2)
            magnitude *= 3
            a = max(round(random.normalvariate(mu=magnitude), rounding), 0)
            for _ in range(random.randint(1, 3)):
                magnitude *= 3
                b = max(round(random.normalvariate(mu=magnitude), rounding), 0)
                c.append(
                    ExcessOfLoss.objects.create(
                        participation=max(0, round(random.random(), 2)),
                        risk_retention=a,
                        risk_limit=b,
                    )
                )
                a = b
        if contract_type == "XL_Event":
            reinstatements = {1: (1, 1), 2: (1, 2)}
            c.append(
                ExcessOfLoss.objects.create(
                    participation=max(0, round(random.random(), 2)),
                    event_retention=max(
                        round(
                            random.normalvariate(mu=magnitude * 3),
                            -1 * int(math.log(magnitude) - 1),
                        ),
                        0,
                    ),
                    event_limit=max(
                        round(
                            random.normalvariate(mu=magnitude * 10),
                            -1 * int(math.log(magnitude) - 1),
                        ),
                        0,
                    ),
                    reinstatements_data=reinstatements,
                )
            )
        return c

    @staticmethod
    def create_contracts(currencies: list[Currency]) -> list[Contract]:
        premium_magnitude = random.choice([10_000 * (3**e) for e in range(10)])
        coverages = ContractsCreation.create_coverages(
            random.choice(("QS", "XL_Risk", "XL_Event")), magnitude=premium_magnitude
        )
        c = []
        for coverage in coverages:
            currency = random.choice(currencies)
            premium = ContractsCreation.create_premium(magnitude=premium_magnitude)
            expenses = ContractsCreation.create_expenses(magnitude=premium_magnitude)
            c.append(
                Contract.objects.create(
                    currency=currency,
                    premium=premium,
                    expenses=expenses,
                    coverage=coverage,
                )
            )
        return c

    @staticmethod
    def create_programs(insureds, currencies):
        nr = 100
        for _ in range(nr):
            contracts = ContractsCreation.create_contracts(currencies)
            currency = random.choice(currencies)
            insured = random.choice(insureds)
            Program.objects.create(
                insured=insured,
                currency=currency,
                start_date=datetime.date(2020, 1, 1),
                end_date=datetime.date(2020, 12, 31),
                contracts={
                    key: value.pk
                    for key, value in zip(range(len(contracts)), contracts)
                },
            )
        return Program.objects.all()
