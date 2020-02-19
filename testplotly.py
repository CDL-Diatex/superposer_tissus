import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output


def dash_scatter(fig):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }

    app.layout = html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig
        ),
        html.Div([
            dcc.Markdown(d("""
            **Click Data**

            Click on points in the graph.
        """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')
    ])

    @app.callback(
        Output('click-data', 'children'),
        [Input('basic-interactions', 'clickData')])
    def display_click_data(clickData):
        if clickData:
            print(clickData)
            image_filename = 'Capture4.PNG'  # replace with your own image
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
            return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        return json.dumps("rien", indent=2)

    app.run_server(debug=True)