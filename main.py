from flask import Flask, render_template, request, url_for, redirect, session
from config import host, user, password, db_name
import psycopg2


app = Flask(__name__)
app.secret_key = 'sdflhsdde_fdgdfk-sdf1'


def get_db_conn():
    connection = psycopg2.connect(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=5433
    )

    return connection


@app.route('/')
def index():
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute('SELECT * FROM Orders;')
        orders = cur.fetchall()
        cur.close()
        conn.close()

        return render_template('index.html', orders=orders)
    except Exception as _d:
        return f"Произошла ошибка повторите попытку, {_d}"


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        login = request.form['login']
        passwordf = request.form['passwrd']
        fio = request.form['fio']
        email = request.form['email']
        role = request.form['role']
        if role == "executor":
            experience = request.form['experience']
            try:
                conn = get_db_conn()
                cur = conn.cursor()
                cur.execute('INSERT INTO Users (login, password, fio, email, role, experience)'
                            'VALUES(%s, %s, %s, %s, %s, %s)',
                            (login, passwordf, fio, email, role, experience))
                conn.commit()
                cur.close()
                conn.close()
                return redirect(url_for('log'))
            except Exception as _dfd:
                return f"Произошла ошибка повторите попытку, {_dfd}"

        try:
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute('INSERT INTO Users (login, password, fio, email, role)'
                        'VALUES(%s, %s, %s, %s, %s)',
                        (login, passwordf, fio, email, role))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('log'))
        except Exception as _dfd:
            return f"Произошла ошибка повторите попытку, {_dfd}"
    else:
        return render_template("register.html")


@app.route('/log', methods=('GET', 'POST'))
def log():
    if request.method == 'POST':
        login = request.form['login']
        passwordl = request.form['passwrd']
        try:
            conn = get_db_conn()
            cur = conn.cursor()
            cur.execute('SELECT * FROM Users WHERE login = %s',
                        (login,))
            account = cur.fetchone()
            if account:
                password_rs = account[2]
                if f'"{password_rs}"' == passwordl or passwordl == password_rs:
                    session['loggedin'] = True
                    session['id'] = account[0]
                    session['login'] = account[1]
                    session['fio'] = account[3]
                    session['email'] = account[4]
                    session['role'] = account[5]
                    if session['role'] == 'executor':
                        session['ex'] = account[6]
                    return redirect(url_for('index'))
                else:
                    cur.close()
                    conn.close()
                    return "пока пока"
        except Exception as _dfd:
            return f"Произошла ошибка повторите попытку, {_dfd}"

    return render_template("log.html")


@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        try:
            customer_name = request.form['customer_name']
            order_details = request.form['order_details']
            price = request.form['price']
            conn = get_db_conn()
            cur = conn.cursor()
            insert_query = "INSERT INTO Orders (name, description, price, user_id) VALUES (%s, %s, %s, %s)"
            cur.execute(insert_query, (customer_name, order_details, price, session['id']))
            conn.commit()
            cur.close()
            conn.close()

            return redirect(url_for('index'))
        except Exception as _df:
            return f"Произошла ошибка повторите попытку, {_df}"

    return render_template('create.html')


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('login', None)
    session.pop('fio', None)
    session.pop('email', None)
    session.pop('role', None)
    session.pop('ex', None)
    return redirect(url_for('index'))


@app.route('/<int:like>/dell', methods=['GET', 'POST'])
def dell(like):
    order_id = int(like)
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('DELETE FROM Orders WHERE order_id = %s;', (order_id,))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('index'))


@app.route('/myacc')
def myacc():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Orders;')
    orders = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('myacc.html', orders=orders)


@app.route('/<int:num>/order')
def order(num):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('UPDATE Orders SET customer = %s WHERE order_id = %s;',
                (session['id'], num,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:num>/prof')
def prof(num):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM Users WHERE user_id = %s;',
                (num,))
    profil = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('prof.html', profil=profil)


if __name__ == "__main__":
    app.run(debug=True)