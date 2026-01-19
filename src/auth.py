# src/auth.py
import os
import sqlite3
import bcrypt
from pathlib import Path
from typing import Tuple

# Ruta a la base de datos, definida por variable de entorno o por defecto 'app.db'
DB_PATH = Path(os.getenv("APP_DB_PATH", "app.db"))


def _conn() -> sqlite3.Connection:
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    
    Returns:
        sqlite3.Connection: Objeto de conexión con row_factory configurado.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def verify(username: str, password: str) -> Tuple[bool, str]:
    """
    Verifica las credenciales del usuario comparando el hash de la contraseña.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña en texto plano.

    Returns:
        Tuple[bool, str]: Una tupla (éxito, mensaje).
    """
    try:
        with _conn() as c:
            row = c.execute(
                "SELECT hash_password FROM users WHERE username=?", (username,)
            ).fetchone()
        
        if row is None:
            return False, "Usuario o contraseña inválidos."
        
        pw_hash = row["hash_password"]
        # bcrypt.checkpw requiere bytes
        if isinstance(pw_hash, str):
            pw_hash = pw_hash.encode('utf-8')
            
        ok = bcrypt.checkpw(password.encode("utf-8"), pw_hash)
        return (ok, "OK" if ok else "Usuario o contraseña inválidos.")
    except Exception as e:
        # En un entorno real, se debería loguear el error 'e'
        return False, "Error verificando credenciales."


def _auth(username: str, password: str) -> bool:
    """
    Función auxiliar para autenticación simple que devuelve solo booleano.

    Args:
        username (str): Nombre de usuario.
        password (str): Contraseña.

    Returns:
        bool: True si la autenticación es exitosa, False en caso contrario.
    """
    ok, _ = verify(username, password)
    return ok
