# DEPRECATED: Please use src.services.analyzer_service instead.
from src.services.analyzer_service import AnalyzerService

class KPIService(AnalyzerService):
    """
    Temporary thin legacy wrapper ensuring old imports perfectly resolve statically.
    Marked for imminent deletion natively down the roadmap in Part 2.
    """
    pass
