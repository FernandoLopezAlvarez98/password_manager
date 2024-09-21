import sqlite3

conn = sqlite3.connect("bd.dat",check_same_thread=False)
cursor = conn.cursor()


def initialize_db():
    cursor.execute(
        '''CREATE TABLE IF NOT EXISTS pass_manager(id text,servicio text, correo text, telefono text, password text)'''
    )

def create_pass(ids,service,email,phone, passwrd):
    try: 
        cursor.execute('''
            INSERT INTO pass_manager(id,servicio,correo,telefono,password)
            VALUES(?,?,?,?,?)
            ''',(ids,service,email,phone,passwrd))
        conn.commit()
        return 0
    except Exception as e:
        return e

def get_all():
    cursor.execute('''SELECT * FROM pass_manager''')
    return cursor.fetchall()

def search(servicio):
    cursor.execute(f"SELECT * FROM pass_manager WHERE servicio LIKE '%{servicio}%'")
    return cursor.fetchall()

def edit(id,service,email,phone):
    try: 
        cursor.execute('''
            UPDATE pass_manager SET servicio=?,correo=?,telefono=?,password=? WHERE id=''
            ''',(id,service,email,phone))
        conn.commit()
        return 0
    except Exception as e:
        return e

def delete(ide):
    try: 
        cursor.execute('''
            DELETE FROM pass_manager WHERE id=?
            ''',(ide,))
        conn.commit()
        return 0
    except Exception as e:
        return e
#print(create_pass("youtube","lfer@gmail.com","9932394079","Ameriacs03"))
#print(get_all())
#print(search("go"))
#print(edit("Hola","","","Americas03"))
#print(delete())
