import sys
from LOGGER import LOGGER
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
from mqtt_init import *

# Creating Client name - should be unique 
global clientname
r=random.randrange(1,10000000)
clientname="IOT_client-Id-"+str(r)

# Initialize LOGGER
logger = LOGGER("IOT_DB_RECORDS.csv")

relay_topic = 'home/daniel/RELAY'

smart_home_topic = 'MY_SMART_HOME'

button_sub_topic = 'home/daniel/BUTTON'
dht_sub_topic = 'home/daniel/DHT'
ldr_sub_topic = 'home/daniel/LDR'
global ON
ON = False

global STATE
STATE = 'OFF'

class Mqtt_client():
    
    def __init__(self):
        # broker IP adress:
        self.broker=''
        self.topic=''
        self.port='' 
        self.clientname=''
        self.username=''
        self.password=''        
        self.subscribeTopic=''
        self.publishTopic=''
        self.publishMessage=''
        self.on_connected_to_form = ''
        
    # Setters and getters
    def set_on_connected_to_form(self,on_connected_to_form):
        self.on_connected_to_form = on_connected_to_form
    def get_broker(self):
        return self.broker
    def set_broker(self,value):
        self.broker= value         
    def get_port(self):
        return self.port
    def set_port(self,value):
        self.port= value     
    def get_clientName(self):
        return self.clientName
    def set_clientName(self,value):
        self.clientName= value        
    def get_username(self):
        return self.username
    def set_username(self,value):
        self.username= value     
    def get_password(self):
        return self.password
    def set_password(self,value):
        self.password= value         
    def get_subscribeTopic(self):
        return self.subscribeTopic
    def set_subscribeTopic(self,value):
        self.subscribeTopic= value        
    def get_publishTopic(self):
        return self.publishTopic
    def set_publishTopic(self,value):
        self.publishTopic= value         
    def get_publishMessage(self):
        return self.publishMessage
    def set_publishMessage(self,value):
        self.publishMessage= value 
        
        
    def on_log(self, client, userdata, level, buf):
        print("log: "+buf)
            
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("connected OK")
            self.on_connected_to_form();            
        else:
            print("Bad connection Returned code=",rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("DisConnected result code "+str(rc))
            
    def on_message(self, client, userdata, msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message from:"+topic, m_decode)
        mainwin.connectionDock.update_btn_state(m_decode)

    def connect_to(self):
        # Init paho mqtt client class        
        self.client = mqtt.Client(self.clientname, clean_session=True) # create new client instance        
        self.client.on_connect=self.on_connect  #bind call back function
        self.client.on_disconnect=self.on_disconnect
        self.client.on_log=self.on_log
        self.client.on_message=self.on_message
        self.client.username_pw_set(self.username,self.password)        
        print("Connecting to broker ",self.broker)        
        self.client.connect(self.broker,self.port)     #connect to broker
    
    def disconnect_from(self):
        self.client.disconnect()                   
    
    def start_listening(self):        
        self.client.loop_start()        
    
    def stop_listening(self):        
        self.client.loop_stop()    
    
    def subscribe_to(self, topic):        
        self.client.subscribe(topic)
              
    def publish_to(self, topic, message):
        self.client.publish(topic,message)
        # Log the publish event
        logger.add_record(
            clientID=clientname,
            transmitter="RELAY",
            topic=topic,
            message=message
        )
      
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(broker_ip)
        
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(broker_port)
        
        self.eClientID=QLineEdit()
        global clientname
        self.eClientID.setText(clientname)
        
        self.eUserName=QLineEdit()
        self.eUserName.setText(username)
        
        self.ePassword=QLineEdit()
        self.ePassword.setEchoMode(QLineEdit.Password)
        self.ePassword.setText(password)
        
        self.eKeepAlive=QLineEdit()
        self.eKeepAlive.setValidator(QIntValidator())
        self.eKeepAlive.setText("60")
        
        self.eSSL=QCheckBox()
        
        self.eCleanSession=QCheckBox()
        self.eCleanSession.setChecked(True)
        
        self.eConnectbtn=QPushButton("Enable/Connect", self)
        self.eConnectbtn.setToolTip("click Me To Connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: gray; color: black")
        
        self.topicsList = QListWidget(self)
        self.topicsList.addItems([button_sub_topic, dht_sub_topic, ldr_sub_topic])
        self.topicsList.setMaximumHeight(100)

        self.ePushtbtn=QPushButton("", self)
        self.ePushtbtn.setToolTip("Do Not Push Me Please")
        self.ePushtbtn.setStyleSheet("background-color: red")

        formLayot=QFormLayout()
        formLayot.addRow("Turn On/Off",self.eConnectbtn)
        formLayot.addRow("Subscribed Topics", self.topicsList)
        formLayot.addRow("Status",self.ePushtbtn)

        widget = QWidget(self)
        widget.setLayout(formLayot)
        self.setTitleBarWidget(widget)
        self.setWidget(widget)     
        self.setWindowTitle("Connect") 
        
    def on_connected(self):
        self.eConnectbtn.setStyleSheet("background-color: green; color: white")
                    
    def on_button_connect_click(self):
        self.mc.set_broker(self.eHostInput.text())
        self.mc.set_port(int(self.ePort.text()))
        self.mc.set_clientName(self.eClientID.text())
        self.mc.set_username(self.eUserName.text())
        self.mc.set_password(self.ePassword.text())        
        self.mc.connect_to()        
        self.mc.start_listening()
        
        # Subscribe To All Topics In The List
        for index in range(self.topicsList.count()):
            topic = self.topicsList.item(index).text()
            self.mc.subscribe_to(topic)
            print(f"Subscribed to: {topic}")
    
    def update_btn_state(self,text):
        global STATE

        if ('DOUBLE CLICK' in text and STATE != 'AUTO TEMP ON') or ('Changed Temp' in text and STATE == 'AUTO TEMP ON'):
            self.ePushtbtn.setText("AUTO TEMP ON (Working...)")
            self.ePushtbtn.setStyleSheet("background-color: orange; color: black")
            STATE = 'AUTO TEMP ON'
            self.mc.publish_to(smart_home_topic,"TEMP MODE ON")
            self.mc.publish_to(relay_topic,STATE)
            return
        
        elif 'DOUBLE CLICK' in text and STATE == 'AUTO TEMP ON':
            self.ePushtbtn.setText("AUTO TEMP OFF")
            self.ePushtbtn.setStyleSheet("background-color: red; color: white")
            STATE = 'AUTO TEMP OFF'
            self.mc.publish_to(smart_home_topic,"TEMP MODE OFF")
            self.mc.publish_to(relay_topic,STATE)
            return




        if ('TRIPLE CLICK' in text and STATE != 'AUTO LIGHT ON') or ('Changed Light' in text and STATE == 'AUTO LIGHT ON'):
            self.ePushtbtn.setText("AUTO LIGHT ON (Working...)")
            self.ePushtbtn.setStyleSheet("background-color: blue; color: white")
            STATE = 'AUTO LIGHT ON'
            self.mc.publish_to(smart_home_topic,"LIGHT MODE ON")
            self.mc.publish_to(relay_topic,STATE)
            return
        
        elif 'TRIPLE CLICK' in text and STATE == 'AUTO LIGHT ON':
            self.ePushtbtn.setText("AUTO LIGHT OFF")
            self.ePushtbtn.setStyleSheet("background-color: red; color: white")
            STATE = 'AUTO LIGHT OFF'
            self.mc.publish_to(smart_home_topic,"LIGHT MODE OFF")
            self.mc.publish_to(relay_topic,STATE)
            return
        


             
        if 'SINGLE CLICK' in text and STATE != 'MANUAL CLOSE':
            self.ePushtbtn.setStyleSheet("background-color: yellow; color: black")
            self.ePushtbtn.setText("Manual CLOSE")
            STATE = 'MANUAL CLOSE'
            self.mc.publish_to(smart_home_topic,"Closing Down All Blinds")
            self.mc.publish_to(relay_topic,STATE)
            return

        elif 'SINGLE CLICK' in text and STATE == 'MANUAL CLOSE':  
            self.ePushtbtn.setStyleSheet("background-color: violet; color: black")
            self.ePushtbtn.setText("Manual OPEN")
            STATE = 'MANUAL OPEN'
            self.mc.publish_to(smart_home_topic,"Opening Up All Blinds")
            self.mc.publish_to(relay_topic,STATE)
            return
        

        if 'Optimal Light Level' in text:
            self.ePushtbtn.setStyleSheet("background-color: green; color: white")
            self.ePushtbtn.setText("Optimal Light Level")
            STATE = 'AUTO LIGHT ON'
            return
        
        if 'Optimal Temperature' in text:
            self.ePushtbtn.setStyleSheet("background-color: green; color: white")
            self.ePushtbtn.setText("Optimal Temperature")
            STATE = 'AUTO TEMP ON'
            return
        


                

           


    



          
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
                
        # Init of Mqtt_client class
        self.mc=Mqtt_client()
        
        # general GUI settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # set up main window
        self.setGeometry(30, 300, 300, 150)
        self.setWindowTitle('RELAY')        

        # Init QDockWidget objects        
        self.connectionDock = ConnectionDock(self.mc)        
        
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)       

app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()
