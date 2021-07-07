import pymongo
import flask
from flask import request, jsonify
from passlib.hash import pbkdf2_sha256
import re
import jwt
import datetime
from os import urandom
from random import choice, randrange
from string import ascii_uppercase

def TODO():
	return 'not implemented'

global client
client = pymongo.MongoClient("mongodb+srv://Dere:dere@basecluster.nnfue.mongodb.net/USER?retryWrites=true&w=majority")


app = flask.Flask(__name__)
app.config["DEBUG"] = True

#Contem os codigos de erro e sucesso
class ids:
	eID = {
	'eID-1':'No name provided',
	'eID-2':'No password provided',
	'eID-3':'User not Exists',
	'eID-4':'Incorrect password',
	'eID-5':'Name in Use',
	'eID-6':'Email in Use',
	'eID-7':'Invalid email',
	'eID-8':'No Email provided',
	'eID-9':'Invalid Token',
	'eID-10':'Token not provided',
	'eID-11':'User allready in game room',
	'eID-12':'ADM cannot connect to his own room'
	}
	sID = {
	'sID-1':'Account created',
	'sID-2':'Match created',
	'sID-3':'Join success'
	}

#contem as funções de autenticação da API
class auth:
	def encode_token(user_id):
		payload = {
		'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=0, minutes=0, seconds=0),
		'iat':datetime.datetime.utcnow(),
		'sub':user_id
		}
		return jwt.encode(payload, 'dere_key', algorithm='HS256')

	def decode_token(token):
		payload = jwt.decode(token, 'dere_key', algorithms='HS256', verify=False)
		return payload['sub']

#contem as funções de uitilidade da API como as funções de geração de codigos
class utility:
	def gen_match_id():
		result = ''.join(choice(ascii_uppercase) for i in range(4))
		result += '-'+str(randrange(10,100))
		return result

#a rota nula da API apenas retorna uma pagina vazia
@app.route('/', methods=['GET'])
def home():
	return "<h1> Ops... </h1><p>Looks like you didn't use any end-point</p>"

#a rota de login da API, requer os itens: "name", "password" e retorna o resultado contendo: "connection", "con", "auth" em caso de sucesso
@app.route('/api/v1/dlark/login/', methods=["GET"])
def dlark_login():
	db_user_data = client.USER.data

	if 'name' in request.args:
		in_name = request.args['name']
	else:
		return {"error":"No NAME provided","eID":1}

	if 'password' in request.args:
		in_password = request.args['password']
	else:
		return {"error":"No PASSWORD provided","eID":2}

	sr_result = db_user_data.find_one({'name':re.compile(in_name, re.IGNORECASE)})

	if type(sr_result) == dict:
		if 'name' in sr_result:
			if pbkdf2_sha256.verify(in_password,sr_result['password']) == True:

				return {"connection":"success","con":True,'auth':auth.encode_token(str(sr_result['_id']))}
			else:
				return {"error":"Incorrect PASSWORD","eID":4}
		else:
			return {"error":"User not exists","eID":3}
	else:
		return {"error":"User not exists","eID":3}

#a rota de registro na API, ela cria uma conta no MongoDB, requer os itens: "name", "password", "email" e retorna o resultado contendo: "success", "sID" em caso de sucesso
@app.route('/api/v1/dlark/register/', methods=["GET"])
def dlark_register():
	db = client.USER.data
	if 'name' in request.args:
		if 'password' in request.args:
			if 'email' in request.args:
				if type(db.find_one({'name':request.args['name']})) == dict:
					return {'error':'Name in Use', 'eID':5}
				if type(db.find_one({'email':request.args['email']})) == dict:
					return {'error':'Email in Use', 'eID':6}

				else:
					if '@' in request.args['email'] and '.' in request.args['email']:

						player_acc = {
							'name':request.args['name'],
							'password':pbkdf2_sha256.hash(request.args['password']),
							'email':request.args['email'],
							'custom_itens':[],
							'matches':[]
							}

						db.insert_one(player_acc)
						return {'success':'Account created','sID':1}

					else:
						return {'error':'Invalid Email','eID':7}
			else:
				return {'error':'No email provided', 'eID':8}
		else: 
			return {'error':'no password provided', 'eID':2}
	else:
		return {'error':'No name provided', 'eID':1}

#uma rota de debug ou uso emergencial feita pra criar uma hash, requer: "value" e retorna: hash
@app.route('/api/help/sha256/make/', methods=["GET"])
def sha256_help():
	if 'value' in request.args:
		return pbkdf2_sha256.hash(request.args['value'])

#uma rota debug ou uso emergencial feita pra criptografar um token, requer: "id" e retorna: token
@app.route('/api/debug/encode/', methods=["GET"])
def encode_debug():
	if 'id' in request.args:
		return auth.encode_token(user_id=request.args['id'])

