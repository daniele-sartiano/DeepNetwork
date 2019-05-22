import base64
import os
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

from src.reader.reader import JsonFlowReader


def main():
    path = os.path.dirname(os.path.realpath(__file__))
    path_data = os.path.join(path, '..', 'reader', 'tests', 'data', 'sample_json_flow.txt')
    config = os.path.join(path, '..', 'reader', 'tests', 'conf', 'json_flow.yaml')
    app = dash.Dash(__name__)
    
    app.layout = html.Div([
        dcc.Upload(
            id='upload-data',
            children= html.Div([
                'Drag and Drop or ', html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        dcc.Graph(
            id='network-flow-chart',
        )
    ])

    def update_chart(contents, n, d):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        reader = JsonFlowReader(decoded.decode('utf-8').split('\n'), config)
        x = []
        y = []
        for el in reader.read():
            x.append(el['FIRST_SWITCHED'])
            y.append(el['IN_BYTES'])
        return {'x': x, 'y': y}

    @app.callback(Output('network-flow-chart', 'figure'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        x = []
        y = []
        if list_of_contents is not None:
            data = [
                update_chart(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]

            for el in data:
                x.extend(el['x'])
                y.extend(el['y'])

        return {
            'data': [
                go.Scatter(
                    x=x,
                    y=y,
                    text=[],
                    mode='markers',
                    opacity=0.7,
                    marker={
                        'size': 15,
                        'line': {'width': 0.5, 'color': 'white'}
                    },
                    name='a'
                )
            ],
            'layout':
                go.Layout(
                    xaxis={'title': 'timestamp'},
                    yaxis={'title': 'Life Expectancy'},
                    margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
            )
        }

    app.run_server(debug=True)


if __name__ == '__main__':
    main()
