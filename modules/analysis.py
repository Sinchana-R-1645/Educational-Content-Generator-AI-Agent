import pandas as pd
import matplotlib.pyplot as plt

from database import get_scores

def generate_chart():

    data = get_scores()

    if len(data) == 0:
        return None

    df = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Subject",
            "Score",
            "Total"
        ]
    )

    fig, ax = plt.subplots()

    ax.plot(
        df["Score"],
        marker='o'
    )

    ax.set_title(
        "Student Progress"
    )

    ax.set_xlabel(
        "Quiz Attempts"
    )

    ax.set_ylabel(
        "Scores"
    )

    return fig
