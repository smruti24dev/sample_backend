import os
import cv2
import numpy as np
import pandas as pd

REAL="dataset/real"
SPOOF="dataset/spoof"

OUTPUT="features.csv"

face = cv2.CascadeClassifier(
    cv2.data.haarcascades+
    "haarcascade_frontalface_default.xml"
)

rows=[]

def process_video(path,label):

    cap=cv2.VideoCapture(path)

    prev=None

    motion=[]

    brightness=[]

    count=0

    while True:

        ret,frame=cap.read()

        if not ret:
            break

        gray=cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        brightness.append(
            np.mean(gray)
        )

        if prev is not None:

            diff=cv2.absdiff(
                gray,
                prev
            )

            motion.append(
                np.mean(diff)
            )

        prev=gray

        count+=1

        if count>150:
            break

    cap.release()

    rows.append({

        "file": os.path.basename(path),

        "motion":
            float(np.mean(motion))
            if len(motion) > 0
            else 0,

        "brightness":
            float(np.mean(brightness))
            if len(brightness) > 0
            else 0,

        "label": label
    })

VIDEO_EXTENSIONS = (
    ".mp4",
    ".mov",
    ".avi",
    ".mkv",
    ".MOV"
)

# ---------------------
# REAL VIDEOS
# ---------------------

for file in os.listdir(REAL):

    full_path = os.path.join(
        REAL,
        file
    )

    if os.path.isfile(full_path) and file.endswith(VIDEO_EXTENSIONS):

        print(
            "REAL:",
            file
        )

        process_video(
            full_path,
            0
        )

# ---------------------
# SPOOF VIDEOS
# ---------------------

for attack_type in os.listdir(SPOOF):

    attack_folder = os.path.join(
        SPOOF,
        attack_type
    )

    if not os.path.isdir(
        attack_folder
    ):

        continue

    for file in os.listdir(
        attack_folder
    ):

        full_path = os.path.join(
            attack_folder,
            file
        )

        if os.path.isfile(full_path) and file.endswith(VIDEO_EXTENSIONS):

            print(
                "SPOOF:",
                attack_type,
                file
            )

            process_video(
                full_path,
                1
            )

pd.DataFrame(rows).to_csv(
    OUTPUT,
    index=False
)

print("saved features.csv")