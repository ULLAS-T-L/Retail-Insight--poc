from typing import Dict, Any, List

class DeterministicAnalyzer:
    """
    Analyzes KPI tabular data using deterministic Python logic to formulate
    a comprehensive analytical payload consisting of a summary, business drivers, 
    and actionable recommendations.
    """
    
    @staticmethod
    def analyze(query_type: str, results: List[Dict[str, Any]], parsed_intent: Dict[str, Any]) -> Dict[str, Any]:
        analysis = {
            "summary": "No data available to summarize.",
            "drivers": [],
            "risks": [],
            "actions": []
        }
        
        if not results:
            return analysis
            
        brand = parsed_intent.get('brand', 'The requested brand')
            
        if query_type == "simple_kpi":
            total_sales = sum(r.get("total_net_sales", 0) for r in results if r.get("total_net_sales") is not None)
            total_units = sum(r.get("total_units", 0) for r in results if r.get("total_units") is not None)
            
            analysis["summary"] = f"{brand} generated ${total_sales:,.2f} in net sales ({total_units:,} units) over this period."
            analysis["drivers"] = ["Overall consistent baseline sales volume."]
            analysis["actions"] = [
                f"Monitor {brand} trends consistently to sustain current throughput.",
                "Review external broader-market impacts that could skew expected baselines."
            ]
            
        elif query_type == "comparison":
            p1_sales = sum(r.get("total_net_sales", 0) for r in results if r.get("period_name") == "Period 1")
            p2_sales = sum(r.get("total_net_sales", 0) for r in results if r.get("period_name") == "Period 2")
            
            diff = p2_sales - p1_sales
            direction = "increased" if diff >= 0 else "decreased"
            analysis["summary"] = f"Sales {direction} by ${abs(diff):,.2f} in Period 2 compared to Period 1."
            
            if diff < 0:
                analysis["drivers"].append("Negative performance momentum spanning Period 2.")
                analysis["actions"].append("Investigate potential stockouts, marketing drops, or negative pricing factors impacting recent dates.")
            elif diff > 0:
                analysis["drivers"].append("Positive growth scaling identified in Period 2.")
                analysis["actions"].append("Identify the positive levers from Period 2 and continue expanding them aggressively.")
            else:
                analysis["drivers"].append("Stagnant growth.")
                analysis["actions"].append("Review historical promotional campaigns to inject new momentum.")
                
        elif query_type == "performance_decline":
            total_sales = sum(r.get("net_sales", 0) for r in results if r.get("net_sales") is not None)
            analysis["summary"] = f"Performance drivers cleanly mapped against a ${total_sales:,.2f} sales window."
            
            avg_dist = sum(r.get("distribution", 0) for r in results) / len(results) if results else 0
            if avg_dist < 0.8:
                analysis["drivers"].append(f"Low geographical distribution average ({avg_dist:.2f}) observed limiting unit sales.")
                analysis["actions"].append("Increase retail availability metrics and patch obvious supply chain routing gaps.")
            else:
                analysis["drivers"].append(f"Healthy distribution reach ({avg_dist:.2f}) recorded uniformly across targets.")
                
            promos = sum(1 for r in results if r.get("promo_flag") == 1)
            if promos < (len(results) * 0.1):
                analysis["drivers"].append("Statistically low promotional activity detected.")
                analysis["actions"].append("Deploy immediate targeted promotions matching high price elasticity to inject unit volume.")
            else:
                analysis["drivers"].append("Promotional cadence continues remaining active.")
                
        elif query_type == "compliance_check":
            violations = len(results)
            analysis["summary"] = f"Mathematical bounds compliance checked. Found {violations} specific violation drops."
            
            if violations > 0:
                analysis["drivers"].append("Target thresholds bounds breached mathematically triggering anomaly flag.")
                analysis["actions"].append("Perform immediate root cause review of non-compliant nodes and halt free-falling market share conditions.")
            else:
                analysis["drivers"].append("No compliance or bounds breaches detected.")
                analysis["actions"].append("System fully stable. Maintain current operational compliance routing.")
                
        return analysis
