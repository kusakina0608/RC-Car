from hi_ui import *
from pymysql import *

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import socket
import numpy as np
import cv2
import gc

class VideoThread(QThread):
    mySignal = Signal(np.ndarray)
    def __init__(self):
        super().__init__()
        HOST = '192.168.0.14'
        PORT = 12345
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cs.connect((HOST, PORT))
    def run(self):
        while True:
            self.getImage()
            # sleep(0.1)
    def recvall(self, sock, count):
        self.buf = b''
        while count:
            self.newbuf = sock.recv(count)
            if not self.newbuf: return None
            self.buf += self.newbuf
            count -= len(self.newbuf)
        return self.buf
    def getImage(self):
        # gc.collect()
        self.cs.send('1'.encode())
        # self.mySignal.emit(cv2.imdecode(np.frombuffer(self.recvall(self.cs, int(self.recvall(self.cs, 16))), dtype='uint8'), 1))
        self.message = '1'
        self.cs.send(self.message.encode())
        self.length = self.recvall(self.cs, 16)
        self.stringData = self.recvall(self.cs, int(self.length))
        self.data = np.frombuffer(self.stringData, dtype='uint8')
        self.decimg = cv2.imdecode(self.data, 1)
        self.mySignal.emit(self.decimg)

class myApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        Ui_MainWindow.setupUi(self, self)
        try:
            self.db = connect(
                host='54.180.32.208',
                user='dev5_1',
                password='1234',
                db='dev5',
            )
            print("OK!")
        except:
            print("ERROR!")
            exit(1)

        self.cur = self.db.cursor()
        self.main()
    def main(self):
        # timer
        self.th = VideoThread()
        self.th.mySignal.connect(self.setImage)
        self.th.start()
        self.tm = QTimer()
        self.tm.setInterval(500)
        self.tm.timeout.connect(self.dispData)
        self.tm.start()
        self.is_night = False

        self.stopPixmap = QPixmap.fromImage(QImage(cv2.imread("no-stopping.png"), 251, 181, 3*251, QImage.Format_RGB888).rgbSwapped())
        pass
    def setImage(self, originalImg):
        h, w, c = originalImg.shape
        bpl = 3 * w
        originalQImg = QImage(originalImg.data, w, h, bpl, QImage.Format_RGB888).rgbSwapped()
        pix1 = QPixmap.fromImage(originalQImg)
        self.video_1.setPixmap(pix1)
        if not self.is_night:
            ########## Edge
            edgeImg = cv2.Canny(originalImg, 100, 200)
            edgeQImg = QImage(edgeImg, w, h, edgeImg.strides[0], QImage.Format_Grayscale8)
            pix2 = QPixmap(edgeQImg)
            self.video_2.setPixmap(pix2)
            self.video_3.setPixmap(self.stopPixmap)
        else:
            ########## histogram equalization
            hist, bins = np.histogram(originalImg.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_normalized = cdf * float(hist.max()) / cdf.max()
            cdf_m = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
            cdf = np.ma.filled(cdf_m, 0).astype('uint8')
            equalizedImg = cdf[originalImg]
            equalizedQImg = QImage(equalizedImg.data, w, h, bpl, QImage.Format_RGB888).rgbSwapped()
            pix3 = QPixmap.fromImage(equalizedQImg)
            self.video_2.setPixmap(self.stopPixmap)
            self.video_3.setPixmap(pix3)
    def dispData(self):
        self.cmd = "select * from command1 order by time desc"
        self.cur.execute(self.cmd)
        self.db.commit()
        res = ""
        self.data = self.cur.fetchall()
        for i in range(len(self.data)):
            res += "["
            res += self.data[i][0].strftime("%a %b %d %H:%M:%S %Y")
            res += "] "
            res += "\t%s\t" % self.data[i][1]
            res += "%8s\t" % self.data[i][2]
            res += "%8s\t" % str(self.data[i][3])
            res += '\n'
            pass
        self.text.setPlainText(res)
        pass
    def closeEvent(self, event):
        self.db.close()
        pass
    def sendCommand(self, cmd, arg):
        curTime = QDateTime().currentDateTime().toString('yyyy-MM-dd hh:mm:ss')
        self.cmd = "INSERT INTO `command1` (`time`, `cmd_string`, `arg_string`, `is_finish`) VALUES ('" + curTime + "', '" + cmd + "', '" + arg + "', '0')"
        self.cur.execute(self.cmd)
        self.db.commit()
    def clickedRight(self):
        print("pressedRight")
        self.sendCommand("right", "clicked")
        pass
    def clickedLeft(self):
        print("clickedLeft")
        self.sendCommand("left", "clicked")
        pass
    def clickedGo(self):
        print("clickedGo")
        self.sendCommand("go", "clicked")
        pass
    def clickedBack(self):
        print("clickedBack")
        self.sendCommand("back", "clicked")
        pass
    def clickedMid(self):
        print("clickedMid")
        self.sendCommand("mid", "clicked")
        pass
    def clickedStop(self):
        print("clickedStop")
        self.sendCommand("stop", "clicked")
        pass
    def clickedNight(self):
        self.is_night = not self.is_night



app = QApplication([])
win = myApp()
win.show()
app.exec_()