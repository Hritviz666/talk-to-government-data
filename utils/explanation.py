def generate_explanation(query):

    intent = query["intent"]

    parts = []

    parts.append(
        f"The system identified a '{intent}' query."
    )

    pollutant = query.get(
        "pollutant"
    )

    if pollutant:

        parts.append(
            f"Pollutant selected: {pollutant}."
        )

    filters = query.get(
        "filters",
        {}
    )

    if filters:

        filter_text = ", ".join(
            [
                f"{k}={v}"
                for k, v in filters.items()
            ]
        )

        parts.append(
            f"Applied filters: {filter_text}."
        )

    parts.append(
        "The query was executed on the Air Quality dataset."
    )

    return " ".join(parts)