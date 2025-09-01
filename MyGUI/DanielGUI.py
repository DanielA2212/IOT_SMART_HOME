import sys
import random
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
from DeInitialization import *

# Creating Client Name - Should Be Unique 
global clientname
r=random.randrange(1,100000)
clientname="IOT_Home_Client_ID_"+str(r)

class DetachableTabWidget(QTabWidget):
    """Custom QTabWidget With Drag-And-Drop Detachment Functionality"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMovable(True)
        self.setTabsClosable(True)
        self.tabBar().setAcceptDrops(True)
        self.detached_windows = []
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPos = event.pos()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if not hasattr(self, 'dragStartPos'):
            return
        if ((event.pos() - self.dragStartPos).manhattanLength() < 
            QApplication.startDragDistance()):
            return
        
        # Start Drag Operation
        drag = QDrag(self)
        mimeData = QMimeData()
        
        # Get The Tab Index At The Drag Start Position
        tab_index = self.tabBar().tabAt(self.dragStartPos)
        if tab_index >= 0:
            mimeData.setText(str(tab_index))
            drag.setMimeData(mimeData)
            
            # Create Drag Pixmap
            tab_rect = self.tabBar().tabRect(tab_index)
            pixmap = QPixmap(tab_rect.size())
            self.tabBar().render(pixmap, QPoint(), QRegion(tab_rect))
            drag.setPixmap(pixmap)
            
            # Execute Drag
            dropAction = drag.exec_(Qt.MoveAction | Qt.CopyAction)
            if dropAction == Qt.CopyAction:
                self.detach_tab(tab_index)
    
    def detach_tab(self, index):
        """Detach Tab To A New Window"""
        if self.count() <= 1:
            return  # Don't Detach The Last Tab
        
        # Get Tab Info
        widget = self.widget(index)
        tab_text = self.tabText(index)
        
        # Remove Tab From Current Widget
        self.removeTab(index)
        
        # Create Detached Window
        detached_window = DetachedTabWindow(widget, tab_text, self)
        detached_window.show()
        self.detached_windows.append(detached_window)
        
        # Connect Reattach Signal
        detached_window.tab_reattached.connect(self.reattach_tab)
        detached_window.window_closed.connect(self.remove_detached_window)
    
    def reattach_tab(self, widget, title):
        """Reattach A Tab From A Detached Window"""
        self.addTab(widget, title)
        self.setCurrentWidget(widget)
    
    def remove_detached_window(self, window):
        """Remove Reference To Closed Detached Window"""
        if window in self.detached_windows:
            self.detached_windows.remove(window)

class DetachedTabWindow(QMainWindow):
    """Window For Detached Tabs"""
    tab_reattached = pyqtSignal(QWidget, str)
    window_closed = pyqtSignal(QMainWindow)
    
    def __init__(self, widget, title, parent_tab_widget):
        super().__init__()
        self.widget = widget
        self.title = title
        self.parent_tab_widget = parent_tab_widget
        
        self.setWindowTitle(f"MQTT - {title}")
        self.setGeometry(100, 100, 600, 500)
        
        # Create Central Widget And Layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        
        # Add Reattach Button
        reattach_button = QPushButton("⮌ Reattach to Main Window")
        reattach_button.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 8px;")
        reattach_button.clicked.connect(self.reattach_tab)
        
        layout.addWidget(reattach_button)
        layout.addWidget(widget)
        
        self.setCentralWidget(central_widget)
        
        # Make Window Accept Drops For Reattachment
        self.setAcceptDrops(True)
    
    def reattach_tab(self):
        """Reattach This Tab To The Main Window"""
        # Remove Widget From This Window
        self.centralWidget().layout().removeWidget(self.widget)
        
        # Signal Parent To Reattach
        self.tab_reattached.emit(self.widget, self.title)
        
        # Close This Window
        self.close()
    
    def closeEvent(self, event):
        """Handle Window Close Event"""
        self.window_closed.emit(self)
        super().closeEvent(event)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()
    
    def dropEvent(self, event):
        # This Would Handle Dropping Tabs From Other Windows
        event.accept()

class Mqtt_client():
    
    def __init__(self):
        # Broker IP Address:
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
        self.client = None  # Initialize Client As None
        
    # Setters And Getters
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
        print("Log: "+buf)
            
    def on_connect(self, client, userdata, flags, rc):
        if rc==0:
            print("Connected OK")
            self.on_connected_to_form();            
        else:
            print("Bad Connection. Returned Code= ",rc)
            
    def on_disconnect(self, client, userdata, flags, rc=0):
        print("Disconnected. Result Code= "+str(rc))
            
    def on_message(self, client, userdata, msg):
        topic=msg.topic
        m_decode=str(msg.payload.decode("utf-8","ignore"))
        print("message from:"+topic, m_decode)
        # Update All Subscribe Tabs (Both Attached And Detached)
        mainwin.update_all_subscribe_tabs(topic, m_decode)

    def connect_to(self):
        # Init Paho Mqtt Client Class        
        self.client = mqtt.Client(self.clientname, clean_session=True) # Create New Client Instance        
        self.client.on_connect=self.on_connect # Bind Call Back Function
        self.client.on_disconnect=self.on_disconnect
        self.client.on_log=self.on_log
        self.client.on_message=self.on_message
        self.client.username_pw_set(self.username,self.password)        
        print("Connecting To Broker: ",self.broker)        
        self.client.connect(self.broker,self.port) # Connect To Broker
    
    def disconnect_from(self):
        self.client.disconnect()                   
    
    def start_listening(self):        
        self.client.loop_start()        
    
    def stop_listening(self):        
        self.client.loop_stop()    
    
    def subscribe_to(self, topic):
        if hasattr(self, 'client') and self.client:
            self.client.subscribe(topic)
        else:
            print("Error: Not connected to MQTT broker. Please connect first.")
            return False
        return True

    def unsubscribe_from(self, topic):
        if hasattr(self, 'client') and self.client:
            self.client.unsubscribe(topic)
        else:
            print("Error: Not connected to MQTT broker.")
            return False
        return True
              
    def publish_to(self, topic, message):
        if hasattr(self, 'client') and self.client:
            self.client.publish(topic,message)
        else:
            print("Error: Not connected to MQTT broker. Please connect first.")
            return False
        return True        
      
class ConnectionDock(QDockWidget):
    """Main """
    def __init__(self,mc):
        QDockWidget.__init__(self)
        
        self.mc = mc
        self.mc.set_on_connected_to_form(self.on_connected)
        self.eHostInput=QLineEdit()
        self.eHostInput.setInputMask('999.999.999.999')
        self.eHostInput.setText(brockerIp)
        
        self.ePort=QLineEdit()
        self.ePort.setValidator(QIntValidator())
        self.ePort.setMaxLength(4)
        self.ePort.setText(brockerPort)
        
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
        
        self.eConnectbtn=QPushButton("Connect", self)
        self.eConnectbtn.setToolTip("Click Me To Connect")
        self.eConnectbtn.clicked.connect(self.on_button_connect_click)
        self.eConnectbtn.setStyleSheet("background-color: #333749; color: white")
        
        formLayot=QFormLayout()
        formLayot.addRow("Host",self.eHostInput )
        formLayot.addRow("Port",self.ePort )
        formLayot.addRow("Client ID", self.eClientID)
        formLayot.addRow("User Name",self.eUserName )
        formLayot.addRow("Password",self.ePassword )
        formLayot.addRow("Keep Alive",self.eKeepAlive )
        formLayot.addRow("SSL",self.eSSL )
        formLayot.addRow("Clean Session",self.eCleanSession )
        formLayot.addRow("",self.eConnectbtn)

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

class PublishTab(QWidget):
    """Single Publisher Tab"""
    def __init__(self, mc, tab_widget, tab_index):
        super().__init__()
        self.mc = mc
        self.tab_widget = tab_widget
        self.tab_index = tab_index
                
        self.ePublisherTopic=QLineEdit()
        self.ePublisherTopic.setPlaceholderText("Enter A Topic To Publish To")

        self.eQOS=QComboBox()
        self.eQOS.addItems(["0","1","2"])

        self.eRetainCheckbox = QCheckBox()

        self.eMessageBox=QPlainTextEdit("Test 123")
        self.ePublishButton = QPushButton("Publish",self)
        self.ePublishButton.setStyleSheet("background-color: #333749; color: white")
        
        # Close Tab Button
        self.eCloseButton = QPushButton("Close Tab",self)
        self.eCloseButton.setStyleSheet("background-color: #e04646; color: white")
        self.eCloseButton.clicked.connect(self.close_tab)

        formLayot=QFormLayout()        
        formLayot.addRow("Topic",self.ePublisherTopic)
        formLayot.addRow("QOS",self.eQOS)
        formLayot.addRow("Retain",self.eRetainCheckbox)
        formLayot.addRow("Message",self.eMessageBox)
        formLayot.addRow("",self.ePublishButton)
        formLayot.addRow("",self.eCloseButton)
        
        self.ePublishButton.clicked.connect(self.on_button_publish_click)
        
        self.setLayout(formLayot)
       
    def on_button_publish_click(self):
        topic = self.ePublisherTopic.text().strip()
        message = self.eMessageBox.toPlainText()
        
        if not topic:
            QMessageBox.warning(self, "Warning", "Please Enter A Topic To Publish To.")
            return
            
        # Try To Publish, Show Error If Not Connected
        if not self.mc.publish_to(topic, message):
            QMessageBox.critical(self, "Connection Error", 
                               "Not Connected To MQTT Broker. Please Connect First.")
            return
            
        self.ePublishButton.setStyleSheet("background-color: cyan; color: black")
        self.ePublishButton.setText("Published!!")
        QTimer.singleShot(4000, lambda: self.ePublishButton.setStyleSheet("background-color: #333749; color: white"))
        QTimer.singleShot(4000, lambda: self.ePublishButton.setText("Publish"))
    
    def close_tab(self):
        # Find The Current Index Of This Tab In The Tab Widget
        if isinstance(self.tab_widget, DetachableTabWidget):
            for i in range(self.tab_widget.count()):
                if self.tab_widget.widget(i) == self:
                    self.tab_widget.removeTab(i)
                    break

class SubscribeTab(QWidget):
    """Single Subscribe Tab"""
    def __init__(self, mc, tab_widget, tab_index):
        super().__init__()   
        self.mc = mc
        self.tab_widget = tab_widget
        self.tab_index = tab_index
        self.subscribed_topic = None
        
        self.eSubscribeTopic=QLineEdit()
        self.eSubscribeTopic.setPlaceholderText("Enter A Topic To Subscribe To")
        
        self.eQOS = QComboBox()
        self.eQOS.addItems(["0","1","2"])
        
        self.eRecMess=QTextEdit()

        self.eSubscribeButton = QPushButton("Subscribe", self)
        self.eSubscribeButton.setStyleSheet("background-color: #333749; color: white")
        self.eSubscribeButton.clicked.connect(self.swap_button)
        
        # Close Tab Button
        self.eCloseButton = QPushButton("Close Tab",self)
        self.eCloseButton.setStyleSheet("background-color: #e04646; color: white")
        self.eCloseButton.clicked.connect(self.close_tab)

        self.formLayot=QFormLayout()       
        self.formLayot.addRow("Topic",self.eSubscribeTopic)
        self.formLayot.addRow("QOS",self.eQOS)
        self.formLayot.addRow("Received",self.eRecMess)
        self.formLayot.addRow("",self.eSubscribeButton)
        self.formLayot.addRow("",self.eCloseButton)
                
        self.setLayout(self.formLayot)

    def swap_button(self):
        topic = self.eSubscribeTopic.text().strip()
        if not topic:
            QMessageBox.warning(self, "Warning", "Please Enter A Topic To Subscribe To.")
            return
            
        print(topic)
        self.subscribed_topic = topic
        
        # Try To Subscribe, Show Error If Not Connected
        if not self.mc.subscribe_to(self.subscribed_topic):
            QMessageBox.critical(self, "Connection Error", 
                               "Not Connected To MQTT Broker. Please Connect First.")
            self.subscribed_topic = None
            return

        # Remove The Subscribe Button
        self.formLayot.removeWidget(self.eSubscribeButton)
        self.eSubscribeButton.deleteLater()

        # Create The Unsubscribe Button
        self.eUnSubscribeButton = QPushButton("UnSubscribe", self)
        self.eUnSubscribeButton.setStyleSheet("background-color: cyan; color: black")
        self.eUnSubscribeButton.clicked.connect(self.swap_back)
        
        # Insert At The Correct Position (Row 3, Which Is After Received Field)
        self.formLayot.insertRow(3, "", self.eUnSubscribeButton)

    def swap_back(self):
        print("Unsubscribing from:", self.eSubscribeTopic.text())
        if self.subscribed_topic:
            self.mc.unsubscribe_from(self.subscribed_topic)
            self.subscribed_topic = None
        self.eRecMess.clear()

        # Remove Unsubscribe Button
        self.formLayot.removeWidget(self.eUnSubscribeButton)
        self.eUnSubscribeButton.deleteLater()

        # Recreate Subscribe Button At The Correct Position (Row 3)
        self.eSubscribeButton = QPushButton("Subscribe", self)
        self.eSubscribeButton.clicked.connect(self.swap_button)
        self.eSubscribeButton.setStyleSheet("background-color: #333749; color: white")
        self.formLayot.insertRow(3, "", self.eSubscribeButton)

    def update_mess_win(self, topic, text):
        # Only Update If This Tab Is Subscribed To The Topic
        if self.subscribed_topic and topic == self.subscribed_topic:
            self.eRecMess.append(f"[{topic}]: {text}")
    
    def close_tab(self):
        # Unsubscribe If Subscribed Before Closing
        if self.subscribed_topic:
            self.mc.unsubscribe_from(self.subscribed_topic)
        # Find The Current Index Of This Tab In The Tab Widget
        if isinstance(self.tab_widget, DetachableTabWidget):
            for i in range(self.tab_widget.count()):
                if self.tab_widget.widget(i) == self:
                    self.tab_widget.removeTab(i)
                    break

class PublishDock(QDockWidget):
    """Publisher With Tabs - Scan-Based Tab Numbering"""
    def __init__(self, mc):
        QDockWidget.__init__(self)
        self.mc = mc
        
        # Create Main Widget And Layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # Create Header With Title And Add Button
        header_layout = QHBoxLayout()
        title_label = QLabel("Publish")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.add_tab_button = QPushButton("+ New Publisher")
        self.add_tab_button.setStyleSheet("background-color: #4CAF50; color: black; font-size: 12px; font-weight: bold; padding: 5px;")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_tab_button)
        
        # Create Detachable Tab Widget
        self.tab_widget = DetachableTabWidget()
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Add First Tab
        self.add_new_tab()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.tab_widget)
        
        self.setWidget(main_widget)
        self.setWindowTitle("Publish")
    
    def get_tab_number_from_name(self, tab_name):
        """Extract Number From Tab Name Like 'Publish 3' -> 3"""
        try:
            return int(tab_name.split()[-1])
        except:
            return 0
    
    def get_highest_tab_number(self):
        """Scan All Current Tabs (Attached + Detached) And Find The Highest Number"""
        highest_number = 0
        
        # Check attached tabs in the main tab widget
        for i in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(i)
            tab_number = self.get_tab_number_from_name(tab_name)
            highest_number = max(highest_number, tab_number)
        
        # Check detached tabs
        for detached_window in self.tab_widget.detached_windows:
            # Extract number from window title (format: "MQTT - Publish X")
            window_title = detached_window.windowTitle()
            if " - " in window_title:
                tab_title = window_title.split(" - ")[1]  # Get "Publish X"
                tab_number = self.get_tab_number_from_name(tab_title)
                highest_number = max(highest_number, tab_number)
        
        return highest_number
    
    def add_new_tab(self):
        # Scan all current tabs and get the next number
        next_tab_number = self.get_highest_tab_number() + 1
        
        new_tab = PublishTab(self.mc, self.tab_widget, self.tab_widget.count())
        new_tab.tab_number = next_tab_number
        tab_name = f"Publish {next_tab_number}"
        self.tab_widget.addTab(new_tab, tab_name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:  # Keep At Least One Tab
            self.tab_widget.removeTab(index)

class SubscribeDock(QDockWidget):
    """Subscribe With Tabs - Scan-Based Tab Numbering"""
    def __init__(self, mc):
        QDockWidget.__init__(self)   
        self.mc = mc
        
        # Create Main Widget And Layout
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        
        # Create Header With Title And Add Button
        header_layout = QHBoxLayout()
        title_label = QLabel("Subscribe")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.add_tab_button = QPushButton("+ New Subscriber")
        self.add_tab_button.setStyleSheet("background-color: #4CAF50; color: black; font-size: 12px; font-weight: bold; padding: 5px;")
        self.add_tab_button.clicked.connect(self.add_new_tab)
        
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.add_tab_button)
        
        # Create Detachable Tab Widget
        self.tab_widget = DetachableTabWidget()
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        
        # Add First Tab
        self.add_new_tab()
        
        layout.addLayout(header_layout)
        layout.addWidget(self.tab_widget)
        
        self.setWidget(main_widget)
        self.setWindowTitle("Subscribe")
    
    def get_tab_number_from_name(self, tab_name):
        """Extract Number From Tab Name Like 'Subscribe 3' -> 3"""
        try:
            return int(tab_name.split()[-1])
        except:
            return 0
    
    def get_highest_tab_number(self):
        """Scan All Current Tabs (Attached + Detached) And Find The Highest Number"""
        highest_number = 0
        
        # Check attached tabs in the main tab widget
        for i in range(self.tab_widget.count()):
            tab_name = self.tab_widget.tabText(i)
            tab_number = self.get_tab_number_from_name(tab_name)
            highest_number = max(highest_number, tab_number)
        
        # Check detached tabs
        for detached_window in self.tab_widget.detached_windows:
            # Extract number from window title (format: "MQTT - Subscribe X")
            window_title = detached_window.windowTitle()
            if " - " in window_title:
                tab_title = window_title.split(" - ")[1]  # Get "Subscribe X"
                tab_number = self.get_tab_number_from_name(tab_title)
                highest_number = max(highest_number, tab_number)
        
        return highest_number
    
    def add_new_tab(self):
        # Scan all current tabs and get the next number
        next_tab_number = self.get_highest_tab_number() + 1
        
        new_tab = SubscribeTab(self.mc, self.tab_widget, self.tab_widget.count())
        new_tab.tab_number = next_tab_number
        tab_name = f"Subscribe {next_tab_number}"
        self.tab_widget.addTab(new_tab, tab_name)
        self.tab_widget.setCurrentIndex(self.tab_widget.count() - 1)
    
    def close_tab(self, index):
        if self.tab_widget.count() > 1:  # Keep At Least One Tab
            # Unsubscribe If Subscribed
            widget = self.tab_widget.widget(index)
            if hasattr(widget, 'subscribed_topic') and widget.subscribed_topic:
                self.mc.unsubscribe_from(widget.subscribed_topic)
            
            self.tab_widget.removeTab(index)
    
    def update_all_tabs(self, topic, message):
        """Update All Subscribe Tabs With New Messages (Both Attached And Detached)"""
        # Update Attached Tabs
        for i in range(self.tab_widget.count()):
            tab = self.tab_widget.widget(i)
            if isinstance(tab, SubscribeTab):
                tab.update_mess_win(topic, message)
        
        # Update Detached Tabs
        for detached_window in self.tab_widget.detached_windows:
            widget = detached_window.widget
            if isinstance(widget, SubscribeTab):
                widget.update_mess_win(topic, message)
        
class MainWindow(QMainWindow):
    
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
                
        # Init Of Mqtt_client Class
        self.mc=Mqtt_client()
        
        # General GUI Settings
        self.setUnifiedTitleAndToolBarOnMac(True)

        # Set Up Main Window
        self.setGeometry(30, 100, 1000, 700)
        self.setWindowTitle('The Best MQTT GUI')        

        # Init QDockWidget Objects        
        self.connectionDock = ConnectionDock(self.mc)        
        self.publishDock = PublishDock(self.mc)
        self.subscribeDock = SubscribeDock(self.mc)
        
        self.addDockWidget(Qt.TopDockWidgetArea, self.connectionDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.subscribeDock)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.publishDock)
    
    def update_all_subscribe_tabs(self, topic, message):
        """Update All Subscribe Tabs With New Messages (Both Attached And Detached)"""
        self.subscribeDock.update_all_tabs(topic, message)
        
        # Also Update Any Detached Publish Tabs (In Case They Have Subscription Functionality)
        for detached_window in self.publishDock.tab_widget.detached_windows:
            widget = detached_window.widget
            if hasattr(widget, 'update_mess_win'):
                widget.update_mess_win(topic, message)


app = QApplication(sys.argv)
mainwin = MainWindow()
mainwin.show()
app.exec_()