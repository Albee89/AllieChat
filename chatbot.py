from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

# Initialising and training the chatbot:
my_bot = ChatBot(
    'Allie',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch'
    ]
)

trainer = ChatterBotCorpusTrainer(my_bot)
trainer.train('chatterbot.corpus.english')
trainer.train('chatterbot.corpus.english.conversations')

# Specify the path to the directory you want to list
directory_path = 'chat_files'

# List files in the specified directory
files_list = os.listdir(directory_path)

for _file in os.listdir('chat_files'):
    chats = open('chat_files/' + _file, 'r').readlines()

    my_bot.train(chats)