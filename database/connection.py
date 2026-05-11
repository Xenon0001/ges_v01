"""
Conexión a base de datos SQLite para GES
Maneja la conexión y operaciones básicas de la base de datos
"""

import sqlite3
import logging
from pathlib import Path
from typing import Optional, Dict, Any, List
from contextlib import contextmanager

from config import DB_PATH

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Gestiona la conexión a la base de datos SQLite"""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_database_exists()
    
    def _ensure_database_exists(self) -> None:
        """Asegura que el directorio de la base de datos exista"""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager para conexiones a la base de datos"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row  # Permite acceso por nombre de columna
            yield conn
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Error de base de datos: {e}")
            if conn:
                conn.rollback()
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SELECT y devuelve los resultados"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Ejecuta INSERT, UPDATE, DELETE y devuelve el número de filas afectadas"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Ejecuta múltiples operaciones INSERT/UPDATE/DELETE"""
        with self.get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            return cursor.rowcount
    
    def get_last_insert_id(self) -> int:
        """Obtiene el último ID insertado"""
        # Obtener el ID fuera del context manager para evitar cierre de conexión
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()
            return result[0] if result and result[0] else 0


# Instancia global de la conexión
db = DatabaseConnection()
