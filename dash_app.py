from textwrap import dedent as d
import dash
import dash_core_components as dcc
import dash_html_components as html
import base64
from dash.dependencies import Input, Output


def dash_scatter(fig,ecru,traite,stats,fig2=[]):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    styles = {
        'pre': {
            'border': 'no border',
        }
    }

    app.layout = html.Div([
        dcc.Graph(
            id='all',
            figure=fig
        ),
        dcc.Graph(
            id='only-matching',
            figure=fig2
        ),
        html.Div(className='row', children=[
            html.Div([
                dcc.Markdown(d("""
                        **Click Data**
                    """)),
                html.Pre(id='click-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                html.H5("Taux de rétention des défauts"),
                html.Div([render_stat(stats)]),
                html.Pre(id='stats-data', style=styles['pre']),
            ], className='three columns'),

            html.Div([
                html.H5("Taux d'apparition des défauts"),
                html.Div([render_stat_apparition(stats)]),
                html.Pre(id='stats-retention-data', style=styles['pre']),
            ], className='three columns')
        ])
    ])

    @app.callback(
        Output('click-data', 'children'),
        [Input('all', 'clickData')])
    def display_click_data(clickData):
        if clickData:
            x= clickData["points"][0]["x"]
            y=clickData["points"][0]["y"]
            donnees=ecru.dataframe.loc[(ecru.dataframe["metrage"]==x) & (ecru.dataframe["position"]==y)]
            id_image=donnees["image"].iloc[0]
            id_roule=donnees["roule"].iloc[0]
            image_filename = 'Matching/'+str(id_roule)+"/Images/"+"d_"+str(id_roule)+"_"+str(id_image)+"_0.jpg"
            encoded_image = base64.b64encode(open(image_filename, 'rb').read())
            return html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()))
        return "Cliquez sur les defauts sur le graph"
    return app

def render_stat(stats):
    defects = {1:"FOD", 2:"TRAME", 3:"CHAINE", 4:"FOD1", 5:"FOD2", 6:"TRAME1", 7:"TRAME2", 8:"CHAINE1", 9:"CHAINE2", 13: "FOD2", 15: "TI Noeud", 24: "FOD 2T", 26: "TI trame",
               27: "TI T-Chaine", 28: "TI T-TRAME", 29: "TI chaine", 3000: "inconnu"}
    rates = stats.staying_rates()
    stats_list=[]
    for defect_type in rates.keys():
        if defect_type in defects.keys():
            stats_list.append(html.Li(defects[defect_type]+" : "+str(round(rates[defect_type][0]*100,2))+"% de "+str(rates[defect_type][1])))
        else:
            stats_list.append(html.Li(str(defect_type)+" : "+str(round(rates[defect_type][0]*100,2))+"% de "+str(rates[defect_type][1])))
    return html.Ul(stats_list)

def render_stat_apparition(stats):
    defects = {1:"FOD", 2:"TRAME", 3:"CHAINE", 4:"FOD1", 5:"FOD2", 6:"TRAME1", 7:"TRAME2", 8:"CHAINE1", 9:"CHAINE2", 13: "FOD2", 15: "TI Noeud", 24: "FOD 2T", 26: "TI trame",
               27: "TI T-Chaine", 28: "TI T-TRAME", 29: "TI chaine", 3000: "inconnu"}
    rates = stats.appearing_defects()
    stats_list=[]
    for defect_type in rates.keys():
        if defect_type in defects.keys():
            stats_list.append(html.Li(defects[defect_type]+" : "+str(round(rates[defect_type][0]*100,2))+"% de "+str(rates[defect_type][1])))
        else:
            stats_list.append(html.Li(str(defect_type)+" : "+str(round(rates[defect_type][0]*100,2))+"% de "+str(rates[defect_type][1])))
    return html.Ul(stats_list)

