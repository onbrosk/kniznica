import json
import sys
from datetime import date, timedelta
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
    QDialog,
    QFormLayout,
    QDialogButtonBox,
    QCheckBox,
    QMessageBox,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt

from backend import (
    knihy,
    clenovia,
    vypozicane,
    najdi_knihu,
    najdi_podla_id,
    uloz_knihy,
    uloz_clenov,
    uloz_vypozicane,
)
from Class.Kniha import Kniha
from Class.Clen import Clen
from Class.VypozicanaKniha import VypozicanaKniha


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

        self.btn_add_book = QPushButton("Pridať")
        self.btn_add_book.clicked.connect(self.add_book)

        search_layout.addWidget(self.book_search_input)
        search_layout.addWidget(self.book_search_btn)
        search_layout.addWidget(self.btn_add_book)
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

        self.btn_add_member = QPushButton("Pridať")
        self.btn_add_member.clicked.connect(self.add_member)
        self.btn_edit_member = QPushButton("Upraviť")
        self.btn_edit_member.clicked.connect(self.edit_member)
        self.btn_delete_member = QPushButton("Zmazať")
        self.btn_delete_member.clicked.connect(self.delete_member)

        members_search_layout.addWidget(self.member_search_input)
        members_search_layout.addWidget(self.member_search_btn)
        members_search_layout.addWidget(self.btn_add_member)
        members_search_layout.addWidget(self.btn_edit_member)
        members_search_layout.addWidget(self.btn_delete_member)
        members_layout.addLayout(members_search_layout)

        self.member_table = QTableView()
        self.member_model = QStandardItemModel()
        self.member_table.setModel(self.member_model)

        self.member_table.setSelectionBehavior(QTableView.SelectRows)
        self.member_table.setSelectionMode(QTableView.SingleSelection)
        self.member_table.clicked.connect(self.on_member_selected)

        self.member_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        members_layout.addWidget(self.member_table)

        self.tabs.addTab(self.members_tab, "Členovia")

        # =========================
        # ZÁLOŽKA ZÁZNAMY
        # =========================
        self.records_tab = QWidget()
        records_layout = QVBoxLayout(self.records_tab)

        records_search_layout = QHBoxLayout()

        self.record_search_input = QLineEdit()
        self.record_search_input.setPlaceholderText(
            "Hľadaj záznam podľa knihy, člena alebo ID..."
        )

        self.record_search_btn = QPushButton("Hľadať")
        self.record_search_btn.clicked.connect(self.search_records)

        self.record_active_only = QCheckBox("Iba aktuálne vypožičané")
        self.record_active_only.stateChanged.connect(self.search_records)

        records_search_layout.addWidget(self.record_search_input)
        records_search_layout.addWidget(self.record_search_btn)
        records_search_layout.addWidget(self.record_active_only)
        records_layout.addLayout(records_search_layout)

        self.record_table = QTableView()
        self.record_model = QStandardItemModel()
        self.record_table.setModel(self.record_model)

        self.record_table.setSelectionBehavior(QTableView.SelectRows)
        self.record_table.setSelectionMode(QTableView.SingleSelection)
        self.record_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )

        records_layout.addWidget(self.record_table)

        self.tabs.addTab(self.records_tab, "Záznamy")

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
        self.btn_edit.clicked.connect(self.edit_book)
        self.btn_delete = QPushButton("Zmazať")
        self.btn_delete.clicked.connect(self.delete_book)
        self.btn_lend = QPushButton("Vypožičať")
        self.btn_lend.clicked.connect(self.lend_book)
        self.btn_return = QPushButton("Vrátiť")
        self.btn_return.clicked.connect(self.return_book)


        self.btn_layout.addWidget(self.btn_edit)
        self.btn_layout.addWidget(self.btn_delete)
        self.btn_layout.addWidget(self.btn_lend)
        self.btn_layout.addWidget(self.btn_return)

        main_layout.addWidget(self.btn_container)

        self.btn_container.hide()

        # Aktuálne výsledky vyhľadávania.
        # Používame priamo objekty z backendu, takže pri kliknutí
        # vieme získať skutočné údaje o knihe.
        self._book_results = []
        self._member_results = []

        # Na začiatku zobrazíme všetky knihy, členov a záznamy.
        self.show_all_books()
        self.show_all_members()
        self.show_all_records()

    # =========================================================
    # ZÁZNAMY
    # =========================================================

    def show_all_records(self):
        self.search_records()

    def search_records(self):
        self.record_model.clear()

        headers = [
            "Kniha",
            "ID knihy",
            "Člen",
            "ID člena",
            "Dátum vypožičania",
            "Dátum vrátenia",
            "Dátum skutočného vrátenia",
            "Vytvorené",
        ]

        self.record_model.setHorizontalHeaderLabels(headers)

        try:
            with open("data/logs/vypozicane.json", "r", encoding="utf-8") as file:
                zaznamy = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            zaznamy = []

        if not isinstance(zaznamy, list):
            zaznamy = [zaznamy] if zaznamy else []

        query = self.record_search_input.text().strip().lower()
        active_only = self.record_active_only.isChecked()

        for zaznam in zaznamy:
            if not isinstance(zaznam, dict):
                continue

            has_return = str(zaznam.get("datum_realneho_vratenia") or "").strip()
            is_active = not has_return

            if active_only and not is_active:
                continue

            if query:
                haystack = " ".join([
                    str(zaznam.get("kniha", "")),
                    str(zaznam.get("kniha_id", "")),
                    str(zaznam.get("clen", "")),
                    str(zaznam.get("clen_id", "")),
                    str(zaznam.get("datum_vypozicania", "")),
                    str(zaznam.get("datum_vratenia", "")),
                ]).lower()
                if query not in haystack:
                    continue

            self.record_model.appendRow([
                QStandardItem(str(zaznam.get("kniha", ""))),
                QStandardItem(str(zaznam.get("kniha_id", ""))),
                QStandardItem(str(zaznam.get("clen", ""))),
                QStandardItem(str(zaznam.get("clen_id", ""))),
                QStandardItem(str(zaznam.get("datum_vypozicania", ""))),
                QStandardItem(str(zaznam.get("datum_vratenia", ""))),
                QStandardItem(str(zaznam.get("datum_realneho_vratenia", ""))),
                QStandardItem(str(zaznam.get("vytvorene", ""))),
            ])

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

        self.details_group.setTitle("Detaily knihy")
        self.details_label.setText(text)
        self.details_group.show()
        self.btn_container.show()

    def open_lend_book_dialog(self, book):
        dialog = QDialog(self)
        dialog.setWindowTitle("Vypožičať knihu")
        form = QFormLayout(dialog)

        member_input = QLineEdit()
        member_input.setPlaceholderText("Zadajte ID člena")
        form.addRow("ID člena:", member_input)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() != QDialog.Accepted:
            return None

        member_id = member_input.text().strip()
        if not member_id:
            QMessageBox.warning(dialog, "Neplatné údaje", "ID člena je povinné.")
            return None

        return member_id

    def open_book_dialog(self, book=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Upraviť knihu" if book else "Pridať knihu")
        form = QFormLayout(dialog)

        fields = {}
        values = {
            "Názov": book.nazov if book else "",
            "Autor": book.autor if book else "",
            "Rok vydania": book.rok_vydania if book else "",
            "Žáner": book.zaner if book else "",
            "Jazyk": book.jazyk if book else "",
            "Poškodenie": book.poskodenie if book else "",
            "ISBN": book.isbn if book else "",
        }

        for label, value in values.items():
            field = QLineEdit(str(value))
            form.addRow(label, field)
            fields[label] = field

        borrowed = QCheckBox()
        borrowed.setChecked(bool(book.je_vypozicana) if book else False)
        form.addRow("Vypožičaná", borrowed)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() != QDialog.Accepted:
            return

        if not fields["Názov"].text().strip() or not fields["Autor"].text().strip():
            QMessageBox.warning(dialog, "Neplatné údaje", "Názov a autor sú povinné.")
            return

        data = {
            "nazov": fields["Názov"].text().strip(),
            "autor": fields["Autor"].text().strip(),
            "rok_vydania": fields["Rok vydania"].text().strip(),
            "zaner": fields["Žáner"].text().strip(),
            "jazyk": fields["Jazyk"].text().strip(),
            "poskodenie": fields["Poškodenie"].text().strip(),
            "je_vypozicana": borrowed.isChecked(),
            "isbn": fields["ISBN"].text().strip(),
        }

        if book:
            for key, value in data.items():
                setattr(book, key, value)
        else:
            next_id = max((int(item.id) for item in knihy), default=0) + 1
            knihy.append(Kniha(next_id, **data))

        try:
            uloz_knihy()
        except OSError as error:
            QMessageBox.critical(self, "Chyba ukladania", f"Knihu sa nepodarilo uložiť: {error}")
            return

        self.search_books() if self.book_search_input.text().strip() else self.show_all_books()
        self.details_group.hide()
        self.btn_container.hide()

    def add_book(self):
        self.open_book_dialog()

    def edit_book(self):
        index = self.book_table.currentIndex()
        row = index.row()
        if row < 0 or row >= len(self._book_results):
            QMessageBox.information(self, "Upraviť knihu", "Najprv vyberte knihu.")
            return
        self.open_book_dialog(self._book_results[row])

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

        self._member_results = list(clenovia)

        for member in self._member_results:
            self.member_model.appendRow([
                QStandardItem(str(member.id)),
                QStandardItem(str(member.meno)),
                QStandardItem(str(member.priezvisko)),
                QStandardItem(str(member.datum_narodenia)),
                QStandardItem(str(member.koniec_clenstva)),
            ])

    def search_members(self):
        query = self.member_search_input.text().strip().lower()

        self.details_group.hide()
        self.btn_container.hide()
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

        self._member_results = [
            member
            for member in clenovia
            if query in str(member.meno).lower()
            or query in str(member.priezvisko).lower()
        ]

        for member in self._member_results:
            self.member_model.appendRow([
                QStandardItem(str(member.id)),
                QStandardItem(str(member.meno)),
                QStandardItem(str(member.priezvisko)),
                QStandardItem(str(member.datum_narodenia)),
                QStandardItem(str(member.koniec_clenstva)),
            ])

    def on_member_selected(self, index):
        row = index.row()
        if row < 0 or row >= len(self._member_results):
            return

        self.show_member_detail(self._member_results[row])

    def show_member_detail(self, member):
        text = (
            f"ID: {member.id}\n"
            f"Meno: {member.meno}\n"
            f"Priezvisko: {member.priezvisko}\n"
            f"Dátum narodenia: {member.datum_narodenia}\n"
            f"Koniec členstva: {member.koniec_clenstva}"
        )

        self.details_group.setTitle("Detaily člena")
        self.details_label.setText(text)
        self.details_group.show()
        self.btn_container.hide()

    def add_member(self):
        self.open_member_dialog()

    def edit_member(self):
        row = self.member_table.currentIndex().row()
        if row < 0 or row >= len(self._member_results):
            QMessageBox.information(self, "Upraviť člena", "Najprv vyberte člena.")
            return
        self.open_member_dialog(self._member_results[row])

    def delete_member(self):
        row = self.member_table.currentIndex().row()
        if row < 0 or row >= len(self._member_results):
            QMessageBox.information(self, "Zmazať člena", "Najprv vyberte člena.")
            return

        member = self._member_results[row]
        member_index = clenovia.index(member)
        clenovia.pop(member_index)

        try:
            uloz_clenov()
        except OSError as error:
            clenovia.insert(member_index, member)
            QMessageBox.critical(
                self,
                "Chyba ukladania",
                f"Člena sa nepodarilo zmazať: {error}",
            )
            return

        self.search_members() if self.member_search_input.text().strip() else self.show_all_members()
        self.details_group.hide()

    def open_member_dialog(self, member=None):
        dialog = QDialog(self)
        dialog.setWindowTitle("Upraviť člena" if member else "Pridať člena")
        form = QFormLayout(dialog)

        fields = {}
        for label, value, placeholder in (
            ("Meno", member.meno if member else "", "Meno"),
            ("Priezvisko", member.priezvisko if member else "", "Priezvisko"),
            (
                "Dátum narodenia",
                member.datum_narodenia if member else "",
                "YYYY-MM-DD",
            ),
            (
                "Koniec členstva",
                member.koniec_clenstva if member else "",
                "YYYY-MM-DD",
            ),
        ):
            field = QLineEdit(str(value))
            field.setPlaceholderText(placeholder)
            form.addRow(label, field)
            fields[label] = field

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        form.addRow(buttons)

        if dialog.exec() != QDialog.Accepted:
            return

        meno = fields["Meno"].text().strip()
        priezvisko = fields["Priezvisko"].text().strip()
        datum_narodenia = fields["Dátum narodenia"].text().strip()
        koniec_clenstva = fields["Koniec členstva"].text().strip()

        if not meno or not priezvisko:
            QMessageBox.warning(dialog, "Neplatné údaje", "Meno a priezvisko sú povinné.")
            return

        try:
            date.fromisoformat(datum_narodenia)
            date.fromisoformat(koniec_clenstva)
        except ValueError:
            QMessageBox.warning(
                dialog,
                "Neplatný dátum",
                "Zadajte oba dátumy vo formáte YYYY-MM-DD.",
            )
            return

        original_values = None
        if member:
            original_values = (
                member.meno,
                member.priezvisko,
                member.datum_narodenia,
                member.koniec_clenstva,
            )
            member.meno = meno
            member.priezvisko = priezvisko
            member.datum_narodenia = datum_narodenia
            member.koniec_clenstva = koniec_clenstva
        else:
            next_id = max((int(item.id) for item in clenovia), default=0) + 1
            member = Clen(next_id, meno, priezvisko, datum_narodenia, koniec_clenstva)
            clenovia.append(member)

        try:
            uloz_clenov()
        except OSError as error:
            if original_values is not None:
                (
                    member.meno,
                    member.priezvisko,
                    member.datum_narodenia,
                    member.koniec_clenstva,
                ) = original_values
            else:
                clenovia.remove(member)
            QMessageBox.critical(
                self,
                "Chyba ukladania",
                f"Člena sa nepodarilo uložiť: {error}",
            )
            return

        self.search_members() if self.member_search_input.text().strip() else self.show_all_members()
        self.details_group.hide()
