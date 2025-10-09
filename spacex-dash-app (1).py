# spacex-dash-app.py
# Dash app for SpaceX launch records

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Read the SpaceX dataset
# Make sure the CSV is in the same folder as this script
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Get min/max payload for the RangeSlider
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Unique launch sites
launch_sites = sorted(spacex_df['Launch Site'].unique())

# Create the Dash app
app = Dash(__name__)
server = app.server  # (optional) helpful when deploying

# -------------------------
# Layout
# -------------------------
app.layout = html.Div(
    children=[
        html.H1(
            'SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
        ),

        # Dropdown (Task 1)
        dcc.Dropdown(
            id='site-dropdown',
            options=[{'label': 'All Sites', 'value': 'ALL'}] +
                    [{'label': s, 'value': s} for s in launch_sites],
            value='ALL',
            placeholder='Select a Launch Site here',
            searchable=True,
            style={'width': '80%', 'margin': 'auto'}
        ),

        html.Br(),

        # Pie chart (Task 2)
        html.Div(
            dcc.Graph(id='success-pie-chart'),
            style={'width': '90%', 'margin': 'auto'}
        ),

        html.Br(),

        # Payload Slider label
        html.P("Payload range (Kg):", style={'textAlign': 'center'}),

        # RangeSlider (Task 3)
        dcc.RangeSlider(
            id='payload-slider',
            min=int(min_payload),
            max=int(max_payload),
            step=1000,
            value=[int(min_payload), int(max_payload)],
            marks={
                int(min_payload): str(int(min_payload)),
                int(max_payload): str(int(max_payload))
            },
            allowCross=False
        ),

        html.Br(),

        # Scatter chart (Task 4)
        html.Div(
            dcc.Graph(id='success-payload-scatter-chart'),
            style={'width': '90%', 'margin': 'auto'}
        ),
    ]
)

# -------------------------
# Callbacks
# -------------------------

# Pie chart callback (Task 2)
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie(selected_site):
    if selected_site == 'ALL':
        # Total number of successful launches per site
        df = spacex_df.groupby('Launch Site', as_index=False)['class'].sum()
        fig = px.pie(
            df,
            values='class',
            names='Launch Site',
            title='Total Successful Launches by Site'
        )
    else:
        # Success vs failure for a single site
        site_df = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = site_df['class'].value_counts().rename_axis('Outcome').reset_index(name='Count')
        counts['Outcome'] = counts['Outcome'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(
            counts,
            values='Count',
            names='Outcome',
            title=f'Launch Outcomes for {selected_site}'
        )

    return fig


# Scatter chart callback (Task 4)
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def update_scatter(selected_site, payload_range):
    low, high = payload_range
    filt = (spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)
    df = spacex_df[filt].copy()

    if selected_site != 'ALL':
        df = df[df['Launch Site'] == selected_site]

    title = ('Correlation between Payload and Success for All Sites'
             if selected_site == 'ALL'
             else f'Correlation between Payload and Success for {selected_site}')

    fig = px.scatter(
        df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        hover_data=['Launch Site', 'class'],
        title=title,
        labels={'class': 'Outcome (1=Success, 0=Failure)'}
    )
    fig.update_traces(marker=dict(size=10, opacity=0.85))
    return fig


# -------------------------
# Main
# -------------------------
if __name__ == '__main__':
   # app.run_server(debug=False)
   #app.run(debug=False)             # or app.run(debug=False, host="0.0.0.0", port=8050)
    
    app.run(debug=False, host="0.0.0.0", port=8051)

