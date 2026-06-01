import random
import pandas as pd
import uuid

NUM_CUSTOMERS = 200

cities = [

    "Bangalore",
    "Mumbai",
    "Delhi",
    "Chennai",
    "Hyderabad",
    "Pune",
    "Kolkata"
]

devices = [

    "Samsung_S24",
    "iPhone15",
    "OnePlus12",
    "Pixel8",
    "VivoX100"
]

profiles = []

for i in range(NUM_CUSTOMERS):

    customer_id = f"C{1000+i}"

    avg_login = random.randint(
        6,
        23
    )

    avg_amount = random.randint(
        500,
        50000
    )

    avg_blink_rate = random.randint(
        10,
        22
    )

    avg_motion = round(

        random.uniform(
            0.20,
            0.60
        ),

        2
    )

    trusted_device = random.choice(
        devices
    )

    location = random.choice(
        cities
    )

    historical_risk = random.randint(
        0,
        40
    )

    profiles.append({

        "customer_id":
            customer_id,

        "avg_login":
            avg_login,

        "avg_amount":
            avg_amount,

        "avg_blink":
            avg_blink_rate,

        "avg_motion":
            avg_motion,

        "trusted_device":
            trusted_device,

        "location":
            location,

        "historical_risk":
            historical_risk
    })

df = pd.DataFrame(
    profiles
)

df.to_csv(

    "dataset/customer_profiles.csv",

    index=False
)

print(

    "Generated:",

    len(df),

    "customer profiles"

)

print(

    df.head()
)