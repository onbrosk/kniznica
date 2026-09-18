from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Kniznica")
        self.resize(1000, 600)

        # Central widget with white background
        central_widget = QWidget(self)
        central_widget.setStyleSheet("background-color: white;")
        self.setCentralWidget(central_widget)

        # Main layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # Title
        title_label = QLabel("Kniznica")
        title_label.setFont(QFont("Segoe UI", 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: black;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Search bar and button
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search books...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                color: black;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #333;
            }
        """)
        search_layout.addWidget(self.search_input)

        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("""
            QPushButton {
                padding: 10px 16px;
                background-color: #222;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #444;
            }
        """)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # Label to display search query
        self.search_result_label = QLabel("")
        self.search_result_label.setFont(QFont("Segoe UI", 14))
        self.search_result_label.setStyleSheet("color: #333;")
        self.search_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.search_result_label)

        layout.addStretch()
        central_widget.setLayout(layout)

        self.search_button.clicked.connect(self.search_books)
        self.search_input.returnPressed.connect(self.search_books)

    def search_books(self):
        query = self.search_input.text().strip()
        if query:
            self.search_result_label.setText(f"Searching for: {query}")
        elif query == "":
            self.search_result_label.setText("Search query is empty. Please enter a search term.")
        else:
            self.search_input.setFocus()
            self.search_result_label.setText("")