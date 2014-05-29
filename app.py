#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from models.Restaurant import Restaurant
from models.Reservation import Reservation
from passlib.hash import sha256_crypt
import requests

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

@app.route('/')
@app.route('/maps')
def maps():
	return render_template('maps.html')

@app.route('/login', methods=['POST', 'GET'])
def signin():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email and password:
			requestServer = requests.get("http://localhost:8080/axis2/services/controler/getRestaurantEmail?email=%s&response=application/json" % (email)).json()
			if '@nil' not in requestServer["return"]:
				jsonResult = requestServer["return"]
				if sha256_crypt.verify(password, jsonResult["password"]):
					session['Restaurant'] = jsonResult
					return redirect(url_for('logged'))
				else:
					error = "Senha invalida"
			else:
				error = "Email invalido"
		else:
			error = "Campos vazios"
	return render_template('login.html', error=error)

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	error = ""
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		name = request.form['name']
		adress = request.form['adress']
		confirm_password = request.form['confirm_password']
		if email and password and name and adress and confirm_password:
			password = sha256_crypt.encrypt(password)
			if sha256_crypt.verify(confirm_password, password):
				requestServer = requests.get("http://localhost:8080/axis2/services/controler/createRestaurant?name=%s&adress=%s&email=%s&password=%s&response=application/json" % (name, adress, email, password)).json()
				if requestServer["return"] == "Restaurante encontrado com sucesso":
					jsonResult = requests.get("http://localhost:8080/axis2/services/controler/getRestaurantEmail?email=%s&response=application/json" % (email)).json()["return"]
					session['Restaurant'] = jsonResult
					return redirect(url_for('logged'))
				else:
					error = requestServer["return"]
			else:
				error = "Campos Password e Confirm Password devem ser iguais"
		else:
			error = "Campos vazios"
	return render_template('signup.html', error=error)

@app.route('/logged', methods=['POST', 'GET'])
def logged():
	message = ""
	if 'Restaurant' in session:
		restaurant = json_to_restaurant(session['Restaurant'])
	if request.method == 'POST':
		description = request.form["description"]
		reservation = request.form.get("reservation") == "True"
		menu = request.form.get("menu") == "True"
		requestServer = requests.get("http://localhost:8080/axis2/services/controler/updateRestaurant?id=%s&description=%s&featureReservation=%s&featureMenu=%s&response=application/json" % (restaurant.idRestaurant, description, reservation, menu)).json()
		if '@nil' not in requestServer["return"]:
			restaurant.description = description
			restaurant.featureReservation = reservation
			restaurant.featureMenu = menu
			message = "Atualizado com sucesso"
		else:
			message = "Não foi possível atualizar o restaurante"
	return render_template('logged.html', restaurant=restaurant, message=message)

@app.route('/reserva')
def reserva():
	if 'Restaurant' in session:
		restaurant = json_to_restaurant(session['Restaurant'])
	requestServer = requests.get("http://localhost:8080/axis2/services/controler/listReservations?idRestaurant=%s&response=application/json" % (restaurant.idRestaurant)).json()
	listReservations = json_to_listResevation(requestServer['return'])
	return render_template('reserva.html', listReservations=listReservations)

@app.route('/places')
def return_places():
	latitude = request.args.get('latitude', 0, type=float)
	longitude = request.args.get('longitude', 0, type=float)
	r = requests.get("http://localhost:8080/axis2/services/controler/listRestaurants?latitude=%s&longitude=%s&response=application/json" % (latitude, longitude)).json()
	return jsonify(r)

@app.route('/updateReservation')
def updateReservation():
	restaurant = json_to_restaurant(session['Restaurant'])
	idReservation = request.args.get('id', 0)
	answer = request.args.get('answer', "")
	requestServer = requests.get("http://localhost:8080/axis2/services/controler/updateReservation?id=%s&idRestaurant=%s&status=%s&response=application/json" % (idReservation, restaurant.idRestaurant, answer)).json()
	return jsonify(requestServer)

@app.route('/profile/<reference>', methods=['POST', 'GET'])
def profile(reference):
	message = ""
	r = requests.get("http://localhost:8080/axis2/services/controler/getRestaurantReference?reference=%s&response=application/json" % (reference)).json()
	jsonResult = r["return"]
	restaurant = json_to_restaurant(jsonResult)
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		date = request.form['date']
		time = request.form['time']
		if name and email and date and time:
			requestServer = requests.get("http://localhost:8080/axis2/services/controler/createReservation?idRestaurant=%s&name=%s&email=%s&date=%s&time=%s&response=application/json" % (restaurant.idRestaurant, name, email, date, time)).json()
			message = requestServer['return']
		else:
			message = "Campos vazios"
	return render_template('profile.html', restaurant=restaurant, message=message)


@app.route('/delete', methods=['POST', 'GET'])
def delete():
	if 'Restaurant' in session:
		restaurant = json_to_restaurant(session['Restaurant'])
	if request.method == 'POST':
		requestServer = requests.get("http://localhost:8080/axis2/services/controler/deleteRestaurant?id=%s&response=application/json" % (restaurant.idRestaurant)).json()
		if requestServer['return'] == "Restaurante deletado com sucesso":
			session.pop('Restaurant', None)
	return redirect(url_for('maps'))

@app.route('/logout')
def logout():
	session.pop('Restaurant', None)
	return redirect(url_for('maps'))


def json_to_restaurant(jsonResult):
	return Restaurant(jsonResult["id"], jsonResult["name"], jsonResult["adress"], jsonResult["latitude"], jsonResult["longitude"], jsonResult["placesID"], jsonResult["email"], jsonResult["password"], jsonResult["description"], jsonResult["referencePlaces"], jsonResult["isPoint"], jsonResult["featureReservation"], jsonResult["featureMenu"])

def json_to_listResevation(jsonResult):
	listReservation = []
	if '@nil' not in jsonResult: 
		if type(jsonResult) == list:
			for item in jsonResult:
				listReservation.append(Reservation(item['id'], item['idRestaurant'], item['name'], item['email'], item['dateTime'], item['status']))
		else:
			listReservation.append(Reservation(jsonResult['id'], jsonResult['idRestaurant'], jsonResult['name'], jsonResult['email'], jsonResult['dateTime'], jsonResult['status']))
	return listReservation

if __name__ == '__main__':
	app.run(debug=True)