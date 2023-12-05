from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)

db_name = "/Users/ruthfisher-bain/PycharmProjects/pythonProject3/newest_chat.db"

#configuring SQLite DB:
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Defining the model for the database using class method:
class Data(db.Model):
    __tablename__ = "weather_table"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(255))
    datetime = db.Column(db.Text(30))
    tempmax = db.Column(db.Integer)
    tempmin = db.Column(db.Float)
    temp = db.Column(db.Integer)
    feelslikemax = db.Column(db.Float)
    feelslikemin = db.Column(db.Integer)
    dew = db.Column(db.Float)
    humidity = db.Column(db.Integer)
    precip = db.Column(db.Integer)
    precipprob = db.Column(db.Integer)
    precipcover = db.Column(db.Integer)
    preciptype = db.Column(db.Text)
    snow = db.Column(db.Integer)
    snowdepth = db.Column(db.Integer)
    windgust = db.Column(db.Integer)
    windspeed = db.Column(db.Integer)
    windir = db.Column(db.Float)
    sealevelpressure = db.Column(db.Float)
    cloudcover = db.Column(db.Float)
    visibility = db.Column(db.Float)
    solarradiation = db.Column(db.Float)
    solarenergy = db.Column(db.Integer)
    uvindex = db.Column(db.Integer)
    severerisk = db.Column(db.Integer)
    sunrise = db.Column(db.Text)
    sunset = db.Column(db.Text)
    moonphase = db.Column(db.Float)
    conditions = db.Column(db.Text)
    description = db.Column(db.Text)
    icon = db.Column(db.Text)
    stations = db.Column(db.Text)



@app.route('/')
def index():
    data = Data.query.all()
    print(data)  # Add this line for debugging
    return render_template('index.html', data=data)

# Flask route to handle weather requests and chatbot response(***TO ADD ***):


#having trouble rendering, the app I checked for any errors before running the app:
if __name__ == '__main__':
    try:
        print(f"Database file path: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
    except Exception as e:
        print(f"Error creating database: {e}")
        # Adding the following line to print the stack trace:
        import traceback
        traceback.print_exc()
    app.run(debug=True)
