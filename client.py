#This interactive python script can contact the flooder to start flooding the Network Interface Card 
#with traffic. 

#   TODOS:
# - storage machanism
# - measure rtt for X seconds, instruct flooder to flood for Y seconds, keep measuring for Z seconds
import time 
import csv
import requests
from icmplib import ping
            
#instruct flooder to start flooding <address> for <duration> seconds after <offset> seconds
def instruct_flooder(address,offset, duration,sink_ip,sink_port,packet_size):
    url = 'http://'+address+':3000/flooder/'
    params = {"key": "ditiseensoortwachtwoord",
        "offset": offset,
        "duration":duration,
        "sink_ip": sink_ip,
        "sink_port": sink_port,
        "packet_size": packet_size}
    x = requests.post(url, data = params)
    assert x.status_code == 200, "flooder can not be reached"
 
# Measure RTT using ICMP of the Server. Data gets stored in a pre-defined csv file
def get_rtt(address,duration):
    interval=0.5
    count = int(duration/interval)
    host = ping(address,count=count,interval=interval,timeout=2)
    print(host.rtts)
    with open('ping_'+address+'.csv',mode='w') as file:
        writer = csv.writer(file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in host.rtts:
            writer.writerow([i,time.time()])

# Helper function to validate IP addresses
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
    print('Usage: start <server IP> <flooder IP> <packet sink IP> <packet sink port> <packet length> <duration> <offset>')
    while True:
        x = input(">>>")
        parsed = x.split()
        if parsed[0] == 'exit':
            break
        if parsed[0] == 'help':
            print('Usage: start <server IP> <flooder IP>')
        if parsed[0] == 'default':
            print('using default values')
            instruct_flooder('127.0.0.1',3,5,'192.168.2.13',161,50)
            get_rtt('1.1.1.1',8)
        if parsed[0] == 'start':
            if len(parsed) == 8:
                if validate_ip(parsed[1]) & validate_ip(parsed[2]) & validate_ip(parsed[3]): 
                    serverIP = parsed[1]
                    flooderIP = parsed[2]
                    packetSinkIP = parsed[3]
                    packetSinkPort = parsed[4]
                    packetLength = parsed[5]
                    duration = parsed[6]
                    offset = parsed[7]

                    #instruct flooder to flood for 10 seconds after 2 seconds
                    instruct_flooder(flooderIP,offset,duration,packetSinkIP,packetSinkPort,packetLength)
                    get_rtt(serverIP,duration + 2*offset)

if __name__ == "__main__":
    main()

