# tests/test_crypto.py
import pytest
from src.crypto import (
    generate_salt,
    derive_key,
    encrypt_data,
    decrypt_data,
    generate_password
)
from cryptography.exceptions import InvalidTag

class TestCryptoFunctions:
    """Tests pour les fonctions cryptographiques critiques"""
    
    # Fixtures communes
    @pytest.fixture
    def sample_data(self):
        return b"Donnee ultra secrete 123!"
    
    @pytest.fixture
    def sample_password(self):
        return "MonSuperMot2Passe!2024"
    
    @pytest.fixture
    def derived_key(self, sample_password):
        salt = generate_salt()
        return derive_key(sample_password, salt), salt

    # Tests unitaires
    def test_salt_generation(self):
        """Test que le sel est unique et de la bonne taille"""
        salt1 = generate_salt()
        salt2 = generate_salt()
        assert len(salt1) == 32
        assert salt1 != salt2  # Probabilité extrêmement faible de collision

    def test_key_derivation(self, sample_password):
        """Vérifie que la dérivation de clé est déterministe"""
        salt = generate_salt()
        key1 = derive_key(sample_password, salt)
        key2 = derive_key(sample_password, salt)
        assert key1 == key2
        assert len(key1) == 32  # 256 bits

    def test_encryption_decryption(self, sample_data, derived_key):
        """Test round-trip chiffrement/déchiffrement"""
        key, salt = derived_key
        encrypted = encrypt_data(sample_data, key)
        decrypted = decrypt_data(encrypted, key)
        assert decrypted == sample_data

    def test_tampered_data(self, sample_data, derived_key):
        """Test la détection de données corrompues"""
        key, salt = derived_key
        encrypted = encrypt_data(sample_data, key)
        
        # Altération du tag d'authentification
        tampered = encrypted[:16] + b'\x00'*16 + encrypted[32:]
        with pytest.raises(InvalidTag):
            decrypt_data(tampered, key)

    def test_wrong_key_fails(self, sample_data):
        """Vérifie qu'une mauvaise clé échoue"""
        salt = generate_salt()
        key1 = derive_key("bon_mot_de_passe", salt)
        key2 = derive_key("mauvais_mot_de_passe", salt)
        
        encrypted = encrypt_data(sample_data, key1)
        with pytest.raises(InvalidTag):
            decrypt_data(encrypted, key2)

    # Tests pour generate_password
    def test_password_length(self):
        """Vérifie la longueur des mots de passe générés"""
        for length in (8, 16, 32):
            pwd = generate_password(length=length)
            assert len(pwd) == length

    def test_password_charset(self):
        """Test l'inclusion des caractères spéciaux"""
        pwd = generate_password(use_symbols=True)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pwd)
        
        pwd_no_symbols = generate_password(use_symbols=False)
        assert all(c.isalnum() for c in pwd_no_symbols)

    def test_password_uniqueness(self):
        """Test (statistique) que les mots de passe sont uniques"""
        passwords = {generate_password() for _ in range(100)}
        assert len(passwords) == 100  # Aucun doublon
