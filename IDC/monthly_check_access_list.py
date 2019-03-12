import pandas as pd
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QGridLayout, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

# core function to make excel file with result
def get_monthly_access_status(val):
    # read each 'actual list' and 'requested list'
    df = pd.read_excel(val + '_출입요청명단.xlsx', sheet_name='Sheet1')
    df2 = pd.read_excel(val + '_출입자명단.xlsx', sheet_name='Sheet1')

    allowed_access_cnt = df.shape[0]
    real_access_cnt = df2.shape[0]
    correct_access = 0
    noshow = []
    not_allowed = []

    # find no show list
    for name in df2['성명']:
        for comp in df['성명']:
            if comp == name:
                correct_access += 1
            if comp not in df2['성명'].values:
                if comp not in noshow:
                    noshow.append(comp)

    # find not allowed but accessed list
    for name in df2['성명']:
        if name not in df['성명'].values:
            not_allowed.append(name)

    # data for making not allowed access list
    df3 = df2.loc[df2['성명'] == not_allowed[0]]

    # data for summary sheet
    data = {
        "구분": ["출입 예정 인원", "실 출입 인원", "확인 완료 인원", "No-show 인원", "미허가 출입 인원"],
        "인원(명)": [allowed_access_cnt, real_access_cnt, correct_access, len(noshow), len(not_allowed)]
    }
    col = ["구분", "인원(명)"]
    df4 = pd.DataFrame(data, columns=col)

    # write new excel file with summary sheet
    with pd.ExcelWriter(val+'_출입자_현황.xlsx') as writer:
        df4.to_excel(writer, sheet_name='요약', index=False)
        df3.to_excel(writer, sheet_name='미허가_출입자', index=False)

class App(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = '출입자 현황 추출'
        self.left = 10
        self.top = 10
        self.width = 270
        self.height = 75
        self.initUI()
        centerp = QDesktopWidget().availableGeometry().center()
        self.move(centerp)
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        text_label = QLabel('연-월 입력 후 실행', self)
        text_label.move(20,0)

        self.textbox = QLineEdit(self)
        self.textbox.setPlaceholderText("2018-01")
        self.textbox.move(20, 25)
        self.textbox.resize(100, 25)

        self.button = QPushButton('실행', self)
        self.button.move(130, 25)

        self.button.clicked.connect(self.on_click)
        self.show()
 
    @pyqtSlot()
    def on_click(self):
        textboxValue = self.textbox.text()
        if textboxValue == "":
            QMessageBox.question(self, '출입자 현황 추출', "정확한 연/월을 입력하세요" + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        else:
            QMessageBox.question(self, '출입자 현황 추출', textboxValue + " 출입자 현황 추출을 실행합니다", QMessageBox.Ok, QMessageBox.Ok)
            get_monthly_access_status(textboxValue)
            QMessageBox.question(self, '출입자 현황 추출', textboxValue + " 출입자 현황 추출 완료", QMessageBox.Ok, QMessageBox.Ok)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
