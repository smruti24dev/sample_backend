import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import classification_report

df=pd.read_csv(
    "features.csv"
)

X=df[
    ["motion","brightness"]
]

y=df["label"]

xtr,xts,ytr,yts=train_test_split(

    X,
    y,

    test_size=0.2
)

model=XGBClassifier()

model.fit(
    xtr,
    ytr
)

pred=model.predict(
    xts
)

print(

classification_report(
yts,
pred
)
)

joblib.dump(
model,
"models/antispoof.pkl"
)