from typing import Optional, Dict, Any, List

class Database:
    """In-memory database for quick testing (no RethinkDB needed)"""
    
    def __init__(self):
        self.data: Dict[str, List[Dict[str, Any]]] = {
            "lessons": [],
            "user_progress": [],
            "recordings": [],
        }

    async def connect(self):
        """Initialize database"""
        print("✓ In-memory database initialized")

    async def close(self):
        """Close database"""
        pass

    async def ensure_db_and_tables(self):
        """Ensure tables exist"""
        print("✓ Database tables ready")

    async def insert_one(self, table: str, document: Dict[str, Any]) -> str:
        """Insert a document"""
        if table not in self.data:
            self.data[table] = []
        self.data[table].append(document)
        return document.get("id", "")

    async def get_by_id(self, table: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID"""
        if table not in self.data:
            return None
        for doc in self.data[table]:
            if doc.get("id") == doc_id:
                return doc
        return None

    async def get_all(self, table: str) -> List[Dict[str, Any]]:
        """Get all documents from a table"""
        return self.data.get(table, [])

    async def get_by_index(self, table: str, index: str, value: Any) -> List[Dict[str, Any]]:
        """Get documents by index field"""
        if table not in self.data:
            return []
        return [doc for doc in self.data[table] if doc.get(index) == value]

    async def update_one(self, table: str, doc_id: str, updates: Dict[str, Any]) -> bool:
        """Update a document"""
        if table not in self.data:
            return False
        for doc in self.data[table]:
            if doc.get("id") == doc_id:
                doc.update(updates)
                return True
        return False

    async def delete_one(self, table: str, doc_id: str) -> bool:
        """Delete a document"""
        if table not in self.data:
            return False
        self.data[table] = [doc for doc in self.data[table] if doc.get("id") != doc_id]
        return True

    async def query(self, query):
        """Execute a custom query"""
        return None

db = Database()
