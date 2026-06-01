import joblib

from app03_behavior_engine import (
    behavior_score
)

from app04_risk_engine import (
    calculate_risk
)

from app06_explainability import (
    explain
)

# -------------------------
# Load trained model
# -------------------------

model = joblib.load(

    "models/antispoof.pkl"
)

# -------------------------
# Demo Session Input
# -------------------------

customer = "C1000"

login_hour = 2

amount = 85000

motion = 0.08

device = "Unknown_Device"

device_score = 70

brightness = 45

# -------------------------
# Anti-spoof prediction
# -------------------------

spoof_probability = model.predict_proba(

    [[motion, brightness]]

)[0][1]

print(

    "Spoof Probability:",

    round(
        spoof_probability,
        2
    )
)

# -------------------------
# Behavior Engine
# -------------------------

behavior = behavior_score(

    customer=customer,

    login_hour=login_hour,

    amount=amount,

    motion=motion,

    device=device
)

print(

    "Behavior Score:",

    behavior
)

# -------------------------
# Risk Engine
# -------------------------

risk = calculate_risk(

    spoof_prob=spoof_probability,

    behavior=behavior,

    device_score=device_score
)

print(

    "Risk Score:",

    risk
)

# -------------------------
# Explainability
# -------------------------

reason = f"""

spoof_probability={spoof_probability}

motion={motion}

device={device}

amount={amount}
"""

explanation = explain(

    risk,

    reason
)

print(

    "\nExplanation:\n"
)

print(
    explanation
)

# -------------------------
# Decision
# -------------------------

if risk >= 70:

    print(

        "\nDecision: BLOCK"

    )

elif risk >= 40:

    print(

        "\nDecision: STEP-UP AUTH"

    )

else:

    print(

        "\nDecision: ALLOW"

    )