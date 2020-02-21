from textwrap import dedent as d
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output


def dash_scatter(fig,ecru,traite,stats):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'no border',
        }
    }

    app.layout = html.Div([
        dcc.Graph(
            id='basic-interactions',
            figure=fig
        ),
        html.Div(className='row', children=[
            html.Div([
                dcc.Markdown(d("""
                        **Click Data**
                    """)),
                html.Pre(id='click-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                html.H5("Stats"),
                html.Div([render_stat(stats)]),
                html.Pre(id='stats-data', style=styles['pre']),
            ], className='three columns'),
        ])
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
            image_filename = 'Matching/'+str(id_roule)+"/Images/"+"d_"+str(id_roule)+"_"+str(id_image)+"_0.jpg"
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
            return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        return "Cliquez sur les defauts sur le graph"
    return app

def render_stat(stats):
    defects = {1: "FOD", 2: "TRAME", 3: "CHAINE", 13: "FOD2", 15: "TI Noeud", 24: "FOD 2T", 26: "TI trame",
               27: "TI T-Chaine", 28: "TI T-TRAME", 29: "TI chaine", 3000: "inconnu"}
    rates = stats.staying_rates()
    stats_list=[]
    # for defect_type in rates.keys():
    #     stats_list.append(html.Li(defects[defect_type]+" : "+str(round(rates[defect_type][0]*100,2))+"% de "+str(rates[defect_type][1])))
    return html.Ul(stats_list)


