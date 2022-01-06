import socket
import threading
import time

drone1_ipaddress = ('192.168.0.107', 8889)
drone2_ipaddress = ('192.168.0.108', 8889)

local1_address = ('', 9010)
local2_address = ('', 9011)

command_connection1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
command_connection2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

command_connection1.bind(local1_address)
command_connection2.bind(local2_address)


# Send function
def send(instruction, delay_time):
    try:
        command_connection1.sendto(instruction.encode(), drone1_ipaddress)
        command_connection2.sendto(instruction.encode(), drone2_ipaddress)
        print("Sending Instruction: " + instruction)
    except Exception as e:
        print("Error while sending: " + str(e))

    time.sleep(delay_time)


# Receive function
def receive():
    while True:
        try:
            drone1_response, ip_address = command_connection1.recvfrom(128)
            drone2_response, ip_address = command_connection2.recvfrom(128)
            print("Received message: from Drone #1: " + drone1_response.decode(encoding='utf-8'))
            print("Received message: from Drone #2: " + drone2_response.decode(encoding='utf-8'))
        except Exception as error:
            command_connection1.close()
            command_connection2.close()
            print("Receiving error: " + str(error))
            break


receiving_thread = threading.Thread(target=receive)
receiving_thread.daemon = True
receiving_thread.start()

box_distance = 150
yaw_rotation = "cw"  # Clockwise rotation
yaw_angle = 180

send("command", 2)
send("takeoff", 5)

for i in range(4):
    send("forward " + str(box_distance), 2)
    send("cw " + str(yaw_angle), 2)

send("land", 3)

print("Mission Success")

command_connection1.close()
command_connection2.close()
