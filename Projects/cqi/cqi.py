import streamlit as st
import numpy as np
import plotly.graph_objs as go

# set page title
st.set_page_config(page_title="CQI Priority Calculator", page_icon=":bar_chart:")

# add page title in main window
st.title("CQI Priority Calculator")

# create a sidebar for selecting values and adding some intro
st.sidebar.markdown("# CQI Priority Calculator")
st.sidebar.markdown("This app calculates the priority (P) of a CQI value based on the **Enhanced Proportinal Fair (EPF)**.")
st.sidebar.markdown("### Enhanced Proportional Fair (EPF)")
st.sidebar.markdown("The EPF is a factor that adjusts the priority of a CQI value. The higher the EPF, the more the priority is biased towards high CQI values.")
st.sidebar.markdown("### Throughput (Thrp)")
st.sidebar.markdown("The Thrp is the actual data rate that the link achieves. It is inversely proportional to the priority - the higher the Thrp, the lower the priority.")

epf = st.sidebar.selectbox('Select Enhanced Proportional Fair (EPF)', (0.5, 1, 2, 3, 4))
thrp = st.sidebar.slider('Select Throughput (Thrp) in Mbps', 1, 25, 1)

# create a function to calculate P
def calculate_priority(cqi, epf, thrp):
    return ((cqi ** epf) / thrp)

# calculate priority
cqi = 1
priority = calculate_priority(cqi, epf, thrp)

# create a plot
x = np.linspace(1, 15, 15)
y = calculate_priority(x, epf, thrp)

fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='CQI Curve'))

for thr in [2, 5, 10, 20, 25]:
    y = calculate_priority(x, epf, thr)
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name=f'Thrp={thr}'))

fig.update_layout(
    title=f'<b>Priority vs CQI (EPF={epf}, Thrp={thrp} Mbps)</b>',
    xaxis=dict(
        title='<b>CQI</b>',
        tickfont=dict(
            size=14,
            color='black'
        )
    ),
    yaxis=dict(
        title='<b>Priority</b>',
        tickfont=dict(
            size=14,
            color='black'
        )
    )
)



st.plotly_chart(fig, use_container_width=True)
