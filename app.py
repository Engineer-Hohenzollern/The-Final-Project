from flask import *
import psycopg2.extras
import psycopg2
import Hash  # pls refer to Hash.py

host = 'localhost'
database = 'my_password_project'
username = 'postgres'
pas = 'richy'
port = 5432
conn = None  # if a connection is established conn != None we can use this logic to close conn in finally block

# ⤴ These parameters are the credentials we need to connect to our database.
# please finetune them for the database you have created.

try:  # we are establishing our connection to the database in a try and except block so in case a connection fails
    # our script won't fail also we can debug the reason why the connection couldn't be established

    with psycopg2.connect(  # the with block will ensure that all transactions are committed to the database if there
            # are no exceptions and if there is an exception all transactions would be withdrawn
            host=host,
            dbname=database,
            user=username,
            password=pas,
            port=port) as conn:

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:  # since we are using with block for the
            # cursor we do not need to close cur in the finally block as with block will do it for us
            cur.execute('DROP TABLE IF EXISTS ric')

            # ⤴️we need drop the tabel inorder to prevent duplicate entries each time we run the script
            # this ensures that there only 3 rows and no duplicate id is created each time we run the script
            # the encrypted password stored in the database will also change each time the script is run refer Hash.py

            create_script = ''' CREATE TABLE IF NOT EXISTS ric (
                                    id      int PRIMARY KEY,
                                    name    varchar(45) NOT NULL,
                                    password  varchar(45) NOT NULL)'''
            # ⤴️tabel is only created if it does not exist
            cur.execute(create_script)

            insert_script = 'INSERT INTO ric (id, name,password) VALUES (%s, %s, %s)'
            insert_values = [(1, 'Name1', Hash.encode('pass1')), (2, 'Name2', Hash.encode('pass2')),
                             (3, 'Name3', Hash.encode('pass3'))]
            # the actual password is not stored only the encrypted password is stored.
            # each encryption string is unique even if the password is reused refer Hash.py .
            for record in insert_values:
                cur.execute(insert_script, record)
            # ⤴ we insert every tuple oas row entry into the table
            cur.execute('SELECT * FROM RIC')
            users = cur.fetchall()  # This will return a list of list where each list is a row entry in the DB table

except Exception as error:
    print(error)  # exception block will capture the error, and it prints out the reason why connection couldn't be
    # established
finally:
    if conn is not None:  # this is to close the connection we have established with the database
        conn.close()

app = Flask(__name__)
app.secret_key = 'Antz.Ai'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # if its POST we will authenticate username and password else if GET we will return
        # render template to the login page

        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x[1] == username]  # we create a 2D list where we will extract the row(list) from
        # the users list in order to access the record of the user if the username exist in our database
        if len(user) == 0:  # we will only execute the elif statement  if user exist inorder to avoid index errors
            pass
        elif Hash.decode(user[0][2]) == password:
            return redirect('/welcome')
            # CASE 1 we will only redirect to the welcome page if password and username match

        return redirect(url_for('login'))  # CASE 2 if username is correct and password is wrong the user is again
        # redirected to the login page

    return render_template('login.html')  # if request.method == 'GET'


@app.route('/welcome')
def profile():
    return render_template('welcome.html')
