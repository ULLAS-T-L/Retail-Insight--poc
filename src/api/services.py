from src.utils.db import QueryRunner
from src.agents.intent_parser import RuleBasedIntentParser
from src.data.sql_templates import SQL_TEMPLATES
from src.agents.analyzer import DeterministicAnalyzer
from typing import Dict, Any, List, Optional

class KPIService:
    """
    Central service layer bridging the user intent, SQL mappings, 
    database querying structure, and downstream analysis.
    """
    
    def __init__(self):
        self.parser = RuleBasedIntentParser()
        self.runner = QueryRunner()
        self.analyzer = DeterministicAnalyzer()

    def _evaluate_compliance_flags(self, query_type: str, results: List[Dict[str, Any]]) -> List[str]:
        flags = []
        if query_type == "compliance_check":
            for r in results:
                flags.append(f"Violation: Product {r.get('product_id', 'Unknown')} on {r.get('date', 'Unknown')} " 
                             f"Market Share: {r.get('market_share', 0):.2f} / Distribution: {r.get('avg_distribution', 0):.2f}.")
        return flags

    def analyze(self, user_query: Optional[str] = None, structured_intent: Optional[Dict[str, Any]] = None) -> dict:
        # 1. Parse intent
        if structured_intent and any(v is not None for v in structured_intent.values()):
            parsed_intent = {k: v for k, v in structured_intent.items() if v is not None}
            if "query_type" not in parsed_intent:
                parsed_intent["query_type"] = "simple_kpi"
                
            from datetime import datetime, timedelta
            if "start_date" not in parsed_intent:
                parsed_intent["start_date"] = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            if "end_date" not in parsed_intent:
                parsed_intent["end_date"] = datetime.now().strftime("%Y-%m-%d")
                
            if parsed_intent.get("query_type") == "compliance_check":
                parsed_intent["market_share_threshold"] = parsed_intent.get("market_share_threshold", 0.5)
                parsed_intent["distribution_threshold"] = parsed_intent.get("distribution_threshold", 0.8)
        elif user_query:
            parsed_intent = self.parser.parse(user_query)
        else:
            raise ValueError("Must provide either a user 'query' or 'structured_intent'.")
            
        query_type = parsed_intent.get("query_type", "simple_kpi")
        
        # 2. Map designated query_type to the corresponding SQL Template
        template_mapping = {
            "simple_kpi": "kpi_timeseries",
            "comparison": "compare_periods",
            "performance_decline": "kpi_drivers",
            "compliance_check": "compliance_check"
        }
        
        template_key = template_mapping.get(query_type, "kpi_timeseries")
        sql_template = SQL_TEMPLATES.get(template_key)
        
        # 3. Securely query db via structured bindings
        try:
            results = self.runner.run_query(sql_template, parsed_intent)
        except Exception as e:
            raise Exception(f"Database error executing template: {str(e)}")
            
        # 4. Process deterministic downstream analysis
        try:
            from src.agents.llm_analyzer import LLMAnalyzer
            analysis_result = LLMAnalyzer.analyze(query_type, results, parsed_intent)
            
            # Ensure the LLM returned the expected dictionary keys to support strict API schema typing
            if not all(k in analysis_result for k in ("summary", "drivers", "actions", "risks")):
                raise ValueError("LLM returned incomplete JSON keys.")
        except Exception as e:
            print(f"LLM Analyzer fallback triggered conditionally: {str(e)}")
            analysis_result = self.analyzer.analyze(query_type, results, parsed_intent)
            
        compliance_flags = self._evaluate_compliance_flags(query_type, results)
        
        return {
            "parsed_intent": parsed_intent,
            "sql_template_used": sql_template.strip(),
            "kpi_data": results,
            "analysis": analysis_result,
            "compliance_flags": compliance_flags if compliance_flags else None
        }
