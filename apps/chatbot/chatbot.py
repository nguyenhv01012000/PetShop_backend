from chatterbot import ChatBot

chatbot = ChatBot(
    'CoronaBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.TimeLogicAdapter',
        'chatterbot.logic.BestMatch',
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': 'I am sorry, but I do not understand. Can you text me back please ?',
            'maximum_similarity_threshold': 0.90
        }
    ],
    database_uri='sqlite:///database.sqlite3'
)

# Training With Own Questions 
from chatterbot.trainers import ListTrainer

trainer = ListTrainer(chatbot)

training_data_quesans = open('apps/chatbot/training_data/ques_ans.txt').read().splitlines()
training_data_personal = open('apps/chatbot/training_data/personal_ques.txt').read().splitlines()
training_data_tan_gai = open('apps/chatbot/training_data/messager_tan_gai.txt').read().splitlines()

training_data = training_data_quesans + training_data_personal + training_data_tan_gai

trainer.train(training_data)

# Training With Corpus
from chatterbot.trainers import ChatterBotCorpusTrainer

trainer_corpus = ChatterBotCorpusTrainer(chatbot)

trainer_corpus.train(
    'chatterbot.corpus.english'
)
