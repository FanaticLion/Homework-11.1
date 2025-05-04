from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton


class TransactionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.label = QLabel("Выберите тип файла для загрузки транзакций:")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["JSON", "CSV", "XLSX"])
        layout.addWidget(self.combo)

        self.btn_load = QPushButton("Загрузить транзакции")
        layout.addWidget(self.btn_load)

        self.setLayout(layout)