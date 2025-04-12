# gui/tab1_convert.py
import os
import shutil
import hashlib
from PIL import Image
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QListWidget, QLineEdit, QMessageBox, QFileDialog
)

class Tab1Convert(QWidget):
    def __init__(self):
        super().__init__()

        self.folder_path = ""
        self.image_list = []

        layout = QVBoxLayout()

        self.select_folder_btn = QPushButton("\U0001F4C1 폴더 선택")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        self.selected_folder_label = QLabel("선택된 폴더: 없음")
        layout.addWidget(self.selected_folder_label)

        self.image_list_widget = QListWidget()
        layout.addWidget(self.image_list_widget)

        self.prefix_input = QLineEdit()
        self.prefix_input.setPlaceholderText("변환 이미지 접두어 (예: train_) 선택사항")
        layout.addWidget(self.prefix_input)

        self.convert_btn = QPushButton("\U0001F5BC PNG로 확장자 일괄 변경")
        self.convert_btn.clicked.connect(self.convert_images_to_png)
        layout.addWidget(self.convert_btn)

        self.duplicate_btn = QPushButton("\U0001F9F9 중복 이미지 정리")
        self.duplicate_btn.clicked.connect(self.find_and_move_duplicates)
        layout.addWidget(self.duplicate_btn)

        self.setLayout(layout)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "이미지 폴더 선택")
        if self.folder_path:
            self.selected_folder_label.setText(f"선택된 폴더: {self.folder_path}")
            self.load_images()

    def load_images(self):
        self.image_list_widget.clear()
        self.image_list = [f for f in os.listdir(self.folder_path)
                           if f.lower().endswith((".jpg", ".jpeg", ".png"))]
        self.image_list_widget.addItems(self.image_list)

    def convert_images_to_png(self):
        prefix = self.prefix_input.text().strip()
        if not prefix:
            QMessageBox.warning(self, "접두어 누락", "접두어를 입력해야 이름이 변경됩니다.")
            return

        convert_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith((".jpg", ".jpeg"))]
        rename_only_files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(".png")]

        all_files = os.listdir(self.folder_path)
        max_index = 0
        for f in all_files:
            if f.startswith(prefix + "_") and f.lower().endswith(".png"):
                try:
                    num = int(os.path.splitext(f[len(prefix) + 1:])[0])
                    max_index = max(max_index, num)
                except ValueError:
                    continue
        index = max_index + 1

        for file in convert_files:
            try:
                file_path = os.path.join(self.folder_path, file)
                img = Image.open(file_path).convert("RGB")
                new_name = f"{prefix}_{index}.png"
                new_path = os.path.join(self.folder_path, new_name)

                while os.path.exists(new_path):
                    index += 1
                    new_name = f"{prefix}_{index}.png"
                    new_path = os.path.join(self.folder_path, new_name)

                img.save(new_path)
                os.remove(file_path)
                index += 1
            except Exception as e:
                print(f"[✘] 변환 실패: {file} → {e}")

        for file in rename_only_files:
            file_path = os.path.join(self.folder_path, file)
            new_name = f"{prefix}_{index}.png"
            new_path = os.path.join(self.folder_path, new_name)

            while os.path.exists(new_path):
                index += 1
                new_name = f"{prefix}_{index}.png"
                new_path = os.path.join(self.folder_path, new_name)

            try:
                os.rename(file_path, new_path)
                index += 1
            except Exception as e:
                print(f"[✘] 이름 변경 실패: {file} → {e}")

        self.load_images()
        QMessageBox.information(self, "완료", "모든 파일 이름이 변경 및 변환되었습니다.")

    def find_and_move_duplicates(self):
        hash_dict = {}
        dup_folder = os.path.join(self.folder_path, "중복")
        os.makedirs(dup_folder, exist_ok=True)

        for file in os.listdir(self.folder_path):
            if file.lower().endswith(".png"):
                filepath = os.path.join(self.folder_path, file)
                with open(filepath, 'rb') as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
                if filehash in hash_dict:
                    existing_path = hash_dict[filehash]
                    dup_index = 1
                    while True:
                        dup_name1 = f"dup{dup_index}_1.png"
                        dup_name2 = f"dup{dup_index}_2.png"
                        if not os.path.exists(os.path.join(dup_folder, dup_name1)) and \
                           not os.path.exists(os.path.join(dup_folder, dup_name2)):
                            shutil.move(existing_path, os.path.join(dup_folder, dup_name1))
                            shutil.move(filepath, os.path.join(dup_folder, dup_name2))
                            break
                        dup_index += 1
                else:
                    hash_dict[filehash] = filepath

        self.load_images()
        QMessageBox.information(self, "완료", "중복 이미지 정리가 완료되었습니다!")