import dash.exceptions
from dash import Dash, dcc, html, no_update
import plotly.express as px
import pandas as pd
import datetime
from dash.dependencies import Input, Output, State
import sys


# ----------------------------------------------------------------------------------
# IDS
DROPDOWN_GRUPOS = "dropdown-grupos"
DROPDOWN_FORMATOS = "dropdown-formatos"
DROPDOWN_USUARIOS = "dropdown-usuarios"
BAR_CHART = "bar-chart"
BOTON_COMIENZO = "boton-comienzo"
BOTON_CONTINUAR = "boton-continuar"
BOTON_SALIR = "boton-salir"
LAYOUT = "layout-principal"
CONTENEDOR_CUESTIONARIO = "contenedor-cuestionario"
PREGUNTA1 = "pregunta-uno"
PREGUNTA2 = "pregunta-dos"
PREGUNTA3 = "pregunta-tres"
PREGUNTA4 = "pregunta-cuatro"

# ----------------------------------------------------------------------------------
# ESTADOS
INICIO = 1
CUESTIONARIO = 2
EJECCUCION = 3
FIN = 4


# ----------------------------------------------------------------------------------
# Inicialización
estadoAplicacion = INICIO
app = Dash(__name__)

app.title = "Probando"


# ----------------------------------------------------------------------------------
# Importar datos
DATOS = pd.read_csv("activityOutput.csv")


# ----------------------------------------------------------------------------------
# Colores



# ----------------------------------------------------------------------------------
# Barchart
def barchartRender() -> html.Div:
    @app.callback(
        Output(BAR_CHART, "children"),
        [Input(DROPDOWN_GRUPOS, "value"),
        Input(DROPDOWN_USUARIOS, "value"),
        Input(DROPDOWN_FORMATOS, "value")]
    )
    def update_bar_chart(grupo: str, usuario:str, formato: str) -> html.Div():
        usuarios_grupo = DATOS.query("group == @grupo").query("user == @usuario")
        if(formato == "Barras"): fig = px.bar(usuarios_grupo, x="task_id", y="value", color="metric")
        if(formato == "Funnel"): fig = px.funnel(usuarios_grupo, x="task_id", y="value", color="metric")
        if(formato == "Cajas"): fig = px.box(usuarios_grupo, x="task_id", y="value", color="metric")
        return html.Div(dcc.Graph(figure=fig), id = BAR_CHART)
    
    return html.Div(id=BAR_CHART)


# ----------------------------------------------------------------------------------
# Dropdown
def dropdownRender() -> html.Div:
    grupos = DATOS['group'].unique()
    return html.Div(
        children=[
            html.H6("Grupo"),
            dcc.Dropdown(
                id=DROPDOWN_GRUPOS,
                options=[{"label": grupo, "value": grupo} for grupo in grupos],
                value=grupos[0],
                multi=False,
            )
        ]
    )
    
def dropdownRender2() -> html.Div:
    formatos = ["Barras", "Cajas", "Funnel"]
    return html.Div(
        children=[
            html.H6("Formato"),
            dcc.Dropdown(
                id=DROPDOWN_FORMATOS,
                options=[{"label": formato, "value": formato} for formato in formatos],
                value="Barras",
                multi=False,
            )
        ]
    )

def dropdownRender3() -> html.Div:
    @app.callback(
        Output(DROPDOWN_USUARIOS, "options"),
        Input(DROPDOWN_GRUPOS, "value")
    )
    def update_dropdown_usuarios(grupo: str) -> html.Div():
        return DATOS[(DATOS.group == grupo)]['user'].unique()
    
    @app.callback(
        Output(DROPDOWN_USUARIOS, "value"),
        Input(DROPDOWN_USUARIOS, "options")
    )
    def update_dropdown_usuarios(usuarios) -> html.Div():
        return usuarios[0]
    
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )


# ----------------------------------------------------------------------------------
# Layout
def cambiarLayout():
    if estadoAplicacion == INICIO:
        return html.Div(
            className="app-div",
            id = LAYOUT,
            children=[
                html.H1("INICIO"),
                html.Hr(),
                html.Button('Comenzar', id=BOTON_COMIENZO)
            ]
        )
    elif estadoAplicacion == CUESTIONARIO:
        return html.Div(
            className="app-div",
            id = LAYOUT,
            children=[
                html.H1("CUESTIONARIO"),
                html.Hr(),
                html.Button('Continuar', id=BOTON_COMIENZO),
            ]
        )
    elif estadoAplicacion == EJECCUCION:
        return html.Div(
            className="app-div",
            id = LAYOUT,
            children=[
                html.H1("GRAFICAS"),
                html.Hr(),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dropdownRender()
                    ]
                ),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dropdownRender2()
                    ]
                ),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dropdownRender3()
                    ]
                ),
                barchartRender()
            ]
        )
    else:
        return html.Div("ERROR")


app.layout = html.Div(
    className="app-div",
    id = LAYOUT,
    children=[
        html.H1("INICIO"),
        html.Hr(),
        html.Button('Comenzar', id=BOTON_COMIENZO)
    ]
)

@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_COMIENZO, 'n_clicks'),
    prevent_initial_call = True
)
def comenzado(nclicks):
    global estadoAplicacion
    if estadoAplicacion == INICIO:
        estadoAplicacion = CUESTIONARIO
        return [
            html.H1("CUESTIONARIO"),
            html.Hr(),
            html.Div(
                id = CONTENEDOR_CUESTIONARIO,
                children=[
                    dcc.Dropdown(
                        id = PREGUNTA1,
                        options=["1", "2","3"],
                        multi=False,
                    ),
                    dcc.Dropdown(
                        id=PREGUNTA2,
                        options=["1", "2", "3"],
                        multi=False,
                    ),
                    dcc.Dropdown(
                        id=PREGUNTA3,
                        options=["1", "2", "3"],
                        multi=False,
                    ),
                    dcc.Dropdown(
                        id=PREGUNTA4,
                        options=["1", "2", "3"],
                        multi=False,
                    )
                ],
            ),
            html.Button('Continuar', id=BOTON_COMIENZO),
        ]
    elif estadoAplicacion == CUESTIONARIO:
        return [
            html.H1("GRAFICAS"),
            html.Hr(),
            html.Div(
                className="contenedor-dropdown",
                children=[
                    dropdownRender()
                ]
            ),
            html.Div(
                className="contenedor-dropdown",
                children=[
                    dropdownRender2()
                ]
            ),
            html.Div(
                className="contenedor-dropdown",
                children=[
                    dropdownRender3()
                ]
            ),
            barchartRender()
        ]
    else:
        return []

# ----------------------------------------------------------------------------------
# Main
def main() -> None:
    app.run()
    
if __name__ == "__main__":
    main()