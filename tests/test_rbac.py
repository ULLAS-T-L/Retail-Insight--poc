import pytest
from src.auth.rbac import has_permission

def test_viewer_permissions():
    assert has_permission("viewer", "can_query_kpi") is True
    assert has_permission("viewer", "can_use_rag") is False
    assert has_permission("viewer", "can_use_memory") is False
    assert has_permission("viewer", "can_access_admin_routes") is False

def test_analyst_permissions():
    assert has_permission("analyst", "can_query_kpi") is True
    assert has_permission("analyst", "can_use_rag") is True
    assert has_permission("analyst", "can_use_memory") is True
    assert has_permission("analyst", "can_access_admin_routes") is False

def test_admin_permissions():
    assert has_permission("admin", "can_query_kpi") is True
    assert has_permission("admin", "can_use_rag") is True
    assert has_permission("admin", "can_use_memory") is True
    assert has_permission("admin", "can_access_admin_routes") is True

def test_invalid_role():
    assert has_permission("hacker", "can_query_kpi") is False
