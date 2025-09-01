import socket

nb=1 # 0- HIT-"139.162.222.115", 1 - open HiveMQ - broker.hivemq.com

brokers=[str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com'))]
brockerIp=brokers[1]

ports=['80','1883']
port=ports[1]
brockerPort=ports[1]

usernames = ['DANIEL','']
passwords = ['DANIEL','']
username = usernames[1]
password = passwords[1]

conn_time = 0 # 0 stands for endless

dis=['daniel/','']
topicsToSub =[dis[1]+'2212','2212']
topicsToPub = [dis[1]+'2212','2212']
