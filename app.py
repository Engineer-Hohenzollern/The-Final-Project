from flask import (
    Flask,
    redirect,
    render_template,
    request,
    url_for
)
import psycopg2.extras
import psycopg2
import Hash # pls refer to Hash.py 

host = 'localhost'
database = 'Waste1'
username = 'postgres'
pas = 'richy'
port = 5432
conn = None

try:
    with psycopg2.connect(
            host=host,
            dbname=database,
            user=username,
            password=pas,
            port=port) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute('DROP TABLE IF EXISTS ric')

            create_script = ''' CREATE TABLE IF NOT EXISTS ric (
                                    id      int PRIMARY KEY,
                                    name    varchar(45) NOT NULL,
                                    password  varchar(45) NOT NULL)'''

            cur.execute(create_script)

            insert_script = 'INSERT INTO ric (id, name,password) VALUES (%s, %s, %s)'
            insert_values = [(1, 'Name1', Hash.encode('pass1')), (2, 'Name2',Hash.encode('pass2')), (3, 'Name3',Hash.encode('pass3'))]
            for record in insert_values:
                cur.execute(insert_script, record)

            cur.execute('SELECT * FROM RIC')
            users = cur.fetchall()
            print(users)


except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()


app = Flask(__name__)
app.secret_key = 'Antz.Ai'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x[1] == username]
        if len(user)==0:
            pass
        elif Hash.decode(user[0][2]) == password:
            return redirect('/welcome')


        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/welcome')
def profile():
    return render_template('welcome.html')
