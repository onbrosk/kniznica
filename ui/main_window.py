import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QLineEdit,
    QPushButton,
    QGroupBox,
    QLabel,
    QHeaderView,
    QTabWidget,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from backend import knihy, clenovia, najdi_knihu


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Knižnica")
        self.resize(1000, 700)

        # Hlavný widget a layout
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)
        self.setCentralWidget(main_widget)

        # Záložky
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # =========================
        # ZÁLOŽKA KNIHY
        # =========================
        self.books_tab = QWidget()
        books_layout = QVBoxLayout(self.books_tab)

        search_layout = QHBoxLayout()

        self.book_search_input = QLineEdit()
        self.book_search_input.setPlaceholderText(
            "Hľadaj knihu podľa názvu alebo autora..."
        )

        self.book_search_btn = QPushButton("Hľadať")
        self.book_search_btn.clicked.connect(self.search_books)

        search_layout.addWidget(self.book_search_input)
        search_layout.addWidget(self.book_search_btn)
        books_layout.addLayout(search_layout)

        self.book_table = QTableView()
        self.book_model = QStandardItemModel()
        self.book_table.setModel(self.book_model)

        self.book_table.setSelectionBehavior(QTableView.SelectRows)
        self.book_table.setSelectionMode(QTableView.SingleSelection)
        self.book_table.clicked.connect(self.on_book_selected)

        self.book_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        books_layout.addWidget(self.book_table)

        self.tabs.addTab(self.books_tab, "Knihy")

        # =========================
        # ZÁLOŽKA ČLENOVIA
        # =========================
        self.members_tab = QWidget()
        members_layout = QVBoxLayout(self.members_tab)

        members_search_layout = QHBoxLayout()

        self.member_search_input = QLineEdit()
        self.member_search_input.setPlaceholderText(
            "Hľadaj člena podľa mena alebo priezviska..."
        )

        self.member_search_btn = QPushButton("Hľadať")
        self.member_search_btn.clicked.connect(self.search_members)

        members_search_layout.addWidget(self.member_search_input)
        members_search_layout.addWidget(self.member_search_btn)
        members_layout.addLayout(members_search_layout)

        self.member_table = QTableView()
        self.member_model = QStandardItemModel()
        self.member_table.setModel(self.member_model)

        self.member_table.setSelectionBehavior(QTableView.SelectRows)
        self.member_table.setSelectionMode(QTableView.SingleSelection)

        self.member_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        members_layout.addWidget(self.member_table)

        self.tabs.addTab(self.members_tab, "Členovia")

        # =========================
        # DETAIL KNIHY
        # =========================
        self.details_group = QGroupBox("Detaily knihy")
        self.details_layout = QVBoxLayout(self.details_group)

        self.details_label = QLabel("Vyber knihu")
        self.details_label.setAlignment(Qt.AlignTop)
        self.details_label.setWordWrap(True)

        self.details_layout.addWidget(self.details_label)

        main_layout.addWidget(self.details_group)

        self.details_group.hide()

        # =========================
        # TLAČIDLÁ
        # =========================
        self.btn_container = QWidget()
        self.btn_layout = QHBoxLayout(self.btn_container)

        self.btn_edit = QPushButton("Upraviť")
        self.btn_delete = QPushButton("Zmazať")
        self.btn_test = QPushButton("Test")

        self.btn_layout.addWidget(self.btn_edit)
        self.btn_layout.addWidget(self.btn_delete)
        self.btn_layout.addWidget(self.btn_test)

        main_layout.addWidget(self.btn_container)

        self.btn_container.hide()

        # Aktuálne výsledky vyhľadávania.
        # Používame priamo objekty z backendu, takže pri kliknutí
        # vieme získať skutočné údaje o knihe.
        self._book_results = []

        # Na začiatku zobrazíme všetky knihy a všetkých členov.
        self.show_all_books()
        self.show_all_members()

    # =========================================================
    # KNIHY
    # =========================================================

    def show_all_books(self):
        self.book_model.clear()

        headers = [
            "ID",
            "Názov",
            "Autor",
            "Rok",
            "Žáner",
            "Jazyk",
            "Poškodená",
            "Vypožičaná",
            "ISBN",
        ]

        self.book_model.setHorizontalHeaderLabels(headers)

        self._book_results = list(knihy)

        for book in self._book_results:
            self.book_model.appendRow([
                QStandardItem(str(book.id)),
                QStandardItem(str(book.nazov)),
                QStandardItem(str(book.autor)),
                QStandardItem(str(book.rok_vydania)),
                QStandardItem(str(book.zaner)),
                QStandardItem(str(book.jazyk)),
                QStandardItem(str(book.poskodenie)),
                QStandardItem(str(book.je_vypozicana)),
                QStandardItem(str(book.isbn)),
            ])

    def search_books(self):
        query = self.book_search_input.text().strip()

        self.details_group.hide()
        self.btn_container.hide()

        if not query:
            self.show_all_books()
            return

        self.book_model.clear()

        headers = [
            "ID",
            "Názov",
            "Autor",
            "Rok",
            "Žáner",
            "Jazyk",
            "Poškodená",
            "Vypožičaná",
            "ISBN",
        ]

        self.book_model.setHorizontalHeaderLabels(headers)

        # Backend vracia objekty Kniha.
        self._book_results = najdi_knihu(query)

        for book in self._book_results:
            self.book_model.appendRow([
                QStandardItem(str(book.id)),
                QStandardItem(str(book.nazov)),
                QStandardItem(str(book.autor)),
                QStandardItem(str(book.rok_vydania)),
                QStandardItem(str(book.zaner)),
                QStandardItem(str(book.jazyk)),
                QStandardItem(str(book.poskodenie)),
                QStandardItem(str(book.je_vypozicana)),
                QStandardItem(str(book.isbn)),
            ])

    def on_book_selected(self, index):
        row = index.row()

        if row < 0 or row >= len(self._book_results):
            return

        book = self._book_results[row]
        self.show_book_detail(book)

    def show_book_detail(self, book):
        text = (
            f"Názov: {book.nazov}\n"
            f"Autor: {book.autor}\n"
            f"Rok: {book.rok_vydania}\n"
            f"Žáner: {book.zaner}\n"
            f"Jazyk: {book.jazyk}\n"
            f"Poškodená: {book.poskodenie}\n"
            f"Vypožičaná: {book.je_vypozicana}\n"
            f"ISBN: {book.isbn}"
        )

        self.details_label.setText(text)
        self.details_group.show()
        self.btn_container.show()

    # =========================================================
    # ČLENOVIA
    # =========================================================

    def show_all_members(self):
        self.member_model.clear()

        headers = [
            "ID",
            "Meno",
            "Priezvisko",
            "Dátum narodenia",
            "Koniec členstva",
        ]

        self.member_model.setHorizontalHeaderLabels(headers)

        for member in clenovia:
            self.member_model.appendRow([
                QStandardItem(str(member.id)),
                QStandardItem(str(member.meno)),
                QStandardItem(str(member.priezvisko)),
                QStandardItem(str(member.datum_narodenia)),
                QStandardItem(str(member.koniec_clenstva)),
            ])

    def search_members(self):
        query = self.member_search_input.text().strip().lower()

        self.member_model.clear()

        headers = [
            "ID",
            "Meno",
            "Priezvisko",
            "Dátum narodenia",
            "Koniec členstva",
        ]

        self.member_model.setHorizontalHeaderLabels(headers)

        if not query:
            self.show_all_members()
            return

        results = [
            member
            for member in clenovia
            if query in str(member.meno).lower()
            or query in str(member.priezvisko).lower()
        ]

        for member in results:
            self.member_model.appendRow([
                QStandardItem(str(member.id)),
                QStandardItem(str(member.meno)),
                QStandardItem(str(member.priezvisko)),
                QStandardItem(str(member.datum_narodenia)),
                QStandardItem(str(member.koniec_clenstva)),
            ])
