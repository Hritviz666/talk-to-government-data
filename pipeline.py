from engine.query_engine import QueryEngine
from engine.chart_engine import ChartEngine
from engine.confidence_engine import ConfidenceEngine

class DataPipeline:

    def __init__(self, df):

        self.query_engine = QueryEngine(df)

        self.chart_engine = ChartEngine()

        self.confidence_engine = (
            ConfidenceEngine()
        )

    def run(self, query):

        result = self.query_engine.execute(
            query
        )

        chart_data = result.get(
            "chart_data"
        )

        chart_path = None

        if chart_data:

            intent = query["intent"]

            if intent in [
                "top_n",
                "bottom_n"
            ]:

                group_by = query[
                    "group_by"
                ]

                chart_path = (
                    self.chart_engine
                    .create_bar_chart(
                        data=chart_data,
                        x_col=group_by,
                        y_col="pollutant_avg",
                        title=result["answer"]
                    )
                )

            elif intent == "compare":

                chart_path = (
                    self.chart_engine
                    .create_bar_chart(
                        data=chart_data,
                        x_col="city",
                        y_col="value",
                        title=result["answer"]
                    )
                )

            elif intent == "distribution":

                chart_path = (
                    self.chart_engine
                    .create_histogram(
                        values=chart_data[
                            "values"
                        ],
                        title=result["answer"]
                    )
                )

        result["chart_path"] = chart_path

        confidence = (
            self.confidence_engine
            .calculate(
            query,
            result
        )
        )

        result["confidence"] = (
            confidence
        )

        result["needs_human_review"] = (
            confidence < 0.70
        )

        return result