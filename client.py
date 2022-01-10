#This interactive python script can contact the flooder to start flooding the Network Interface Card 
#with traffic. 

#   TODOS:
# - storage machanism
# - measure rtt for X seconds, instruct flooder to flood for Y seconds, keep measuring for Z seconds
import csv
import requests
from icmplib import ping
import time
import socket
# import matplotlib.pyplot as plt

# serverSock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
# server_address = '127.0.0.1'
# server_port = 31338
# server = (server_address,server_port)
# serverSock.bind(server)
# print("Listening on " + server_address + ':' + str(server_port))
      
#instruct flooder to start flooding <address> for <duration> seconds after <offset> seconds
def instruct_flooder(flooderIP,flooderPort,offset, duration,sink_ip,sink_port,packet_size):
    url = 'http://'+flooderIP+':'+flooderPort+'/flooder/'
    params = {"key": "ditiseensoortwachtwoord",
        "offset": offset,
        "duration":duration,
        "sink_ip": sink_ip,
        "sink_port": sink_port,
        "packet_size": packet_size}
    x = requests.post(url, data = params)
    assert x.status_code == 200, "flooder can not be reached"

def get_rtt(serverIP,serverPort,duration):
    startTime = time.time() * 10 #starttime in deciseconds. 10 here means 10 measurements per second
    rtts = [] #is going to hold the rtt values
    prev = startTime
    print('Starting to measure RTT')
    try:
        clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        addr = (str(serverIP),int(serverPort))
    except:
        print("error opening socket")
        
    while True:
        if time.time() > startTime/10 + duration: #ends the measurement after the <duration> amount of secunds
            break
        if (time.time()*10) - prev > 1: #makes sure echoing is only done every 10th of a second
            clientSocket.sendto(str(time.time_ns()).encode(),addr) #send the amount of nanoseconds since epoch to server
            payload, client_address = clientSocket.recvfrom(1024) #start receiving, only completes after 1 received message
            rtts.append(time.time_ns() - int(payload.decode())) #calculate the rtt based on the value in the message and current time
            prev = time.time()*10
    print('Measuring RTT complete, got ' + str(len(rtts)) + ' datapoints')

    with open('ping_'+serverIP+'.csv',mode='w') as file:
        writer = csv.writer(file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in rtts:
            writer.writerow([i])

def validate_ip(s):
    a = s.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True
 
def main():
    serverIP = ''
    flooderIP = ''
    print('Usage: start <server IP> <Server Port> <flooder IP> <flooder port> <packet sink IP> <packet sink port> <packet length> <duration> <offset>')
    while True:
        x = input(">>>")
        parsed = x.split()
        if parsed[0] == 'exit':
            break
        if parsed[0] == 'help':
            print('Usage: start <server IP> <server Port> <flooder IP> <flooder port> <packet sink IP> <packet sink port> <packet length> <duration> <offset>')
        if parsed[0] == 'start':
            if len(parsed) == 10:
                if validate_ip(parsed[1]) & validate_ip(parsed[3]) & validate_ip(parsed[5]): 
                    serverIP = parsed[1]
                    serverPort = parsed[2]
                    flooderIP = parsed[3]
                    flooderPort = parsed[4]
                    packetSinkIP = parsed[5]
                    packetSinkPort = parsed[6]
                    packetLength = parsed[7]
                    duration = parsed[8]
                    offset = parsed[9]

                    instruct_flooder(flooderIP,flooderPort,offset,duration,packetSinkIP,packetSinkPort,packetLength)
                    get_rtt(serverIP,serverPort,int(duration) + 2*int(offset))

if __name__ == "__main__":
    main()

