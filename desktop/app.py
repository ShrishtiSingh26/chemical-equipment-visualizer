import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QFileDialog, QLabel, QMessageBox
)
import matplotlib.pyplot as plt

API_BASE = "http://127.0.0.1:8000/api"
AUTH = ("admin", "123")


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(400, 300)

        # ---- State ----
        self.csv_uploaded = False
        self.last_save_dir = os.getcwd()

        # ---- Layout ----
        self.layout = QVBoxLayout()

        self.label = QLabel("Upload CSV to visualize equipment data")
        self.status_label = QLabel("Status: Idle")

        self.upload_btn = QPushButton("Upload CSV")
        self.history_btn = QPushButton("View Last 5 Uploads")
        self.pdf_btn = QPushButton("Download PDF Report")

        # Disable PDF button initially
        self.pdf_btn.setEnabled(False)

        # ---- Signals ----
        self.upload_btn.clicked.connect(self.upload_file)
        self.history_btn.clicked.connect(self.view_history)
        self.pdf_btn.clicked.connect(self.download_pdf)

        # ---- Add Widgets ----
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.upload_btn)
        self.layout.addWidget(self.history_btn)
        self.layout.addWidget(self.pdf_btn)

        self.setLayout(self.layout)

    # ---------------- Upload CSV ----------------
    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV", "", "CSV Files (*.csv)"
        )
        if not file_path:
            return

        self.status_label.setText("Status: Uploading...")
        QApplication.processEvents()

        with open(file_path, "rb") as f:
            response = requests.post(
                f"{API_BASE}/upload/",
                files={"file": f},
                auth=AUTH
            )

        if response.status_code != 200:
            self.status_label.setText("Status: Upload failed")
            QMessageBox.critical(self, "Error", "Upload failed")
            return

        data = response.json()
        self.show_chart(data["type_distribution"])

        # Enable PDF download after successful upload
        self.csv_uploaded = True
        self.pdf_btn.setEnabled(True)
        self.status_label.setText("Status: Done")

    # ---------------- Download PDF ----------------
    def download_pdf(self):
        if not self.csv_uploaded:
            QMessageBox.warning(self, "Warning", "Upload a CSV first")
            return

        response = requests.get(
            f"{API_BASE}/report/",
            auth=AUTH
        )

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to download PDF")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF",
            os.path.join(self.last_save_dir, "equipment_report.pdf"),
            "PDF Files (*.pdf)"
        )

        if not file_path:
            return

        self.last_save_dir = os.path.dirname(file_path)

        with open(file_path, "wb") as f:
            f.write(response.content)

        QMessageBox.information(self, "Success", "PDF downloaded successfully")

    # ---------------- Chart ----------------
    def show_chart(self, dist):
        plt.figure()
        plt.pie(dist.values(), labels=dist.keys(), autopct='%1.1f%%')
        plt.title("Equipment Type Distribution")
        plt.show(block=False)

    # ---------------- History ----------------
    def view_history(self):
        response = requests.get(f"{API_BASE}/history/", auth=AUTH)

        if response.status_code != 200:
            QMessageBox.critical(self, "Error", "Failed to fetch history")
            return

        history = response.json()
        text = ""

        for h in history:
            s = h["summary"]
            text += (
                f"Date: {h['uploaded_at']}\n"
                f"Total: {s['total_equipment']}, "
                f"Flowrate: {s['avg_flowrate']:.2f}, "
                f"Pressure: {s['avg_pressure']:.2f}, "
                f"Temp: {s['avg_temperature']:.2f}\n\n"
            )

        QMessageBox.information(self, "Upload History", text)


# ---------------- Run App ----------------
app = QApplication(sys.argv)
window = App()
window.show()
sys.exit(app.exec_())
