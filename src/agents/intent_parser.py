import re
from datetime import datetime, timedelta

class RuleBasedIntentParser:
    """
    A simple rule-based parser that maps user questions into:
    - brand
    - region
    - channel
    - query_type 
    - period info
    """
    
    @staticmethod
    def parse(query: str, structured_intent: dict = None) -> dict:
        query_lower = query.lower()
        if not structured_intent:
            structured_intent = {}
        
        # 1. Determine query_type
        if any(w in query_lower for w in ["compare", "vs", "versus"]):
            query_type = "comparison"
        elif any(w in query_lower for w in ["decline", "drop", "why", "driver"]):
            query_type = "performance_decline"
        elif any(w in query_lower for w in ["compliance", "threshold", "breach", "anomaly"]):
            query_type = "compliance_check"
        else:
            query_type = "simple_kpi"
            
        # 2. Extract entities (Dummy rule-based extraction)
        brand = "AlphaBrand" if "alpha" in query_lower else "BetaBrand"
        region = "South" if "south" in query_lower else "North"
        channel = "E-commerce" if "online" in query_lower or "e" in query_lower else "Hypermarket"
        
        # 3. Handle Period Info
        # Default scenario: Fetch last 30 days based on 'today'
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        
        params = {
            "query_type": query_type,
            "brand": brand,
            "region": region,
            "channel": channel,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }
        
        # Advanced Period Handling for Comparisons
        if query_type == "comparison":
            # Map default interval (Period 2) against the immediate preceding period (Period 1)
            params["period_2_end"] = params["end_date"]
            params["period_2_start"] = params["start_date"]
            
            period_1_end = start_date - timedelta(days=1)
            period_1_start = period_1_end - timedelta(days=30)
            
            params["period_1_end"] = period_1_end.strftime("%Y-%m-%d")
            params["period_1_start"] = period_1_start.strftime("%Y-%m-%d")
            
        # Threshold constants injection for Compliance queries
        if query_type == "compliance_check":
            params["market_share_threshold"] = 0.5     # e.g., flag if drop below 50%
            params["distribution_threshold"] = 0.8     # e.g., flag if distributed below 80%
            
        # 4. Integrate structured_intent bounds explicitly overriding defaults securely
        params.update(structured_intent)
        
        # 5. Extract finalized template paths natively reliably
        template_map = {
            "simple_kpi": "kpi_timeseries",
            "comparison": "compare_periods",
            "performance_decline": "kpi_drivers",
            "compliance_check": "compliance_check"
        }
        sql_template = template_map.get(params["query_type"], "kpi_timeseries")
        
        return {
            "query_type": params["query_type"],
            "sql_template": sql_template,
            "template_params": params
        }
