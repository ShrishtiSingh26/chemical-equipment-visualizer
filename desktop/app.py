import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QFileDialog, QLabel, QMessageBox
)
import matplotlib.pyplot as plt

API_BASE = "http://127.0.0.1:8000/api"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")

        self.layout = QVBoxLayout()

        self.label = QLabel("Upload CSV to visualize equipment data")
        self.upload_btn = QPushButton("Upload CSV")
        self.history_btn = QPushButton("View Last 5 Uploads")

        self.upload_btn.clicked.connect(self.upload_file)
        self.history_btn.clicked.connect(self.view_history)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.history_btn)

        self.setLayout(self.layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path:
            return

        files = {'file': open(file_path, 'rb')}
        response = requests.post(f"{API_BASE}/upload/", files=files)

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Upload failed")
            return

        data = response.json()
        self.show_chart(data["type_distribution"])

    def show_chart(self, dist):
        plt.figure()
        plt.pie(dist.values(), labels=dist.keys(), autopct='%1.1f%%')
        plt.title("Equipment Type Distribution")
        plt.show()

    def view_history(self):
        response = requests.get(f"{API_BASE}/history/")
        history = response.json()

        text = ""
        for h in history:
            text += (
                f"Date: {h['uploaded_at']}\n"
                f"Total: {h['total_equipment']}, "
                f"Flowrate: {h['avg_flowrate']:.2f}, "
                f"Pressure: {h['avg_pressure']:.2f}, "
                f"Temp: {h['avg_temperature']:.2f}\n\n"
            )

        QMessageBox.information(self, "Upload History", text)

app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
