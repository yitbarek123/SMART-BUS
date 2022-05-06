import sys
import grpc
import os
sys.path.append("./service_spec")

import smart_bus_pb2 as pb2
import smart_bus_pb2_grpc as pb2_grpc
import logging
import multiprocessing
import random
import time
if len(sys.argv) == 2:
    grpc_port = sys.argv[1]
else:
    grpc_port="9998"



def check_ticket(channel):
    ticket=input("enter ticket id: ")
    device_id=input("enter device id: ")
    stub = pb2_grpc.SmartBusStub(channel)
    ticket_status=stub.checkTicket(pb2.checkTicketInputs(ticket_id=ticket,device_id=device_id))
    print(ticket_status)
    return str(ticket_status)

def check_ticket_off(channel):
    ticket=input("enter ticket id: ")
    device_id=input("enter device id: ")
    stub = pb2_grpc.SmartBusStub(channel)
    ticket_status=stub.checkTicketOff(pb2.checkTicketInputs(ticket_id=ticket,device_id=device_id))
    print(ticket_status)
    return str(ticket_status)

with grpc.insecure_channel('localhost:'+str(grpc_port)) as channel:
    check_ticket(channel)

with grpc.insecure_channel('localhost:'+str(grpc_port)) as channel:
    check_ticket_off(channel)