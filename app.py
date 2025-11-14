import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from shiny import App, ui, render, reactive

# setup and clean data
df = pd.read_csv("attendance_anonymised.csv")
df.rename({"Long Description": "Module Name", "Postive Marks": "Attended", "Planned Start Date": "Date",}, axis=1, inplace=True)
df["Date"] = pd.to_datetime(df["Date"])
modules = list(np.unique(df["Module Name"]))

# setup interface objects
gui = ui.page_fluid(
    ui.h1("Average attendance over time"),
    ui.input_select("dropdown", "Module name", choices=modules, selected=None),
    ui.output_plot("plot")
    )

# setup server and reactive plotting function
def server(input, output, session):
    @render.plot(alt="line-graph")
    def plot():
        # select correct module and take average for each date, then plot it
        data = df[df["Module Name"] == input.dropdown()][["Date", "Attended"]].groupby("Date").mean()
        fig, ax = plt.subplots()
        ax.plot(data)
        plt.xlabel("Date")
        plt.ylabel("Avg. attendance")
        return fig

app = App(gui, server)