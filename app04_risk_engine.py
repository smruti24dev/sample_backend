def calculate_risk(

    spoof_prob,

    behavior,

    device_score

):

    # -------------------------
    # Weighted scoring
    # -------------------------

    score = (

        spoof_prob * 50 +

        behavior * 0.30 +

        device_score * 0.20

    )

    score = round(
        score,
        2
    )

    return min(
        score,
        100
    )


# -------------------------
# Test
# -------------------------

if __name__ == "__main__":

    risk = calculate_risk(

        spoof_prob=0.88,

        behavior=65,

        device_score=70
    )

    print(

        "Risk Score:",

        risk
    )