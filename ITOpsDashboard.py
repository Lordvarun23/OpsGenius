'''import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Fetch data from Flask API
def fetch_data(endpoint):
    response = requests.get(f'http://127.0.0.1:5000/api/{endpoint}')
    return response.json()

it_operations_data = fetch_data('it-operations')
asset_management_data = fetch_data('asset-management')
network_performance_data = fetch_data('network-performance')

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("IT Operations Dashboard"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("System Health"),
            dcc.Graph(
                id='system-health-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=['CPU Usage', 'Memory Usage', 'Disk Space'],
                            y=[it_operations_data['performance_metrics']['cpu_usage'],
                               it_operations_data['performance_metrics']['memory_usage'],
                               it_operations_data['performance_metrics']['disk_space']],
                            marker_color=['#4caf50', '#ffeb3b', '#f44336']
                        )
                    ],
                    'layout': go.Layout(
                        title='Performance Metrics',
                        yaxis={'title': 'Percentage'}
                    )
                }
            )
        ], width=6),
        dbc.Col([
            html.H3("Incidents"),
            dcc.Graph(
                id='incidents-graph',
                figure={
                    'data': [
                        go.Pie(
                            labels=[incident['type'] for incident in it_operations_data['incidents']],
                            values=[1] * len(it_operations_data['incidents']),
                            hole=.3
                        )
                    ],
                    'layout': go.Layout(
                        title='Incidents by Type'
                    )
                }
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Asset Management"),
            dcc.Graph(
                id='asset-management-graph',
                figure={
                    'data': [
                        go.Bar(
                            x=[asset['type'] for asset in asset_management_data['assets']],
                            y=[1] * len(asset_management_data['assets']),
                            marker_color='#17a2b8'
                        )
                    ],
                    'layout': go.Layout(
                        title='Assets by Type',
                        xaxis={'title': 'Asset Type'},
                        yaxis={'title': 'Count'}
                    )
                }
            )
        ], width=6),
        dbc.Col([
            html.H3("Network Performance"),
            dcc.Graph(
                id='network-performance-graph',
                figure={
                    'data': [
                        go.Scatter(
                            x=list(range(24)),
                            y=network_performance_data['bandwidth_usage'],
                            mode='lines+markers',
                            name='Bandwidth Usage'
                        ),
                        go.Scatter(
                            x=list(range(24)),
                            y=network_performance_data['latency'],
                            mode='lines+markers',
                            name='Latency'
                        )
                    ],
                    'layout': go.Layout(
                        title='Network Performance',
                        xaxis={'title': 'Hour'},
                        yaxis={'title': 'Value'}
                    )
                }
            )
        ], width=6)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=False)


'''

'''import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Expose the server variable for use in Flask routes

# Function to fetch data from Flask API
def fetch_data(endpoint):
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/{endpoint}')
        response.raise_for_status()  # Raise an HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Flask API: {e}")
        return {}

# Define the layout of the Dash app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("IT Operations Dashboard"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("System Health"),
            dcc.Graph(id='system-health-graph')
        ], width=6),
        dbc.Col([
            html.H3("Incidents"),
            dcc.Graph(id='incidents-graph')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Asset Management"),
            dcc.Graph(id='asset-management-graph')
        ], width=6),
        dbc.Col([
            html.H3("Network Performance"),
            dcc.Graph(id='network-performance-graph')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Download Report", id="html-button", color="primary", n_clicks=0)
        ], width=12, className="d-grid gap-2")
    ]),
    dcc.Interval(
        id='interval-component',
        interval=15*60*1000,  # Default 15 minutes in milliseconds
        n_intervals=0
    ),
    dcc.Dropdown(
        id='refresh-interval',
        options=[
            {'label': '15 Minutes', 'value': 15*60*1000},
            {'label': '30 Minutes', 'value': 30*60*1000},
            {'label': '1 Hour', 'value': 60*60*1000}
        ],
        value=15*60*1000,
        clearable=False,
        style={'margin-top': '10px'}
    ),
], fluid=True)

@app.callback(
    Output('system-health-graph', 'figure'),
    Output('incidents-graph', 'figure'),
    Output('asset-management-graph', 'figure'),
    Output('network-performance-graph', 'figure'),
    Input('refresh-interval', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(interval, n_intervals):
    it_operations_data = fetch_data('it-operations')
    asset_management_data = fetch_data('asset-management')
    network_performance_data = fetch_data('network-performance')

    # Create figures for the graphs
    system_health_figure = {
        'data': [
            go.Bar(
                x=['CPU Usage', 'Memory Usage', 'Disk Space'],
                y=[it_operations_data.get('performance_metrics', {}).get('cpu_usage', 0),
                   it_operations_data.get('performance_metrics', {}).get('memory_usage', 0),
                   it_operations_data.get('performance_metrics', {}).get('disk_space', 0)],
                marker_color=['#4caf50', '#ffeb3b', '#f44336']
            )
        ],
        'layout': go.Layout(
            title='Performance Metrics',
            yaxis={'title': 'Percentage'}
        )
    }

    incidents_figure = {
        'data': [
            go.Pie(
                labels=[incident['type'] for incident in it_operations_data.get('incidents', [])],
                values=[1] * len(it_operations_data.get('incidents', [])),
                hole=.3
            )
        ],
        'layout': go.Layout(
            title='Incidents by Type'
        )
    }

    asset_management_figure = {
        'data': [
            go.Bar(
                x=[asset['type'] for asset in asset_management_data.get('assets', [])],
                y=[1] * len(asset_management_data.get('assets', [])),
                marker_color='#17a2b8'
            )
        ],
        'layout': go.Layout(
            title='Assets by Type',
            xaxis={'title': 'Asset Type'},
            yaxis={'title': 'Count'}
        )
    }

    network_performance_figure = {
        'data': [
            go.Scatter(
                x=list(range(24)),
                y=network_performance_data.get('bandwidth_usage', [0]*24),
                mode='lines+markers',
                name='Bandwidth Usage'
            ),
            go.Scatter(
                x=list(range(24)),
                y=network_performance_data.get('latency', [0]*24),
                mode='lines+markers',
                name='Latency'
            )
        ],
        'layout': go.Layout(
            title='Network Performance',
            xaxis={'title': 'Hour'},
            yaxis={'title': 'Value'}
        )
    }

    return system_health_figure, incidents_figure, asset_management_figure, network_performance_figure

@app.callback(
    Output('html-button', 'n_clicks'),
    Input('html-button', 'n_clicks')
)
def trigger_report_download(n_clicks):
    if n_clicks:
        # Trigger the download using JavaScript
        return dash.no_update

if __name__ == '__main__':
    app.run_server(port=8050, debug=False)'''
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import requests
import dash_daq as daq

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

