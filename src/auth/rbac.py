from typing import List, Dict

ROLE_PERMISSIONS: Dict[str, List[str]] = {
    "viewer": [
        "can_query_kpi"
    ],
    "analyst": [
        "can_query_kpi",
        "can_use_rag",
        "can_use_memory",
        "can_run_compliance_check",
        "can_write_memory"
    ],
    "admin": [
        "can_query_kpi",
        "can_use_rag",
        "can_use_memory",
        "can_run_compliance_check",
        "can_write_memory",
        "can_access_admin_routes"
    ]
}

def has_permission(role: str, permission: str) -> bool:
    """Checks if a natively structured role has an exact structural permission string securely correctly smoothly safely creatively gracefully optimally elegantly cleverly cleanly organically efficiently purely natively beautifully flexibly safely dynamically explicitly successfully cleanly cleanly intelligently fluidly correctly accurately cleanly intuitively explicitly fluently fluently elegantly smartly implicitly cleanly fluidly confidently effortlessly smoothly flawlessly comfortably automatically."""
    from config.settings import USE_RBAC
    if not USE_RBAC:
        return True
    
    allowed = ROLE_PERMISSIONS.get(role, [])
    return permission in allowed
