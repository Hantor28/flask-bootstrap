from flask import Flask, render_template, json, request, redirect, session, url_for, flash
import pymysql
from constant import conn

app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

connection = conn()


@app.route('/')
def main():
    if session.get('role')==1:
        return redirect('admin')
    if session.get('role')==2:
        return redirect('manager')
    if session.get('role')==3:
        return redirect('staff')
    else:
        return redirect('login')

@app.route('/login')
def showSignin():
        return render_template('signin.html')

@app.route('/admin')
def adminDashboard():
    if session.get('user'):
        return render_template('admin/admin_dashboard.html')
    else:
        return redirect('login')

@app.route('/manager')
def managerDashboard():
    if session.get('user'):
        return render_template('manager_dashboard.html')
    else:
        return redirect('login')

@app.route('/staff')
def staffDashboard():
    if session.get('user'):
        return render_template('staff_dashboard.html')
    else:
        return redirect('login')

@app.route('/validateLogin', methods=['GET', 'POST'])
def validateLogin():
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    try: 
        with connection.cursor() as cursor:
            sql = 'SELECT * FROM `am_db`.`users` WHERE `email` = %s AND `password` = %s'
            cursor.execute(sql, (email, password,))
            connection.commit()
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['user'] = account['username']
                session['role'] = account['role']
                session['password'] = account['password']
                session['phone_number'] = account['phone_number']
                session['avatar'] = account['avatar']


                return redirect('/')
            else:
                msg = 'Incorrect username/password!'

        return render_template('signin.html', msg=msg)
    finally:
        cursor.close()
        

@app.route('/logout')
def logout():
   session.pop('loggedin', None)
   session.pop('user', None)
   return redirect('/')


@app.route('/admin/show_users')
def admin_show_users():
        try: 
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `am_db`.`users`"
                result = cursor.execute(sql)
                connection.commit()
                users = cursor.fetchall()
            if result > 0:
                return render_template('admin_show_users.html', users=users)
            else:
                msg = 'No Articles Found'
                return render_template('admin_show_users.html', msg=msg)
        finally:
            cursor.close()

@app.route('/manager/show_users')
def manager_show_users():
        try: 
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `am_db`.`users`"
                result = cursor.execute(sql)
                connection.commit()
                users = cursor.fetchall()
            if result > 0:
                return render_template('manager_show_users.html', users=users)
            else:
                msg = 'No Articles Found'
                return render_template('manager_show_users.html', msg=msg)
        finally:
            cursor.close()

@app.route('/admin/add_user_form')
def add_user_form():
    return render_template('add_user.html')

@app.route('/admin/add_user', methods=['GET', 'POST'])
def add_user():
    au_email = request.form['au_email']
    au_username = request.form['au_username']
    au_role = request.form['au_role']
    au_phonenum = request.form['au_phonenum']

    try: 
        with connection.cursor() as cursor:
            sql = 'INSERT INTO users(email, password, username, role, phone_number, avatar ) VALUES(%s, 123456,  %s, %s, %s,"https://www.w3schools.com/howto/img_avatar.png")'
            cursor.execute(sql, (au_email, au_username, au_role, au_phonenum, ))
            connection.commit()
            flash('User added','success')
            return redirect('/admin/show_users')
    finally:
        cursor.close()

@app.route('/admin/edit_user_form/id=<string:id>', methods=['GET', 'POST'])
def edit_user_form(id):
    try: 
        with connection.cursor() as cursor:
            sql = "SELECT * FROM am_db.users WHERE id = %s"
            cursor.execute(sql, [id],)
            connection.commit()
            user = cursor.fetchone()
        return render_template('edit_user.html', user=user)
    finally:
        cursor.close()


