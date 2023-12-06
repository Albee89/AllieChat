import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer, ChatterBotCorpusTrainer
from flask_sqlalchemy import SQLAlchemy
import jsonify

app = Flask(__name__)
socketio = SocketIO(app)

# Configuration for SQLite DB
db_name = "/Users/ruthfisher-bain/PycharmProjects/pythonProject3/newest_chat.db"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the model for the database using the class method
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


# Create a ChatBot instance with SQLStorageAdapter
my_bot = ChatBot(
    'Allie',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///newest_chat.db',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ]
)

# Create a ListTrainer instance
list_trainer = ListTrainer(my_bot)

# Train the ChatBot using conversations
introductions = [
    "Hi, how are you?",
    "Hello! My name is AllieChat, and I love to chat! How can I help you today?",
    "I love to chat, I'm AllieChat!",
    "Weather is my passion! How can I help?",
    "I'm AllieChat and I'm here for all your ExploreUK weather needs!"
]

# Training the ListTrainer with strings directly:
list_trainer.train(list(intro for intro in introductions))

# Train the ChatBot using data from the "weather_table" table in the database
try:
    for item in Data.query.all():
        list_trainer.train([item.conditions])
except Exception as e:
    print(f"Error training with data from weather_table: {e}")

# Use ChatterBotCorpusTrainer for training: 
corpus_trainer = ChatterBotCorpusTrainer(my_bot)
corpus_trainer.train('chatterbot.corpus.english')
corpus_trainer.train('chatterbot.corpus.english.conversations')


# Routes
@app.route('/')
def index():
    return render_template('base.html')



#retrain route so the chatbot keeps learning:
def retrain_chatbot():
    try:
        for item in Data.query.all():
            list_trainer.train([item.conditions])
    except Exception as e:
        print(f"Error retraining with data from weather_table: {e}")

# New route for the chatbot:
@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if request.method == 'POST':
        # User has submitted a message via a form
        user_input = request.form['user_input']

        # Retrain the chatbot with the latest data from weather_table
        retrain_chatbot()

        # Get a response from the chatbot
        response = get_chatbot_response(user_input)
        return jsonify({'user_input': user_input, 'bot_response': response})

    # Render the chatbot template for GET requests
    return render_template('chatbot.html')


# SocketIO event added for handling messages:
@socketio.on('message')
def handle_message(msg):
    response = get_chatbot_response(msg)
    socketio.emit('message', {'user': msg, 'bot': response})
    
    
def get_chatbot_response(user_input):
    try:
        response = my_bot.get_response(user_input)
        return response.text
    except Exception as e:
        # Handle exceptions, print the error for debugging
        print(f"Error getting chatbot response: {e}")
        return "I'm sorry, I couldn't understand that."


# Run the app through SocketIO
if __name__ == '__main__':
    try:
        print(f"Database file path: {app.config['SQLALCHEMY_DATABASE_URI']}")
        db.create_all()
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True, use_reloader=False)
    except Exception as e:
        print(f"Error creating database or running app: {e}")
        import traceback

        traceback.print_exc()



