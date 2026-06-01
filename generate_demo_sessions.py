import pandas as pd
import random
from datetime import datetime

rows = [

    {
        "session_id":"S001",
        "customer_id":"C1000",
        "scenario":"valid_normal",
        "transaction_amount":2500,
        "login_hour":21,
        "device":"Samsung_S24",
        "gaze_deviation":0.08,
        "face_visibility":0.95,
        "blink_rate":18,
        "motion_score":0.42,
        "video_path":"demo_sessions/valid_normal/user1.mp4",
        "expected":"ALLOW"
    },

    {
        "session_id":"S002",
        "customer_id":"C1001",
        "scenario":"valid_side_glance",
        "transaction_amount":3000,
        "login_hour":20,
        "device":"iPhone15",
        "gaze_deviation":0.40,
        "face_visibility":0.82,
        "blink_rate":17,
        "motion_score":0.39,
        "video_path":"demo_sessions/valid_side_glance/user2.mp4",
        "expected":"ALLOW"
    },

    {
        "session_id":"S003",
        "customer_id":"C1002",
        "scenario":"valid_low_attention",
        "transaction_amount":1800,
        "login_hour":19,
        "device":"Pixel8",
        "gaze_deviation":0.55,
        "face_visibility":0.70,
        "blink_rate":15,
        "motion_score":0.36,
        "video_path":"demo_sessions/valid_low_attention/user3.mp4",
        "expected":"STEP_UP"
    },

    {
        "session_id":"S004",
        "customer_id":"C1003",
        "scenario":"valid_night_login",
        "transaction_amount":12000,
        "login_hour":2,
        "device":"OnePlus12",
        "gaze_deviation":0.10,
        "face_visibility":0.88,
        "blink_rate":16,
        "motion_score":0.44,
        "video_path":"demo_sessions/valid_night_login/user4.mp4",
        "expected":"STEP_UP"
    },

    {
        "session_id":"S005",
        "customer_id":"C1000",
        "scenario":"spoof_replay",
        "transaction_amount":90000,
        "login_hour":3,
        "device":"Unknown_Device",
        "gaze_deviation":0.02,
        "face_visibility":0.98,
        "blink_rate":2,
        "motion_score":0.05,
        "video_path":"demo_sessions/spoof_replay/attack.mp4",
        "expected":"BLOCK"
    }
]

df = pd.DataFrame(rows)

df.to_csv(

    "demo_sessions.csv",

    index=False

)

print(df)
print("\ncreated demo_sessions.csv")