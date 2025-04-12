# main.py
import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import LoraPrepper  # 여기서 정의된 클래스 사용

def main():
    app = QApplication(sys.argv)
    window = LoraPrepper()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
