import mysql.connector
import hashlib


def mysqlconnect():
    usdb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="mouad123",
        database = "tddb"
    )
    return usdb

def ft_extract(lst):
    r = ()
    for i in lst:
        r = r + i
    return r

def hashing(password):
    h_pass = hashlib.sha256()
    password = password.encode()
    h_pass.update(password)
    return h_pass.hexdigest()

def e_check(email):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("select email from u_table where email = %s",(email,))
    result = ft_extract(cursor.fetchall())
    if email in result :
        return True
    else :
        return False

def u_check(email, password):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("select email, passwd from u_table where email = %s",(email,))
    password = hashing(password)
    result = ft_extract(cursor.fetchall())
    if email in result and password in result:
        return True
    else:
        return False
    
def add_user(firstname, lastname, email, password):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    password = hashing(password)
    cursor.execute("insert into u_table (firstname, lastname, email, passwd) values (%s, %s, %s, %s)",(firstname, lastname, email, password))
    usdb.commit()

def add_task(task,id_user):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("insert into task (item, statu, id_user) values (%s, %s, %s)",(task,"In progress",id_user))
    usdb.commit()

def get_task(id_user):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("select * from task where id_user = %s",(id_user,))
    tasks = cursor.fetchall()
    return tasks

def get_id(email):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("select id from u_table where email = %s",(email,))
    result = ft_extract(cursor.fetchall())
    return result[0]

def delete_task(id,id_user):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("delete from task where id = %s and id_user = %s",(id, id_user))
    usdb.commit()

def edit_statu(id, id_user):
    usdb = mysqlconnect()
    cursor = usdb.cursor()
    cursor.execute("update task set statu = 'Done' where id = %s and id_user = %s",(id, id_user))
    usdb.commit()