import os
import cv2
import joblib
import numpy as np

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from app03_behavior_engine import behavior_score
from app04_risk_engine import calculate_risk
from app06_explainability import explain

# --------------------------------
# DEMO INPUT
# --------------------------------

VIDEO_PATH = "demo_customer_video.mp4"# demo_customer_video

CUSTOMER_ID = "C1000"

TRANSACTION_AMOUNT = 4500

LOGIN_HOUR = 21

DEVICE = "Samsung_S24"

DEVICE_SCORE = 15

DEFAULT_BRIGHTNESS = 45

MAX_FRAMES = 120

# --------------------------------
# VALIDATE INPUT
# --------------------------------

if not os.path.exists(VIDEO_PATH):

    raise FileNotFoundError(

        f"Video not found: {VIDEO_PATH}"
    )

# --------------------------------
# LOAD MODELS
# --------------------------------

print("Loading anti-spoof model...")

antispoof_model = joblib.load(
    "models/antispoof.pkl"
)

print("Loading embedding model...")

embedding_model = HuggingFaceEmbeddings(

    model_name="BAAI/bge-small-en-v1.5"
)

print("Loading vector database...")

vectordb = Chroma(

    persist_directory="./vector_db",

    embedding_function=embedding_model
)

# --------------------------------
# FEATURE EXTRACTION
# --------------------------------

def extract_video_features(video_path):

    cap = cv2.VideoCapture(
        video_path
    )

    motion_values = []

    brightness_values = []

    previous = None

    frames = 0

    while True:

        ret, frame = cap.read()

        if not ret:

            break

        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        brightness_values.append(

            np.mean(gray)
        )

        if previous is not None:

            diff = cv2.absdiff(

                gray,

                previous
            )

            motion_values.append(

                np.mean(diff)
            )

        previous = gray

        frames += 1

        if frames >= MAX_FRAMES:

            break

    cap.release()

    # safer defaults

    if len(motion_values) == 0:

        normalized_motion = 0.10

    else:

        raw_motion = np.mean(
            motion_values
        )

        normalized_motion = min(

            raw_motion / 50.0,

            1.0
        )

    if len(brightness_values) == 0:

        brightness_score = DEFAULT_BRIGHTNESS

    else:

        brightness_score = float(

            np.mean(
                brightness_values
            )
        )

    return (

        round(
            normalized_motion,
            3
        ),

        round(
            brightness_score,
            2
        )
    )

# --------------------------------
# VIDEO ANALYSIS
# --------------------------------

print("\nReading customer video...")

motion_score, brightness = extract_video_features(

    VIDEO_PATH
)

# --------------------------------
# ANTI-SPOOF
# --------------------------------

normalized_brightness = min(

    brightness / 255.0,

    1.0
)

normalized_motion = min(

    motion_score,

    1.0
)

# --------------------------------
# ANTI-SPOOF
# --------------------------------

normalized_brightness = min(

    brightness / 255.0,

    1.0
)

normalized_motion = min(

    motion_score,

    1.0
)

spoof_probability = antispoof_model.predict_proba(

    [[

        normalized_motion,

        normalized_brightness

    ]]

)[0][1]

spoof_probability = float(
    spoof_probability
)

# --------------------------------
# Reduce false positives
# for calm / low-motion users
# --------------------------------

if normalized_motion < 0.05:

    spoof_probability *= 0.65

spoof_probability = round(

    min(
        spoof_probability,
        1.0
    ),

    3
)

# --------------------------------
# BEHAVIOR ENGINE
# --------------------------------

behavior = behavior_score(

    customer=CUSTOMER_ID,

    login_hour=LOGIN_HOUR,

    amount=TRANSACTION_AMOUNT,

    motion=motion_score,

    device=DEVICE
)

# --------------------------------
# RISK ENGINE
# --------------------------------

risk = calculate_risk(

    spoof_prob=spoof_probability,

    behavior=behavior,

    device_score=DEVICE_SCORE
)

risk = round(
    risk,
    2
)

# --------------------------------
# DEBUG OUTPUT
# --------------------------------

print("\n------ DEBUG ------")

print(

    "Motion:",

    motion_score
)

print(

    "Brightness:",

    brightness
)

print(

    "Spoof Probability:",

    spoof_probability
)

print(

    "Behavior:",

    behavior
)

print(

    "Risk:",

    risk
)

# --------------------------------
# VECTOR SEARCH
# --------------------------------

query = f"""

spoof={spoof_probability}

motion={motion_score}

amount={TRANSACTION_AMOUNT}

"""

retrieved_context = ""

try:

    docs = vectordb.similarity_search(

        query,

        k=3
    )

    retrieved_context = "\n".join(

        [

            x.page_content

            for x in docs

        ]
    )

except Exception:

    retrieved_context = "No matching context"

# --------------------------------
# GEMINI EXPLANATION
# --------------------------------

reason = f"""

Measured signals only:

motion={normalized_motion}

brightness={normalized_brightness}

spoof_probability={spoof_probability}

behavior_score={behavior}

risk_score={risk}

Only explain measured signals.
Do not infer replay attacks,
blinks,
masks,
or emulator usage.

Context:

{retrieved_context}

"""

explanation = explain(

    risk,

    reason
)

# --------------------------------
# DECISION ENGINE
# --------------------------------

# strong spoof evidence

if spoof_probability > 0.97:

    decision = "BLOCK"

# suspicious but not definitive

elif risk > 80:

    decision = "STEP_UP"

else:

    decision = "ALLOW"

# --------------------------------
# OUTPUT
# --------------------------------

print("\n====================")

print(

    "Decision:",

    decision
)

print(

    "\nExplanation:\n"
)

print(
    explanation
)