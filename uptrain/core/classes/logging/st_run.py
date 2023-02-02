import streamlit as st
import pandas as pd
from glob import glob
import os
import sys
import plotly.graph_objects as go
import numpy as np
import json


def return_plotly_fig(y_axis, x_axis='Num predictions', x_log=False, y_log=False):
    fig = go.Figure()
    fig.update_xaxes(title_text=x_axis)
    fig.update_yaxes(title_text=y_axis)
    if x_log:
        fig.update_xaxes(type="log")
    if y_log:
        fig.update_yaxes(type="log")
    return fig


# Getting the streamlit log folder
log_folder = sys.argv[1]

st.set_page_config(
    page_title="UpTrain AI Dashboard",
    layout="wide",
)
st.title("UpTrain AI Live Dashboard")
st_style = """
            <style>
            footer {visibility: hidden;}
            </style>
           """
st.markdown(st_style, unsafe_allow_html=True)

sub_dirs = [path[0] for path in os.walk(log_folder)]
st.sidebar.title("Select dashboards to view")
for sub_dir in sub_dirs:
    if sub_dir.split('/')[-2] == 'line_plots':
        plot_name = sub_dir.split('/')[-1]
        
        if st.sidebar.checkbox(f"Line-plot for {plot_name}"):
            st.markdown(f"### Line chart for {plot_name}")

            # Getting the list of all csv files in streamlit logs 
            csv_files = [file for path,_,_ in os.walk(sub_dir)
                            for file in glob(os.path.join(path, "*.csv"))]

            scol1, scol2 = st.columns(2)
            with scol1:
                x_log = st.checkbox(
                    "log x", help="Plot x-axis in log-scale",
                    key=plot_name + 'x'
                )
            with scol2:
                y_log = st.checkbox(
                    "log y", help="Plot y-axis in log-scale",
                    key=plot_name + 'y'
                    )
            fig = return_plotly_fig(plot_name, x_log=x_log, y_log=y_log)
            for i, csv_file in enumerate(csv_files):
                # Reading the csv file
                df = pd.read_csv(csv_file)

                # Getting plot_id
                plot_id = csv_file.split('/')[-1].split('.')[0]
                fig = fig.add_trace(go.Scatter(
                                x=df['count'],
                                y=df[plot_id],
                                name=str(i) + ", " + plot_id,
                                ))
            st.plotly_chart(fig)

        st.sidebar.markdown("""---""")
