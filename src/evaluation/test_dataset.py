# A rigorous dataset evaluating intent extraction, RAG hits, memory, and LLM formatting.
EVALUATION_DATASET = [
    {
        "id": "tc_01",
        "question": "What is the sales performance for AlphaBrand in hypermarkets?",
        "expected_query_type": "simple_kpi",
        "expected_sql_template": "kpi_timeseries",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["AlphaBrand", "hypermarkets", "sales"],
        "is_follow_up": False
    },
    {
        "id": "tc_02",
        "question": "Check compliance violations for AlphaBrand.",
        "expected_query_type": "compliance_check",
        "expected_sql_template": "fetch_compliance_check",
        "expected_relevant_doc": "policy_brand_alpha.txt",
        "expected_kpi_fields": ["distribution"],
        "expected_answer_keywords": ["violation", "compliance", "AlphaBrand"],
        "expected_compliance_flag": True,
        "is_follow_up": False
    },
    {
        "id": "tc_03",
        "question": "Compare BetaBrand and DeltaBrand sales in the North region.",
        "expected_query_type": "comparison",
        "expected_sql_template": "kpi_comparison",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["BetaBrand", "DeltaBrand", "North", "compare"],
        "is_follow_up": False
    },
    {
        "id": "tc_04",
        "question": "Why did sales drop for GammaBrand in convenience stores?",
        "expected_query_type": "performance_decline",
        "expected_sql_template": "kpi_drivers",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["distribution", "out_of_stock"],
        "expected_answer_keywords": ["drop", "GammaBrand", "drivers", "convenience"],
        "is_follow_up": False
    },
    {
        "id": "tc_05",
        "question": "What about the same brand in the Drug channel?",
        "expected_query_type": "simple_kpi",
        "expected_sql_template": "kpi_timeseries",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["GammaBrand", "Drug"],
        "is_follow_up": True,
        "previous_turn_id": "tc_04"
    },
    {
        "id": "tc_06",
        "question": "What are the rules for DeltaBrand?",
        "expected_query_type": "compliance_check",
        "expected_sql_template": "fetch_compliance_check",
        "expected_relevant_doc": "policy_brand_delta.txt",
        "expected_kpi_fields": ["distribution"],
        "expected_answer_keywords": ["DeltaBrand", "rules", "policy"],
        "is_follow_up": False
    },
    {
        "id": "tc_07",
        "question": "Show me GammaBrand metrics.",
        "expected_query_type": "simple_kpi",
        "expected_sql_template": "kpi_timeseries",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["GammaBrand"],
        "is_follow_up": False
    },
    {
        "id": "tc_08",
        "question": "Are they compliant with the shelf limits?",
        "expected_query_type": "compliance_check",
        "expected_sql_template": "fetch_compliance_check",
        "expected_relevant_doc": "policy_brand_gamma.txt",
        "expected_kpi_fields": ["distribution"],
        "expected_answer_keywords": ["GammaBrand", "compliance", "shelf"],
        "is_follow_up": True,
        "previous_turn_id": "tc_07"
    },
    {
        "id": "tc_09",
        "question": "Compare AlphaBrand in West versus East.",
        "expected_query_type": "comparison",
        "expected_sql_template": "kpi_comparison",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["AlphaBrand", "West", "East"],
        "is_follow_up": False
    },
    {
        "id": "tc_10",
        "question": "What is the overall performance of all brands in the South?",
        "expected_query_type": "simple_kpi",
        "expected_sql_template": "kpi_timeseries",
        "expected_relevant_doc": None,
        "expected_kpi_fields": ["net_sales"],
        "expected_answer_keywords": ["South", "performance"],
        "is_follow_up": False
    }
]
