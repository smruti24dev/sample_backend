import random
import pandas as pd
from datetime import datetime, timedelta

# -----------------------
# Load customer profiles
# -----------------------

profiles = pd.read_csv(
    "dataset/customer_profiles.csv"
)

NUM_TRANSACTIONS = 10000

cities = [

    "Bangalore",
    "Mumbai",
    "Delhi",
    "Pune",
    "Hyderabad",
    "Chennai",
    "Kolkata",
    "Foreign"
]

devices = [

    "Samsung_S24",
    "iPhone15",
    "OnePlus12",
    "Pixel8",
    "VivoX100",
    "Unknown_Device",
    "Emulator"
]

rows = []

start_date = datetime.now()

for i in range(NUM_TRANSACTIONS):

    customer = profiles.sample(
        1
    ).iloc[0]

    customer_id = customer["customer_id"]

    # --------------------
    # Inject fraud %
    # --------------------

    fraud = random.random() < 0.15

    avg_login = int(
        customer["avg_login"]
    )

    avg_amount = float(
        customer["avg_amount"]
    )

    avg_motion = float(
        customer["avg_motion"]
    )

    avg_blink = float(
        customer["avg_blink"]
    )

    trusted_device = str(
        customer["trusted_device"]
    )

    home_location = str(
        customer["location"]
    )

    # --------------------
    # Create transaction
    # --------------------

    if fraud:

        amount = round(

            avg_amount *

            random.uniform(
                4,
                25
            ),

            2
        )

        login_hour = random.choice(

            [0,1,2,3,4,5]

        )

        device = random.choice(

            [

                "Unknown_Device",

                "Emulator"

            ]

        )

        location = "Foreign"

        beneficiary_new = 1

        rooted_device = 1

        blink_rate = random.randint(
            0,
            5
        )

        motion_score = round(

            random.uniform(
                0.01,
                0.15
            ),

            2
        )

        spoof_probability = round(

            random.uniform(
                0.70,
                0.99
            ),

            2
        )

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

        device = trusted_device

        location = home_location

        beneficiary_new = random.choice(

            [0,0,0,1]

        )

        rooted_device = 0

        blink_rate = max(

            1,

            int(

                avg_blink +

                random.randint(
                    -3,
                    3
                )
            )
        )

        motion_score = round(

            avg_motion +

            random.uniform(
                -0.08,
                0.08
            ),

            2
        )

        spoof_probability = round(

            random.uniform(
                0.01,
                0.25
            ),

            2
        )

    timestamp = start_date - timedelta(

        minutes=random.randint(
            1,
            100000
        )
    )

    deviation_motion = round(

        abs(

            motion_score -

            avg_motion

        ),

        2
    )

    deviation_blink = abs(

        blink_rate -

        avg_blink
    )

    txn_velocity = random.randint(
        1,
        25
    )

    risk_label = (

        "high"

        if fraud

        else "low"
    )

    rows.append({

        "transaction_id":
            f"T{i+1}",

        "customer_id":
            customer_id,

        "timestamp":
            timestamp,

        "transaction_amount":
            amount,

        "login_hour":
            login_hour,

        "device":
            device,

        "location":
            location,

        "beneficiary_new":
            beneficiary_new,

        "rooted_device":
            rooted_device,

        "blink_rate":
            blink_rate,

        "motion_score":
            motion_score,

        "spoof_probability":
            spoof_probability,

        "txn_velocity_24h":
            txn_velocity,

        "avg_customer_motion":
            avg_motion,

        "avg_customer_blink":
            avg_blink,

        "deviation_motion":
            deviation_motion,

        "deviation_blink":
            deviation_blink,

        "historical_risk":
            customer[
                "historical_risk"
            ],

        "risk_label":
            risk_label
    })

df = pd.DataFrame(
    rows
)

df.to_csv(

    "dataset/transactions.csv",

    index=False
)

print(

    "Generated:",

    len(df),

    "transactions"

)

print(

    df.head()
)