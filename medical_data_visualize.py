import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# 1. Import the data
df = pd.read_csv("medical_examination.csv")


# 2. Add overweight column
df["overweight"] = (
    df["weight"] / ((df["height"] / 100) ** 2) > 25
).astype(int)


# 3. Normalize cholesterol and glucose
df["cholesterol"] = df["cholesterol"].apply(lambda x: 0 if x == 1 else 1)
df["gluc"] = df["gluc"].apply(lambda x: 0 if x == 1 else 1)


def draw_cat_plot():
    # 4–6. Create categorical dataframe
    df_cat = pd.melt(
        df,
        id_vars=["cardio"],
        value_vars=["cholesterol", "gluc", "smoke", "alco", "active", "overweight"]
    )

    df_cat = (
        df_cat
        .groupby(["cardio", "variable", "value"])
        .size()
        .reset_index(name="total")
    )

    # 7. Draw the categorical plot
    fig = sns.catplot(
        data=df_cat,
        x="variable",
        y="total",
        hue="value",
        col="cardio",
        kind="bar"
    ).fig

    # 8–9. Return figure
    return fig


def draw_heat_map():
    # 10–11. Clean the data
    df_heat = df[
        (df["ap_lo"] <= df["ap_hi"]) &
        (df["height"] >= df["height"].quantile(0.025)) &
        (df["height"] <= df["height"].quantile(0.975)) &
        (df["weight"] >= df["weight"].quantile(0.025)) &
        (df["weight"] <= df["weight"].quantile(0.975))
    ]

    # 12. Calculate correlation matrix
    corr = df_heat.corr()

    # 13. Generate mask
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14. Set up matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 10))

    # 15. Draw heatmap
    sns.heatmap(
        corr,
        mask=mask,
        annot=True,
        fmt=".1f",
        square=True,
        center=0,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5}
    )

    # 16–17. Return figure
    return fig