@app.route('/admin/edit_user/id=<string:id>', methods=['GET', 'POST'])
def edit_user(id):
    eu_username = request.form['eu_username']
    eu_password = request.form['eu_password']
    eu_role = request.form['eu_role']
    eu_phonenum = request.form['eu_phonenum']
    try: 
        with connection.cursor() as cursor:
            sql = "UPDATE am_db.users SET username = %s, password = %s, role = %s, phone_number = %s WHERE id = %s"
            cursor.execute (sql,(eu_username, eu_password, eu_role, eu_phonenum, [id],))
            connection.commit()

            flash('User updated', 'success')
            return redirect('/admin/show_users')
    finally:
        cursor.close()

@app.route('/admin/delete_user/id=<string:id>', methods=['POST'])
def delete_user(id):
    try: 
        with connection.cursor() as cursor:
            sql="DELETE FROM am_db.users WHERE id = %s"
            cursor.execute(sql, [id])
            connection.commit()
            flash('User deleted', 'success')

            return redirect('/admin/show_users')
    finally:
        cursor.close()

@app.route('/admin/show_accounts')
def admin_show_accounts():
        try: 
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `am_db`.`accounts`"
                result = cursor.execute(sql)
                connection.commit()
                accounts = cursor.fetchall()
            if result > 0:
                return render_template('admin_show_accounts.html', accounts=accounts)
            else:
                msg = 'No accounts found'
                return render_template('admin_show_accounts.html', msg=msg)
        finally:
            cursor.close()

@app.route('/manager/show_accounts')
def manager_show_accounts():
        try: 
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `am_db`.`accounts`"
                result = cursor.execute(sql)
                connection.commit()
                accounts = cursor.fetchall()
            if result > 0:
                return render_template('manager_show_accounts.html', accounts=accounts)
            else:
                msg = 'No accounts found'
                return render_template('manager_show_accounts.html', msg=msg)
        finally:
            cursor.close()

@app.route('/admin/add_account_form', methods=['GET', 'POST'])
def add_account_form():
    return render_template('add_account.html')

@app.route('/admin/add_account', methods=['GET', 'POST'])
def add_account():
    aa_email = request.form['aa_email']
    aa_storename = request.form['aa_storename']
    aa_region = request.form['aa_region']
    aa_type = request.form['aa_type']
    aa_emailpass = request.form['aa_emailpass']
    aa_amzpass = request.form['aa_amzpass']
    aa_po = request.form['aa_po']
    aa_poname = request.form['aa_poname']
    aa_visa = request.form['aa_visa']
    aa_note = request.form['aa_note']
    aa_bank = request.form['aa_bank']
    aa_pic1 = request.form['aa_pic1']
    aa_pic2 = request.form['aa_pic2']
    aa_manager = request.form['aa_manager']
    aa_monthlyfees = request.form['aa_monthlyfees']
    aa_transferdate = request.form['aa_transferdate']
    aa_cost = request.form['aa_cost']

    try: 
        with connection.cursor() as cursor:
            sql = "INSERT INTO accounts(active_date, region, store_name, email, email_password,type , amz_password, po, po_name, visa, bank_information, pic1, pic2, manager, monthly_fees, transfer_date, note, cost) VALUES(now(),%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute (sql,(aa_region, aa_storename, aa_email, aa_emailpass, aa_type, aa_amzpass, aa_po, aa_poname, aa_visa, aa_bank, aa_pic1, aa_pic2, aa_manager, aa_monthlyfees, aa_transferdate, aa_note, aa_cost))
            connection.commit()

            flash('Account updated', 'success')
            return redirect('/admin/show_accounts')
    finally:
        cursor.close()


@app.route('/admin/edit_account_form/id=<string:id>', methods=['GET', 'POST'])
def edit_account_form(id):
    try: 
        with connection.cursor() as cursor:
            sql = "SELECT * FROM am_db.accounts WHERE id = %s"
            cursor.execute(sql, [id],)
            connection.commit()
            account = cursor.fetchone()

        return render_template('edit_account.html', account=account)
    finally:
        cursor.close()

