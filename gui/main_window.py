# gui/main_window.py
from PyQt5.QtWidgets import QMainWindow, QTabWidget
from .tab1_convert import Tab1Convert
from .tab2_tag_editor import Tab2TagEditor
from .tab3_augment import Tab3Augment

class LoraPrepper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoRA Prepper")
        self.setGeometry(100, 100, 1000, 700)

        self.tabs = QTabWidget()
        self.tab1 = Tab1Convert()
        self.tab2 = Tab2TagEditor()
        self.tab3 = Tab3Augment(use_pil=True)  # PIL 방식 사용

        self.tabs.addTab(self.tab1, "확장자 변경 및 중복 정리")
        self.tabs.addTab(self.tab2, "태깅 편집")
        self.tabs.addTab(self.tab3, "이미지 증강")

        self.setCentralWidget(self.tabs)

        # 폴더 선택 버튼 클릭 시 Tab2, Tab3에 경로 전달
        self.tab1.select_folder_btn.clicked.connect(self.update_tab2_folder_path)

    def update_tab2_folder_path(self):
        self.tab2.set_folder_path(self.tab1.folder_path)
        self.tab3.set_folder_path(self.tab1.folder_path)