# Fetch data from Flask API
def fetch_data(endpoint):
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/{endpoint}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return {}

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("IT Operations Dashboard"), className="mb-4")
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("System Health"),
            dcc.Graph(id='system-health-graph')
        ], width=6),
        dbc.Col([
            html.H3("Incidents"),
            dcc.Graph(id='incidents-graph')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.H3("Asset Management"),
            dcc.Graph(id='asset-management-graph')
        ], width=6),
        dbc.Col([
            html.H3("Network Performance"),
            dcc.Graph(id='network-performance-graph')
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Button("Download Report", id="html-button", color="primary", n_clicks=0)
        ], width=12, className="d-grid gap-2")
    ]),
    dcc.Interval(
        id='interval-component',
        interval=15*60*1000,  # Default 15 minutes in milliseconds
        n_intervals=0
    ),
    dcc.Dropdown(
        id='refresh-interval',
        options=[
            {'label': '15 Minutes', 'value': 15*60*1000},
            {'label': '30 Minutes', 'value': 30*60*1000},
            {'label': '1 Hour', 'value': 60*60*1000}
        ],
        value=15*60*1000,
        clearable=False,
        style={'margin-top': '10px'}
    ),
    html.Script('''
        document.getElementById('html-button').addEventListener('click', function() {
            window.location.href = '/generate-html';
        });
    ''')
], fluid=True)

@app.callback(
    Output('system-health-graph', 'figure'),
    Output('incidents-graph', 'figure'),
    Output('asset-management-graph', 'figure'),
    Output('network-performance-graph', 'figure'),
    Input('refresh-interval', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_graphs(interval, n_intervals):
    it_operations_data = fetch_data('it-operations')
    asset_management_data = fetch_data('asset-management')
    network_performance_data = fetch_data('network-performance')

    system_health_figure = {
        'data': [
            go.Bar(
                x=['CPU Usage', 'Memory Usage', 'Disk Space'],
                y=[it_operations_data.get('performance_metrics', {}).get('cpu_usage', 0),
                   it_operations_data.get('performance_metrics', {}).get('memory_usage', 0),
                   it_operations_data.get('performance_metrics', {}).get('disk_space', 0)],
                marker_color=['#4caf50', '#ffeb3b', '#f44336']
            )
        ],
        'layout': go.Layout(
            title='Performance Metrics',
            yaxis={'title': 'Percentage'}
        )
    }

    incidents_figure = {
        'data': [
            go.Pie(
                labels=[incident['type'] for incident in it_operations_data.get('incidents', [])],
                values=[1] * len(it_operations_data.get('incidents', [])),
                hole=.3
            )
        ],
        'layout': go.Layout(
            title='Incidents by Type'
        )
    }

    asset_management_figure = {
        'data': [
            go.Bar(
                x=[asset['type'] for asset in asset_management_data.get('assets', [])],
                y=[1] * len(asset_management_data.get('assets', [])),
                marker_color='#17a2b8'
            )
        ],
        'layout': go.Layout(
            title='Assets by Type',
            xaxis={'title': 'Asset Type'},
            yaxis={'title': 'Count'}
        )
    }

    network_performance_figure = {
        'data': [
            go.Scatter(
                x=list(range(24)),
                y=network_performance_data.get('bandwidth_usage', [0]*24),
                mode='lines+markers',
                name='Bandwidth Usage'
            ),
            go.Scatter(
                x=list(range(24)),
                y=network_performance_data.get('latency', [0]*24),
                mode='lines+markers',
                name='Latency'
            )
        ],
        'layout': go.Layout(
            title='Network Performance',
            xaxis={'title': 'Hour'},
            yaxis={'title': 'Value'}
        )
    }

    return system_health_figure, incidents_figure, asset_management_figure, network_performance_figure

if __name__ == '__main__':
    app.run_server(port=8050, debug=False)
