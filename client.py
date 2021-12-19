#This interactive python script can contact the flooder to start flooding the Network Interface Card 
#with traffic. 

#   TODOS:
# - storage machanism
# - measure rtt for X seconds, instruct flooder to flood for Y seconds, keep measuring for Z seconds
import time 
import csv
import requests
import sys, getopt
from icmplib import ping
            
#instruct flooder to start flooding <address> for <duration> seconds
def instruct_flooder(address,duration):
    url = 'https://'+address+'/flooder/'
    myobj = {'key': 'ditiseensoortwachtwoord','duration':duration}
    x = requests.post(url, data = myobj)
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
    print('Usage: start <server IP> <flooder IP>')
    while True:
        x = input(">>>")
        parsed = x.split()
        if parsed[0] == 'exit':
            break
        if parsed[0] == 'help':
            print('Usage: start <server IP> <flooder IP>')
        if parsed[0] == 'start':
            if len(parsed) == 3:
                if validate_ip(parsed[1]) & validate_ip(parsed[2]): 
                    serverIP = parsed[1]
                    flooderIP = parsed[2]
                    get_rtt(serverIP,5)

if __name__ == "__main__":
    main()

