import pandas as pd


class QueryEngine:

    

    def __init__(self, df):
        self.df = df

    def apply_filters(self, df, filters):

        if not filters:
            return df

        for column, value in filters.items():

            if value is None:
                continue

            df = df[
                df[column]
                .astype(str)
                .str.lower()
                ==
                str(value).lower()
            ]

        return df
    
    def clean_pollutant_data(self, df):

        return df.dropna(
            subset=["pollutant_avg"]
        )

    def average(self, query):

        print("========== NEW QUERY ENGINE ==========")

        pollutant = query["pollutant"]

        df = self.df

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        df = self.clean_pollutant_data(df)

        value = df["pollutant_avg"].mean()

        return {
            "answer": f"Average {pollutant} is {value:.2f}",

            "data": {
                "average": float(value)
            },

            "provenance": {
                "intent": "average",
                "rows_used": len(df),
                "filters": query.get("filters", {}),
                "pollutant": pollutant
            },

            "chart_data": None
        }

    def maximum(self, query):

        pollutant = query["pollutant"]

        df = self.df

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        df = self.clean_pollutant_data(df)

        if df.empty:
            return {
                "answer": f"No data found for {pollutant}",
                "data": None,
                "provenance": {},
                "chart_data": None
            }

        idx = df["pollutant_avg"].idxmax()

        row = df.loc[idx]

        return {
            "answer":
                f"Highest {pollutant} found in "
                f"{row['city']} "
                f"with value "
                f"{row['pollutant_avg']}",

            "data": row.to_dict(),

            "provenance": {
                "intent": "maximum",
                "rows_used": len(df),
                "pollutant": pollutant
            },

            "chart_data": None
        }

    def count(self, query):

        target = query.get(
            "target",
            "records"
        )

        if target == "station":

            value = self.df[
                "station"
            ].nunique()

        else:

            value = len(self.df)

        return {
            "answer": f"Count is {value}",

            "data": {
                "count": int(value)
            },

            "provenance": {
                "intent": "count",
                "target": target
            },

            "chart_data": None
        }

    def compare(self, query):

        pollutant = query["pollutant"]

        cities = query["cities"]

        df = self.df

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        result = []

        for city in cities:

            city_df = df[
                df["city"].str.lower()
                ==
                city.lower()
            ]

            city_df = self.clean_pollutant_data(
                city_df
            )

            avg = city_df["pollutant_avg"].mean()

            result.append({
                "city": city,
                "value": float(avg)
            })

        return {
            "answer":
                f"Comparison completed for {pollutant}",

            "data": result,

            "provenance": {
                "intent": "compare",
                "pollutant": pollutant,
                "cities": cities
            },

            "chart_data": result
        }

    def minimum(self, query):

        df = self.df.copy()

        pollutant = query.get("pollutant")

        if pollutant:
            df = df[
                df["pollutant_id"].str.upper()
                ==
                pollutant.upper()
            ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        if df.empty:
            return {
                "answer": "No matching data found",
                "data": None,
                "provenance": {
                    "intent": "minimum"
                },
                "chart_data": None
            }
        
        df = self.clean_pollutant_data(df)

        minimum = float(
            df["pollutant_avg"].min()
        )

        return {
            "answer":
                f"Minimum {pollutant} is "
                f"{minimum:.2f}",

            "data": {
                "minimum": minimum
            },

            "provenance": {
                "intent": "minimum",
                "rows_used": len(df),
                "filters":
                    query.get("filters", {}),
                "pollutant": pollutant
            },

            "chart_data": None
        }
    
    def top_n(self, query):

        pollutant = query["pollutant"]

        group_by = query["group_by"]

        n = query.get("n", 5)

        df = self.df.copy()

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        df = self.clean_pollutant_data(df)

        if df.empty:
            return {
                "answer": "No matching data found",
                "data": None,
                "provenance": {},
                "chart_data": None
            }

        result = (
            df.groupby(group_by)["pollutant_avg"]
            .mean()
            .sort_values(ascending=False)
            .head(n)
            .reset_index()
        )

        records = result.to_dict(
            orient="records"
        )

        return {
            "answer":
                f"Top {n} {group_by}s by {pollutant}",

            "data": records,

            "provenance": {
                "intent": "top_n",
                "rows_used": len(df),
                "group_by": group_by,
                "pollutant": pollutant
            },

            "chart_data": records
        }
    
    def bottom_n(self, query):

        pollutant = query["pollutant"]

        group_by = query["group_by"]

        n = query.get("n", 5)

        df = self.df.copy()

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        df = self.clean_pollutant_data(df)

        if df.empty:
            return {
                "answer": "No matching data found",
                "data": None,
                "provenance": {},
                "chart_data": None
            }

        result = (
            df.groupby(group_by)["pollutant_avg"]
            .mean()
            .sort_values(ascending=True)
            .head(n)
            .reset_index()
        )

        records = result.to_dict(
            orient="records"
        )

        return {
            "answer":
                f"Bottom {n} {group_by}s by {pollutant}",

            "data": records,

            "provenance": {
                "intent": "bottom_n",
                "rows_used": len(df),
                "group_by": group_by,
                "pollutant": pollutant
            },

            "chart_data": records
        }

    def summary(self, query):

        df = self.df.copy()

        pollutant = query.get("pollutant")

        if pollutant:
            df = df[
                df["pollutant_id"].str.upper()
                ==
                pollutant.upper()
            ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        df = self.clean_pollutant_data(df)

        if df.empty:
            return {
                "answer": "No matching data found",
                "data": None,
                "provenance": {},
                "chart_data": None
            }

        stats = {
            "count": int(len(df)),
            "mean": float(df["pollutant_avg"].mean()),
            "median": float(df["pollutant_avg"].median()),
            "min": float(df["pollutant_avg"].min()),
            "max": float(df["pollutant_avg"].max())
        }

        return {
            "answer": f"Summary statistics for {pollutant}",
            "data": stats,
            "provenance": {
                "intent": "summary",
                "rows_used": len(df),
                "pollutant": pollutant,
                "filters": query.get("filters", {})
            },
            "chart_data": None
        }


    def unique_values(self, query):

        column = query["column"]

        values = sorted(
            self.df[column]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        return {
            "answer":
                f"Found {len(values)} unique values in {column}",
            "data": values,
            "provenance": {
                "intent": "unique_values",
                "column": column
            },
            "chart_data": None
        }


    def station_lookup(self, query):

        station = query["station"]

        df = self.df[
            self.df["station"]
            .astype(str)
            .str.contains(
            station,
            case=False,
            na=False,
            regex=False
            )
        ]

        if df.empty:
            return {
                "answer": f"No station found matching {station}",
                "data": None,
                "provenance": {
                    "intent": "station_lookup"
                },
                "chart_data": None
            }

        rows = df.head(20).to_dict(
            orient="records"
        )

        return {
            "answer":
                f"Found {len(df)} records for station {station}",
            "data": rows,
            "provenance": {
                "intent": "station_lookup",
                "station": station
            },
            "chart_data": None
        }


    def location_filter(self, query):

        df = self.df.copy()

        pollutant = query.get("pollutant")

        if pollutant:
            df = df[
                df["pollutant_id"].str.upper()
                ==
                pollutant.upper()
            ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        rows = df.head(100).to_dict(
            orient="records"
        )

        return {
            "answer":
                f"Found {len(df)} matching rows",
            "data": rows,
            "provenance": {
                "intent": "location_filter",
                "rows_used": len(df),
                "filters": query.get("filters", {})
            },
            "chart_data": None
        }


    def distribution(self, query):

        pollutant = query["pollutant"]

        df = self.df.copy()

        df = df[
            df["pollutant_id"].str.upper()
            ==
            pollutant.upper()
        ]

        df = self.apply_filters(
            df,
            query.get("filters", {})
        )

        df = self.clean_pollutant_data(df)

        values = (
            df["pollutant_avg"]
            .dropna()
            .tolist()
        )

        return {
            "answer":
                f"Distribution for {pollutant}",
            "data": {
                "values": values
            },
            "provenance": {
                "intent": "distribution",
                "rows_used": len(df),
                "pollutant": pollutant
            },
            "chart_data": {
                "type": "histogram",
                "values": values
            }
        }

    def execute(self, query):

        intent = query["intent"]

        if intent == "average":
            return self.average(query)

        elif intent == "maximum":
            return self.maximum(query)

        elif intent == "minimum":
            return self.minimum(query)

        elif intent == "count":
            return self.count(query)

        elif intent == "compare":
            return self.compare(query)
        
        elif intent == "top_n":
            return self.top_n(query)
        
        elif intent == "bottom_n":
            return self.bottom_n(query)
        
        elif intent == "summary":
            return self.summary(query)

        elif intent == "unique_values":
            return self.unique_values(query)

        elif intent == "station_lookup":
            return self.station_lookup(query)

        elif intent == "location_filter":
            return self.location_filter(query)

        elif intent == "distribution":
            return self.distribution(query)

        elif intent == "refuse":
            return {
                "answer":
                    query.get(
                        "reason",
                        "Cannot answer from dataset"
                    ),

                "data": None,

                "provenance": {
                    "intent": "refuse"
                },

                "chart_data": None
            }
        

        raise ValueError(
            f"Intent not implemented: {intent}"
        )