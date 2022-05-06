from concurrent import futures
import sys
import grpc
import time
import ast

sys.path.append("./service_spec")


import time
import subprocess

from time import sleep

import smart_bus_pb2_grpc

import smart_bus_pb2


import logging


import pymysql

import random


db_connection=pymysql.connect(host="127.0.0.1",port=7118,
                                user="root",password="test")


cursor_instance=db_connection.cursor()

sql="CREATE DATABASE IF NOT EXISTS ticket CHARACTER SET utf8 COLLATE utf8_general_ci"

cursor_instance.execute(sql)
db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                    password="test",database="ticket")
cursor = db.cursor()

sql = """CREATE TABLE  IF NOT EXISTS TICKETS (
   id INT NOT NULL AUTO_INCREMENT,
   purchased_time VARCHAR(100) NOT NULL,
   ticket_id VARCHAR(100) NOT NULL,
   device_id VARCHAR(100),
   status VARCHAR(100),
   last_check VARCHAR(100),
   PRIMARY KEY (id)
   )"""


cursor.execute(sql)


db.close()

def ticket_purchased():
    response="www"
    json_value="www"
    ticket_id="07B0009700384340"#str(random.randint(1,10000000))
    purchased_time=str(int(time.time()))
    
    #insert

    db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                password="test",database="ticket")

    purchased_date="today"

    sql = "INSERT INTO TICKETS(ticket_id,purchased_time) VALUES ('%s', '%s')" % (ticket_id, purchased_time)
    try:
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
    db.close()


    #read
    db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                password="test",database="ticket")
    cursor = db.cursor()
    sql_query = "SELECT * FROM TICKETS WHERE  ticket_id = '%s'" % (ticket_id)
    try:
        cursor.execute(sql_query)
        result=cursor.fetchall()
        print(result)
        if len(result)==0:
            result="no cache"
        else:
            result=str(result[0][0])
    except Exception as e:
        result="can't fetch content"
        print(e)
    db.close()
    #print(response)
    #return smart_bus_pb2.checkTicketOutput(response=str(response))

def print_all():
    response="www"
    json_value="www"
    ticket_id=str(random.randint(1,10000000))
    purchased_time=str(int(time.time()))
    
    #insert


    purchased_date="today"




    #read
    db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                password="test",database="ticket")
    cursor = db.cursor()
    sql_query = "SELECT * FROM TICKETS"
    try:
        cursor.execute(sql_query)
        result=cursor.fetchall()
        print(result)
        if len(result)==0:
            result="no result"
        else:
            result=str(result[0][0])
    except Exception as e:
        result="can't fetch content"
        print(e)
    db.close()
    #print(response)
    #return smart_bus_pb2.checkTicketOutput(response=str(response))


ticket_purchased()

print_all()

