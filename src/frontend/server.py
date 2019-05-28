import base64
import datetime
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
        html.Div(id='container')
    ])

    def get_data(contents, n, d):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        reader = JsonFlowReader(decoded.decode('utf-8').split('\n'), config)
        return reader.hosts2flow()

    @app.callback(Output('container', 'children'),
                  [Input('upload-data', 'contents')],
                  [State('upload-data', 'filename'),
                   State('upload-data', 'last_modified')])
    def update_output(list_of_contents, list_of_names, list_of_dates):
        hosts = {}
        traces = []
        if list_of_contents is not None:
            data = [
                get_data(c, n, d) for c, n, d in
                zip(list_of_contents, list_of_names, list_of_dates)]

            for d in data:
                for h in d:
                    if h not in hosts:
                        hosts[h] = d[h]
                    else:
                        hosts[h].extend(d[h])
            for h, flows in hosts.items():
                x = []
                y = []
                for flow in flows:
                    if 'L7_PROTO_NAME' in flow:
                        x.append(datetime.datetime.utcfromtimestamp(flow['FIRST_SWITCHED']))
                        #x.append(flow['FIRST_SWITCHED'])
                        y.append(flow['IN_BYTES'] + flow['OUT_BYTES'])
                traces.append({'host': h, 'x': x, 'y': y})

        graphs = []
        for trace in traces:
            print(trace)
            graphs.append(
                dcc.Graph(
                    id='graph-{}'.format(trace['host']),
                    figure={
                        'data': [
                            go.Scatter(
                                x=trace['x'],
                                y=trace['y'],
                                text=[trace['host']],
                                mode='markers',
                                opacity=0.7,
                                name=trace['host']
                            ) for trace in traces
                        ],
                        'layout':
                            go.Layout(
                                xaxis={'title': 'time'},
                                yaxis={'title': 'output bytes'}
                            )
                    }
                )
            )

        print(len(graphs))
        return graphs

        # return {
        #     'data': [
        #         go.Scatter(
        #             x=trace['x'],
        #             y=trace['y'],
        #             text=[trace['host']],
        #             mode='markers',
        #             opacity=0.7,
        #             # marker={
        #             #     'size': 15,
        #             #     'line': {'width': 0.5, 'color': 'white'}
        #             # },
        #             name=trace['host']
        #         ) for trace in traces
        #     ],
        #     'layout':
        #         go.Layout(
        #             xaxis={'title': 'timestamp'},
        #             yaxis={'title': 'output bytes'},
        #             # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
        #             # legend={'x': 0, 'y': 1},
        #             # hovermode='closest'
        #     )
        # }

    app.run_server(debug=True, host='192.168.1.99')


if __name__ == '__main__':
    main()
