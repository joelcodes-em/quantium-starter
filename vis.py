import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load and prepare data
df = pd.read_csv('formatted_output.csv')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')


# Create color scheme
region_colors = {
    'north': '#4E79A7',  # Muted blue
    'east': '#F28E2B',   # Orange
    'south': '#E15759',  # Red
    'west': '#76B7B2',   # Teal
    'all': '#59A14F'     # Green
}

app = dash.Dash(__name__)

app.layout = html.Div([
    # Header with logo placeholder
    html.Div([
        html.H1("Soul Foods - Pink Morsel Performance", 
                style={'color': '#2c3e50', 'margin-bottom': '5px'}),
        html.P("Regional Sales Analysis | Q1 2021", 
               style={'color': '#7f8c8d', 'margin-top': '0'})
    ], style={'textAlign': 'center', 'padding': '20px', 'background': '#f8f9fa'}),
    
    # Control panel
    html.Div([
        html.Div([
            html.Label("Select Region:", style={'font-weight': 'bold'}),
            dcc.RadioItems(
                id='region-radio',
                options=[{'label': r.capitalize(), 'value': r} 
                        for r in ['all', 'north', 'east', 'south', 'west']],
                value='all',
                labelStyle={'display': 'block', 'margin': '5px 0'},
                inputStyle={'margin-right': '8px'}
            )
        ], style={'padding': '15px', 'background': 'white', 'border-radius': '5px'})
    ], style={'width': '20%', 'display': 'inline-block', 'vertical-align': 'top', 'padding': '15px'}),
    
    # Main visualization area
    html.Div([
        dcc.Graph(id='sales-chart', style={'height': '500px'}),
        
        # Summary stats table
        html.Div(id='stats-table', style={
            'margin-top': '20px',
            'background': 'white',
            'padding': '15px',
            'border-radius': '5px'
        })
    ], style={'width': '75%', 'display': 'inline-block', 'padding': '15px'})
], style={'font-family': 'Arial, sans-serif', 'max-width': '1200px', 'margin': '0 auto'})

@app.callback(
    [Output('sales-chart', 'figure'),
     Output('stats-table', 'children')],
    [Input('region-radio', 'value')]
)
def update_chart(selected_region):
    # Filter data
    if selected_region == 'all':
        filtered_df = df
        show_all_regions = True
    else:
        filtered_df = df[df['region'] == selected_region]
        show_all_regions = False
    
    # Create figure
    fig = go.Figure()
    
    if show_all_regions:
        for region in df['region'].unique():
            region_df = df[df['region'] == region]
            fig.add_trace(go.Scatter(
                x=region_df['date'],
                y=region_df['sales'],
                name=region.capitalize(),
                line=dict(color=region_colors[region], width=3),
                mode='lines+markers',
                marker=dict(size=8),
                hovertemplate='<b>%{x|%b %d}</b><br>Sales: $%{y:,.0f}'
            ))
    else:
        fig.add_trace(go.Scatter(
            x=filtered_df['date'],
            y=filtered_df['sales'],
            line=dict(color=region_colors[selected_region], width=3),
            mode='lines+markers',
            marker=dict(size=10),
            hovertemplate='<b>%{x|%b %d}</b><br>Sales: $%{y:,.0f}'
        ))
    
    # Price increase line
   
    # Style layout
    fig.update_layout(
        title=dict(
            text=f'<b>Pink Morsel Daily Sales</b><br><span style="font-size:12px;color:#7f8c8d">{"All Regions" if show_all_regions else selected_region.capitalize() + " Region"}</span>',
            x=0.03,
            y=0.95,
            xanchor='left'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            title='Date',
            tickformat='%b %d'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#f0f0f0',
            title='Sales (USD)',
            tickprefix='$',
            rangemode='tozero'
        ),
        hovermode='x unified',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.3,
            xanchor='center',
            x=0.5
        ),
        margin=dict(l=50, r=50, b=50, t=100),
        height=450
    )
    
    # Create summary stats
    if selected_region == 'all':
        stats = df.groupby('region')['sales'].agg(['sum', 'mean']).reset_index()
        stats.columns = ['Region', 'Total Sales', 'Average Daily Sales']
    else:
        stats = filtered_df['sales'].agg(['sum', 'mean']).to_frame().T
        stats.columns = ['Total Sales', 'Average Daily Sales']
        stats.insert(0, 'Region', selected_region.capitalize())
    
    stats['Total Sales'] = stats['Total Sales'].map('${:,.0f}'.format)
    stats['Average Daily Sales'] = stats['Average Daily Sales'].map('${:,.0f}'.format)
    
    stats_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in stats.columns],
        data=stats.to_dict('records'),
        style_header={
            'backgroundColor': '#2c3e50',
            'color': 'white',
            'fontWeight': 'bold'
        },
        style_cell={
            'textAlign': 'center',
            'padding': '8px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ]
    )
    
    return fig, stats_table

if __name__ == '__main__':
    app.run(debug=True)