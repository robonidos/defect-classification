# -*- coding: utf-8 -*-

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Read in the data from Excel
df = pd.read_csv(
    "C://Users//rupadhyay//Desktop//ML//Defect classification and forecasting//Data//Results//Final_results.csv"
)
df.columns
# Get a list of all the avilable Projects
mgr_options = df["Project"].unique()

# Create the app
app = dash.Dash()

# Populate the layout with HTML and graph components
app.layout = html.Div(children=[
    html.H2("Defect Classification Report"),
    html.Div(
        [
            dcc.Dropdown(
                id="Project",
                options=[{
                    'label': i,
                    'value': i
                } for i in mgr_options],
                value='All Projects'),
        ],
        style={'width': '10%',
               'display': 'inline-block'}),
    dcc.Graph(id='funnel-graph',style={'height': 500 ,'width': '50%'
})
], )


# Add the callbacks to support the interactive components
@app.callback(
    dash.dependencies.Output('funnel-graph', 'figure'),
    [dash.dependencies.Input('Project', 'value')])
def update_graph(Project):
    if Project == "All Projects":
        df_plot = df.copy()
    else:
        df_plot = df[df['Project'] == Project]


    pv = pd.pivot_table(
        df_plot,
        #index=['System List'],
        index=['Predicted Label'],
        columns=['System List'],
        values=['Key'],
        aggfunc=np.size)#,
        #fill_value=0)

    if Project=="All Projects":
        trace1 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations.Payout Innovations - Finance (Active)')], name='PM')
        trace2 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations.Payout Innovations - Provider Pairing module (Active)')],
                    name='ATRBN')
        trace3 = go.Bar(x=pv.index, y=pv[('Key', 'Provider Care Management Solutions (Active)')], name='PCMS')
        trace4 = go.Bar(x=pv.index,
                    y=pv[('Key', 'Payout Innovations.Payout Innovations - Provider_Preference module (GBD) (Active)')],
                    name='AFNTY')
        trace5 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations (Active)')], name='FT')


        return {
            'data': [trace1,trace2, trace3, trace4,trace5],
            'layout':
            go.Layout(
                title='Defect Status for {}'.format(Project),
                barmode='stack')
        }

    elif Project=="PYM_INN":

        trace1 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations.Payout Innovations - Finance (Active)')], name='PM')
        trace2 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations.Payout Innovations - Provider Pairing module (Active)')],
                    name='ATRBN')
        trace3 = go.Bar(x=pv.index,
                    y=pv[('Key', 'Payout Innovations.Payout Innovations - Provider_Preference module (GBD) (Active)')],
                    name='AFNTY')
        trace4 = go.Bar(x=pv.index, y=pv[('Key', 'Payout Innovations (Active)')], name='FT')


        return {
            'data': [trace1,trace2, trace3, trace4],
            'layout':
            go.Layout(
                title='Defect Status for {}'.format(Project),
                barmode='stack')
        }

    elif Project=="PCMS":

        trace1 = go.Bar(x=pv.index, y=pv[('Key', 'Provider Care Management Solutions (Active)')], name='PCMS')

        return {
            'data': [trace1],
            'layout':
            go.Layout(
                title='Defect Status for {}'.format(Project),
                barmode='stack')
        }


if __name__ == '__main__':
    app.run_server(debug=True)
