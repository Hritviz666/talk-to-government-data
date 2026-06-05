import os
import uuid

import matplotlib.pyplot as plt


class ChartEngine:

    def __init__(self):

        self.output_dir = "charts"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def create_bar_chart(
        self,
        data,
        x_col,
        y_col,
        title
    ):

        plt.figure(
            figsize=(8, 5)
        )

        x = [
            row[x_col]
            for row in data
        ]

        y = [
            row[y_col]
            for row in data
        ]

        plt.bar(x, y)

        plt.title(title)

        plt.xticks(
            rotation=45,
            ha="right"
        )

        plt.tight_layout()

        filename = (
            f"{uuid.uuid4()}.png"
        )

        path = os.path.join(
            self.output_dir,
            filename
        )

        plt.savefig(path)

        plt.close()

        return path

    def create_histogram(
        self,
        values,
        title
    ):

        plt.figure(
            figsize=(8, 5)
        )

        plt.hist(
            values,
            bins=20
        )

        plt.title(title)

        plt.tight_layout()

        filename = (
            f"{uuid.uuid4()}.png"
        )

        path = os.path.join(
            self.output_dir,
            filename
        )

        plt.savefig(path)

        plt.close()

        return path