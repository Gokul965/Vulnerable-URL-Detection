from flask import Flask, request, render_template
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
warnings.filterwarnings('ignore')
from feature import generate_data_set

from sklearn.ensemble import GradientBoostingClassifier

data = pd.read_csv("phishing.csv")

data = data.drop(['Index'],axis = 1)


X = data.drop(["class"],axis =1)
y = data["class"]


gbc = GradientBoostingClassifier(max_depth=4,learning_rate=0.7)


gbc.fit(X,y)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", xx= -1)


@app.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "POST":

        url = request.form["url"]
        x = np.array(generate_data_set(url)).reshape(1,30) 
        y_pred =gbc.predict(x)[0]
        
        
        y_pro_phishing = gbc.predict_proba(x)[0,0]
        y_pro_non_phishing = gbc.predict_proba(x)[0,1]
        
        pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
        return render_template('index.html',xx =round(y_pro_non_phishing,2),url=url )
        
        
        
    return render_template("index.html", xx =-1)


if __name__ == "__main__":
    app.run(debug=True)