#This interactive python script can contact the flooder to start flooding the Network Interface Card 
#with traffic. 

import csv
import requests
import time
import socket
import configparser
import matplotlib.pyplot as plt
import math

      
#instruct flooder to start flooding <address> for <duration> seconds after <offset> seconds
def instruct_flooder(flooderIP,flooderPort,measureDuration,floodDuration,sink_ip,sink_port,packet_size):
    url = 'http://'+flooderIP+':'+flooderPort+'/flooder/'
    params = {
        "measureDuration": measureDuration,
        "floodDuration":floodDuration,
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

    with open('results/ping_'+serverIP+'.csv',mode='w') as file:
        writer = csv.writer(file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in rtts:
            writer.writerow([i])

    #Drawing
    fig, ax = plt.subplots()
    ax.plot(rtts,label='rtt')
    ax.legend()
    ax.set_ylabel('RTT (ms)')
    ax.set_xlabel('Request number')
    plt.savefig('results/figure')
    plt.show()


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
    config = configparser.ConfigParser()
    config.read('config.ini')
    serverIP = config['SERVER']['IP']
    serverPort = int(config['SERVER']['Port'])
    flooderIP = config['FLOODER']['IP']
    flooderPort = config['FLOODER']['Port']
    packetSinkIP = config['PACKETSINK']['IP']
    packetSinkPort = int(config['PACKETSINK']['Port'])
    measureDuration = int(config['SCHEME']['MeasureDuration'])          
    floodDuration = int(config['SCHEME']['FloodDuration'])
    packetLength = int(config['SCHEME']['PacketLength'])

    if floodDuration > measureDuration:
        print('ERROR: measureduration must be bigger then floodduration')
        exit()

    if not(validate_ip(serverIP) & validate_ip(flooderIP) & validate_ip(packetSinkIP)): 
        print('ERROR: one of the provided IPs not valid')
        exit()

    instruct_flooder(flooderIP,flooderPort,measureDuration,floodDuration,packetSinkIP,packetSinkPort,packetLength)
    get_rtt(serverIP,serverPort,measureDuration)

if __name__ == "__main__":
    main()

