import mysql.connector

conn = mysql.connector.connect(
    host = "localhost" , 
    user = "root" ,
    passwd = "jJubJGiKwLizQkrrpBvrdMgEcAvy$N0z6kPP8$D@!hKA5&Ox0BB20FAL0n7HyEUd",
    database = 'webserverdb_v2'
    
)

userinfo = 'AKD324kegnSDG3nsdg'

c = conn.cursor(buffered=True)

#c.execute("""CREATE TABLE file_link (file_name text NOT NULL,link_code text NOT NULL)""")
#c.execute(f"CREATE TABLE {userinfo} (username text NOT NULL , password text NOT NULL)")
#c.execute("INSERT INTO AKD324kegnSDG3nsdg VALUES (%s , %s)",['admin' , '9bd8ec47190b344b009885a33eced36f6f511ddae835d36b45e2a121c69a1a59'])
#twillio2007


class Files:
    def __init__(self , name , code):
        self.name = name 
        self.code = code 

    def get_filename(self):
        return self.name 

    def get_code(self):
        return self.code

    def check_if_name_exist(self):
        c.execute("SELECT * FROM file_link WHERE file_name = %s", [self.name])
        if c.fetchall():
            return True 
        return False 

    def check_if_code_exist(self):
        c.execute("SELECT * FROM file_link WHERE link_code = %s", [self.code])
        if c.fetchall():
            return True 
        return False 

    def save_to_db(self):
        c.execute("INSERT INTO file_link VALUES (%s,%s)", [self.name , self.code])
        conn.commit()

    def get_all_db():
        c.execute("SELECT * FROM file_link")
        return c.fetchall()

    def get_file_info(code):
        c.execute("SELECT * FROM file_link WHERE link_code = %s" , [code])
        return c.fetchall()
    
    def delete(self):
        c.execute("DELETE FROM file_link WHERE link_code = %s" , [self.code])
        conn.commit()

class VerifyUser:
    def __init__(self , username , password):
        self.username = username
        self.password = password 

    def verify(self):   
        c.execute("SELECT * FROM AKD324kegnSDG3nsdg WHERE username = %s AND password = %s" , [self.username , self.password])
        if c.fetchall():
            return True 
        else:
            return False