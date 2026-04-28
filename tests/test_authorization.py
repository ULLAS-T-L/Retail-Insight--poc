import pytest
from src.data.db import DatabaseWrapper
from src.data.query_runner import QueryRunner

def test_database_rejects_destructive_sql():
    db = DatabaseWrapper()
    runner = QueryRunner(db)
    
    # We must mock the SQL_TEMPLATES dictionary locally for this test since it relies on exact string matches natively
    from src.data.sql_templates import SQL_TEMPLATES
    
    SQL_TEMPLATES["mock_delete"] = "DELETE FROM kpi_data WHERE brand = 'AlphaBrand';"
    SQL_TEMPLATES["mock_drop"] = "DROP TABLE kpi_data;"
    SQL_TEMPLATES["mock_update"] = "UPDATE kpi_data SET sales = 9999;"
    
    with pytest.raises(ValueError) as excinfo:
        runner.run_template("mock_delete", {})
    assert "CRITICAL: Unauthorized destructive SQL keyword detected" in str(excinfo.value)
    
    with pytest.raises(ValueError):
        runner.run_template("mock_drop", {})
        
    with pytest.raises(ValueError):
        runner.run_template("mock_update", {})
