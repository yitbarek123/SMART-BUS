import RPi.GPIO as GPIO
import time
import cv2
import threading

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


#pin number
sensor = 11
buzzer = 22

#initialize sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor,GPIO.IN)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.output(buzzer,False)

print ("IR Sensor Ready.....")
print (" ")


def get_qr(ticket):
    ticket.cap = ticket.cv2.VideoCapture(0)
    # QR code detection object
    detector = ticket.cv2.QRCodeDetector()
    ticket_id=None
    time_taken=0
    start_time=int(time.time())
    #activate camera for only 1 mminute , if there is a person and if ticket id is None.
    while ticket_id==None and time_taken<60 and ticket.camera:
        time_taken=int(time.time())-start_time
        # get the image
        _, img = ticket.cap.read()
        # get bounding box coords and data
        data, bbox, _ = detector.detectAndDecode(img)
        
        # if there is a bounding box, draw one, along with the data
        if(bbox is not None):
            for i in range(len(bbox)):
                ticket.cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
                        0, 255), thickness=2)
            ticket.cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), ticket.cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 255, 0), 2)
            if data:
                print("data found: ", data)
                ticket_id=data
        # display the image preview
        ticket.cv2.imshow("code detector", img)
        if(ticket.cv2.waitKey(1) == ord("q")):
            break
    # free camera object and exit
    ticket.cap.release()
    ticket.cv2.destroyAllWindows()
    return ticket_id



def turnoff_buzzer(ticket):
    while True:
        #if there is no person
        if GPIO.input(sensor)==1:
            # turn off camera and alarm
            GPIO.output(buzzer,False)   
            ticket.camera=False
            ticket.seat=0
            #removes the ticket from cloud server if there is no block
            if ticket.ticket_id!="":
                print("removing")
                check_ticket_off(ticket.ticket_id,ticket.device_id)
                ticket.ticket_id=""
        time.sleep(1)

#grpc call to cloud for adding ticket 
def check_ticket(ticket_id,device_id):
    with grpc.insecure_channel('192.168.8.102:'+str(grpc_port)) as channel:
        stub = pb2_grpc.SmartBusStub(channel)
        ticket_status=stub.checkTicket(pb2.checkTicketInputs(ticket_id=str(ticket_id),device_id=device_id))
        print("ticket status")
        print(ticket_status)
        return str(ticket_status)


#grpc call to cloud for removing ticket when the person moves away
def check_ticket_off(ticket_id,device_id):
    with grpc.insecure_channel('192.168.8.102:'+str(grpc_port)) as channel:
        stub = pb2_grpc.SmartBusStub(channel)
        ticket_status=stub.checkTicketOff(pb2.checkTicketInputs(ticket_id=str(ticket_id),device_id=device_id))
        print("ticket status")
        print(ticket_status)
        return str(ticket_status)

class Ticket():
    def __init__(self):
        #use static variable to store sensor and camera variables. Later can be used for removing.
        #use last_otpt variables for not printing the values again
        self.ticket_id = "" 
        self.device_id = "Lamverde32" 
        self.cv2=cv2
        self.cap=None
        self.camera=False
        self.seat=0
        self.last_otpt=""
        self.last_otpt2=""
        self.last_otpt3=""


try:
   ticket = Ticket()
   ticket_id=None
   device_id = "Lamverde32"

   #run a thread that checks conditions and turns the buzzer off in background
   t1 = threading.Thread(target=turnoff_buzzer, args=(ticket,))
   t1.start()
   
   #start detection 
   while True:
      if GPIO.input(sensor)!=ticket.last_otpt:
        print(GPIO.input(sensor))
        ticket.last_otpt=GPIO.input(sensor)
      
      if GPIO.input(sensor)==0 and ticket.seat==0:
          if GPIO.input(sensor)==0 :
              print("there is person")
              ticket.seat=1
              ticket.camera=True
              ticket_id=get_qr(ticket)
              time.sleep(0.2)
              print("ticket id")
              print(ticket_id)
              if ticket_id==None:
                GPIO.output(buzzer,True)
                otpt="No ticket!!!"
                if otpt!=ticket.last_otpt3:
                    print(otpt)
                    ticket.last_otpt3=otpt
              else:
                ticket_status=check_ticket(ticket_id,device_id)
                print(device_id in ticket_status)
                if device_id not in ticket_status :
                    GPIO.output(buzzer,True)
                else:
                    ticket.ticket_id=ticket_id
      # if no person seats
      if GPIO.input(sensor)==1:
        
        otpt="there is no person"
        if otpt!=ticket.last_otpt2:
            print(otpt)
            ticket.last_otpt2=otpt
        GPIO.output(buzzer,False)

except KeyboardInterrupt:
    GPIO.cleanup()


