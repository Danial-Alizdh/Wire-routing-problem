from PyQt5 import QtCore, QtGui, sip
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QHBoxLayout,
                            QMainWindow, QTableView, QDockWidget, QFormLayout, 
                            QWidget, QCheckBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys

class SingleLinkedList :

    class SingleLinkedListNode :
        def __init__(self, data = 0.0, next = None) :
            self.data = data
            self._next = next

    def __init__(self) :
        self.head = None
        self._size = 0

    def __len__(self) :
        return self._size
    
    def is_empty(self) :
        return self._size == 0

    def Add2First(self, inp):
        if type(self.head) == type(inp):
            inp._next = self.head
            self.head = inp
        else:
            self.head = self.SingleLinkedListNode(inp, self.head )
            self._size += 1
        return self.head

    def Add2End (self, inp):
        if type(self.head) != type(inp):
            new_node= self.SingleLinkedListNode(inp, None)
        else:
            new_node=inp
            new_node._next = None
        if self._size == 0:
            self.head = new_node
        else:
            before_node = self.head
            while before_node._next != None:
                before_node = before_node._next
            before_node._next=new_node
        
        self._size += 1
        
        return self.head    

    def RemoveFirstNode(self) :
        if self._size == 0 :
            return 0, None
        else :
            tmp = self.head
            self.head = self.head._next
            self._size -= 1
            return 1, tmp

    def RemoveLastNode(self) :
        if self._size == 0 :
            return 0, None
        elif self._size == 1 :
            flag, delete_node = self.RemoveFirstNode()
        else :
            before_node = self.head
            while before_node._next._next != None :
                before_node = before_node._next
            delete_node = before_node._next
            before_node._next = None
            flag = 1
            self._size -= 1

        return flag, delete_node

    def Show(self):
        tmp = self.head
        while tmp != None:
            print(tmp.data,end='-->')
            tmp = tmp._next

    def ShowFirst(self) :
        return self.head.data

    def ShowEnd(self) :
        tmp = self.head
        while tmp._next != None :
            tmp = tmp._next
        return tmp.data

    def inList(self, value) :
        tmp = self.head
        while tmp != None :
            if tmp.data == value :
                return True
            tmp = tmp._next
        return False

class Stack :
    def __init__(self) :
        self.list = SingleLinkedList()

    def push(self, data) :
        self.list.Add2First(data)

    def pop(self) :
        flag, tmp = self.list.RemoveFirstNode()
        return tmp.data

    def peak(self) :
        return self.list.ShowFirst()

    def size(self) :
        return self.list._size

class ListQueue :
    def __init__(self) :
        self.list = SingleLinkedList()
        self.backup = []

    def enQueue(self, data) :
        self.list.Add2First(data)
        self.backup.append(data)
    
    def deQueue(self) :
        flag, tmp = self.list.RemoveLastNode()
        return tmp.data

    def size(self) :
        return self.list._size

    def inQueue(self, p) :
        for c in self.backup :
            if (c.x == p.x) and (c.y == p.y):
                return True
        return False

class ArrayQueue :
    def __init__(self, n = 10) :
        self.backup = []
        self.n = n
        self.array = [0] * n
        self.front = - 1
        self.rear = - 1
        
    def enQueue(self, item):
        if self.rear == self.n - 1:
            return
        else:
            if self.front == -1 and self.rear == -1:
                self.front = 0
                self.rear = 0
            else:
                self.rear += 1
            self.array[self.rear] = item
            self.backup.append(item)

    def deQueue(self):
        if self.front == -1 or self.front > self.rear:
            return
        else:
            item = self.array[self.front]
            if self.rear == self.front:
                self.rear = -1
                self.front = -1

            self.front += 1
            return item

    def size(self) :
        return len(self.array)

    def inQueue(self, p) :
        for c in self.backup :
            if (c.x == p.x) and (c.y == p.y):
                return True
        return False

class TableModel(QtCore.QAbstractTableModel):
    COLORS = ['#ffffff', '#eb2626', '#32d627', '#2671eb'] #W, R, G, B

    def __init__(self, data, a, b):
        super(TableModel, self).__init__()
        self._data = data
        self.a = a
        self.b = b
        self._editable = False

    def data(self, index, role):
        try :
            if role == Qt.DisplayRole or role == Qt.EditRole:
                value = self._data[index.row()][index.column()]

                if isinstance(value, float):
                    return "%.2f" % value

                if isinstance(value, str):
                    return '"%s"' % value

                return value

            if role == Qt.BackgroundRole:
                value = self._data[index.row()][index.column()]

                if ((index.row() == self.a.y and index.column() == self.a.x)):
                    return QtGui.QColor(self.COLORS[2])

                elif ((index.row() == self.b.y and index.column() == self.b.x)):
                    return QtGui.QColor(self.COLORS[1])

                elif ((isinstance(value, int) or isinstance(value, float)) and value == -1):
                    return QtGui.QColor(self.COLORS[3])                

                elif (isinstance(value, int) or isinstance(value, float)):
                    return QtGui.QColor(self.COLORS[0])

            if role == Qt.TextAlignmentRole:
                value = self._data[index.row()][index.column()]

                if isinstance(value, int) or isinstance(value, float):
                    return Qt.AlignVCenter + Qt.AlignRight

            if role == Qt.ForegroundRole:
                value = self._data[index.row()][index.column()]

                if ( (isinstance(value, int) or isinstance(value, float)) and ( (value == -1) or (index.row() == self.a.y and index.column() == self.a.x) or index.row() == self.b.y and index.column() == self.b.x) ):
                    return QtGui.QColor('white')
        
        except :
            pass

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            return True
        return False

    def flags(self, index):
        flags = super().flags(index)
        if self._editable:
            flags = Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
        return flags

    def rowCount(self, index):
        if self._data != None:
            return len(self._data)
        return 0

    def columnCount(self, index):
        if self._data != None:
            return len(self._data[0])
        return 0
    
    def setEditable(self, editable):
        self._editable = editable

