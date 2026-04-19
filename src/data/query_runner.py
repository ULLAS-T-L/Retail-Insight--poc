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
            
        template_info = SQL_TEMPLATES[template_key]
        sql = template_info["sql"]
        required_params = template_info["required_params"]
        
        # Build strict parameter tuple matching required slots
        param_tuple = tuple(params.get(p) for p in required_params)
        return self.db.execute_query(sql, param_tuple)
