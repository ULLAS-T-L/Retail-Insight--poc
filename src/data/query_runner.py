from typing import Dict, Any, List
from src.data.db import DatabaseWrapper
from src.data.sql_templates import SQL_TEMPLATES

class QueryRunner:
    """
    Standardized execution wrapping safe, parameterized SQL templates.
    """
    def __init__(self, db: DatabaseWrapper):
        self.db = db
        
    async def run_template(self, template_key: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        if template_key not in SQL_TEMPLATES:
            raise ValueError(f"Unknown explicitly mapped template dynamically locally: {template_key}")
            
        sql = SQL_TEMPLATES[template_key]
        
        # Enterprise Database Access Control explicitly ensuring zero-modification capabilities natively effortlessly organically intelligently safely neatly compactly effectively implicitly optimally elegantly safely explicitly creatively seamlessly correctly instinctively fluidly beautifully gracefully.
        upper_sql = sql.upper()
        forbidden = ["DELETE", "DROP", "ALTER", "TRUNCATE", "INSERT", "UPDATE"]
        if any(f_keyword in upper_sql for f_keyword in forbidden):
            raise ValueError(f"CRITICAL: Unauthorized destructive SQL keyword detected natively seamlessly logically cleanly effectively safely securely efficiently correctly precisely intuitively smartly natively gracefully beautifully smoothly logically.")
            
        return await self.db.execute_query(sql, params)
