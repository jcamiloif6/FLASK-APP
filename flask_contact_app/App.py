from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

#Mysql Connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# settings
app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts1')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts1 = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
     if request.method == 'POST': 
         fullname = request.form['fullname']
         phone = request.form['phone']
         email = request.form['email']
         age = request.form['age']
         profession = request.form['profession']
         cur = mysql.connection.cursor()   
         cur.execute("INSERT INTO contacts1 (fullname, phone, email, age, profession) VALUES(%s, %s, %s, %s, %s)",
         (fullname, phone, email, age, profession))
         mysql.connection.commit()
         flash('Contact Adedd Succesfully')
         return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contacts1 WHERE id = %s", [id])
    data = cur.fetchall()
    cur.close()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        age = request.form['age']
        profession = request.form['profession']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contacts1
            SET fullname = %s,
                phone = %s,
                email = %s,
                age = %s,
                profession = %s
            WHERE id = %s
        """, (fullname, email, phone, age, profession, id))
        flash('Contact Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def delete_contact(id):
     cur = mysql.connection.cursor()
     cur.execute('DELETE FROM contacts1 WHERE id = {0}'.format(id))
     mysql.connection.commit()
     flash('Contact Removed Succesfully')
     return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(port = 3000, debug = True)
