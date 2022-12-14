from flask import Flask, render_template, url_for, request, redirect
from datebase import Database

app = Flask(__name__)
db = Database()


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/admin/tickets', methods=['GET'])
def tickets():
    tickets = db.get_tickets_for_table()
    return render_template('tickets.html', tickets=tickets)


@app.route('/admin', methods=['GET'])
def admin():
    autos = db.get_autos()
    name_clients = db.get_name_clients()
    tickets = db.get_tickets()
    tunning = db.get_tunnings()
    return render_template('admin.html', autos=autos, name_clients=name_clients, tickets=tickets, tunning=tunning)


@app.route('/client', methods=['POST'])
def new_client():
    name = request.form['name']
    surname = request.form['surname']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    db.add_client(name, surname, email, phone, address.replace('\n', ' '))
    return redirect('/')


@app.route('/admin/ticket', methods=['POST'])
def create_ticket():
    date = request.form['date']
    client = request.form['client']
    auto_num = request.form['auto_num']
    auto = request.form['auto']
    desc = request.form['desc']
    db.create_ticket(date, client, auto_num, auto, desc)
    return redirect('/admin')

@app.route('/admin/auto', methods=['POST'])
def create_auto():
    name = request.form['name']
    model = request.form['model']
    year = request.form['year']
    db.create_auto(name, model, year)
    return redirect('/admin')

@app.route('/admin/tunning', methods=['POST'])
def create_tun():
    name = request.form['name']
    desc = request.form['desc']
    cost = request.form['cost']
    db.create_tunning(name, desc, cost)
    return redirect('/admin')

@app.route('/admin/order', methods=['POST'])
def create_order():
    ticket = request.form['ticket']
    cost = request.form['cost']
    db.create_order(ticket, cost)
    return redirect('/admin')

@app.route('/admin/tun_in_ticket', methods=['POST'])
def create_tun_in_ticket():
    ticket = request.form['ticket']
    tun = request.form['tun']
    db.add_tunning_in_ticket(tun, ticket)
    return redirect('/admin')

app.run()