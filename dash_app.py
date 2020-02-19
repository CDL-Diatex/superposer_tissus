import json
from textwrap import dedent as d

import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output


def dash_scatter(fig,ecru,traite):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'no border',
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
            **Defect Pictures**
        """)),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns')
    ])

    @app.callback(
        Output('click-data', 'children'),
        [Input('basic-interactions', 'clickData')])
    def display_click_data(clickData):
        if clickData:
            x= clickData["points"][0]["x"]
            y=clickData["points"][0]["y"]
            donnees=ecru.dataframe[ecru.dataframe["metrage"]==x]
            id_image=donnees["image"].iloc[0]
            id_roule=donnees["roule"].iloc[0]
            image_filename = 'Matching/'+str(id_roule)+"/Images/"+"d_26_"+str(id_image)+"_0.jpg"
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
            return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        return "Cliquez sur les defauts sur le graph"

    app.run_server(debug=True)