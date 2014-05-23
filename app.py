from flask import Flask, render_template, request, session, redirect, url_for
from models.Restaurant import Restaurant

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
        if request.form['email'] and request.form['password']:
            if checkEmail(request.form['email']):
                session['email'] = request.form['email']
                return redirect(url_for('logged'))
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
        if email and password and name and adress:
            list_restaurants.append(Restaurant(email, password, name, adress))
            session['email'] = email
            return redirect(url_for('logged'))
        else:
            error = "Campos vazios"
    return render_template('signup.html', error=error)

@app.route('/logged')
def logged():
    if 'email' in session:
        restaurant = getEmail(session['email'])
        return render_template('logged.html', restaurant=restaurant)

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')


def checkEmail(email):
    for restaurant in list_restaurants:
        if restaurant.email == email:
            return True
    return False

def getEmail(email):
    for restaurant in list_restaurants:
        if restaurant.email == email:
            return restaurant
    return None

if __name__ == '__main__':
    list_restaurants = []
    app.run(debug=True)