#uma rota debug para uso emergencial feita para descriptografar um token, requer "token" e retorna: decoded token
@app.route('/api/debug/decode/',  methods=["GET"])
def decode_debug():
	if 'token' in request.args:
		return auth.decode_token(token=request.args['token'])

#a rota feita para criar partidas no MongoDB, requer: "token", "name" e retorna: "success", "sID", "match_id" em caso de sucesso
@app.route('/api/v1/dlark/new_match', methods=["GET"])
def new_match():
	player_db = client.USER.data
	game_db = client.MATCH.data

	if 'token' in request.args:
		if 'name' in request.args:
			player_data = player_db.find_one({'name':request.args['name']})
			if str(player_data['_id']) == auth.decode_token(request.args['token']):
				match_id_var = utility.gen_match_id()

				while game_db.find_one({'match_id':match_id_var}) == dict:
					match_id_var = utility.gen_match_id()

				match_data = {
				'match_id':utility.gen_match_id(),
				'adm':{'name':request.args['name'],'id':str(player_data['_id'])},
				'players':[],
				'characters':[],
				'enemies':[],
				'game_type':"D'Lark",
				'player_requests':[],
				'match_pos':0,
				'turn':0
				}
				game_db.insert_one(match_data)

				return {'success':'Match created','sID':2, 'match_id':match_data['match_id']}
			else:
				return {'error':'invalid token','eID':9}
		else:
			return {'error':'No name provided', 'eID':1}
	else:
		return {'error':'No token provided', 'eID':10}

#a rota para se juntar a uma partida, requer: "token", "name", "match_id" e retorna: "success", "sID" em em caso de sucesso
@app.route('/api/v1/dlark/join_match', methods=["GET"])
def join_match():
	game_db = client.MATCH.data

	if 'token' in request.args:
		if 'name' in request.args:
			if 'match_id' in request.args:
				player_data = client.USER.data.find_one({'name':request.args['name']})
				if str(player_data['_id']) == auth.decode_token(request.args['token']):
					match_data = game_db.find_one({'match_id':re.compile(request.args['match_id'], re.IGNORECASE)})
					if 'match_id' in match_data:

						if match_data['adm']['id'] == str(player_data['_id']):
							return {'error':'Adm cannot enter his own room', 'eID':12}

						for player_pos, data in enumerate(match_data['player_requests']):
							if match_data['player_requests'][player_pos]['id'] == str(player_data['_id']):
								return {'error':'User allready in match', 'eID':11}

						for player_pos, data in enumerate(match_data['players']):
							if match_data['player_requests'][player_pos]['id'] == str(player_data['_id']):
								return {'error':'User allready in match', 'eID':11}


						match_players_request = match_data['player_requests']

						match_players_request.append({'name':request.args['name'], 'id':str(player_data['_id'])})

						game_db.update_one({'match_id':request.args['match_id']}, {'$set':{'player_requests':match_players_request}})
						return {'success':'Player joined the room','sID':3}

#a rota que permite jogadores criarem os personagens dos jogadores
@app.route('/api/v1/dlark/new_character', methods=['GET'])
def new_character():
	return TODO()

#a a rota que permite ADMs criar inimigos
@app.route('/api/v1/dlark/new_enemy', methods=['GET'])
def new_enemy():
	return TODO()

#a a rota que permite ADMs aceitar jogadores na fila de espera
@app.route('/api/v1/dlark/accept_player', methods=['GET'])
def accept_player():
	return TODO()

#a a rota que permite ADMs passarem para o próximo turno
@app.route('/api/v1/dlark/roll_turn', methods=['GET'])
def roll_turn():
	return TODO()

#a a rota que permite ADMs adicionarem itens aos jogadores
@app.route('/api/v1/dlark/add_item_to_player', methods=['GET'])
def add_item_to_player():
	return TODO()

#a a rota que permite ADMs removerem itens de jogadores
@app.route('/api/v1/dlark/remove_item_from_player', methods=['GET'])
def remove_item_from_player():
	return TODO()

#a a rota que permite ADMs modificarem algum status de um personagem
@app.route('/api/v1/dlark/modify_stats_from_character', methods=['GET'])
def modify_stats_from_character():
	return TODO()

#a a rota que permite ADMs adicionarem um efeito a um jogador
@app.route('/api/v1/dlark/add_effect_to_character', methods=['GET'])
def add_effect_to_character():
	return TODO()

#a a rota que permite usuarios equiparem seus itens
@app.route('/api/v1/dlark/equip_item', methods=['GET'])
def equip_item():
	return TODO()

app.run()