#!/usr/bin/env python3

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



if len(sys.argv) == 2:
    grpc_port = sys.argv[1]
else:
    grpc_port="9998"

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


class SmartBus(smart_bus_pb2_grpc.SmartBusServicer):
    #Set status the device id
    def checkTicket(self, request, context):
        ticket_id=request.ticket_id
        device_id=request.device_id
        db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                    password="test",database="ticket")
        cursor = db.cursor()
        sql_query = "SELECT * FROM TICKETS WHERE  ticket_id = '%s'" % (ticket_id)
        try:
            cursor.execute(sql_query)
            db.close()
            result=cursor.fetchall()
            if len(result)==0:
                #if the ticket id is not registered or not purchased
                result="Invalid ticket"
                return smart_bus_pb2.checkTicketOutput(response=str(result))
            else:
                print(result)
                #If the ticket is registered
                status=str(result[0][4])
                last_check=str(result[0][5])

                #check if the ticket is not expired, using the timestamp
                print("last check",last_check)
                if last_check !='None':
                    if int(time.time()) - int(last_check) >420000000000000000000000:
                        result="Expired ticket"
                        return smart_bus_pb2.checkTicketOutput(response=str(result))

                #check status if the ticket is not used by other device
                print("status",status)
                if status!='None':
                    result="Someone is using it"
                    return smart_bus_pb2.checkTicketOutput(response=str(result))  
                
                last_check=str(int(time.time()))
                db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                    password="test",database="ticket")
                cursor = db.cursor()
                
                #update the device
                sql = "UPDATE TICKETS SET status='%s', last_check='%s' WHERE ticket_id = '%s'" % (device_id,last_check,ticket_id)
                try:
                    cursor.execute(sql)
                    print(device_id)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()

        except Exception as e:
            result="can't fetch content"
            print(e)
        db.close()
        return smart_bus_pb2.checkTicketOutput(response=str(device_id))


    #Set status to none when the person stands
    def checkTicketOff(self, request, context):
        ticket_id=request.ticket_id
        device_id=request.device_id
        db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                    password="test",database="ticket")
        cursor = db.cursor()
        sql_query = "SELECT * FROM TICKETS WHERE  ticket_id = '%s'" % (ticket_id)
        try:
            cursor.execute(sql_query)
            db.close()
            result=cursor.fetchall()
            if len(result)==0:
                #if the ticket id is not registered or not purchased
                result="Invalid ticket"
                return smart_bus_pb2.checkTicketOutput(response=str(result))
            else:
                print(result)
                #If the ticket is registered
                status=str(result[0][4])
                last_check=str(result[0][5])
                db=pymysql.connect(host="127.0.0.1",port=7118,user="root",
                                    password="test",database="ticket")
                cursor = db.cursor()
                #update the device
                sql = "UPDATE TICKETS SET status='%s' WHERE ticket_id = '%s'" % ("None", ticket_id)
                try:
                    cursor.execute(sql)
                    print(device_id)
                    db.commit()
                except Exception as e:
                    print(e)
                    db.rollback()
        except Exception as e:
            result="can't fetch content"
            print(e)
        db.close()
        return smart_bus_pb2.checkTicketOutput(response=str(device_id))



def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1000))
    smart_bus_pb2_grpc.add_SmartBusServicer_to_server(SmartBus(), server)
    server.add_insecure_port('[::]:'+str(grpc_port))
    server.start()
    print("Server listening on 0.0.0.0:{}".format(grpc_port))
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    main()

