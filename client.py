#This interactive python script can contact the flooder to start flooding the Network Interface Card 
#with traffic. 

#   TODOS:
# - storage machanism
# - measure rtt for X seconds, instruct flooder to flood for Y seconds, keep measuring for Z seconds
import csv
import requests
from icmplib import ping
# import matplotlib.pyplot as plt
            
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

# def draw_plot(filename):
#     #x = []
#     y = []
#     with open('ping_'+filename+'.csv',mode='r') as file:
#         reader = csv.reader(file,delimiter=',')
        
#         for row in reader:
#             #x.append(row[1])
#             y.append(float(row[0]))

#     fig = plt.figure()
#     plt.plot(y)
#     fig.savefig(filename+'.png', dpi=fig.dpi)
#     print('plot drawn')

 
# Measure RTT using ICMP of the Server. Data gets stored in a pre-defined csv file
def get_rtt(serverIP,duration):
    interval=0.1
    count = int(int(duration)/interval)
    print('pinging ' + serverIP + ' ' + str(count) + ' times')
    host = ping(serverIP,count,interval,timeout=1)
    print('pinging complete')
    with open('ping_'+serverIP+'.csv',mode='w') as file:
        writer = csv.writer(file,delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for i in host.rtts:
            writer.writerow([i])
    # draw_plot(address)

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
    print('Usage: start <server IP> <flooder IP> <flooder port> <packet sink IP> <packet sink port> <packet length> <duration> <offset>')
    while True:
        x = input(">>>")
        parsed = x.split()
        if parsed[0] == 'exit':
            break
        if parsed[0] == 'help':
            print('Usage: start <server IP> <flooder IP> <flooder port> <packet sink IP> <packet sink port> <packet length> <duration> <offset>')
        if parsed[0] == 'start':
            if len(parsed) == 9:
                if validate_ip(parsed[1]) & validate_ip(parsed[2]) & validate_ip(parsed[4]): 
                    serverIP = parsed[1]
                    flooderIP = parsed[2]
                    flooderPort = parsed[3]
                    packetSinkIP = parsed[4]
                    packetSinkPort = parsed[5]
                    packetLength = parsed[6]
                    duration = parsed[7]
                    offset = parsed[8]

                    instruct_flooder(flooderIP,flooderPort,offset,duration,packetSinkIP,packetSinkPort,packetLength)
                    get_rtt(serverIP,int(duration) + 2*int(offset))

if __name__ == "__main__":
    main()

