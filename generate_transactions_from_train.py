import random
import pandas as pd
from datetime import datetime, timedelta

# -------------------------
# INPUT FILES
# -------------------------

TRAIN_FILE = "train.csv"

PROFILE_FILE = "dataset/customer_profiles.csv"

OUTPUT_FILE = "dataset/transactions.csv"

# -------------------------
# LOAD DATA
# -------------------------

crime_df = pd.read_csv(
    TRAIN_FILE
)

profiles = pd.read_csv(
    PROFILE_FILE
)

# -------------------------
# FRAUD CATEGORY MAPPING
# -------------------------

fraud_map = {

    "Online Financial Fraud": {

        "risk":"high",

        "amount_multiplier":(5,25),

        "spoof_probability":(0.7,0.99),

        "device":["Unknown_Device","Emulator"],

        "location":"Foreign"
    },

    "Cyber Attack/ Dependent Crimes": {

        "risk":"high",

        "amount_multiplier":(3,15),

        "spoof_probability":(0.6,0.95),

        "device":["Emulator"],

        "location":"Foreign"
    },

    "Online and Social Media Related Crime": {

        "risk":"medium",

        "amount_multiplier":(2,8),

        "spoof_probability":(0.4,0.8),

        "device":["Unknown_Device"],

        "location":"OtherCity"
    }
}

rows = []

NUM_ROWS = 15000

start = datetime.now()

# -------------------------
# GENERATE SYNTHETIC TXNS
# -------------------------

for i in range(NUM_ROWS):

    customer = profiles.sample(
        1
    ).iloc[0]

    crime = crime_df.sample(
        1
    ).iloc[0]

    category = str(
        crime["category"]
    )

    customer_id = customer[
        "customer_id"
    ]

    avg_amount = float(
        customer["avg_amount"]
    )

    avg_login = int(
        customer["avg_login"]
    )

    avg_motion = float(
        customer["avg_motion"]
    )

    avg_blink = float(
        customer["avg_blink"]
    )

    historical_risk = int(
        customer["historical_risk"]
    )

    is_fraud = random.random() < 0.20

    # -------------------------
    # FRAUD TRANSACTION
    # -------------------------

    if is_fraud:

        mapping = fraud_map.get(

            category,

            {

                "risk":"high",

                "amount_multiplier":(3,12),

                "spoof_probability":(0.6,0.9),

                "device":["Unknown_Device"],

                "location":"Foreign"
            }
        )

        amount = round(

            avg_amount *

            random.uniform(

                mapping["amount_multiplier"][0],

                mapping["amount_multiplier"][1]

            ),

            2
        )

        login_hour = random.choice(

            [0,1,2,3,4,5]

        )

        device = random.choice(

            mapping["device"]

        )

        location = mapping[
            "location"
        ]

        blink = random.randint(
            0,
            4
        )

        motion = round(

            random.uniform(
                0.01,
                0.15
            ),

            2
        )

        spoof = round(

            random.uniform(

                mapping[
                    "spoof_probability"
                ][0],

                mapping[
                    "spoof_probability"
                ][1]

            ),

            2
        )

        beneficiary_new = 1

        rooted = 1

        risk_label = "high"

    # -------------------------
    # LEGITIMATE
    # -------------------------

    else:

        amount = round(

            avg_amount *

            random.uniform(
                0.5,
                1.8
            ),

            2
        )

        login_hour = max(

            0,

            min(

                23,

                avg_login +

                random.randint(
                    -2,
                    2
                )
            )
        )

        device = customer[
            "trusted_device"
        ]

        location = customer[
            "location"
        ]

        blink = max(

            1,

            int(

                avg_blink +

                random.randint(
                    -2,
                    2
                )
            )
        )

        motion = round(

            avg_motion +

            random.uniform(
                -0.08,
                0.08
            ),

            2
        )

        spoof = round(

            random.uniform(
                0.01,
                0.20
            ),

            2
        )

        beneficiary_new = random.choice(
            [0,0,0,1]
        )

        rooted = 0

        risk_label = "low"

    rows.append({

        "transaction_id":

            f"T{i+1}",

        "customer_id":

            customer_id,

        "category":

            category,

        "subcategory":

            crime[
                "sub_category"
            ],

        "transaction_amount":

            amount,

        "login_hour":

            login_hour,

        "device":

            device,

        "location":

            location,

        "blink_rate":

            blink,

        "motion_score":

            motion,

        "spoof_probability":

            spoof,

        "beneficiary_new":

            beneficiary_new,

        "rooted_device":

            rooted,

        "historical_risk":

            historical_risk,

        "crime_context":

            str(

                crime[
                    "crimeaditionalinfo"
                ]

            )[:250],

        "risk_label":

            risk_label,

        "timestamp":

            start -

            timedelta(

                minutes=random.randint(
                    1,
                    200000
                )
            )
    })

# -------------------------
# SAVE
# -------------------------

df = pd.DataFrame(
    rows
)

df.to_csv(

    OUTPUT_FILE,

    index=False
)

print(

    "Generated:",

    len(df),

    "rows"
)

print(

    df.head()
)