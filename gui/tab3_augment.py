# gui/tab3_augment.py
import os
import numpy as np
from PIL import Image
import albumentations as A
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout
)

class Tab3Augment(QWidget):
    def __init__(self, use_pil=False):  # use_pil 인자를 받도록 수정
        super().__init__()
        self.folder_path = ""
        self.use_pil = use_pil

        layout = QVBoxLayout()

        self.select_btn = QPushButton("📂 이미지 폴더 선택")
        self.select_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_btn)

        self.folder_label = QLabel("선택된 폴더: 없음")
        layout.addWidget(self.folder_label)

        count_layout = QHBoxLayout()
        count_layout.addWidget(QLabel("이미지당 증강 수: "))
        self.augment_count_spin = QSpinBox()
        self.augment_count_spin.setMinimum(1)
        self.augment_count_spin.setMaximum(50)
        self.augment_count_spin.setValue(10)
        count_layout.addWidget(self.augment_count_spin)
        layout.addLayout(count_layout)

        self.run_btn = QPushButton("✨ 이미지 증강 실행")
        self.run_btn.clicked.connect(self.run_augmentation)
        layout.addWidget(self.run_btn)

        self.setLayout(layout)

        self.augmentation_pipeline = A.Compose([
            A.Rotate(limit=15, p=0.5),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            A.GaussNoise(p=0.3),
        ])

    def set_folder_path(self, path):
        self.folder_path = path
        self.folder_label.setText(f"선택된 폴더: {self.folder_path}")

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "원본 이미지 폴더 선택")
        if folder:
            self.set_folder_path(folder)

    def run_augmentation(self):
        if not self.folder_path:
            QMessageBox.warning(self, "오류", "먼저 폴더를 선택하세요.")
            return

        output_dir = os.path.join(self.folder_path, "augmented")
        os.makedirs(output_dir, exist_ok=True)
        count = self.augment_count_spin.value()

        for filename in os.listdir(self.folder_path):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                img_path = os.path.join(self.folder_path, filename)
                try:
                    image = Image.open(img_path).convert("RGB")
                    image = np.array(image)
                except Exception as e:
                    print(f"[⚠] 이미지 로드 실패: {filename} - {e}")
                    continue

                base_output_dir = os.path.join(output_dir, os.path.splitext(filename)[0])
                os.makedirs(base_output_dir, exist_ok=True)

                for i in range(count):
                    augmented = self.augmentation_pipeline(image=image)
                    augmented_image = augmented['image']
                    save_path = os.path.join(base_output_dir, f"aug_{i}.png")
                    Image.fromarray(augmented_image).save(save_path)

        QMessageBox.information(self, "완료", f"이미지 증강이 완료되었습니다!\n위치: {output_dir}")