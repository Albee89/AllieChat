import os
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
import pandas as pd
from dotenv import load_dotenv
import requests


app = Flask(__name__)
socketio = SocketIO(app)

load_dotenv()

db_name = "/Users/ruthfisher-bain/PycharmProjects/pythonProject3/newest_chat.db"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#accessing API key from environment:
api_key = os.getenv('API_KEY')

# Defining the model for the database using the class method:
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

my_bot = ChatBot(
    'Allie',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///newest_chat.db',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ]
)

list_trainer = ListTrainer(my_bot)

introductions = [
    "Hi, how are you?",
    "Hello! My name is AllieChat, and I love to chat! How can I help you today?",
    "I love to chat, I'm AllieChat!",
    "Weather is my passion! How can I help?",
    "I'm AllieChat and I'm here for all your ExploreUK weather needs!"
]

list_trainer.train(list(intro for intro in introductions))

try:
    for item in Data.query.all():
        list_trainer.train([item.conditions])
except Exception as e:
    print(f"Error training with data from weather_table: {e}")

corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')
corpus_trainer.train('chatterbot.corpus.english.conversations')

#training the bot using pandas:
blogger_locations = pd.read_csv('weather_forecast.csv')
try:
    for index, row in blogger_locations.iterrows():
        conditions = row['conditions']
        list_trainer.train([conditions])
except Exception as e:
    print(f"Error training with data from weather_forecast.csv: {e}")


#training bot using Open Weather Map data and my API key:
def fetch_openweather_data_for_multiple_cities(cities):
    weather_data_list = []

    for city in cities:
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {
            'q': city,
            'appid': api_key,
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            weather_data = response.json()
            description = weather_data.get('weather')[0].get('description')
            weather_data_list.append({'city': city, 'description': description})
        except requests.exceptions.RequestException as e:
            print(f"Error fetching OpenWeather data for {city}: {e}")

    return weather_data_list

# List of cities t fulfill customer needs of returning more than one location at a time
city_names = ['CorfeCastle', 'TheCotswolds', 'Bristol', 'Oxford', 'Norwich', 'Stonehenge',
              'WatergateBay', 'Birmingham' ]

# Fetching weather data from Open Weather API for multiple cities:
weather_data_list = fetch_openweather_data_for_multiple_cities(city_names)

# Training the chatbot with the Open Weather data:
try:
    for weather_data in weather_data_list:
        description = weather_data.get('description')
        if description:
            list_trainer.train([description])
except Exception as e:
    print(f"Error training with OpenWeather data: {e}")

#retrain chatbot function to consistently train AllieChat:

def retrain_chatbot():
    try:
        all_weather_data = Data.query.all()
        for item in all_weather_data:
            list_trainer.train([item.conditions])

        print("Chatbot retrained successfully with weather data.")
    except Exception as e:
        print(f"Error retraining with data from weather_table: {e}")


#defining chatbot response:
def get_chatbot_response(user_input, weather_conditions=None):
    try:
        if weather_conditions:
            response = my_bot.get_response(f"Weather conditions: {weather_conditions}")
        else:
            response = my_bot.get_response(user_input)
        return response.text
    except Exception as e:
        print(f"Error getting chatbot response: {e}")
        return "I'm sorry, I couldn't understand that."


#app route with index.html template:
@app.route('/')
def home():
    return render_template('index.html')

#establishing socket.io library server:
@socketio.on('message')
def handle_message(msg):
    user_input = msg['user_input']
    weather_conditions = msg.get('weather_conditions')

    try:
        if weather_conditions:
            response_text = my_bot.get_response(f"Weather conditions: {weather_conditions}").text
        else:
            response_text = my_bot.get_response(user_input).text

        socketio.emit('message', {'user_input': user_input, 'bot_response': response_text})
    except Exception as e:
        print(f"Error getting chatbot response: {e}")
        socketio.emit('message', {'user_input': user_input, 'bot_response': "I'm sorry, I couldn't understand that."})


@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('userInput')
    weather_conditions = request.json.get('weatherConditions')

    try:
        if weather_conditions:
            response_text = my_bot.get_response(f"Weather conditions: {weather_conditions}").text
        else:
            response_text = my_bot.get_response(user_input).text

        return jsonify({'userInput': user_input, 'botResponse': response_text})
    except Exception as e:
        print(f"Error getting chatbot response: {e}")
        return jsonify({'userInput': user_input, 'botResponse': "I'm sorry, I couldn't understand that."})


#running the app:
if __name__ == '__main__':
    try:
        # Print the database file path for debugging purposes
        print(f"Database file path: {app.config['SQLALCHEMY_DATABASE_URI']}")

        # Creating the database tables- this was a huge step I had initially missed!
        db.create_all()

        # Run the Flask app with SocketIO
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)

    except Exception as e:
        print(f"Error creating database or running app: {e}")
        import traceback
        traceback.print_exc()