@app.route('/admin/edit_account/id=<string:id>', methods=['GET', 'POST'])
def edit_account(id):
    ea_email = request.form['ea_email']
    ea_storename = request.form['ea_storename']
    ea_region = request.form['ea_region']
    ea_type = request.form['ea_type']
    ea_emailpass = request.form['ea_emailpass']
    ea_amzpass = request.form['ea_amzpass']
    ea_po = request.form['ea_po']
    ea_poname = request.form['ea_poname']
    ea_visa = request.form['ea_visa']
    ea_note = request.form['ea_note']
    ea_bank = request.form['ea_bank']
    ea_pic1 = request.form['ea_pic1']
    ea_pic2 = request.form['ea_pic2']
    ea_manager = request.form['ea_manager']
    ea_monthlyfees = request.form['ea_monthlyfees']
    ea_transferdate = request.form['ea_transferdate']
    ea_cost = request.form['ea_cost']

    try: 
        with connection.cursor() as cursor:
            sql = "UPDATE am_db.accounts SET email=%s, active_date=now(), store_name=%s, region=%s, type=%s, email_password=%s, amz_password=%s, po=%s, po_name=%s, visa=%s, note=%s, bank_information=%s, pic1=%s, pic2=%s, manager=%s, monthly_fees=%s, transfer_date=%s, cost = %s WHERE id=%s"
            cursor.execute (sql,(ea_email, ea_storename, ea_region, ea_type, ea_emailpass, ea_amzpass, ea_po, ea_poname, ea_visa, ea_note, ea_bank, ea_pic1, ea_pic2, ea_manager, ea_monthlyfees, ea_transferdate, ea_cost, [id],))
            connection.commit()

            flash('Account updated', 'success')
            return redirect('/admin/show_accounts')
    finally:
        cursor.close()

@app.route('/admin/delete_account/id=<string:id>', methods=['GET', 'POST'])
def delete_account(id):
    try: 
        with connection.cursor() as cursor:
            sql="DELETE FROM accounts WHERE id = %s"
            cursor.execute(sql, [id])
            connection.commit()

            flash('Account deleted', 'success')

        return redirect('/admin/show_accounts')
    finally:
        cursor.close()

@app.route('/show_orders')
def show_orders():
    try: 
        with connection.cursor() as cursor:
            sql1 = "SELECT * FROM `am_db`.`orders`"
            result=cursor.execute(sql1)
            connection.commit()
            orders = cursor.fetchall()
            print(result)
            print(orders)

            sql2="SELECT email FROM accounts"
            cursor.execute(sql2)
            connection.commit()
            accounts = cursor.fetchall()

            print(accounts)

        if result > 0:
            return render_template('orders.html', orders=orders, accounts= accounts)
        else:
            msg = 'No orders found'
            return render_template('orders.html', msg=msg)
    finally:
        cursor.close()

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    return 

@app.route('/edit_order/id=<string:id>', methods=['GET', 'POST'])
def edit_order(id):
    _account = request.form['eo_account']
    _designid = request.form['eo_designid']
    _createdate = request.form['eo_createdate']
    try: 
        with connection.cursor() as cursor:
            sql = "UPDATE am_db.orders SET account=%s, design_id=%s, createdate=%s WHERE id=%s"
            cursor.execute (sql,(_account, _designid, _createdate,[id]))
            connection.commit()

            flash('Order updated', 'success')
            return redirect('/show_orders')
    finally:
        cursor.close()

@app.route('/delete_order/id=<string:id>', methods=['GET', 'POST'])
def delete_order(id):
    try: 
        with connection.cursor() as cursor:
            sql="DELETE FROM orders WHERE id = %s"
            cursor.execute(sql, [id])
            connection.commit()

            flash('Order deleted', 'success')

        return redirect('/show_orders')
    finally:
        cursor.close()

if __name__ == "__main__":
    app.run(debug=True)