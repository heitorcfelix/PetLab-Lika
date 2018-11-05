import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot

dbNSFP_DIRECTORY = "/bioinfo/dbNSFPv3.5a/"
dbNSFP_FILENAME = "dbNSFP3.5a_variant.chr21"

df = pd.read_csv(dbNSFP_DIRECTORY + dbNSFP_FILENAME, sep='\t')
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
plot(fig, filename = 'parallelViz/' + dbNSFP_FILENAME + '.html')