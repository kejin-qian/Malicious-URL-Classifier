from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import application, db
from app.models import URL
import src.prediction
from validator_collection import validators, checkers

# home page
@application.route('/')
def index():
    return render_template("index.html")

# about page
@application.route('/About')
def about():
    return render_template("about.html")

# prediction page
@application.route('/handle_data', methods = ['POST'])
def handle_data():
    # get user input
    user_input = request.form['url']
    valid_input = src.prediction.url_format(user_input)

    # check if user input is a valid url
    valid = checkers.is_url(valid_input)
    if valid:
            # read in the model
            RF = src.prediction.readModel('model/randomForest.pkl')
            # generate features
            features = src.prediction.generateFeature(user_input)
            ext = features['file extension'][0]
            country = features['country'][0]
            # make predicitons
            result = src.prediction.getPrediction(RF, features, encoding_in = 'model/classes.npy', pred_out = 'prediction/user_pred.txt')
            
            # get the predicted result and probability
            predicted_result_string = result[0]
            predicted_result_prob = result[1]

            # store user inputs in RDS 
            url_i = URL(url=request.form['url'], pred = result[2])
            db.session.add(url_i)
            db.session.commit()
            return render_template("handle_data.html", url = user_input, result = predicted_result_string,
                                                        update = features['update_age(days)'][0], country = country, createage = features['create_age(months)'][0], domainlen = features['len of domain'][0],
                                                        subdomain = features['no of subdomain'][0], expireage = features['expiry_age(months)'][0])
    # if url is not valid, return the error page
    else:
        return render_template('error.html')

    


if __name__ == "__main__":
    # application.run(debug = True)
    application.run(debug=application.config["DEBUG"], port=application.config["PORT"], host=application.config["HOST"])

