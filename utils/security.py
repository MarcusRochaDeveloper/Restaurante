import os
import bcrypt
from cryptography.fernet import Fernet

class SecurityManager:
    def __init__(self):
        self.cipher = Fernet(self._carregar_ou_criar_chave())
    
    def _carregar_ou_criar_chave(self):
        arquivo_chave = 'secret.key'
        if os.path.exists(arquivo_chave):
            with open(arquivo_chave, 'rb') as chave:
                return chave.read()
        else:
            chave = Fernet.generate_key()
            with open(arquivo_chave, 'wb') as chave_arquivo:
                chave_arquivo.write(chave)
            return chave
    
    def hash_senha(self, senha: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(senha.encode(), salt).decode()
    
    def verificar_senha(self, senha: str, hash_senha: str) -> bool:
        return bcrypt.checkpw(senha.encode(), hash_senha.encode())
    
    def encriptar(self, texto: str) -> str:
        return self.cipher.encrypt(texto.encode()).decode()
    
    def desencriptar(self, token: str) -> str:
        return self.cipher.decrypt(token.encode()).decode()

security_manager = SecurityManager()