class Point :
    def __init__(self, x, y, value) :
        self.x = x
        self.y = y
        self.value = value

    def print(self):
        return "X: " + str(self.x + 1) + "\tY: " + str(self.y + 1) + "\tValue: " + str(self.value) + "\n"

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.a = None
        self.b = None
        self.result = None

        self.setWindowTitle('Find Path')
        self.setWindowIcon(QIcon('./Images/logo.png'))
        # self.setGeometry(100, 100, 1100, 300)

        #Table
        self.updateTable()

        #create dok
        self.dock = QDockWidget('Buttons')
        self.dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        # create form
        self.form = QWidget()
        self.layout = QFormLayout(self.form)
        self.form.setLayout(self.layout)

        #add btn
        read_file_btn = QPushButton('Read from file')
        read_file_btn.clicked.connect(self.read_file)
        self.layout.addRow(read_file_btn)

        load_btn = QPushButton('Load')
        load_btn.clicked.connect(self.load_matrix)
        self.layout.addRow(load_btn)

        save_btn = QPushButton('Save matrix')
        save_btn.clicked.connect(self.save_matrix)
        self.layout.addRow(save_btn)

        run_btn = QPushButton('Run')
        run_btn.clicked.connect(self.run)
        self.layout.addRow(run_btn)

        show_btn = QPushButton('Show result')
        show_btn.clicked.connect(self.showResult)
        self.layout.addRow(show_btn)

        edit_table_check = QCheckBox("Edit table")
        edit_table_check.setChecked(False)
        edit_table_check.stateChanged.connect(self.editTable)
        self.layout.addRow(edit_table_check)

        self.create_table_check = QCheckBox("Create table")
        self.create_table_check.setChecked(False)
        self.create_table_check.stateChanged.connect(self.createTable)
        self.layout.addRow(self.create_table_check)

        self.dock.setWidget(self.form)

    def updateTable(self):
        if self.data != None :
            width = len(self.data[0]) * 120
            height = len(self.data) * 37
        else :
            width = 1100
            height = 300
        self.setGeometry(100, 100, int(width), int(height))
        self.table = QTableView(self)
        self.model = TableModel(self.data, self.a, self.b)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

    def show_popup(self, title, text, details):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(text)
        if details != None :
            msg.setDetailedText(details)
        msg.exec_()

    def read_file(self) :
        self.data = []
        with open(r'./data/matrix.txt', 'r') as rf:
            lines = rf.read().splitlines()
            lineA = lines[0]
            values = lineA.split(", ")
            self.a = Point(int(values[0]), int(values[1]), int(values[2]))
            lineB = lines[1]
            values = lineB.split(", ")
            self.b = Point(int(values[0]), int(values[1]), int(values[2]))
            for i in range(2, len(lines)):
                line = lines[i]
                d = []
                values = line.split(", ")
                for value in values:
                    d.append(int(value))
                self.data.append(d)

        rf.close()
        self.updateTable()

    def editTable(self) :
        self.model.setEditable(not self.model._editable)

    def createGetPositions(self) :
        labelX = QLabel("row")
        x = QLineEdit()
        x.setFixedWidth(50)

        labelY = QLabel("col")
        y = QLineEdit()
        y.setFixedWidth(50)

        hBox = QHBoxLayout()
        hBox.addWidget(labelX)
        hBox.addWidget(x)
        hBox.addWidget(labelY)
        hBox.addWidget(y)

        return [x, y, hBox]

    def deleteLayout(self, cur_lay):        
        if cur_lay is not None:
            count = cur_lay.count()
            if cur_lay == self.layout :
                x = 7
            else :
                x = count
            for i in range(x) :
                item = cur_lay.itemAt(count - i - 1)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
                    sip.delete(item.layout())

    def createTable(self, checked) :
        if checked == QtCore.Qt.Checked:
            self.Mx, self.My, hbox = self.createGetPositions()
            self.layout.addRow(QLabel("M-size"), hbox)
            self.Ax, self.Ay, hbox = self.createGetPositions()
            self.layout.addRow(QLabel("a"), hbox)
            self.Bx, self.By, hbox = self.createGetPositions()
            self.layout.addRow(QLabel("b"), hbox)
            btn = QPushButton('Submit')
            btn.clicked.connect(self.setTableInfo)
            btn.setFixedWidth(60)
            self.layout.addRow(btn)
        else:
            self.deleteLayout(self.layout)

    def setTableInfo(self) :
        data = []
        for i in range(int(self.Mx.text())):
            d = [0] * int(self.My.text())
            data.append(d)

        self.data = data
        self.a = Point(int(self.Ax.text()), int(self.Ay.text()), 0)
        self.b = Point(int(self.Bx.text()), int(self.By.text()), 0)

        self.updateTable()
        self.create_table_check.setChecked(False)

    def load_matrix(self) :
        self.data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, -1, -1, -1, -1, 0, 0],
            [0, -1, -1, -1, -1, 0, 0, 0, -1],
            [0, 0, 0, 0, -1, 0, -1, 0, 0],
            [0, -1, 0, -1, -1, 0, 0, -1, 0],
            [0, 0, -1, 0, 0, 0, 0, 0, 0],
            [-1, 0, 0, 0, 0, -1, 0, -1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        self.a = Point(1, 1, 0)
        self.b = Point(5, 4, 0)
        self.updateTable()

    def save_matrix(self) :
        with open('./data/saved_matrix.txt','w') as wf:
            wf.write(str(self.a.x) + ", " + str(self.a.y) + ", " + str(self.a.value) + "\n")
            wf.write(str(self.b.x) + ", " + str(self.b.y) + ", " + str(self.b.value) + "\n")
            for row in self.data:
                for i in range(len(row) - 1):
                    wf.write(str(row[i]) + ", ")
                wf.write(str(row[i+1]) + "\n")

        wf.close()

    def samePosition(self, x, y) :
        if (x.x == y.x) and (x.y == y.y) :
            return True
        return False

    def run(self) :
        maxX = len(self.data[0])
        maxY = len(self.data)
        # q = ListQueue()
        q = ArrayQueue(len(self.data[0]) * len(self.data))
        q.enQueue(self.a)
        while True :
            p = q.deQueue()

            if self.samePosition(p, self.b):
                self.b.value = p.value
                break

            if  (p.x + 1 < maxX): #Right
                c = Point(p.x+1, p.y, self.data[p.y][p.x+1])
                if (c.value != -1) and (not q.inQueue(c)):
                    c.value = p.value + 1
                    q.enQueue(c)
                    self.data[p.y][p.x+1] = p.value + 1

            if (p.y - 1 >= 0): #Up
                c = Point(p.x, p.y-1, self.data[p.y-1][p.x])
                if (c.value != -1) and (not q.inQueue(c)):
                    c.value = p.value + 1
                    q.enQueue(c)
                    self.data[p.y-1][p.x] = p.value + 1

            if (p.y + 1 < maxY): #Down
                c = Point(p.x, p.y+1, self.data[p.y+1][p.x])
                if (c.value != -1) and (not q.inQueue(c)):
                    c.value = p.value + 1
                    q.enQueue(c)
                    self.data[p.y+1][p.x] = p.value + 1

            if (p.x - 1 >= 0): #Left
                c = Point(p.x-1, p.y, self.data[p.y][p.x-1])
                if (c.value != -1) and (not q.inQueue(c)):
                    c.value = p.value + 1
                    q.enQueue(c)
                    self.data[p.y][p.x-1] = p.value + 1
        
        s = Stack()
        s.push(self.b)
        while True :
            p = s.peak()

            if self.samePosition(p, self.a):
                break

            if (p.x + 1 < maxX): #Right
                c = Point(p.x+1, p.y, self.data[p.y][p.x+1])
                if (c.value != -1) and (c.value == p.value - 1):
                    s.push(c)

            if (p.y - 1 >= 0): #Up
                c = Point(p.x, p.y-1, self.data[p.y-1][p.x])
                if (c.value != -1) and (c.value == p.value - 1):
                    s.push(c)

            if (p.y + 1 < maxY): #Down
                c = Point(p.x, p.y+1, self.data[p.y+1][p.x])
                if (c.value != -1) and (c.value == p.value - 1):
                    s.push(c)

            if (p.x - 1 >= 0): #Left
                c = Point(p.x-1, p.y, self.data[p.y][p.x-1])
                if (c.value != -1) and (c.value == p.value - 1):
                    s.push(c)

        self.setResult(s)

        self.show_popup("Successfully", "Done", None)

    def showResult(self) :        
        self.show_popup("Show Result", "Click \"Show Details...\" button to see path", self.result)

    def setResult(self, s) :
        self.result = ""
        for i in range(s.size()) :
            self.result += s.pop().print()

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec_()