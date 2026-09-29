from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from backend import najdi_knihu


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

        # Results list
        self.results_list = QListWidget()
        self.results_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ccc;
                border-radius: 6px;
                font-size: 14px;
                color: black;
                background-color: #f9f9f9;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:hover {
                background-color: #e8e8e8;
            }
            QListWidget::item:selected {
                background-color: #d0d0d0;
            }
        """)
        layout.addWidget(self.results_list)

        layout.addStretch()
        central_widget.setLayout(layout)

        self.search_button.clicked.connect(self.search_books)
        self.search_input.returnPressed.connect(self.search_books)

    def search_books(self):
        query = self.search_input.text().strip()
        if not query:
            self.search_result_label.setText("Search query is empty. Please enter a search term.")
            self.results_list.clear()
            return

        results = najdi_knihu(query)
        self.results_list.clear()

        if results:
            self.search_result_label.setText(f"Found {len(results)} result(s) for: \"{query}\"")
            for kniha in results:
                data = kniha.ziskaj_data()
                item_text = f"{data[1]} — {data[2]} ({data[3]}) | Žáner: {data[4]} | Jazyk: {data[5]} | ISBN: {data[8]}"
                item = QListWidgetItem(item_text)
                self.results_list.addItem(item)
        else:
            self.search_result_label.setText(f"No results found for: \"{query}\"")