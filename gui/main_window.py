from PySide6.QtWidgets import (QMainWindow, QVBoxLayout, QWidget, QTableWidget,
                              QTableWidgetItem, QPushButton, QHBoxLayout,QApplication, 
                              QMessageBox, QInputDialog, QLineEdit, QHeaderView)
from PySide6.QtCore import Qt,QTimer
from gui.add_dialog import AddEditDialog

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Gestionnaire de Mots de Passe Sécurisé")
        self.resize(800, 600)
        
        self._setup_ui()
        self._load_entries()
        
    def _setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        
        # Tableau pour afficher les entrées
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Titre", "Nom d'utilisateur", "Mot de passe", "URL"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        # Boutons
        btn_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("Ajouter")
        self.add_btn.clicked.connect(self._add_entry)
        
        self.edit_btn = QPushButton("Modifier")
        self.edit_btn.clicked.connect(self._edit_entry)
        
        self.delete_btn = QPushButton("Supprimer")
        self.delete_btn.clicked.connect(self._delete_entry)
        
        self.copy_pwd_btn = QPushButton("Copier MDP")
        self.copy_pwd_btn.clicked.connect(self._copy_password)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.copy_pwd_btn)
        
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    
    def _load_entries(self):
        self.table.setRowCount(0)
        entries = self.db.get_entries()
        
        for row, entry in enumerate(entries):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(entry['title']))
            self.table.setItem(row, 1, QTableWidgetItem(entry['username']))
            
            # Afficher le mot de passe masqué
            pwd_item = QTableWidgetItem("*" * 8)
            pwd_item.setData(Qt.UserRole, entry['password'])  # Stocker le vrai mdp
            self.table.setItem(row, 2, pwd_item)
            
            self.table.setItem(row, 3, QTableWidgetItem(entry['url']))
    
    def _add_entry(self):
        dialog = AddEditDialog(self)
        if dialog.exec() == AddEditDialog.Accepted:
            self.db.add_entry(
                dialog.title, 
                dialog.username, 
                dialog.password,
                dialog.url,
                dialog.notes
            )
            self._load_entries()
    
    def _edit_entry(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une entrée à modifier")
            return
            
        row = selected[0].row()
        entry = self.db.get_entries()[row]
        
        dialog = AddEditDialog(self)
        dialog.setWindowTitle("Modifier l'entrée")
        dialog.title_edit.setText(entry['title'])
        dialog.username_edit.setText(entry['username'])
        dialog.password_edit.setText(entry['password'])
        dialog.url_edit.setText(entry['url'])
        dialog.notes_edit.setPlainText(entry['notes'])
        
        if dialog.exec() == AddEditDialog.Accepted:
            self.db.update_entry(
                row,
                dialog.title, 
                dialog.username, 
                dialog.password,
                dialog.url,
                dialog.notes
            )
            self._load_entries()
    
    def _delete_entry(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une entrée à supprimer")
            return
            
        row = selected[0].row()
        entry = self.db.get_entries()[row]
        
        reply = QMessageBox.question(
            self, 
            "Confirmation", 
            f"Voulez-vous vraiment supprimer l'entrée '{entry['title']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.delete_entry(row)
            self._load_entries()
    
    def _copy_password(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une entrée")
            return
            
        row = selected[0].row()
        password_item = self.table.item(row, 2)
        password = password_item.data(Qt.UserRole)
        
        clipboard = QApplication.clipboard()
        clipboard.setText(password)
        
        QMessageBox.information(
            self, 
            "Mot de passe copié", 
            "Le mot de passe a été copié dans le presse-papiers. Il sera effacé après 30 secondes.",
            QMessageBox.Ok
        )
        
        # Effacer le presse-papiers après 30 secondes
        QTimer.singleShot(30000, lambda: clipboard.clear())
