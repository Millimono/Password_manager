import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from gui.login_dialog import LoginDialog
from database import PasswordDatabase
from cryptography.exceptions import InvalidTag

def main():
    app = QApplication(sys.argv)
    
    while True:  # Boucle pour réessayer en cas d'erreur
        login_dialog = LoginDialog()
        
        # Annulation par l'utilisateur
        if login_dialog.exec() != LoginDialog.Accepted:
            sys.exit(0)
            
        try:
            # Tentative de connexion
            db = PasswordDatabase(login_dialog.db_path, login_dialog.master_password)
            break  # Sortie de la boucle si succès
            
        except InvalidTag:
            # Erreur de mot de passe
            QMessageBox.critical(
                login_dialog,
                "Échec de la connexion",
                "Mot de passe maître incorrect !\nVeuillez réessayer."
            )
        except Exception as e:
            # Autres erreurs (fichier corrompu, etc)
            QMessageBox.critical(
                login_dialog,
                "Erreur critique",
                f"Impossible de charger la base de données :\n{str(e)}"
            )
            sys.exit(1)

    # Si la connexion réussit
    from gui.main_window import MainWindow
    window = MainWindow(db)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
