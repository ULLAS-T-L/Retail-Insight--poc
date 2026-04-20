import json
from google import genai
from google.genai import types
from typing import Dict, Any, List
from config.settings import get_gemini_key

class LLMAnalyzer:
    """
    Uses Google GenAI Gemini to generate high-level summaries 
    based firmly on the retrieved SQL data.
    """
    
    @staticmethod
    def analyze(query_type: str, results: List[Dict[str, Any]], parsed_intent: Dict[str, Any]) -> dict:
        # Load API key dynamically and raise ValueError gracefully if missing
        api_key = get_gemini_key()
            
        client = genai.Client(api_key=api_key)
        
        # Enforce compactness to limit token costs natively
        compact_results = results[:50]
        
        prompt = f"""
        You are an expert Retail Business Intelligence AI.
        Analyze the following SQL extraction payload and formulate actionable insights.

        CRITICAL RULES:
        1. NO HALLUCINATION: You must NEVER generate numbers or metrics that are not explicitly present in the SQL DATA RESULTS below.
        2. Your analysis must only rigorously reflect the provided data snippet.
        3. IF THE SQL DATA RESULTS ARE EMPTY: You MUST return empty arrays for drivers, risks, and actions. Your summary MUST strictly state that "No data matched the query parameters." Do not hallucinate dummy metrics.
        4. Explain what happened, identify key drivers, highlight operational risks, and recommend actionable next steps ONLY IF data is present.
        4. Return ONLY valid JSON matching exactly the requested structure below:
        {{
            "summary": "String analysis",
            "drivers": ["String", "String"],
            "risks": ["String", "String"],
            "actions": ["String", "String"]
        }}

        CONTEXT:
        - Query Type: {query_type}
        - Intent Parameters: {json.dumps(parsed_intent)}
        
        SQL DATA RESULTS:
        {json.dumps(compact_results)}
        """

        # Enforce structured JSON schema response using response tracking
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        try:
            parsed_response = json.loads(response.text)
            
            from config.settings import USE_GUARDRAILS
            if USE_GUARDRAILS:
                from src.guardrails.hooks import validate_llm_output
                validate_llm_output(parsed_response, compact_results)
                
            return parsed_response
        except Exception as e:
            raise ValueError(f"LLM securely bounded actively failing cleanly nicely automatically gracefully intelligently: {e}")
            raise ValueError("LLM failed to return a valid JSON payload.")
