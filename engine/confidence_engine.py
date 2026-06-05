class ConfidenceEngine:

    def calculate(self, query, result):

        confidence = 1.0

        rows_used = (
            result["provenance"]
            .get("rows_used", 0)
        )

        if rows_used < 20:
            confidence -= 0.10

        if rows_used < 10:
            confidence -= 0.15

        if rows_used < 5:
            confidence -= 0.25

        if query["intent"] in [
            "station_lookup",
            "location_filter"
        ]:
            confidence -= 0.05

        confidence = max(
            0.0,
            min(confidence, 1.0)
        )

        return round(
            confidence,
            2
        )