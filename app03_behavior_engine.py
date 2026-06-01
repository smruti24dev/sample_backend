import pandas as pd

# -------------------------
# Load customer profiles
# -------------------------

profiles = pd.read_csv(
    "dataset/customer_profiles.csv"
)

def behavior_score(
    customer,
    login_hour,
    amount,
    motion,
    device
):

    customer_rows = profiles[
        profiles.customer_id == customer
    ]

    if len(customer_rows) == 0:

        print(
            "Customer not found"
        )

        return 50

    row = customer_rows.iloc[0]

    score = 0

    # -------------------------
    # Login behavior
    # -------------------------

    if abs(

        login_hour -

        int(row["avg_login"])

    ) > 3:

        score += 8

    # -------------------------
    # Amount anomaly
    # -------------------------

    if amount > (

        float(row["avg_amount"]) * 3

    ):

        score += 15

    # -------------------------
    # Motion anomaly
    # -------------------------

    if abs(

        motion -

        float(row["avg_motion"])

    ) > 0.25:

        score += 20

    # -------------------------
    # Device mismatch
    # -------------------------

    if device != str(

        row["trusted_device"]

    ):

        score += 10

    return min(
        score,
        100
    )


# -------------------------
# Test
# -------------------------

if __name__ == "__main__":

    risk = behavior_score(

        customer="C1000",

        login_hour=2,

        amount=85000,

        motion=0.08,

        device="Unknown_Device"
    )

    print(

        "Behavior score:",

        risk
    )