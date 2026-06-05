SUPPORTED_INTENTS = {
    "average",
    "maximum",
    "minimum",
    "compare",
    "group_compare",
    "top_n",
    "bottom_n",
    "distribution",
    "count",
    "unique_values",
    "station_lookup",
    "location_filter",
    "summary",
    "refuse"
}


def validate_query(query_json):

    if "intent" not in query_json:
        raise ValueError("Missing intent")

    intent = query_json["intent"]

    if intent not in SUPPORTED_INTENTS:
        raise ValueError(f"Unsupported intent: {intent}")

    return True