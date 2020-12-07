import sys
sys.path.append('./Raspi-MotorHAT-python3')
from Raspi_MotorHAT import Raspi_MotorHAT, Raspi_DCMotor
from Raspi_PWM_Servo_Driver import PWM
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pymysql import *
from sense_hat import SenseHat
from time import sleep
import time
import atexit

class pollingThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Initialize Motor
        self.mh = Raspi_MotorHAT(addr=0x6f)
        self.myMotor = self.mh.getMotor(2)
        self.mySpeed = 100;
        self.myMotor.setSpeed(self.mySpeed)
        # Initialize Servo Motor
        self.pwm = PWM(0x6F)
        self.pwm.setPWMFreq(60)
        self.myAngle = 350;
        self.pwm.setPWM(0, 0, self.myAngle);
        # Try to connect database
        try:
            self.db = connect(
                host='54.180.32.208',
                user='dev5_1',
                password='1234',
                db='dev5',
            )
            print("Successfully connected to database(Polling)")
            self.cur = self.db.cursor()
        except:
            print("An error occurred while connecting to database(Polling)")
            exit(1)
        while True:
            time.sleep(0.1)
            self.getQuery()
        pass
    def getQuery(self):
        self.cmd = "select * from command1 where is_finish=0 order by time desc limit 1"
        self.cur.execute(self.cmd)
        self.db.commit()
        res = ""
        self.data = self.cur.fetchall()
        try:
            cmdTime = self.data[0][0]  # time
            cmdType = self.data[0][1]  # Type
            cmdArg = self.data[0][2]  # Arg
            cmdFinish = self.data[0][3]  # finish
            res = "[" + cmdTime.strftime("%Y-%m-%d, %H:%M:%S") + "] "
            res += "\t%s\t" % cmdType
            res += "%8s\t" % cmdArg
            res += "%8s\t" % str(cmdFinish)
            print(res)
            if cmdFinish == 0:
                print("[", cmdTime.strftime("%Y-%m-%d, %H:%M:%S"), "]")
                print(cmdType)
                print(cmdArg)
                self.cmd = "update command1 set is_finish=1 where is_finish=0"
                self.cur.execute(self.cmd)
                self.db.commit()
                if cmdArg == "clicked":
                    if cmdType == "mid": self.mid()
                    if cmdType == "stop": self.stop()
                    if cmdType == "go": self.go()
                    if cmdType == "back": self.back()
                    if cmdType == "left": self.left()
                    if cmdType == "right": self.right()
        except:
            pass
    def go(self):
        print("MOTOR GO")
        self.mySpeed += 40;
        if self.mySpeed > 250:
            self.mySpeed = 250
        self.myMotor.setSpeed(abs(self.mySpeed))
        if self.mySpeed > 0:
            self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        else:
            self.myMotor.run(Raspi_MotorHAT.FORWARD)
    def back(self):
        print("MOTOR BACK")
        self.mySpeed -= 40;
        if self.mySpeed < -250:
            self.mySpeed = -250
        self.myMotor.setSpeed(abs(self.mySpeed))
        if self.mySpeed > 0:
            self.myMotor.run(Raspi_MotorHAT.BACKWARD)
        else:
            self.myMotor.run(Raspi_MotorHAT.FORWARD)
    def left(self):
        print("MOTOR LEFT")
        self.myAngle -= 35
        if self.myAngle < 280:
            self.myAngle = 280
        self.pwm.setPWM(0, 0, self.myAngle)
    def right(self):
        print("MOTOR RIGHT")
        self.myAngle += 35
        if self.myAngle > 420:
            self.myAngle = 420
        self.pwm.setPWM(0, 0, self.myAngle)
    def mid(self):
        print("MOTOR MID")
        self.myAngle = 350
        self.pwm.setPWM(0, 0, self.myAngle)
    def stop(self):
        print("MOTOR STOP")
        self.mySpeed = 0;
        self.myMotor.setSpeed(abs(self.mySpeed))
        self.myMotor.run(Raspi_MotorHAT.RELEASE)


class sensingThread(QThread):
    def __init__(self):
        super().__init__()

    def run(self):
        # Get SenseHat
        self.sense = SenseHat()
        # Try to connect database
        try:
            self.db = connect(
                host='54.180.32.208',
                user='dev5_1',
                password='1234',
                db='dev5',
            )
            print("Successfully connected to database(Sensing)")
            self.cur = self.db.cursor()
        except:
            print("An error occurred while connecting to database(Sensing)")
            exit(1)
        while True:
            self.setQuery()
            time.sleep(1)
        pass
    def setQuery(self):
        pres = self.sense.get_pressure()
        temp = self.sense.get_temperature()
        humi = self.sense.get_humidity()

        p = round((pres-1000)/100, 3)
        t = round(temp/100, 3)
        h = round(humi/100, 3)
        m = str(p) + "|" + str(t) + "|" + str(h)
        msg = "Press: " + str(p) + " Temp: " + str(t) + " Humi: " + str(h)
        print(msg)
        self.cmd = "INSERT INTO `sensing1` (time, num1, num2, num3, meta_string, is_finish) VALUES ('"+ QDateTime().currentDateTime().toString('yyyy-MM-dd hh:mm:ss') +"', " + str(p) + ", " + str(t) + ", " + str(h) + ", '" + str(m) + "', 0)"
        print(self.cmd)
        self.cur.execute(self.cmd)
        self.db.commit()
        pass


th1 = pollingThread()
th2 = sensingThread()
th1.start()
th2.start()
# app = QApplication([])
while True:
    pass