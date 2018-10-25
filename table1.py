import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import pandas as pd

FILENAME = "dbNSFP3.5a_variant.chrM"
COLUMN_NAMES = [""]
pd.set_option('display.max_columns', 300)

df = pd.read_csv("/bioinfo/dbNSFPv3.5a/" + FILENAME, sep='\t')
#df = df[COLUMN_NAMES]

df = df.head()

def generate_table(dataframe):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(len(dataframe))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='dbNSFP'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': u'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='MTL'
    ),
    generate_table(df),
])

if __name__ == '__main__':
    app.run_server(debug=True)
