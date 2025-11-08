from main_app import XpenseT
import mysql.connector
app= XpenseT()
#step1:save data
app.userinfo_data_from_DB()
#step2 : create account 
# print(app.create_ac("hasan","12345","nazmul","fahim","2004-10-30","01891491410","nazmulfahim000@gmail.com"))
#step 3 :log in to account 
app.log_in("hasan","12345")
#save loged in accounts Expense data
# app.xpense_track_data()

#track initial total ammount
# app.total_amount_extract("hasan")


#create account test..
#test add amount 
# app.add_amount(100,"2nd comment")
#test expense amount
app.expense_amount(20,"totato kinsi")
