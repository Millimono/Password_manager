from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                              QPushButton, QMessageBox, QFileDialog,QHBoxLayout)
from PySide6.QtCore import Qt
import os

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion - Gestionnaire de Mots de Passe")
        self.setFixedSize(400, 300)
        
        self.db_path = ""
        self.master_password = ""
        
        self._setup_ui()
    
    def _setup_ui(self):
        layout = QVBoxLayout()
        
        # Sélection de la base de données
        self.db_label = QLabel("Fichier de base de données:")
        self.db_path_edit = QLineEdit()
        self.db_path_edit.setPlaceholderText("Sélectionnez un fichier ou créez-en un nouveau")
        self.db_browse_btn = QPushButton("Parcourir...")
        self.db_browse_btn.clicked.connect(self._browse_db)
        
        db_layout = QHBoxLayout()
        db_layout.addWidget(self.db_path_edit)
        db_layout.addWidget(self.db_browse_btn)
        
        # Mot de passe maître
        self.pwd_label = QLabel("Mot de passe maître:")
        self.pwd_edit = QLineEdit()
        self.pwd_edit.setEchoMode(QLineEdit.Password)
        
        # Boutons
        self.login_btn = QPushButton("Connexion / Créer")
        self.login_btn.clicked.connect(self._validate)
        self.cancel_btn = QPushButton("Annuler")
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.login_btn)
        btn_layout.addWidget(self.cancel_btn)
        
        layout.addWidget(self.db_label)
        layout.addLayout(db_layout)
        layout.addWidget(self.pwd_label)
        layout.addWidget(self.pwd_edit)
        layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def _browse_db(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Sélectionner ou créer un fichier de base de données",
            "",
            "Fichiers de base de données (*.db);;Tous les fichiers (*)"
        )
        
        if path:
            self.db_path_edit.setText(path)
    
    def _validate(self):
        self.db_path = self.db_path_edit.text()
        self.master_password = self.pwd_edit.text()
        
        if not self.db_path:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un fichier de base de données")
            return
            
        if not self.master_password:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer un mot de passe maître")
            return
            
        self.accept()
