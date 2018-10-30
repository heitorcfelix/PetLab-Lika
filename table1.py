import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import os
from dash.dependencies import Input, Output
from time import sleep

dbNSFP_DIRECTORY = "/bioinfo/dbNSFPv3.5a/"
COLUMN_NAMES = [""]
pd.set_option('display.max_columns', 300)

df1 = pd.read_csv("/bioinfo/dbNSFPv3.5a/" + "dbNSFP3.5a_variant.chrM", sep='\t')
#df1 = df1.head()
df2 = pd.read_csv("/bioinfo/dbNSFPv3.5a/" + "dbNSFP3.5a_variant.chrY", sep='\t')
df2 = df2.head()

#df = df[COLUMN_NAMES]

def generate_table(filename):
    if(filename == "dbNSFP3.5a_variant.chrM"):
        df = df1
    else:
        df = df2
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in df.columns])] +

        # Body
        [html.Tr([
            html.Td(df.iloc[i][col]) for col in df.columns
        ]) for i in range(len(df))]
    )

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
    html.Div(id='table-container')
])

@app.callback(Output('table-container', 'children'), [Input('my-dropdown', 'value')])
def update_table(value):
    return generate_table(value)

if __name__ == '__main__':
    app.run_server(debug=True)
