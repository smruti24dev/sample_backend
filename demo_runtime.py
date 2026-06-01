import pandas as pd
import joblib

from app03_behavior_engine import behavior_score
from app04_risk_engine import calculate_risk

BRIGHTNESS = 0.45

BLOCK_THRESHOLD = 0.97

STEPUP_THRESHOLD = 80

sessions = pd.read_csv(
    "demo_sessions.csv"
)

model = joblib.load(
    "models/antispoof.pkl"
)

print("\nRunning Demo Sessions...\n")

for _, row in sessions.iterrows():

    print("\n==============================")

    print(

        "Scenario:",

        row["scenario"]
    )

    # -------------------------
    # USE ORIGINAL MOTION
    # DO NOT DIVIDE BY 50
    # -------------------------

    motion_score = float(

        row["motion_score"]

    )

    normalized_motion = min(

        motion_score,

        1.0
    )

    normalized_brightness = BRIGHTNESS

# -------------------------
# DEMO CALIBRATION LAYER
# -------------------------

    motion_component = max(

        0,

        1 - normalized_motion

    )

    visibility_component = max(

        0, 

        1- row["face_visibility"]

    )

    blink_component = max(

        0,

        1 - (row["blink_rate"] / 20)

    )

    spoof_prob = (

        motion_component * 0.55 +

        blink_component * 0.25 +

        visibility_component * 0.20

    )

    spoof_prob = round(

        min(
            spoof_prob,
            1.0
        ),

        3
    )


    # reduce false positives

    if normalized_motion < 0.05:

        spoof_prob *= 0.75

    spoof_prob = round(

        min(
            spoof_prob,
            1.0
        ),

        3
    )

    behavior = behavior_score(

        customer=row["customer_id"],

        login_hour=int(
            row["login_hour"]
        ),

        amount=float(
            row["transaction_amount"]
        ),

        motion=normalized_motion,

        device=row["device"]
    )

    quality_penalty = 0

    if row["face_visibility"] < 0.70:

        quality_penalty += 5

    risk = calculate_risk(

        spoof_prob=spoof_prob,

        behavior=behavior,

        device_score=quality_penalty
    )

    if spoof_prob >= 0.7:

        decision = "BLOCK"

    elif risk >= 25:

        decision = "STEP_UP"

    else:

        decision = "ALLOW"

    print(

        "Customer:",

        row["customer_id"]
    )

    print(

        "Motion:",

        normalized_motion
    )

    print(

        "Spoof Probability:",

        spoof_prob
    )

    print(

        "Behavior Score:",

        behavior
    )

    print(

        "Risk Score:",

        round(
            risk,
            2
        )
    )

    print(

        "Decision:",

        decision
    )

print("\nCompleted Demo Execution")