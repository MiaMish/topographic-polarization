import pandas as pd
from matplotlib import pyplot as plt


def show_polarization_metrics(polarization_metrics_df):
    columns_for_rolling_mean = [col for col in list(polarization_metrics_df.columns) if col.endswith(" groups count") or col.endswith(" giant size ratio") or col.endswith(" is interaction successful") or col.endswith(" is agent revised")]
    rolling_mean_metrics_df = polarization_metrics_df.copy()[columns_for_rolling_mean].rolling(window=100).mean()
    rolling_mean_metrics_df = rolling_mean_metrics_df.apply(pd.to_numeric)

    rolling_mean_metrics_df.plot(
        y=[col for col in list(rolling_mean_metrics_df.columns) if col.endswith(" groups count")],
        title="Group Count"
    )
    plt.show()

    rolling_mean_metrics_df.plot(
        y=[col for col in list(rolling_mean_metrics_df.columns) if col.endswith(" giant size ratio")],
        title="Giant Size Ratio",

    )
    plt.show()

    rolling_mean_metrics_df.plot(
        y=[col for col in list(rolling_mean_metrics_df.columns) if col.endswith(" is interaction successful")],
        title="Successful Interactions",

    )
    plt.show()

    print("Polarization Metrics Summary:")
    columns_for_metrics_summary = [col for col in list(polarization_metrics_df.columns) if col.endswith(" groups count") or col.endswith(" giant size ratio")]
    print(polarization_metrics_df[columns_for_metrics_summary].tail(1).transpose().to_markdown())
