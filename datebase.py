import pymysql

class Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='123',
            database='tunning_cars'
        )
        
    def add_client(self, name, surnmae, email, phone, address):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO clients (name, surname, discount_id, phone_number, email, address) '
                           f'VALUES ("{name}", "{surnmae}", 1, "{phone}", "{email}", "{address}")')
            self.connection.commit()
            
    def get_autos(self):
        autos = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM autos')
            for row in cursor.fetchall():
                autos.append([row[0], f'{row[1]} {row[2]} ({row[3]})'])
        return autos
    
    def get_name_clients(self):
        clients = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM clients')
            for row in cursor.fetchall():
                clients.append([row[0], f'{row[1]} {row[2]}'])
        return clients
    
    def create_ticket(self, date, client, auto_num, auto, desc):
         with self.connection.cursor() as cursor:
            cursor.execute(f'SELECT * FROM client_autos WHERE autos_id = {auto} AND gos_number = "{auto_num}"')
            if len(cursor.fetchall()) == 0:
                cursor.execute(f'INSERT INTO client_autos (gos_number, autos_id) VALUES ("{auto_num}", {auto})')
                self.connection.commit()
                cursor.execute(f'SELECT id FROM client_autos WHERE autos_id = {auto} AND gos_number = "{auto_num}"')
                car_num_id = cursor.fetchall()[0][0]
            else:
                cursor.execute(f'SELECT id FROM client_autos WHERE autos_id = {auto} AND gos_number = "{auto_num}"')
                car_num_id = cursor.fetchall()[0][0]
                
            date = date.replace('-', '*')
            cursor.execute(f'INSERT INTO tickets (date, description, clients_id, client_autos_id1) '
                           f'VALUES ("{date}", "{desc}", {client}, {car_num_id})')
            self.connection.commit()
            
    def create_auto(self, name, model, year):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO autos (name, model, year) VALUES ("{name}", "{model}", "{year}")')
            self.connection.commit()
            
    def create_tunning(self, title, desc, cost):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO tunnings (title, description, cost) VALUES ("{title}", "{desc}", {float(cost)})')
            self.connection.commit()
            
    def get_tickets(self):
        tickets = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT tickets.id, tickets.date, clients.name, clients.surname, autos.name, autos.model, client_autos.gos_number FROM tickets ' 
                            'INNER JOIN client_autos ON tickets.client_autos_id1 = client_autos.id '
                            'INNER JOIN autos ON autos.id = client_autos.autos_id '
                            'INNER JOIN clients ON tickets.clients_id = clients.id')
            for row in cursor.fetchall():
                tickets.append([row[0], f'{row[2]} {row[3]} - {row[4]} {row[5]} ({row[6]}) - {row[1]}'])
        return tickets
    
    def get_tunnings(self):
        tun = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT * FROM tunnings')
            for row in cursor.fetchall():
                tun.append([row[0], f'{row[1]} - {row[3]}'])
        return tun
    
    def add_tunning_in_ticket(self, tun, ticket):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO tickets_has_tunnings (tunnings_id, tickets_id) VALUES ({tun}, {ticket})')
            self.connection.commit()
            
    def create_order(self, ticket, cost):
        with self.connection.cursor() as cursor:
            cursor.execute(f'INSERT INTO orders (result_cost, tickets_id) VALUES ({cost}, {ticket})')
            self.connection.commit()
            
    def get_tickets_for_table(self):
        tickets = []
        with self.connection.cursor() as cursor:
            cursor.execute('SELECT tickets_has_tunnings.tickets_id, clients.name, clients.surname, autos.name, autos.model, client_autos.gos_number, tunnings.title, tunnings.cost FROM clients '
                            'INNER JOIN tickets ON tickets.clients_id = clients.id '
                            'INNER JOIN client_autos ON tickets.client_autos_id1 = client_autos.id '
                            'INNER JOIN autos ON client_autos.autos_id = autos.id '
                            'INNER JOIN tickets_has_tunnings ON tickets_has_tunnings.tickets_id = tickets.id '
                            'INNER JOIN tunnings ON tickets_has_tunnings.tunnings_id = tunnings.id')
            fetchall = cursor.fetchall()
            for i in range(fetchall[len(fetchall) - 1][0]):
                tickets.append([])
            for row in fetchall:
                tickets[row[0] - 1].append([row[0] - 1, f'{row[1]} {row[2]}', f'{row[3]} {row[4]} ({row[5]})', row[6], row[7]])
        return tickets
                