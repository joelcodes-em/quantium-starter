import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load and prepare the data
df = pd.read_csv('formatted_output.csv') 
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Create the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Food Sales", style={'textAlign': 'center'}),
    
    dcc.Graph(
        id='sales-chart',
        figure=px.line(
            df,
            x='date',
            y='sales',
            title='Sales Over Time',
            labels={
                'date': 'Date',
                'sales': 'Sales (USD)'
            }
        ).update_layout(
            title_x=0.5,
            shapes=[{
                'type': 'line',
                'xref': 'x',
                'yref': 'paper',
                'x0': '2021-01-15',
                'y0': 0,
                'x1': '2021-01-15',
                'y1': 1,
                'line': {
                    'color': 'red',
                    'width': 2,
                    'dash': 'dash'
                }
            }],
            annotations=[{
                'x': '2021-01-15',
                'y': 1.05,
                'xref': 'x',
                'yref': 'paper',
                'text': 'Price Increase (Jan 15, 2021)',
                'showarrow': False,
                'font': {
                    'color': 'red'
                }
            }]
        )
    ),
    
    html.Div([
        html.H3("Key Insight:"),
    ], style={'margin': '20px'})
])

if __name__ == '__main__':
    app.run(debug=True)