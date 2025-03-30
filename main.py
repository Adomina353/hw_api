import json
from json import JSONEncoder


from flask import Flask, request, jsonify

from model.twit import Twit
from model.user import User
twits= []
app = Flask(__name__)
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return{'body': obj.body, 'author': obj.author.username}

        elif isinstance(obj, User):
            return {'username': obj.username}
        return super().default(obj)

app.json_encoder = CustomJSONEncoder
@app.route('/twit', methods=['POST'])
def create_twit():
    '''{"body": "Hello", "author": "1@mail.ru"}'''
    twit_json=request.get_json()
    username=twit_json['author']
    author=User(username)
    twit=Twit(twit_json['body'], author)
    twits.append(twit)
    return jsonify({'status':'ok'})

@app.route('/twit', methods=['GET'])
def read_twits():
    result=[{'body': twit.body, 'author': twit.author.username} for twit in twits]
    return jsonify({"twits": result})


@app.route('/twit/<int:twit_id>', methods=['DELETE'])
def delete_twit(twit_id):
    if twit_id < 0 or twit_id >= len(twits):
        return jsonify({'error': 'Twit not found'}), 404

    deleted_twit = twits.pop(twit_id)  # Удаляем твит по индексу
    return jsonify({
        'status': 'deleted',
        'deleted_twit': {
            'body': deleted_twit.body,
            'author': deleted_twit.author.username
        }
    })


@app.route('/twit/<int:twit_id>', methods=['PUT'])
def update_twit(twit_id):
    '''{"body": "Updated body", "author": "username"}'''
    new_data = request.get_json()
    twits[twit_id].body = new_data['body']  # Обновляем текст твита
    return jsonify(
        {'status': 'updated', 'twit': {'body': twits[twit_id].body, 'author': twits[twit_id].author.username}})





if __name__ == '__main__':
    app.run(debug=True)