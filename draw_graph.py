import numpy as np
import math
import plotly.graph_objects as go


class Graph():
    @staticmethod
    def draw(data1, data2=[], name="inconnu", rotation="inconnu"):
        defects = {1: "FOD", 2: "TRAME", 3: "CHAINE", 4: "FOD1", 5: "FOD2", 6: "TRAME1", 7: "TRAME2", 8: "CHAINE1",
                   9: "CHAINE2", 13: "FOD2", 15: "TI Noeud", 24: "FOD 2T", 26: "TI trame",
                   27: "TI T-Chaine", 28: "TI T-TRAME", 29: "TI chaine", 3000: "inconnu"}
        data_1 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 13: [], 15: [], 24: [], 26: [], 27: [],
                  28: [], 29: [], 3000: []}
        data_2 = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 13: [], 15: [], 24: [], 26: [], 27: [],
                  28: [], 29: [], 3000: []}

        for e in data1:
            if not math.isnan(e[3]):  # si le défaut a été requalifié
                if e[3] in defects.keys():
                    data_1[e[3]].append([e[0], e[1]])
                else:
                    data_1[3000].append([e[0], e[1]])
            else:
                if e[2] in defects.keys():
                    data_1[e[2]].append([e[0], e[1]])
                else:
                    data_1[3000].append([e[0], e[1]])

        for e in data2:
            if not math.isnan(e[3]):  # si le défaut a été requalifié
                if e[3] in defects.keys():
                    data_2[e[3]].append([e[0], e[1]])
                else:
                    data_2[3000].append([e[0], e[1]])
            else:
                if e[2] in defects.keys():
                    data_2[e[2]].append([e[0], e[1]])
                else:
                    data_2[3000].append([e[0], e[1]])
        fig = go.Figure()
        for key in data_1.keys():
            data_1[key] = np.array(data_1[key])
            if len(data_1[key]) > 0:
                X = data_1[key][:, 0]
                Y = data_1[key][:, 1]
                fig.add_trace(go.Scatter(x=X,
                                         y=Y,
                                         mode='markers',
                                         name=defects[key],
                                         marker={"size": 5, "symbol": "circle", "color": "blue"}))

        for key in data_2.keys():
            data_2[key] = np.array(data_2[key])
            if len(data_2[key]) > 0:
                X = data_2[key][:, 0]
                Y = data_2[key][:, 1]
                fig.add_trace(go.Scatter(x=X,
                                         y=Y,
                                         mode='markers',
                                         name=defects[key],
                                         marker={"size": 5, "color": "red"}))
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.update_xaxes(nticks=20)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightPink')
        fig.update_yaxes(nticks=20)
        fig.update_layout(
            title=f"{name} rotation = {rotation} ",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"
            ))
        scatter = fig.data[0]
        return fig
