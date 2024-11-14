import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor


class CalculatorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.max_rows = 20
        self.min_rows = 2
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.fields = []

        self.total_label = QLabel("Total: 0")
        self.total_label.setAlignment(Qt.AlignRight)

        self.set_total_color(True)

        for _ in range(self.min_rows):
            self.add_row()

        self.layout.addWidget(self.total_label)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Add Row")
        self.add_button.clicked.connect(self.add_row)
        button_layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Row")
        self.remove_button.clicked.connect(self.remove_row)
        button_layout.addWidget(self.remove_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear_fields)
        button_layout.addWidget(self.clear_button)

        self.update_button_states()

        self.layout.addLayout(button_layout)

        self.setLayout(self.layout)
        self.setWindowTitle('Odds & Stake Calculator')
        self.resize(400, 400)

    def update_button_states(self):
        if hasattr(self, 'add_button') and hasattr(self, 'remove_button'):
            self.add_button.setEnabled(len(self.fields) < self.max_rows)
            self.remove_button.setEnabled(len(self.fields) > self.min_rows)

    def add_row(self):
        if len(self.fields) < self.max_rows:
            percentage_input = QLineEdit()
            percentage_input.setPlaceholderText("Percentage")
            percentage_input.textChanged.connect(lambda _, idx=len(self.fields): self.update_from_percentage(idx))

            odds_input = QLineEdit()
            odds_input.setPlaceholderText("Odds")
            odds_input.textChanged.connect(lambda _, idx=len(self.fields): self.update_from_odds(idx))

            winnings_input = QLineEdit()
            winnings_input.setPlaceholderText("Winnings")
            winnings_input.textChanged.connect(lambda _, idx=len(self.fields): self.update_winnings(idx))

            stake_output = QLineEdit()
            stake_output.setPlaceholderText("Stake")
            stake_output.setReadOnly(True)

            row_layout = QHBoxLayout()
            row_layout.addWidget(percentage_input)
            row_layout.addWidget(odds_input)
            row_layout.addWidget(winnings_input)
            row_layout.addWidget(stake_output)

            self.layout.insertLayout(len(self.fields), row_layout)
            self.fields.append((percentage_input, odds_input, winnings_input, stake_output))

            self.update_button_states()

    def remove_row(self):
        if len(self.fields) > self.min_rows:
            row = self.fields.pop()
            for widget in row:
                widget.deleteLater()
            self.update_button_states()
            self.update_stakes()

    def clear_fields(self):
        for percentage_input, odds_input, winnings_input, stake_output in self.fields:
            percentage_input.clear()
            odds_input.clear()
            winnings_input.clear()
            stake_output.clear()
        self.total_label.setText("Total: 0")
        while len(self.fields) > self.min_rows:
            self.remove_row()
        self.resize(400, 400)
        self.update_button_states()

    def update_from_percentage(self, index):
        percentage_input, odds_input, _, _ = self.fields[index]
        try:
            percentage = float(percentage_input.text())
            odds = 1 / percentage if percentage != 0 else 0
            odds_input.blockSignals(True)
            odds_input.setText(f"{odds:.2f}")
            odds_input.blockSignals(False)
            self.update_stakes()
        except ValueError:
            odds_input.setText("")

    def update_from_odds(self, index):
        percentage_input, odds_input, _, _ = self.fields[index]
        try:
            odds = float(odds_input.text())
            percentage = 1 / odds if odds != 0 else 0
            percentage_input.blockSignals(True)
            percentage_input.setText(f"{percentage:.2f}")
            percentage_input.blockSignals(False)
            self.update_stakes()
        except ValueError:
            percentage_input.setText("")

    def update_stakes(self):
        total_stake = 0
        winnings_value = 0
        for _, odds_input, winnings_input, stake_output in self.fields:
            try:
                odds = float(odds_input.text())
                winnings = float(winnings_input.text())
                winnings_value = winnings
                stake = winnings / odds if odds != 0 else 0
                stake_output.setText(f"{stake:.2f}")
                total_stake += stake
            except ValueError:
                stake_output.setText("0")
        self.total_label.setText(f"Total: {total_stake:.2f}")
        self.set_total_color(total_stake <= winnings_value)

    def update_winnings(self, index):
        winnings_text = self.fields[index][2].text()
        for i, (_, _, winnings_input, _) in enumerate(self.fields):
            if i != index:
                winnings_input.setText(winnings_text)
        self.update_stakes()

    def set_total_color(self, is_within_winnings):
        palette = self.total_label.palette()
        if is_within_winnings:
            palette.setColor(QPalette.WindowText, QColor('green'))
        else:
            palette.setColor(QPalette.WindowText, QColor('red'))
        self.total_label.setPalette(palette)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())
