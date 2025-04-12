# gui/tab2_tag_editor.py
import os
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QListWidget, QVBoxLayout, QLabel, QTextEdit, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class Tab2TagEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.folder_path = ""
        self.current_txt_path = ""

        layout = QHBoxLayout()

        self.left_panel = QVBoxLayout()
        self.tag_search_input = QLineEdit()
        self.tag_search_input.setPlaceholderText("태그로 이미지 필터링")
        self.tag_search_input.textChanged.connect(self.filter_images_by_tag)
        self.left_panel.addWidget(self.tag_search_input)

        self.tag_image_list_widget = QListWidget()
        self.tag_image_list_widget.itemClicked.connect(self.load_selected_image_and_tag)
        self.left_panel.addWidget(self.tag_image_list_widget)

        layout.addLayout(self.left_panel, 3)

        right_panel = QVBoxLayout()

        self.tag_image_label = QLabel("이미지 미리보기")
        self.tag_image_label.setFixedHeight(300)
        self.tag_image_label.setFixedWidth(300)
        right_panel.addWidget(self.tag_image_label)

        self.tag_text_edit = QTextEdit()
        right_panel.addWidget(self.tag_text_edit)

        self.tag_edit_input = QLineEdit()
        self.tag_edit_input.setPlaceholderText("추가/삭제할 태그 입력")
        right_panel.addWidget(self.tag_edit_input)

        self.tag_position_combo = QComboBox()
        self.tag_position_combo.addItems(["맨 뒤에 추가", "맨 앞에 추가"])
        right_panel.addWidget(self.tag_position_combo)

        self.add_tag_btn = QPushButton("➕ 전체 파일에 태그 추가")
        self.add_tag_btn.clicked.connect(self.add_tag_to_all_files)
        right_panel.addWidget(self.add_tag_btn)

        self.remove_tag_btn = QPushButton("➖ 전체 파일에서 태그 제거")
        self.remove_tag_btn.clicked.connect(self.remove_tag_from_all_files)
        right_panel.addWidget(self.remove_tag_btn)

        self.replace_tag_input_old = QLineEdit()
        self.replace_tag_input_old.setPlaceholderText("기존 태그 (예: brown hair)")
        right_panel.addWidget(self.replace_tag_input_old)

        self.replace_tag_input_new = QLineEdit()
        self.replace_tag_input_new.setPlaceholderText("변경할 태그 (예: light brown hair)")
        right_panel.addWidget(self.replace_tag_input_new)

        self.replace_tag_btn = QPushButton("🔁 태그 일괄 치환")
        self.replace_tag_btn.clicked.connect(self.replace_tag_in_all_files)
        right_panel.addWidget(self.replace_tag_btn)

        self.save_tag_btn = QPushButton("💾 현재 태깅 저장")
        self.save_tag_btn.clicked.connect(self.save_tag_text)
        right_panel.addWidget(self.save_tag_btn)

        layout.addLayout(right_panel, 3)
        self.setLayout(layout)

    def set_folder_path(self, folder_path):
        self.folder_path = folder_path
        self.load_tag_images()

    def load_tag_images(self):
        self.tag_image_list_widget.clear()
        if not self.folder_path:
            return
        image_files = [f for f in os.listdir(self.folder_path)
                       if f.lower().endswith(".png")]
        self.tag_image_list_widget.addItems(image_files)

    def filter_images_by_tag(self):
        keyword = self.tag_search_input.text().strip().lower()
        self.tag_image_list_widget.clear()
        if not keyword:
            self.load_tag_images()
            return
        matched_files = []
        for f in os.listdir(self.folder_path):
            if f.lower().endswith(".txt"):
                with open(os.path.join(self.folder_path, f), 'r', encoding='utf-8') as tf:
                    content = tf.read().lower()
                    if keyword in content:
                        image_name = f.replace(".txt", ".png")
                        if os.path.exists(os.path.join(self.folder_path, image_name)):
                            matched_files.append(image_name)
        self.tag_image_list_widget.addItems(matched_files)

    def load_selected_image_and_tag(self, item):
        filename = item.text()
        img_path = os.path.join(self.folder_path, filename)
        txt_path = os.path.join(self.folder_path, os.path.splitext(filename)[0] + ".txt")

        if os.path.exists(img_path):
            pixmap = QPixmap(img_path)
            scaled_pixmap = pixmap.scaled(
                self.tag_image_label.width(),
                self.tag_image_label.height(),
                aspectRatioMode=Qt.KeepAspectRatio
            )
            self.tag_image_label.setPixmap(scaled_pixmap)

        if os.path.exists(txt_path):
            with open(txt_path, 'r', encoding='utf-8') as f:
                self.tag_text_edit.setPlainText(f.read())
        else:
            self.tag_text_edit.setPlainText("")

        self.current_txt_path = txt_path

    def save_tag_text(self):
        if self.current_txt_path:
            with open(self.current_txt_path, 'w', encoding='utf-8') as f:
                f.write(self.tag_text_edit.toPlainText())
            QMessageBox.information(self, "저장 완료", "태깅 내용이 저장되었습니다.")

    def add_tag_to_all_files(self):
        tag = self.tag_edit_input.text().strip()
        if not tag:
            return
        position = self.tag_position_combo.currentText()
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(".txt"):
                txt_path = os.path.join(self.folder_path, file)
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                tags = [t.strip() for t in content.split(",") if t.strip()]
                if tag not in tags:
                    if position == "맨 앞에 추가":
                        tags.insert(0, tag)
                    else:
                        tags.append(tag)
                    with open(txt_path, 'w', encoding='utf-8') as f:
                        f.write(", ".join(tags))
        QMessageBox.information(self, "완료", "모든 파일에 태그가 추가되었습니다.")

    def remove_tag_from_all_files(self):
        tag = self.tag_edit_input.text().strip()
        if not tag:
            return
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(".txt"):
                txt_path = os.path.join(self.folder_path, file)
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                tags = [t.strip() for t in content.split(",") if t.strip() and t.strip() != tag]
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(", ".join(tags))
        QMessageBox.information(self, "완료", "모든 파일에서 태그가 제거되었습니다.")

    def replace_tag_in_all_files(self):
        old_tag = self.replace_tag_input_old.text().strip()
        new_tag = self.replace_tag_input_new.text().strip()
        if not old_tag or not new_tag:
            QMessageBox.warning(self, "입력 누락", "기존 태그와 변경할 태그를 모두 입력해 주세요.")
            return
        for file in os.listdir(self.folder_path):
            if file.lower().endswith(".txt"):
                txt_path = os.path.join(self.folder_path, file)
                with open(txt_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                tags = [t.strip() for t in content.split(",")]
                tags = [new_tag if t == old_tag else t for t in tags]
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(", ".join(tags))
        QMessageBox.information(self, "완료", f"'{old_tag}' → '{new_tag}' 치환 완료")