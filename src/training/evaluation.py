"""
===========================================================
Evaluation

Project : QuantFormer
===========================================================
"""

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import matplotlib.pyplot as plt


def evaluate_predictions(
    labels,
    predictions
):

    print(
        classification_report(
            labels,
            predictions,
            digits=4
        )
    )

    cm = confusion_matrix(
        labels,
        predictions
    )

    ConfusionMatrixDisplay(
        confusion_matrix=cm
    ).plot()

    plt.show()