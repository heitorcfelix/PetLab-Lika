import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

dbNSFP_DIRECTORY = "/bioinfo/dbNSFPv3.5a/"
pd.set_option('display.max_columns', 300)

df = pd.read_csv("dbNSFP3.5a_variant.chrM", sep='\t')
df = df.loc[df['rs_dbSNP150'] != '.']

COLUMN_NAMES = [name for name in df if 'rankscore' in name]

df = df[COLUMN_NAMES[:4]]
df = df.replace('.', 0)
df = df.astype(float)

#intervalo da janela de visualizacao
constraintInterval = list([0.0,0.5])

#intervalo de valores exibidos
valuesRange = list([0.0,1.0])

#cores da escala (valor crescente): roxo, azul, ciano, verde, amarelo, vermelho
scale = colorscale = [[0,'#920099'],[0.2,'#006EFF'],[0.4,'#00FFDB'],[0.6,'#08CC00'],[0.8, '#EFFF00'], [1,'#FF3B00']]
lineConfig = dict(color = df[df.columns[0]], colorscale = scale)


#lista de ranges de cada coordenada e que parte do dataframe deve ser acessada para pegar os valores da mesma
listOfDimensions = list([
            dict(range = valuesRange,
                constraintrange = constraintInterval,
                label = 'Score1', values = df[df.columns[0]]),
            dict(range = valuesRange,
                 constraintrange = constraintInterval,
                label = 'Score2', values = df[df.columns[1]]),
            dict(range = valuesRange,
                 constraintrange = constraintInterval,
                label = 'Score3', values = df[df.columns[2]]),
            dict(range = valuesRange,
                 constraintrange = constraintInterval,
                label = 'Score4', values = df[df.columns[3]])
        ])

data = [
    go.Parcoords(line = lineConfig, dimensions = listOfDimensions)
]

layout = go.Layout(
    plot_bgcolor = '#FFFFFF',
    paper_bgcolor = '#FFFFFF'
)

fig = go.Figure(data = data, layout = layout)
plot(fig)

'''
def generate_table(filename):
    if(filename == "dbNSFP3.5a_variant.chrM"):
        df = df1
    else:
        df = df2
    return df.to_dict('records')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dropdown = [{"label": dbNSFP_file, "value": dbNSFP_file} for dbNSFP_file in os.listdir(dbNSFP_DIRECTORY) if "dbNSFP3.5a_variant.chr" in dbNSFP_file]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='dbNSFP'),
    dcc.Dropdown(
        options= sorted(dropdown, key=lambda k: k['label']),
        value='dbNSFP3.5a_variant.chrM',
	id='my-dropdown'
    ),
    dt.DataTable(
        rows = df1.to_dict('records'),
        columns = df1.columns,
        filterable = False,
        sortable = True,
        selected_row_indices = [],
        id='datatable'
    )
])

@app.callback(Output('datatable', 'rows'), [Input('my-dropdown', 'value')])
def update_table(value):
    return generate_table(value)

if __name__ == '__main__':
    app.run_server(debug=True)'''