# Persistir solo usuarios, chats (con thread_id único) y archivos. No hay tabla de mensajes separada (mensajes en chats).
from getpass import getpass
import uuid
import bcrypt
import os
import sys
import sqlite3
import time
import json
import hashlib
from pathlib import Path
from typing import Optional, List, Dict, Any, Union

# Ruta de la base de datos
DB_PATH = Path(os.getenv("APP_DB_PATH", "app.db"))

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  hash_password TEXT NOT NULL,
  created_at REAL NOT NULL DEFAULT (strftime('%s','now'))
);

CREATE TABLE IF NOT EXISTS chats (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  thread_id TEXT UNIQUE NOT NULL,
  title TEXT NOT NULL,
  created_at REAL NOT NULL DEFAULT (strftime('%s','now')),
  updated_at REAL NOT NULL DEFAULT (strftime('%s','now')),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS messages (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  content TEXT NOT NULL,
  role TEXT NOT NULL,
  type TEXT,
  chat_id INTEGER NOT NULL,
  thread_id TEXT NOT NULL,
  created_at REAL NOT NULL DEFAULT (strftime('%s','now')),
  updated_at REAL NOT NULL DEFAULT (strftime('%s','now')),
  FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  chat_id INTEGER NOT NULL,
  original_name TEXT NOT NULL,
  stored_path TEXT NOT NULL,
  sha256 TEXT,
  created_at REAL NOT NULL DEFAULT (strftime('%s','now')),
  meta TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (chat_id) REFERENCES chats(id) ON DELETE CASCADE,
  UNIQUE(sha256, chat_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_chats_user ON chats(user_id, updated_at);
CREATE INDEX IF NOT EXISTS idx_files_user ON files(user_id, created_at);
"""


def _conn() -> sqlite3.Connection:
    """Establece conexión con la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Inicializa la base de datos creando las tablas si no existen."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _conn() as c:
        c.executescript(SCHEMA)


# ---- Usuarios ----
def create_user(username: str, password: str) -> int:
    """Crea un nuevo usuario con contraseña hasheada."""
    with _conn() as c:
        hash_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        cur = c.execute(
            "INSERT INTO users(username, hash_password) VALUES (?, ?)",
            (username, hash_password),
        )
        return int(cur.lastrowid)


def get_user_id(username: str) -> Optional[int]:
    """Obtiene el ID de usuario dado su nombre de usuario."""
    with _conn() as c:
        r = c.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()
        return int(r["id"]) if r else None


def list_users() -> List[Dict[str, Any]]:
    """Lista todos los usuarios registrados."""
    with _conn() as c:
        return [
            dict(r)
            for r in c.execute(
                "SELECT id, username, hash_password, created_at FROM users ORDER BY created_at DESC"
            ).fetchall()
        ]


def list_chats(user_id: int) -> List[Dict[str, Any]]:
    """Lista los chats de un usuario específico."""
    q = """SELECT id, title, thread_id, created_at, updated_at 
           FROM chats WHERE user_id=? ORDER BY updated_at DESC"""
    with _conn() as c:
        return [dict(r) for r in c.execute(q, (user_id,)).fetchall()]


def get_chat_by_id(id: int) -> Optional[Dict[str, Any]]:
    """Obtiene un chat por su ID numérico."""
    with _conn() as c:
        r = c.execute("SELECT * FROM chats WHERE id=?", (id,)).fetchone()
        return dict(r) if r else None


def get_chat_by_thread(thread_id: str) -> Optional[Dict[str, Any]]:
    """Obtiene un chat por su thread_id."""
    with _conn() as c:
        r = c.execute("SELECT * FROM chats WHERE thread_id=?", (thread_id,)).fetchone()
        return dict(r) if r else None


def get_chat_id_by_thread(thread_id: str) -> Optional[int]:
    """Obtiene el ID numérico de un chat dado su thread_id."""
    with _conn() as c:
        r = c.execute("SELECT id FROM chats WHERE thread_id=?", (thread_id,)).fetchone()
        return r["id"] if r else None


def get_last_thread_id_for_user(user_id: int) -> Optional[str]:
    """Obtiene el thread_id del último chat modificado por el usuario."""
    with _conn() as c:
        r = c.execute(
            "SELECT thread_id FROM chats WHERE user_id=? ORDER BY updated_at DESC",
            (user_id,),
        ).fetchone()
        return r["thread_id"] if r else None


def create_chat(user_id: int, title: str) -> int:
    """Crea un nuevo chat y devuelve su ID numérico."""
    now = time.time()
    thread_id = str(uuid.uuid4())
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO chats(user_id, title, thread_id, created_at, updated_at) VALUES (?,?,?,?,?)",
            (user_id, title, thread_id, now, now),
        )
        return int(cur.lastrowid)


def rename_chat(thread_id: str, title: str) -> None:
    """Renombra un chat existente."""
    with _conn() as c:
        c.execute(
            "UPDATE chats SET title=?, updated_at=? WHERE thread_id=?",
            (title, time.time(), thread_id),
        )


def touch_chat(thread_id: str) -> None:
    """Actualiza la fecha de modificación de un chat."""
    with _conn() as c:
        c.execute(
            "UPDATE chats SET updated_at=? WHERE thread_id=?", (time.time(), thread_id)
        )


def delete_chat_by_thread(thread_id: str) -> None:
    """Elimina un chat dado su thread_id."""
    with _conn() as c:
        c.execute("DELETE FROM chats WHERE thread_id=?", (thread_id,))


# Mensajes
def persist_message(
    content: str, role: str, type: str, chat_id: int, thread_id: str
) -> int:
    """Guarda un mensaje en la base de datos."""
    with _conn() as c:
        cur = c.execute(
            "INSERT INTO messages(content, role, type, chat_id, thread_id) "
            "VALUES (?,?,?,?,?)",
            (content, role, type, chat_id, thread_id),
        )
        return int(cur.lastrowid)


def load_chat_messages(chat_id: int) -> List[Dict[str, Any]]:
    """Carga todos los mensajes de un chat específico."""
    with _conn() as c:
        r = c.execute(
            """SELECT content, role, type, chat_id, thread_id, created_at 
            FROM messages WHERE chat_id=? ORDER BY created_at ASC""",
            (chat_id,),
        ).fetchall()
        return [dict(row) for row in r]


# ---- Archivos ----
def _sha256(path: Path) -> str:
    """Calcula el hash SHA256 de un archivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def get_sha(id: int) -> str:
    """Obtiene el hash SHA256 de un archivo guardado."""
    with _conn() as c:
        return c.execute("SELECT sha256 FROM files WHERE id=?", (id,)).fetchone()[
            "sha256"
        ]


def add_file(
    user_id: int,
    chat_id: int,
    original_name: str,
    stored_path: Path,
    meta: Optional[Dict] = None,
) -> int:
    """Registra un nuevo archivo en la base de datos."""
    if meta is None:
        meta = {}
    now = time.time()
    checksum = _sha256(stored_path) if stored_path.exists() else None
    with _conn() as c:
        cur = c.execute(
            "INSERT OR IGNORE INTO files(user_id, chat_id, original_name, stored_path, sha256, created_at, meta) "
            "VALUES (?,?,?,?,?,?,?)",
            (
                user_id,
                chat_id,
                original_name,
                str(stored_path),
                checksum,
                now,
                json.dumps(meta),
            ),
        )
        return int(cur.lastrowid)


def get_files_by_chat_id(chat_id: int) -> List[Dict[str, Any]]:
    """Obtiene todos los archivos asociados a un chat."""
    q = """SELECT id, original_name, stored_path, created_at, meta 
            FROM files WHERE chat_id=? ORDER BY created_at DESC"""
    with _conn() as c:
        return [dict(r) for r in c.execute(q, (chat_id,)).fetchall()]


# CLI
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python src/db.py init")
        print("  python src/db.py add <username>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "init":
        init_db()
    elif cmd == "add":
        if len(sys.argv) != 3:
            print("Falta <username>")
            sys.exit(1)
        u = sys.argv[2]
        p = getpass("Password: ")
        p2 = getpass("Repetir: ")
        if p != p2:
            print("No coinciden.")
            sys.exit(1)
        uid = create_user(u, p)
        print(f"Usuario creado id={uid}")
    elif cmd == "drop":
        with _conn() as c:
            id = sys.argv[2]
            c.execute("DELETE FROM messages where id = ?", (id,))
    elif cmd == "edit":
        with _conn() as c:
            id = sys.argv[2]
            new_content = sys.argv[3]
            c.execute("UPDATE messages SET content = ? WHERE id = ?", (new_content, id))
    elif cmd == "list":
        users = list_users()
        print("Usuarios:")
        for user in users:
            print(f" - {user['username']} (id={user['id']})")
        sys.exit(0)
