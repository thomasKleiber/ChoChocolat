from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import signal

import mesure
import commande

# description de la fenêtre dans laquelle il y a le graphique
cmd = commande.consigne()
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.setWindowTitle('Chaud Chocolat')
mw.resize(800,800)
cw = QtGui.QWidget()
mw.setCentralWidget(cw)
l = QtGui.QVBoxLayout()
cw.setLayout(l)
pw = pg.PlotWidget(name='Plot1')
l.addWidget(pw)                                      
pw.showGrid(x = True, y = True, alpha = 0.3)  
mw.show()
p1 = pw.plot()
p1.setPen((200,200,100))

    


# variables qui contiendront les data du graphique
xd=[]
yd=[]
t=0
cmd_ctr = 0

# fonction appelée périodiquement pour :
# - mesurer  chaque coup
# - puis une fois sur 5:
#   - met à jour la commande du relais
#   - met à jour le graphe
def updateData():
    global xd, yd, t, cmd, cmd_ctr
    mes = mesure.get()
    cmd_ctr += 1
    cmd_ctr %= 5
    if cmd_ctr == 0:
        cmd.run(t, mes)

        xd.append(t)
        yd.append(mes)
        p1.setData(y=yd, x=xd)
    t += timer_period_s

# timer = bout de code qui s'exécute périodiquement
timer_period_s = .05
timer = QtCore.QTimer()
timer.timeout.connect(updateData)
timer.start(timer_period_s * 1000)

def _interrupt_handler(signum, frame):
    QtGui.QApplication.quit()


signal.signal(signal.SIGINT, _interrupt_handler)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        try:
            QtGui.QApplication.instance().exec_()
        finally:
            print('quit!')
            timer.stop()
            cmd.clean()
            
