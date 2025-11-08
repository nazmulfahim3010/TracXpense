import mysql.connector  # type: ignore
import json

class XpenseT:
    def __init__(self,user_name=None,password=None,file_name=None,user_id=None):
        self._user_name=user_name
        self._password=password
        self.file_name=file_name
        self._total=None
        self.user_data=[]
        self._total_amount=0.0
        self.user_id=user_id
        ...
    def userinfo_data_from_DB(self):
        file_name="user_info_data.json"
        mydb=mysql.connector.connect(
            host="localhost",
            user= "root",
            password="30102004",
            database = "XpenseTrack"
        )

        cursor=mydb.cursor(dictionary=True)

        cursor.execute(
        '''
SELECT u.u_id,u.user_name,p.password 
FROM user_info u
join user_pass p on u.u_id=p.user_id;
        '''
        )
        user_info = cursor.fetchall()
        self.load_data(user_info,file_name) # type: ignore

    def colect_uid(self,user_name):
        mydb=mysql.connector.connect(
            host="localhost",
            user= "root",
            password="30102004",
            database = "XpenseTrack"
        )

        cursor=mydb.cursor(dictionary=True)
        cursor.execute(
            """
select u_id,user_name from user_info;
            """
        )
        info=cursor.fetchall()

        for data in info:
            if data["user_name"]==user_name:
                print("u_id checking")
                return data["u_id"]
        cursor.close()
        mydb.close()


    def load_data(self,data,file_name=None):
        with open(file_name, "w") as json_file:
            json.dump(data, json_file, indent=4,default=str)
        print("✅load done")
        ...
        #-----------------properties-----------------#
    @property
    def total(self):
        return self._total
    @total.setter
    def total(self,total):
        self._total=total
    
    @property
    def user_id(self):
        return self._user_id
    @user_id.setter
    def user_id(self,user_id):
        self._user_id=user_id


    @property
    def total_amount(self):
        return self._total_amount
    @total_amount.setter
    def total_amount(self,amount):
        self._total_amount=amount


    @property
    def user_name(self):
        return self._user_name
    @user_name.setter
    def user_name(self,user_name):
        self._user_name=user_name


    @property 
    def password(self):
        return self._password
    @password.setter
    def password(self,new_password):
        self._password=new_password
            #--------------------end--------------------#
    def log_in(self,user_name,password):
        self.user_name=user_name
        self.password=password
        find=False
        for info in self.user_data:
            if(info["user_name"]==self.user_name and info["password"]==self.password):
                find=True # account find 
                self.user_id=info["u_id"]
                return True
        if find==False:
            return False # no account find 
    
    def create_ac(self, user_name, password, first_name, last_name, date_of_birth, contact, email):
        if self.log_in(user_name, password):
            return False  # you already have an account
        else:
            self.user_name = user_name
            self.password = password

            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="30102004",
                database="XpenseTrack"
            )
            cursor = mydb.cursor()

            
            query = '''
            INSERT INTO user_info (user_name, first_name, last_name, date_of_birth, contact, email)
            VALUES (%s, %s, %s, %s, %s, %s);
            '''
            values = (self.user_name, first_name, last_name, date_of_birth, contact, email)
            cursor.execute(query, values)
            mydb.commit()

            # Step 2: Get the auto-generated user_id
            user_id = cursor.lastrowid
            print("✅ User ID created:", user_id)

            # Step 3: Insert into user_pass
            query_1 = '''
            INSERT INTO user_pass (user_id, user_name, password)
            VALUES (%s, %s, %s);
            '''
            values_1 = (user_id, self.user_name, self.password)
            cursor.execute(query_1, values_1)
            mydb.commit()
            print("✅ Password saved for user.")

            # Step 4: Create user-specific table
            query_2 = f"""
            DROP TABLE IF EXISTS {self.user_name}_add;
            CREATE TABLE {self.user_name}_add (
                id INT AUTO_INCREMENT PRIMARY KEY,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                appended DECIMAL(8,2),
                total DECIMAL(8,2),
                expense DECIMAL(8,2),
                expense_comment TEXT,
                stat ENUM('ADD','EXPENSE') NOT NULL
            );
            """
            cursor.execute(query_2)
            mydb.commit()

            cursor.close()
            mydb.close()
            print("✅ Account created successfully.")
            return True
        
    def total_amount_extract(self, user_name):
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="30102004",
            database="XpenseTrack"
        )
        cursor = db.cursor()

        try:
            cursor.execute(f"""
                SELECT total FROM {user_name}_add
                ORDER BY id DESC
                LIMIT 1;
            """)
            total_row = cursor.fetchone()

            if total_row and total_row[0] is not None:
                self.total = total_row[0]
                print(f"✅ Total found: {self.total}")
            else:
                self.total = 0.00
                print("ℹ️ No previous total found, setting to 0.00")

        except Exception as e:
            self.total = 0.00
            print("❌ Error fetching total:", e)

        finally:
            cursor.close()
            db.close()


    def xpense_track_data(self):
        file_name=f"{self.user_name}_xpense_data.json"
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="30102004",
            database="XpenseTrack"
        )
        cursor=mydb.cursor(dictionary=True)
        query=(f"""
select * from {self.user_name}_add
                """)
        cursor.execute(query)
        user_xpense=cursor.fetchall()
        self.load_data(user_xpense,file_name)
        cursor.execute(f"""
CREATE INDEX xpense_history ON {self.user_name}_add(id);
            """)
        mydb.commit()

        cursor.close()
        mydb.close()
        print("✅xpense track data listed")

    def add_amount(self, amount, comment='N/A'):
        if self.total is None:
            self.total_amount_extract(self.user_name)

        new_total = float(self.total) + float(amount)

        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="30102004",
            database="XpenseTrack"
        )
        cursor = mydb.cursor()

        query = f"""
            INSERT INTO {self.user_name}_add (appended, expense_comment, total, stat)
            VALUES (%s, %s, %s, %s);
        """
        value = (amount, comment, new_total, 'ADD')
        cursor.execute(query, value)
        mydb.commit()

        cursor.close()
        mydb.close()

        self.total = new_total
        print(f"✅ Money Added. New total: {self.total:.2f}")
    

    def expense_amount(self,amount,comment='N/A'):
        if self.total is None:
            self.total_amount_extract(self.user_name)
        
        new_total=float(self.total)-float(amount)
        if new_total>0:
            mydb=mysql.connector.connect(
                host='localhost',
                user='root',
                password='30102004',
                database='XpenseTrack'
            )

            cursor=mydb.cursor()

            query = f"""
                INSERT INTO {self.user_name}_add (expense, expense_comment, total, stat)
                VALUES (%s, %s, %s, %s);
            """
            value = (amount, comment, new_total, 'EXPENSE')
            cursor.execute(query, value)
            mydb.commit()

            cursor.close()
            mydb.close()

            self.total = new_total
            print(f"✅ Money Added. New total: {self.total:.2f}")
            return True
        else:
            print("❌ Not Eligable")
            return False
        ...  

