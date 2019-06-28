import os
import sys

from dotenv import load_dotenv
from flask import Flask, json

load_dotenv()
generator_path = os.getenv('DRAMATURGIO_PATH', '..')
sys.path.append(generator_path)
sys.path.append(f'{generator_path}/..')

from lib.story.story import Story
from lib.encoders.json_encoder import CustomEncoder

app = Flask(__name__)
story = Story()


@app.route('/')
def index():
    return f'Server Works!\n{sys.path}'


@app.route('/play')
def say_hello():
    return 'Hello from Server'


@app.route('/sequences')
def print_sequences():
    print(story)
    response = json.dumps(story.get_sequences(), cls=CustomEncoder, ensure_ascii=False), 'application/json'
    return response
    # for i, sequence in enumerate(story.get_sequences()):
    #    print(f"Sequence {i}\n{sequence}\n\n")
    # return f"<p>{'</p><p>'.join(map(lambda x: f'{x}<br>', story.get_sequences()))}</p>".replace("\n", "<br>")
