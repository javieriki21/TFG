import dash.exceptions
from dash import Dash, dcc, html, no_update
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
import sys

class Rol:
    PROFESOR = 0
    ESTUDIANTE = 1
    ANALISTA = 2

class ModeloUsuario:
    rol = Rol.PROFESOR
    edad = 0


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
CUESTIONARIO = 1
EJECCUCION = 2
FIN = 3


# ----------------------------------------------------------------------------------
# Inicialización
estadoAplicacion = CUESTIONARIO
UsuarioAplicacion = ModeloUsuario()

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
    if estadoAplicacion == CUESTIONARIO:
        return html.Div(
            className="app-div",
            id = LAYOUT,
            children=[
                html.H1("CUESTIONARIO"),
                html.Hr(),
                html.H2("Rol"),
                dcc.Dropdown(
                    id=PREGUNTA1,
                    placeholder="Enter your rol...",
                    options=[
                        {'label': "Profesor", 'value': Rol.PROFESOR},
                        {'label': "Estudiante", 'value': Rol.ESTUDIANTE},
                        {'label': "Analista", 'value': Rol.ANALISTA}
                    ],
                    value = None,
                    multi=False,
                ),
                html.H2("Edad"),
                dcc.Input(
                    id=PREGUNTA2,
                    placeholder = "Enter your age...",
                    type='number',
                    min=1,
                    max=100,
                    step=1,
                    value = None,
                    size = 0,
                ),
                html.Hr(),
                dcc.Dropdown(
                    id=PREGUNTA3,
                    options=["1", "2", "3"],
                    value = None,
                    multi=False,
                ),
                dcc.Dropdown(
                    id=PREGUNTA4,
                    options=["1", "2", "3"],
                    value = None,
                    multi=False,
                ),
                html.Button('Continuar', id=BOTON_COMIENZO),
            ]
        )
    elif estadoAplicacion == EJECCUCION:
        print(UsuarioAplicacion.rol)
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


app.layout = cambiarLayout

@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_COMIENZO, 'n_clicks'),
    [State(PREGUNTA1, 'value'),
    State(PREGUNTA2, 'value'),
    State(PREGUNTA3, 'value'),
    State(PREGUNTA4, 'value'),],
    prevent_initial_call = True
)
def comenzado(nclicks, p1, p2, p3, p4):
    global estadoAplicacion
    if p1 is None:
        raise PreventUpdate
    if p2 is None:
        raise PreventUpdate
    if p3 is None:
        raise PreventUpdate
    if p4 is None:
        raise PreventUpdate
    else:
        UsuarioAplicacion.rol = p1
        UsuarioAplicacion.edad = p2
        estadoAplicacion = EJECCUCION

# ----------------------------------------------------------------------------------
# Main
def main() -> None:
    app.run()
    
if __name__ == "__main__":
    main()