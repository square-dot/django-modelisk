import random

type = (
    "Insurance",
    "Insurance Company",
    "Insurance Society",
    "Mutual",
    "Mutual Insurers",
    "Insurance Co.",
    "Assurance Co.",
    "Insurance Group",
    "Insurance Department",
    "Union",
    "Mutual Group",
    "Capital",
    "Insurance",
)
name = (
    "Lifeline",
    "The Bernadelli",
    "Indursky & Sons",
    "Varnelle",
    "Schneiber",
    "Pleister",
    "LLPT",
    "Ronald Wilkes",
    "Brown Star",
    "Liberty",
    "ROC",
    "PK Lines",
    "Wildies",
    "Rookstar",
    "Pence",
    "Breighton",
    "Pell",
    "UTR",
    "PkW",
    "Von Merten",
    "Merton",
    "Skylar",
    "Bersell",
    "Finpars",
    "P&T",
    "Beler",
    "Prestons",
    "Flirsing Barles",
    "Los Bueros",
    "Würthly",
    "Amar Sen",
    "Fessari",
    "Murdelle",
    "Bührlens",
    "Presos do Soto",
    "Mitzuro Yabashi",
    "Parandanan",
    "Samsang",
    "Prizlet Heirs",
    "KKTP",
    "Brollen",
    "Persicic",
    "The Pillars",
    "Parisienne",
    "Vournec",
    "Barles",
    "HSKB",
    "Bertanc",
    "Bulgakovian",
    "Blackstones",
    "Frisian",
)
single_name = (
    "Insuritas",
    "Assurelines",
    "Insuricare",
    "Umbrellife",
    "Assuricare",
    "Mutualmotor",
    "Brolife",
    "Gercare",
    "Brassurance",
)

def test_insurance_name_generator():
    if random.random() < 0.02:
        return random.choice(single_name)
    if random.random() < 0.05:
        return random.choice(name)
    if random.random() < 0.2:
        cc = random.sample(name, 2)
        return cc[0] + " & " + cc[1] + " " + random.choice(type)
    return random.choice(name) + " " + random.choice(type)
