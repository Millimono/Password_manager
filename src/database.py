import json
from pathlib import Path
from crypto import encrypt_data, decrypt_data, generate_salt, derive_key
import os

class PasswordDatabase:
    def __init__(self, db_path, master_password):
        self.db_path = Path(db_path)
        self.master_password = master_password
        self.salt = self._get_or_create_salt()
        self.key = derive_key(master_password, self.salt)
        self.entries = self._load_entries()

    def _get_or_create_salt(self):
        if self.db_path.exists():
            with open(self.db_path, 'rb') as f:
                salt = f.read(32)
                return salt
        else:
            salt = generate_salt()
            with open(self.db_path, 'wb') as f:
                f.write(salt)
            return salt

    def _load_entries(self):
        if not self.db_path.exists():
            return []
            
        with open(self.db_path, 'rb') as f:
            f.seek(32)  # Skip salt
            encrypted_data = f.read()
            
        if not encrypted_data:
            return []
            
        decrypted_data = decrypt_data(encrypted_data, self.key)
        return json.loads(decrypted_data)

    def save_entries(self):
        data = json.dumps(self.entries).encode('utf-8')
        encrypted_data = encrypt_data(data, self.key)
        
        with open(self.db_path, 'wb') as f:
            f.write(self.salt)
            f.write(encrypted_data)

    def add_entry(self, title, username, password, url='', notes=''):
        self.entries.append({
            'title': title,
            'username': username,
            'password': password,
            'url': url,
            'notes': notes
        })
        self.save_entries()

    def get_entries(self):
        return self.entries

    def update_entry(self, index, title, username, password, url='', notes=''):
        if 0 <= index < len(self.entries):
            self.entries[index] = {
                'title': title,
                'username': username,
                'password': password,
                'url': url,
                'notes': notes
            }
            self.save_entries()

    def delete_entry(self, index):
        if 0 <= index < len(self.entries):
            del self.entries[index]
            self.save_entries()
