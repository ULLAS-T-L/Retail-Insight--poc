from typing import Dict, Any, List
from src.data.db import DatabaseWrapper
from src.data.sql_templates import SQL_TEMPLATES

class QueryRunner:
    """
    Standardized execution wrapping safe, parameterized SQL templates.
    """
    def __init__(self, db: DatabaseWrapper):
        self.db = db
        
    def run_template(self, template_key: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if template_key not in SQL_TEMPLATES:
            raise ValueError(f"Unknown template: {template_key}")
            
        sql = SQL_TEMPLATES[template_key]
        return self.db.execute_query(sql, params)
