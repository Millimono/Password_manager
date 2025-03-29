from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
                              QPlainTextEdit, QDialogButtonBox, QPushButton)
from PySide6.QtCore import Qt
from crypto import generate_password

class AddEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ajouter une nouvelle entrée")
        self.setFixedSize(500, 400)
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        form = QFormLayout()
        
        self.title_edit = QLineEdit()
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.url_edit = QLineEdit()
        self.notes_edit = QPlainTextEdit()
        
        form.addRow("Titre:", self.title_edit)
        form.addRow("Nom d'utilisateur:", self.username_edit)
        form.addRow("Mot de passe:", self.password_edit)
        form.addRow("URL:", self.url_edit)
        form.addRow("Notes:", self.notes_edit)
        
        # Bouton pour générer un mot de passe
        self.generate_pwd_btn = QPushButton("Générer un mot de passe fort")
        self.generate_pwd_btn.clicked.connect(self._generate_password)
        
        # Boutons standard
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        
        layout.addLayout(form)
        layout.addWidget(self.generate_pwd_btn)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def _generate_password(self):
        password = generate_password(16, True)
        self.password_edit.setText(password)
    
    @property
    def title(self):
        return self.title_edit.text().strip()
    
    @property
    def username(self):
        return self.username_edit.text().strip()
    
    @property
    def password(self):
        return self.password_edit.text()
    
    @property
    def url(self):
        return self.url_edit.text().strip()
    
    @property
    def notes(self):
        return self.notes_edit.toPlainText().strip()
