"""
Knowledge Base Database
SQLite-based storage for notes
"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class NotesDatabase:
    """Manage notes in SQLite database"""
    
    def __init__(self, db_path: str = "~/.aigem2/knowledge_base.db"):
        self.db_path = Path(db_path).expanduser()
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT,
                folder TEXT DEFAULT 'root',
                tags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_deleted BOOLEAN DEFAULT 0
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                parent_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (parent_id) REFERENCES folders(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def create_note(self, title: str, content: str = "", folder: str = "root", tags: List[str] = None) -> int:
        """Create new note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tags_json = json.dumps(tags) if tags else "[]"
        
        cursor.execute("""
            INSERT INTO notes (title, content, folder, tags)
            VALUES (?, ?, ?, ?)
        """, (title, content, folder, tags_json))
        
        note_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return note_id
    
    def get_note(self, note_id: int) -> Optional[Dict]:
        """Get note by ID"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM notes WHERE id = ? AND is_deleted = 0
        """, (note_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            note = dict(row)
            note['tags'] = json.loads(note['tags'])
            return note
        return None
    
    def get_all_notes(self, folder: str = None) -> List[Dict]:
        """Get all notes (optionally filtered by folder)"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if folder:
            cursor.execute("""
                SELECT * FROM notes WHERE folder = ? AND is_deleted = 0
                ORDER BY updated_at DESC
            """, (folder,))
        else:
            cursor.execute("""
                SELECT * FROM notes WHERE is_deleted = 0
                ORDER BY updated_at DESC
            """)
        
        rows = cursor.fetchall()
        conn.close()
        
        notes = []
        for row in rows:
            note = dict(row)
            note['tags'] = json.loads(note['tags'])
            notes.append(note)
        
        return notes
    
    def update_note(self, note_id: int, title: str = None, content: str = None, tags: List[str] = None):
        """Update existing note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        updates = []
        values = []
        
        if title is not None:
            updates.append("title = ?")
            values.append(title)
        
        if content is not None:
            updates.append("content = ?")
            values.append(content)
        
        if tags is not None:
            updates.append("tags = ?")
            values.append(json.dumps(tags))
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        values.append(note_id)
        
        query = f"UPDATE notes SET {', '.join(updates)} WHERE id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def delete_note(self, note_id: int):
        """Soft delete note"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE notes SET is_deleted = 1 WHERE id = ?
        """, (note_id,))
        
        conn.commit()
        conn.close()
    
    def search_notes(self, query: str) -> List[Dict]:
        """Search notes by title or content"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT * FROM notes 
            WHERE (title LIKE ? OR content LIKE ?) AND is_deleted = 0
            ORDER BY updated_at DESC
        """, (search_term, search_term))
        
        rows = cursor.fetchall()
        conn.close()
        
        notes = []
        for row in rows:
            note = dict(row)
            note['tags'] = json.loads(note['tags'])
            notes.append(note)
        
        return notes