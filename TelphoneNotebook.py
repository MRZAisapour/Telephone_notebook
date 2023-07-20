import psycopg2
import random

global Current_Connection, Cursor


def CNewPhonebook(cursor):
    global Current_Connection, Cursor
    x = input("insert name of the phonebook: ")
    cursor.execute("CREATE USER admin WITH ENCRYPTED PASSWORD 'admin';")
    cursor.execute(f"CREATE DATABASE {x};")
    cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {x} TO admin;")
    Current_Connection = psycopg2.connect(
        user="admin",
        password="admin",
        host="localhost",
        database=x
    )
    Cursor = Current_Connection.cursor()
    Current_Connection.autocommit = True
    Cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    Username VARCHAR(50) NOT NULL,
    Userpass VARCHAR(50),
    Name     VARCHAR(50) NOT NULL,
    Phone    VARCHAR(50) NOT NULL,
    UserID   SERIAL      PRIMARY KEY);"""
                   )
    Cursor.execute(f"""INSERT INTO users(Username, Userpass, Name, Phone, UserID)
    VALUES('admin', 'admin', 'admin','0',0);""")


# done
def CNewUser(user):
    if user != "admin":
        print("You are not the admin")
        return 0
    firstname = input("Enter the Firstname: ")
    lastname = input("Enter the lastname: ")
    Username = firstname + "_" + lastname
    Userpass = input("Enter the Userpass: ")
    phone = input("Enter the Phonenumber: ")
    Cursor.execute(f"""INSERT INTO users(Username, Name, Userpass, Phone)
    VALUES('{Username}', '{Username}', '{Userpass}', '{phone}');""")


# done
def RemoveUser(user):
    if user == "admin":
        x = input(
            "you are the admin, if you want to delete another account Enter 1 else Enter 2 for deleting the phonebook: ")
        if x == "2":
            Cursor.execute("DELETE TABLE Users;")
            print("THE DATABASE HAS BEEN DELETED")
            return "END"
        elif x == "1":
            user = input("enter the username: ")
            Cursor.execute(f"""DELETE FROM users
                   WHERE Username = '{user}';""")
            print(f"{user} has been deleted")
            return "admin"
    else:
        Cursor.execute(f"""DELETE FROM users
                   WHERE Username = '{user}';""")
        print(f"{user} has been deleted")
        return "admin"


# done
def AddContact(user):
    first = input("firstname: ")
    last = input("lastname: ")
    phonenumber = input("phonenumber: ")
    x = first + "_" + last
    Cursor.execute(f"""INSERT INTO users(Username, Name, Phone)
                   VALUES('{user}', '{x}', '{phonenumber}');""")


# done
def EditContact(user):
    first = input("firsname of the contact: ")
    last = input("lastname of the contact: ")
    x = first + "_" + last
    ECFN = input("edited contact firstname: ")
    ECLN = input("edited contact lastname: ")
    ECN = ECFN + "_" + ECLN
    EPN = input("edited phone number: ")
    if user == "admin":
        Cursor.execute(f"""UPDATE users
        SET Name = '{ECN}',
            phone = '{EPN}'
        WHERE Name = '{x}';"""
                       )
    else:
        Cursor.execute(f"""UPDATE users
            SET Name = '{ECN}',
                phone = '{EPN}'
            WHERE Name = '{x}' AND username = '{user}';"""
                       )
    print("DONE!")


# done
def RemoveContact(user):
    first = input("firsname of the contact: ")
    last = input("lastname of the contact: ")
    x = first + "_" + last
    Cursor.execute(f"""DELETE FROM users
                   WHERE name = '{x}' and username = '{user}';"""
                   )


# done
def SearchUser(user):
    if user != "admin":
        print("you are not the admin")
        return 0
    x = input("search: ")
    Cursor.execute(f"""SELECT username FROM users
                WHERE username LIKE '%{x}%' AND Userpass != '';"""
                   )
    record = Cursor.fetchall()
    print(record)
    pass


# done
def SearchContact(user):
    x = input("search: ")
    if user == "admin":
        Cursor.execute(f"""SELECT name,phone FROM users
                    WHERE Name LIKE '{x}%' OR phone Like'{x}%';"""
                       )
        record = Cursor.fetchall()
    else:
        Cursor.execute(f"""SELECT name,phone FROM users
                    WHERE (Username = '{user}') AND (Name LIKE '{x}%' OR phone Like'{x}%');"""
                       )
        record = Cursor.fetchall()
    print("all i found: ")
    for i in record:
        print("contact's name:", i[0])
        print("phone number:", i[1])
        print("--------------------------------")


# done
def LogOut(user):
    if user == "admin":
        print("you are the admin. You can't log out!")
    else:
        user = "admin"
        print("you are logged out")
        return user


# done
def LogIn(user):
    if user != "admin":
        print("you are not the admin")
        return user
    x = input("Enter the username: ")
    p = input("Enter the password: ")
    Cursor.execute(f"""SELECT Username, Userpass FROM USERS
                       WHERE Username = '{x}' AND Userpass = '{p}';""")
    n = Cursor.fetchone()
    try:
        if len(n) == 0:
            print("please try again")
        else:
            print("you are logged in")
            return x
    except(TypeError):
        print("Try again")
        return "admin"


# done
con = psycopg2.connect(
    user="postgres",
    password="12345678",
    host="localhost"
)
con.autocommit = True
cursor = con.cursor()
CNewPhonebook(cursor)
Current_Admin = "admin"
Current_User = "admin"
flag = True
while True:
    print("1:create new phonebook")
    print("2:create new user")
    print("3:remove user:")
    print("4:add contact")
    print("5:edit contact")
    print("6:remove contact")
    print("7:search user")
    print("8:search contact")
    if Current_User != "admin": print("9:log out")
    print("e:exit")
    if Current_User == "admin": print("LI:LogIn")
    inp = input()
    if inp == "1": CNewPhonebook(cursor)
    if inp == "2": CNewUser(Current_User)
    if inp == "3":
        Current_User = RemoveUser(Current_User)
    if inp == "4": AddContact(Current_User)
    if inp == "5": EditContact(Current_User)
    if inp == "6": RemoveContact(Current_User)
    if inp == "7": SearchUser(Current_User)
    if inp == "8": SearchContact(Current_User)
    if inp == "9":
        Current_User = LogOut(Current_User)
    if inp == "LI":
        Current_User = LogIn(Current_User)
    if inp == "e": break
    if Current_User == "END":
        break

