import dash.exceptions
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_extensions.enrich import DashProxy, MultiplexerTransform
from dash.dependencies import Input, Output, State
from usuario import Role
from usuario import Usuario
import time
import os
import pickle

# ----------------------------------------------------------------------------------
# IDS
DROPDOWN_INFO_PUZZLE = "dropdown-info-puzzle"
DROPDOWN_GRUPOS_ACTIVITY = "dropdown-grupos-a"
DROPDOWN_USUARIOS_ACTIVITY = "dropdown-usuarios-a"
DROPDOWN_GRUPOS_DIFFICULTY = "dropdown-grupos-d"
DROPDOWN_GRUPOS = "dropdown-grupos"
DROPDOWN_USUARIOS = "dropdown-usuarios"
DROPDOWN_USUARIOS2 = "dropdown-usuarios2"
DROPDOWN_USUARIOS3 = "dropdown-usuarios3"
DROPDOWN_USUARIOS4 = "dropdown-usuarios4"
DROPDOWN_USUARIOS5 = "dropdown-usuarios5"
DROPDOWN_USUARIOS6 = "dropdown-usuarios6"
DROPDOWN_USUARIOS7 = "dropdown-usuarios7"
DROPDOWN_USUARIOS8 = "dropdown-usuarios8"
DROPDOWN_USUARIOS9 = "dropdown-usuarios9"
BAR_CHART = "bar-chart"

BOTON_LOGIN = "boton-login"
BOTON_TERMINAR_LOGIN = "boton-terminar-login"

BOTON_REGISTRO = "boton-registro"
BOTON_CONTINUAR_REGISTRO = "boton-continuar-registro"
BOTON_TERMINAR_REGISTRO = "boton-terminar-registro"
REGEDAD = "registro-edad"
REGROL = "registro-rol"
REGUNAME = "registro-username"

TEST = "test"
ANTERIOR_PREGUNTA = "anterior-pregunta"
SIGUIENTE_PREGUNTA = "siguiente-pregunta"
PREGUNTA1 = "pregunta-uno"
PREGUNTA2 = "pregunta-dos"
PREGUNTA3 = "pregunta-tres"
PREGUNTA4 = "pregunta-cuatro"
PREGUNTA5 = "pregunta-cinco"
RESPUESTA = "respuesta"

BOTON_GOTOHOME = "boton-gotohome"
BOTON_GOTOLOGIN = "boton-gotologin"
BOTON_GOTOREGISTRO = "boton-gotoregistro"
BOTON_CLOSE_SESSION = "botn-cerrar-sesion"

LAYOUT = "layout-principal"
GLOBAL = "layout-global"

CONTENEDOR_01 = "contenedor-01"
CONTENEDOR_02 = "contenedor-02"
CONTENEDOR_03 = "contenedor-03"
CONTENEDOR_04 = "contenedor-04"
CONTENEDOR_05 = "contenedor-05"
CONTENEDOR_06 = "contenedor-06"
CONTENEDOR_07 = "contenedor-07"
CONTENEDOR_08 = "contenedor-08"
CONTENEDOR_09 = "contenedor-09"
CONTENEDOR_PUZZLE = "contenedor-puzzle"

BOTON_MAS_01 = "boton-mas-01"
BOTON_MAS_02 = "boton-mas-02"
BOTON_MAS_03 = "boton-mas-03"
BOTON_MAS_04 = "boton-mas-04"
BOTON_MAS_05 = "boton-mas-05"
BOTON_MAS_06 = "boton-mas-06"
BOTON_MAS_07 = "boton-mas-07"
BOTON_MAS_08 = "boton-mas-08"
BOTON_MAS_09 = "boton-mas-09"
BOTON_GLOBAL_INFO = "boton-global-info"

BARRA_LATERAL = "barra-lateral"
BOTON_SECCION_1 = "boton-seccion-1"
BOTON_SECCION_2 = "boton-seccion-2"
BOTON_SECCION_3 = "boton-seccion-3"
BOTON_SECCION_4 = "boton-seccion-4"
GRAFICAS = "graficas"

# ----------------------------------------------------------------------------------
# ESTADOS
HOME = 0
INICIO_SESION = 1
REGISTRO = 2
EJECCUCION = 3
FIN = 4

# ----------------------------------------------------------------------------------
# Inicialización
estadoAplicacion = HOME
seccionActual = 1
UsuarioAplicacion = Usuario()

tipoGraficas = 2
nGraficasSeccion = 4
addAyuda = True
contenidoSimplificado = True
navegacionAnidada = True

# Contar tiempo seccion
TInicioSeccion = 0.0
TFinSeccion = 0.0
# Contar tiempo sesión
# Número de clicks
nclicks_inicio = 0
nclicks_fin = 0
# Número de clicks cambios sección
nclicks_cambio_seccion = 0
# Tiempo inactividad máximo
tiempoInMax = 0.0
TUltimoClick = 0.0
# Tiempo en cada sección
tSecciones = [0.0] * 4

# Preguntas
ContadorPreguntas = 1
Respuesta1 = None
Respuesta2 = None
Respuesta3 = None
Respuesta4 = None
Respuesta5 = None
RespuestasCorrectas = ["D", "C", "E", "D", "C"]

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()],
                external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Probando"

# ----------------------------------------------------------------------------------
# Importar datos
DATOS = pd.read_csv("activityOutput.csv")
datosFunnelUser = pd.read_csv("funnelOutput.csv")
datosFunnelPuzzle = pd.read_csv("pruebaBinarioV2.csv")
total_puzzles = 30
datosFunnelUser = pd.read_csv("funnelOutput.csv")
# datosFunnelPuzzle$level_puzzle <- factor(datosFunnelPuzzle$level_puzzle, levels = c("Basic Puzzles", "Intermediate Puzzles","Advanced Puzzles")) ## En ese factor falta poner todos los niveles en el orden de la plataforma de los puzles
# datosFunnelPuzzle<-datosFunnelPuzzle%>% filter(level_puzzle != "SAND")

dfSequence = pd.read_csv("sequenceOutput.csv")
dfActivity = pd.read_csv("activityOutput.csv")
# dfActivity<-dfActivity%>% filter(level_puzzle != "SAND")
datosDiff = pd.read_csv("levelsOfDifficultyOutput.csv")
seqWithinDf = pd.read_csv("seqWPOutput.csv")
commonErrorsDf = pd.read_csv("commonOutput.csv")
datosCompetencyELO = pd.read_csv("datosCompetencyELO_normalized.csv")
datosDifficultyELO = pd.read_csv("datosDifficultyELO_normalized.csv")

# ----------------------------------------------------------------------------------
# Colores
coloresTemaClaro = {
    'background': '#FFFFF',
    'backgroundBarraArriba': '#0063bb',
    'textoBarraArriba': '#FFFFFF',
    'texto': '#000000',
    'botonDesactivado': '#D3D3D3',
    'botonActivado': '#0063bb',
}

coloresTemaOscuro = {
    'background': '#000000',
    'backgroundBarraArriba': '#00001A',
    'textoBarraArriba': '#FFFFFF',
    'texto': '#111111'
}

coloresFondo = coloresTemaClaro
coloresGraficas1 = [
    '#7FDBFF'
]
coloresGraficas = coloresGraficas1

colors = {
    'col1': '#7FDBFF',
    'col2': '#7FDBFF',
    'col3': '#7FDBFF',
    'col1': '#7FDBFF',
    'col1': '#7FDBFF',

}

# ----------------------------------------------------------------------------------
# Layouts Inicio
layoutHome = html.Div(
    className="app-div",
    children=[
        html.H1("BIENVENIDO"),
        dbc.Container([
            dbc.Row([
                dbc.Col(width=True),
                dbc.Col(dbc.Button('LOGIN', id=BOTON_GOTOLOGIN)),
                dbc.Col(width=1),
                dbc.Col(dbc.Button('REGISTER', id=BOTON_GOTOREGISTRO)),
                dbc.Col(width=True)
            ], justify='center')
        ])
    ],
    style={'textAlign': 'center', 'margin': 'auto', 'padding': '60px'}
)
layoutInicioSesion = html.Div(
    className="app-div",
    children=[
        dbc.Container([
            dbc.Row([html.H1("LOGIN"), html.Hr()], style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    html.H2("Username"),
                    dcc.Input(
                        id=REGUNAME,
                        placeholder="Enter your username...",
                        value=None,
                        style={'width': '500px'}
                    ),
                ], width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_TERMINAR_LOGIN, style={'width': '200px'}), width="True",
                        style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ], fluid=True),
    ],
    style={'textAlign': 'left', 'margin': 'auto', 'padding': '50px'}
)

layoutInicioSesionError = html.Div(
    className="app-div",
    children=[
        dbc.Container([
            dbc.Row([html.H1("LOGIN"), html.Hr()], style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([
                    html.H2("Username"),
                    dcc.Input(
                        id=REGUNAME,
                        placeholder="No existe usuario con ese nombre",
                        value=None,
                        style={'width': '500px'}
                    ),
                ], width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_TERMINAR_LOGIN, style={'width': '200px'}), width="True",
                        style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ], fluid=True),
    ],
    style={'textAlign': 'left', 'margin': 'auto', 'padding': '50px'}
)

layoutRegistro = html.Div(
    className="app-div",
    children=[
        dbc.Container([
            dbc.Row([html.H1("REGISTRO"), html.Hr()], style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([html.H2("Role"),
                         dcc.Dropdown(
                             id=REGROL,
                             placeholder="Enter your role...",
                             options=[
                                 {'label': "Profesor", 'value': Role.PROFESOR},
                                 {'label': "Estudiante", 'value': Role.ESTUDIANTE},
                                 {'label': "Director", 'value': Role.DIRECTOR}
                             ],
                             value=None,
                             multi=False,
                             style={'width': '500px'}
                         ),
                         html.H2("Age"),
                         dcc.Input(
                             id=REGEDAD,
                             placeholder="Enter your age...",
                             type='number',
                             min=1,
                             max=100,
                             step=1,
                             value=None,
                             style={'width': '500px'}
                         ),
                         html.H2("Username"),
                         dcc.Input(
                             id=REGUNAME,
                             placeholder="Enter your username...",
                             value=None,
                             style={'width': '500px'}
                         ),
                         ], width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_CONTINUAR_REGISTRO, style={'width': '200px'}), width="True",
                        style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ], fluid=True),
    ],
    style={'textAlign': 'left', 'margin': 'auto', 'padding': '50px'}
)

layoutRegistroError = html.Div(
    className="app-div",
    children=[
        dbc.Container([
            dbc.Row([html.H1("REGISTRO"), html.Hr()], style={'textAlign': 'center'}),
            dbc.Row([
                dbc.Col([html.H2("Role"),
                         dcc.Dropdown(
                             id=REGROL,
                             placeholder="Enter your role...",
                             options=[
                                 {'label': "Profesor", 'value': Role.PROFESOR},
                                 {'label': "Estudiante", 'value': Role.ESTUDIANTE},
                                 {'label': "Director", 'value': Role.DIRECTOR}
                             ],
                             value=None,
                             multi=False,
                             style={'width': '500px'}
                         ),
                         html.H2("Age"),
                         dcc.Input(
                             id=REGEDAD,
                             placeholder="Enter your age...",
                             type='number',
                             min=1,
                             max=100,
                             step=1,
                             value=None,
                             style={'width': '500px'}
                         ),
                         html.H2("Username"),
                         dcc.Input(
                             id=REGUNAME,
                             placeholder="Ya existe un usuario con este nombre",
                             value=None,
                             style={'width': '500px'}
                         ),
                         ], width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_CONTINUAR_REGISTRO, style={'width': '200px'}), width="True",
                        style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ], fluid=True),
    ],
    style={'textAlign': 'left', 'margin': 'auto', 'padding': '50px'}
)

pregunta1 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 1"), width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'),
                        style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test1.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) 20ºF", 'value': "A"},
                {'label': "B) 80ºF", 'value': "B"},
                {'label': "C) 70ºF", 'value': "C"},
                {'label': "D) 60ºF", 'value': "D"},
                {'label': "E) 50ºF", 'value': "E"},
            ],
            value=Respuesta1,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta2 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 2"), width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'),
                        style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test2.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) The student acceptance rate has grown over the years", 'value': "A"},
                {'label': "B) The number of accepted students has decreased over the years", 'value': "B"},
                {'label': "C) It was more difficult to be accepted to the program in 2007 than in previous years",
                 'value': "C"},
                {'label': "D) Based on the chart, the acceptance rate will decrease further in 2008", 'value': "D"},
                {'label': "E) None of the above", 'value': "E"},
            ],
            value=Respuesta2,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta3 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 3"), width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'),
                        style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test3.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) 42%", 'value': "A"},
                {'label': "B) 8%", 'value': "B"},
                {'label': "C) 30%", 'value': "C"},
                {'label': "D) 15%", 'value': "D"},
                {'label': "E) 2.5%", 'value': "E"},
            ],
            value=Respuesta3,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta4 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 4"), width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'),
                        style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test4.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) 14%", 'value': "A"},
                {'label': "B) 30%", 'value': "B"},
                {'label': "C) 28%", 'value': "C"},
                {'label': "D) 34%", 'value': "D"},
                {'label': "E) 24%", 'value': "E"},
            ],
            value=Respuesta4,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta5 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 5"), width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(className='bi bi-arrow-right'),
                        style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test5.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) February", 'value': "A"},
                {'label': "B) April", 'value': "B"},
                {'label': "C) July", 'value': "C"},
                {'label': "D) September", 'value': "D"},
                {'label': "E) November", 'value': "E"},
            ],
            value=Respuesta5,
            multi=False,
            style={'textAlign': 'left'}
        ),
        dbc.Col(dbc.Button('Continuar', id=BOTON_TERMINAR_REGISTRO,
                           style={'width': '200px', 'color': coloresFondo['textoBarraArriba'],
                                  'backgroundColor': coloresFondo['backgroundBarraArriba']}), width="True",
                style={'textAlign': 'right'})
    ]
)
layoutTest = html.Div(
    className="app-div",
    children=[
        html.H1("Graph Literacy Test"),
        html.Hr(),
        html.H4(
            "Este test sirve para tomar una estimación inicial del nivel de entenidimiento de gráficos del usuario"),
        html.Div(
            id=TEST,
            children=[
                pregunta1
            ]
        )
    ],
    style={'textAlign': 'center', 'margin': 'auto', 'padding': '50px'}
)


# ----------------------------------------------------------------------------------
# Gráficas

def activityRender() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_01, "children"),
    [Input(DROPDOWN_GRUPOS_ACTIVITY, "value"),
     Input(DROPDOWN_USUARIOS_ACTIVITY, "value")],
)
def update_activity_chart(grupo: str, usuario: str) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    usuarios_grupo = dfActivity.query("group == @grupo").query("user == @usuario")
    metrica = "event"
    eventos = usuarios_grupo.query("metric == @metrica")
    metrica = "active_time"
    tiempoActivo = usuarios_grupo.query("metric == @metrica")
    metrica = "different_events"
    distintosEventos = usuarios_grupo.query("metric == @metrica")

    xValues = eventos.iloc[:]["task_id"]

    if tipoGraficas == 0:
        fig1 = px.bar(distintosEventos, x=xValues, y="value", color=xValues)
        fig2 = px.bar(eventos, x=xValues, y="value", color=xValues)
        fig3 = px.bar(tiempoActivo, x=xValues, y="value", color=xValues)
    elif tipoGraficas ==1:
        fig1 = px.line(distintosEventos, x=xValues, y="value", markers=True)
        fig2 = px.line(eventos, x=xValues, y="value", markers=True)
        fig3 = px.line(tiempoActivo, x=xValues, y="value", markers=True)
    else:
        fig1 = px.pie(distintosEventos, names=xValues, values="value")
        fig2 = px.pie(eventos, names=xValues, values="value")
        fig3 = px.pie(tiempoActivo, names=xValues, values="value")

    fig1.update_layout(
        title="Different events",
        xaxis_title = "",
        yaxis_title="Number of events",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig2.update_layout(
        title="Total events",
        xaxis_title = "",
        yaxis_title="Number of events",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig3.update_layout(
        title="Active time",
        xaxis_title = "",
        yaxis_title="Time (seconds)",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )

    if not navegacionAnidada:
        return html.Div(
            id=BAR_CHART,
            children = [
                dbc.Container([
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig1)]),
                        dbc.Col([dcc.Graph(figure=fig2)]),
                    ]),
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig3)]),
                    ])
                ])
            ]
        )
    else:
        return html.Div(
            id=BAR_CHART,
            children=[
                dbc.Container([
                    dbc.Row([
                        dbc.Col([dcc.Graph(figure=fig1)]),
                        dbc.Col([dcc.Graph(figure=fig2)]),
                        dbc.Col([dcc.Graph(figure=fig3)]),
                    ]),
                    dbc.Row([
                        dbc.Col([
                            html.Div(
                                children=[
                                    html.H6("Puzzle"),
                                    dcc.Dropdown(
                                        id=DROPDOWN_INFO_PUZZLE,
                                        options=xValues,
                                        multi=False,
                                        clearable=True,
                                    )
                                ]
                            )
                        ])
                    ]),
                    dbc.Row([
                        html.Div(
                            id = CONTENEDOR_PUZZLE,
                            children=[]
                        )
                    ])
                ])
            ]
        )
@app.callback(
    Output(CONTENEDOR_PUZZLE, "children"),
    [Input(DROPDOWN_INFO_PUZZLE, "value"),
     Input(DROPDOWN_USUARIOS_ACTIVITY, "value")]
)
def update_puzzle(puzzle: str, usuario:str) -> html.Div():
    global tipoGraficas
    valores = dfActivity.query("user == @usuario").query("task_id == @puzzle")
    metricas = ["snapshot", "paint", "rotate_view", "move_shape", "scale_shape", "create_shape", "delete_shape", "undo_action", "redo_action"]

    yValues = [valores.iloc[3]["value"], valores.iloc[4]["value"],valores.iloc[5]["value"], valores.iloc[6]["value"], valores.iloc[7]["value"], valores.iloc[8]["value"], valores.iloc[9]["value"], valores.iloc[10]["value"], valores.iloc[11]["value"]]
    if tipoGraficas == 0:
        fig1 = px.bar(metricas, x=metricas, y=yValues, color=metricas)
    else:
        fig1 = px.pie(metricas, names=metricas, values=yValues, color=metricas)

    fig1.update_layout(
        title="Type of events events",
        xaxis_title="Type of event",
        yaxis_title="Number of events",
        legend_title="Type"
    )
    return [dcc.Graph(figure=fig1)]

def difficultyRender() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_01, "children"),
    [Input(DROPDOWN_GRUPOS_DIFFICULTY, "value"),
     Input(BOTON_GLOBAL_INFO, "n_clicks")],
)
def update_difficulty_chart(grupo: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if grupo is None:
        raise PreventUpdate

    if not navegacionAnidada:
        nclicks = 0

    dificultad=datosDiff.fillna(0)

    if nclicks % 2 == 0:
        dificultad = dificultad.query("group == @grupo")
    else:
        dificultad = dificultad.groupby(["task_id"]).mean()
        dificultad["task_id"]=dificultad.index

    if tipoGraficas == 0 or tipoGraficas == 1:
        fig1 = px.bar(dificultad, x="task_id", y="completed_time", color="completed_time")
        fig2 = px.bar(dificultad, x="task_id", y="actions_completed", color="actions_completed")
        fig3 = px.bar(dificultad, x="task_id", y="p_incorrect", color="p_incorrect")
        fig4 = px.bar(dificultad, x="task_id", y="p_abandoned", color="p_abandoned")
        fig5 = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")
    else:
        fig1 = px.line(dificultad, x="task_id", y="completed_time", markers=True)
        fig2 = px.line(dificultad, x="task_id", y="actions_completed", markers=True)
        fig3 = px.line(dificultad, x="task_id", y="p_incorrect", markers=True)
        fig4 = px.line(dificultad, x="task_id", y="p_abandoned", markers=True)
        fig5 = px.line(dificultad, x="task_id", y="norm_all_measures", markers=True)
    fig1.update_layout(
        title="Active time",
        xaxis_title="",
        yaxis_title="",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig2.update_layout(
        title="Number of actions",
        xaxis_title="",
        yaxis_title="",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig3.update_layout(
        title="Percentage incorrect",
        xaxis_title="",
        yaxis_title="",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig4.update_layout(
        title="Percentage abandoned",
        xaxis_title="",
        yaxis_title="",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )
    fig5.update_layout(
        title="General difficulty meassure",
        xaxis_title="",
        yaxis_title="",
        legend_title="Puzzles",
        xaxis={'showticklabels': False}
    )

    if nclicks % 2 == 0:
        if contenidoSimplificado:
            return html.Div(
                id=BAR_CHART,
                children = [
                    dbc.Container([
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig1)]),
                            dbc.Col([dcc.Graph(figure=fig2)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig5)]),
                        ])
                    ])
                ]
            )
        else:
            return html.Div(
                id=BAR_CHART,
                children = [
                    dbc.Container([
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig1)]),
                            dbc.Col([dcc.Graph(figure=fig2)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig3)]),
                            dbc.Col([dcc.Graph(figure=fig4)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig5)]),
                        ])
                    ])
                ]
            )
    else:
        if contenidoSimplificado:
            return html.Div(
                id=BAR_CHART,
                children = [
                    html.H2("All groups global mean"),
                    dbc.Container([
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig1)]),
                            dbc.Col([dcc.Graph(figure=fig2)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig5)]),
                        ])
                    ])
                ]
            )
        else:
            return html.Div(
                id=BAR_CHART,
                children = [
                    html.H2("All groups global mean"),
                    dbc.Container([
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig1)]),
                            dbc.Col([dcc.Graph(figure=fig2)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig3)]),
                            dbc.Col([dcc.Graph(figure=fig4)]),
                        ]),
                        dbc.Row([
                            dbc.Col([dcc.Graph(figure=fig5)]),
                        ])
                    ])
                ]
            )

def funnelRender() -> html.Div:
    return html.Div(id=BAR_CHART)

@app.callback(
    Output(CONTENEDOR_01, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS, "value"),
     Input(BOTON_MAS_01, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15,15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started" ,"Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color = yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)

        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        tam = [5] * len(xValues)

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"], size = tam)

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()
def funnelRender2() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_02, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS2, "value"),
     Input(BOTON_MAS_02, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()

def funnelRender3() -> html.Div:
    return html.Div(id=BAR_CHART)

@app.callback(
    Output(CONTENEDOR_03, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS3, "value"),
     Input(BOTON_MAS_03, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()


def funnelRender4() -> html.Div:
    return html.Div(id=BAR_CHART)

@app.callback(
    Output(CONTENEDOR_04, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS4, "value"),
     Input(BOTON_MAS_04, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()

def funnelRender5() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_05, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS5, "value"),
     Input(BOTON_MAS_05, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()
def funnelRender6() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_06, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS6, "value"),
     Input(BOTON_MAS_06, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()
def funnelRender7() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_07, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS7, "value"),
     Input(BOTON_MAS_07, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()

def funnelRender8() -> html.Div:
    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_08, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS8, "value"),
     Input(BOTON_MAS_08, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()

def funnelRender9() -> html.Div:

    return html.Div(id=BAR_CHART)
@app.callback(
    Output(CONTENEDOR_09, "children"),
    [Input(DROPDOWN_GRUPOS, "value"),
     Input(DROPDOWN_USUARIOS9, "value"),
     Input(BOTON_MAS_09, "n_clicks")],
)
def update_bar_chart(grupo: str, usuario: str, nclicks: int) -> html.Div():
    global tipoGraficas
    global contenidoSimplificado
    global navegacionAnidada
    global seccionActual

    if not navegacionAnidada:
        nclicks = 0

    if usuario is None or grupo is None:
        raise PreventUpdate

    if usuario == "":
        return html.Div()

    if seccionActual == 1 and nclicks % 2 == 0:
        usuarios_grupo = datosFunnelUser.query("group == @grupo").query("user == @usuario")
        xValues = ["Started", "Create shape", "Submitted", "Completed"]

        yValues = [usuarios_grupo.iloc[0]["started"], usuarios_grupo.iloc[0]["create_shape"],
                   usuarios_grupo.iloc[0]["submitted"], usuarios_grupo.iloc[0]["completed"]]
        if contenidoSimplificado:
            xValues = [xValues[0], xValues[3]]
            yValues = [yValues[0], yValues[3]]

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x=xValues, y=yValues, color=xValues, range_y=[0, 30])
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        elif tipoGraficas == 1:
            fig = px.funnel(usuarios_grupo, x=yValues, y=xValues, range_x=[-15, 15])
            fig.update_layout(
                title="Puzzles completados",
                yaxis_title="Estado del puzzle",
                xaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        else:
            xValues.insert(0, "Total")
            yValues.insert(0, 30)
            if not contenidoSimplificado:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started", "Create shape", "Submitted"],
                    value=yValues
                )
            else:
                data = dict(
                    character=xValues,
                    parent=["", "Total", "Started"],
                    value=yValues
                )
            fig = px.sunburst(
                data,
                names='character',
                parents='parent',
                values='value',
                color=xValues,
                branchvalues="total",
            )
            fig.update_layout(
                title="Puzzles completados",
                xaxis_title="Estado del puzzle",
                yaxis_title="Número de puzzles",
                legend_title="Estado"
            )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 1:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")

        tasks = dfActivity.query("task_id != @cadenaError").iloc[:]["task_id"].unique()
        yValues = [0] * len(tasks)
        for i in range(0, len(tasks)):
            idTask = tasks[i]
            estados = usuarios_grupo.query("task_id == @idTask")
            if len(estados) == 0:
                yValues[i] = "Not started"
            elif len(estados) == 1:
                if contenidoSimplificado:
                    if estados.iloc[0]["funnel"] == "completed":
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    yValues[i] = estados.iloc[0]["funnel"]
            else:
                funnels = estados.iloc[:]["funnel"]
                if contenidoSimplificado:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    else:
                        yValues[i] = "started"
                else:
                    if "completed" in funnels:
                        yValues[i] = "completed"
                    elif "submitted" in funnels:
                        yValues[i] = "submitted"
                    elif "create_shape" in funnels:
                        yValues[i] = "shape_created"
                    else:
                        yValues[i] = "started"
        categories_ordered = np.array(
            ["completed", "submitted", "shape_created", "started", "Not started"])

        fig = px.bar(usuarios_grupo, x=tasks, y=yValues, color=yValues, category_orders={"y": categories_ordered})
        fig.update_layout(
            title="Puzzles completados",
            xaxis_title="Puzzle",
            yaxis_title="Estado",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2 and nclicks % 2 == 0:
        cadenaError = "Unnecessary"
        usuarios_grupo = dfSequence.query("user == @usuario").query("task_id != @cadenaError")
        dificultad = datosDiff.query("group == @grupo")

        xValues = usuarios_grupo.iloc[:]["sequence"]
        yValues = [0] * len(xValues)
        for i in range(0, len(yValues)):
            idTask = usuarios_grupo.iloc[i]["task_id"]
            dif = dificultad.loc[dificultad['task_id'] == idTask]
            dif = dif.iloc[0]["norm_all_measures"]
            if tipoGraficas == 0:
                yValues[i] = max(dif, 0.02)
            else:
                yValues[i] = dif

        colorPuzzles = usuarios_grupo.iloc[:]["funnel"]

        if contenidoSimplificado:
            for i in range(0, len(colorPuzzles)):
                if colorPuzzles.iloc[i] != "completed":
                    colorPuzzles.iloc[i] = "started"

        if tipoGraficas == 0:
            fig = px.bar(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])
        else:
            fig = px.scatter(usuarios_grupo, x="sequence", y=yValues, color=colorPuzzles, hover_data=["task_id"])

        fig.update_layout(
            title="Secuencia entre puzzles",
            xaxis_title="Número de secuencia",
            yaxis_title="Dificultad",
            legend_title="Estados"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    elif seccionActual == 2:
        dificultad = datosDiff.query("group == @grupo")

        fig = px.bar(dificultad, x="task_id", y="norm_all_measures", color="norm_all_measures")

        fig.update_layout(
            title="Dificultad de los puzzles",
            xaxis_title="Puzzle",
            yaxis_title="Dificultad",
            legend_title="Dificultad"
        )
        return html.Div(dcc.Graph(figure=fig), id=BAR_CHART)
    else:
        return html.Div()

# ----------------------------------------------------------------------------------
# Dropdown
def dropdownGrupos() -> html.Div:
    grupos = DATOS['group'].unique()
    return html.Div(
        children=[
            html.H6("Grupo"),
            dcc.Dropdown(
                id=DROPDOWN_GRUPOS,
                options=[{"label": grupo, "value": grupo} for grupo in grupos],
                multi=False,
                placeholder='Selecciona grupo...',
            )
        ]
    )

def dropdownGruposActivity() -> html.Div:
    grupos = DATOS['group'].unique()
    return html.Div(
        children=[
            html.H6("Grupo"),
            dcc.Dropdown(
                id=DROPDOWN_GRUPOS_ACTIVITY,
                options=[{"label": grupo, "value": grupo} for grupo in grupos],
                multi=False,
                placeholder='Selecciona grupo...',
            )
        ]
    )
def dropdownGruposDifficulty() -> html.Div:
    grupos = DATOS['group'].unique()
    return html.Div(
        children=[
            html.H6("Grupo"),
            dcc.Dropdown(
                id=DROPDOWN_GRUPOS_DIFFICULTY,
                options=[{"label": grupo, "value": grupo} for grupo in grupos],
                multi=False,
                placeholder='Selecciona grupo...',
            )
        ]
    )

# def dropdownRender2() -> html.Div:
#     formatos = ["Barras", "Cajas", "Funnel"]
#     return html.Div(
#         children=[
#             html.H6("Formato"),
#             dcc.Dropdown(
#                 id=DROPDOWN_FORMATOS,
#                 options=[{"label": formato, "value": formato} for formato in formatos],
#                 value="Barras",
#                 multi=False,
#             )
#         ]
#     )
@app.callback(
    Output(DROPDOWN_USUARIOS_ACTIVITY, "options"),
    Input(DROPDOWN_GRUPOS_ACTIVITY, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()

@app.callback(
    Output(DROPDOWN_USUARIOS_ACTIVITY, "value"),
    Input(DROPDOWN_USUARIOS_ACTIVITY, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    return usuarios[0]
def dropdownUsuariosActivity() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS_ACTIVITY,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )
def dropdownUsuarios() -> html.Div:


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

def dropdownUsuarios2() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS2,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )
@app.callback(
    Output(DROPDOWN_USUARIOS2, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()

@app.callback(
    Output(DROPDOWN_USUARIOS2, "value"),
    Input(DROPDOWN_USUARIOS2, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 1:
        return usuarios[1]
    else:
        return ""

def dropdownUsuarios3() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS3,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )

@app.callback(
    Output(DROPDOWN_USUARIOS3, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()

@app.callback(
    Output(DROPDOWN_USUARIOS3, "value"),
    Input(DROPDOWN_USUARIOS3, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 2:
        return usuarios[2]
    else:
        return ""
def dropdownUsuarios4() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS4,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )
@app.callback(
    Output(DROPDOWN_USUARIOS4, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()

@app.callback(
    Output(DROPDOWN_USUARIOS4, "value"),
    Input(DROPDOWN_USUARIOS4, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 3:
        return usuarios[3]
    else:
        return ""

def dropdownUsuarios5() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS5,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )
@app.callback(
    Output(DROPDOWN_USUARIOS5, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()


@app.callback(
    Output(DROPDOWN_USUARIOS5, "value"),
    Input(DROPDOWN_USUARIOS5, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 4:
        return usuarios[4]
    else:
        return ""

def dropdownUsuarios6() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS6,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )

@app.callback(
    Output(DROPDOWN_USUARIOS6, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()


@app.callback(
    Output(DROPDOWN_USUARIOS6, "value"),
    Input(DROPDOWN_USUARIOS6, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 5:
        return usuarios[5]
    else:
        return ""

def dropdownUsuarios7() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS7,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )

@app.callback(
    Output(DROPDOWN_USUARIOS7, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()


@app.callback(
    Output(DROPDOWN_USUARIOS7, "value"),
    Input(DROPDOWN_USUARIOS7, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 6:
        return usuarios[6]
    else:
        return ""

def dropdownUsuarios8() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS8,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )

@app.callback(
    Output(DROPDOWN_USUARIOS8, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()


@app.callback(
    Output(DROPDOWN_USUARIOS8, "value"),
    Input(DROPDOWN_USUARIOS8, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 7:
        return usuarios[7]
    else:
        return ""

def dropdownUsuarios9() -> html.Div:
    return html.Div(
        children=[
            html.H6("Usuario"),
            dcc.Dropdown(
                id=DROPDOWN_USUARIOS9,
                multi=False,
                clearable=True,
                placeholder='Selecciona usuario...',
            )
        ]
    )

@app.callback(
    Output(DROPDOWN_USUARIOS9, "options"),
    Input(DROPDOWN_GRUPOS, "value")
)
def update_dropdown_usuarios(grupo: str) -> html.Div():
    return DATOS[(DATOS.group == grupo)]['user'].unique()


@app.callback(
    Output(DROPDOWN_USUARIOS9, "value"),
    Input(DROPDOWN_USUARIOS9, "options")
)
def update_dropdown_usuarios(usuarios) -> html.Div():
    if len(usuarios) > 8:
        return usuarios[8]
    else:
        return ""

def getColorBoton():
    if navegacionAnidada:
        return "primary"
    else:
        return "secondary"

def getTextoBoton():
    if navegacionAnidada:
        return "+"
    else:
        return ""

def getTextoBoton2():
    if navegacionAnidada:
        return "View global"
    else:
        return ""

# Layouts secciones
def lSeccion1() -> html.Div:
    global nGraficasSeccion
    if nGraficasSeccion == 1:
        return html.Div(
            children=[
                html.H1("Dashboard"),
                html.Hr(),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dbc.Container([
                            dbc.Row([
                                dbc.Col(dropdownGrupos()),
                                dbc.Col(dropdownUsuarios()),
                                dbc.Col(dbc.Button(getTextoBoton(), id=BOTON_MAS_01, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)
                            ], justify=True)
                        ], fluid=True)
                    ]),
                html.Div(
                    id=CONTENEDOR_01,
                    className="contenedor-dropdown",
                    children=[
                        funnelRender()
                    ]
                ),
            ]
        )
    elif nGraficasSeccion == 4:
        return html.Div(
            children=[
                html.H1("Dashboard"),
                html.Hr(),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dbc.Container([
                            dbc.Row(dropdownGrupos()),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_01, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_01,
                                                children=[funnelRender()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios2(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_02, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_02,
                                                children=[funnelRender2()]
                                            )
                                        ]
                                    ),
                                ),
                            ], justify=True),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios3(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_03, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_03,
                                                children=[funnelRender3()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios4(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_04, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_04,
                                                children=[funnelRender4()]
                                            )
                                        ]
                                    ),
                                ),
                            ], justify=True),
                        ], fluid=True)
                    ]),
            ]
        )
    else:
        return html.Div(
            children=[
                html.H1("Dashboard"),
                html.Hr(),
                html.Div(
                    className="contenedor-dropdown",
                    children=[
                        dbc.Container([
                            dbc.Row(dropdownGrupos()),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios(), width=True),
                                                    dbc.Col(dbc.Button(getTextoBoton(), id=BOTON_MAS_01, className="ms-auto",
                                                                       n_clicks=0, color = getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_01,
                                                children=[funnelRender()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios2(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_02, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_02,
                                                children=[funnelRender2()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios3(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_03, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_03,
                                                children=[funnelRender3()]
                                            )
                                        ]
                                    ),
                                ),
                            ], justify=True),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios4(), width=True),
                                                    dbc.Col(dbc.Button(getTextoBoton(), id=BOTON_MAS_04, className="ms-auto",
                                                                       n_clicks=0, color = getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_04,
                                                children=[funnelRender4()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios5(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_05, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_05,
                                                children=[funnelRender5()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios6(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_06, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_06,
                                                children=[funnelRender6()]
                                            )
                                        ]
                                    ),
                                ),
                            ], justify=True),
                            dbc.Row([
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios7(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_07, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_07,
                                                children=[funnelRender7()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios8(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_08, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_08,
                                                children=[funnelRender8()]
                                            )
                                        ]
                                    ),
                                ),
                                dbc.Col(
                                    html.Div(
                                        className="contenedor-dropdown",
                                        children=[
                                            dbc.Container([
                                                dbc.Row([
                                                    dbc.Col(dropdownUsuarios9(), width=True),
                                                    dbc.Col(
                                                        dbc.Button(getTextoBoton(), id=BOTON_MAS_09, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=1)

                                                ])
                                            ]),
                                            html.Div(
                                                id=CONTENEDOR_09,
                                                children=[funnelRender9()]
                                            )
                                        ]
                                    ),
                                ),
                            ], justify=True),
                        ], fluid=True)
                    ]),
            ]
        )
def lSeccion2() -> html.Div:
    return html.Div(
        children=[
            html.H1("Dashboard"),
            html.Hr(),
            html.Div(
                children=[
                    dbc.Container([
                        dbc.Row([
                            dbc.Col(dropdownGruposActivity()),
                            dbc.Col(dropdownUsuariosActivity())
                        ], justify=True)
                    ], fluid=True)
                ]),
            html.Div(
                id=CONTENEDOR_01,
                className="contenedor-dropdown",
                children=[
                    activityRender()
                ]
            ),
        ]
    )
def lSeccion3() -> html.Div:
    return html.Div(
        children=[
            html.H1("Dashboard"),
            html.Hr(),
            html.Div(
                className="contenedor-dropdown",
                children=[
                    dbc.Container([
                        dbc.Row([
                            dbc.Col(dropdownGruposDifficulty(), width=True),
                            dbc.Col(dbc.Button(getTextoBoton2(), id=BOTON_GLOBAL_INFO, className="ms-auto",
                                                                   n_clicks=0, color=getColorBoton()), width=2)
                        ], justify=True)
                    ], fluid=True)
                ]),
            html.Div(
                id=CONTENEDOR_01,
                className="contenedor-dropdown",
                children=[
                    activityRender()
                ]
            ),
        ]
    )


# Modal ayuda
def contenidoModal():
    return "Seleccione un grupo y un usuario dentro de ese grupo para observar su progreso.\n\n La gráfica contiene 4 barras. Estas barras representarán respectivamente el número de puzzles comenzados por el alumno, el número de puzzles en los que el alumnos ha creado al menos una figura, el número de puzzles entregados y el número de puzzles completados."

def comentariosAyuda():
    global addAyuda
    if addAyuda:
        return html.Div([
            html.Div(
                [
                    dbc.Modal(
                        [
                            dbc.ModalHeader(dbc.ModalTitle("Ayuda")),
                            dbc.ModalBody(contenidoModal()),
                            dbc.ModalFooter(
                                dbc.Button(
                                    "Close", id="close", className="ms-auto", n_clicks=0
                                )
                            ),
                        ],
                        id="modal",
                        is_open=False,
                    ),
                ]
            ),
            dbc.Button("Ayuda", id="open", n_clicks=0),
        ])
    else:
        return html.Div()


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# ----------------------------------------------------------------------------------
# Layout global
app.layout = html.Div(
    id=GLOBAL,
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Container([
                            dbc.Row([
                                dbc.Col(html.I(id=BOTON_GOTOHOME, className='bi bi-house-door-fill'),
                                        style={'font-size': '2em'}, width="auto"),
                                dbc.Col(html.H1('ShadowSpect Dashboard'), width="auto"),
                                dbc.Col(width=True),
                                dbc.Col(html.I(id=BOTON_CLOSE_SESSION, className='bi bi-power'),
                                        style={'font-size': '2em'}, width="auto")
                            ], justify=True)
                        ], fluid=True)
                    ]),
                ], width=True, style={"color": coloresFondo['textoBarraArriba'],
                                      'backgroundColor': coloresFondo['backgroundBarraArriba']})
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        id=LAYOUT,
                        children=[
                            layoutHome
                        ],
                    )
                ], width=True)
            ], justify="start"),
        ], fluid=True)

    ],
    style={"color": coloresFondo['texto'], 'backgroundColor': coloresFondo['background'], 'textAlign': 'center',
           'margin': 'auto'})

# ----------------------------------------------------------------------------------
# Layout aplicación
def layoutEjecucion():
    return html.Div(
        className="app-div",
        id=LAYOUT,
        children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col([html.Div(
                        id=BARRA_LATERAL,
                        children=[dbc.Container([
                            dbc.Row([
                                dbc.Stack([
                                    html.H1(),
                                    html.H1(),
                                    dbc.Button('Funnel', id=BOTON_SECCION_1),
                                    dbc.Button('Sequence between puzzles', id=BOTON_SECCION_2),
                                    dbc.Button('Levels of activity', id=BOTON_SECCION_3),
                                    dbc.Button('Levels of difficulty', id=BOTON_SECCION_4),
                                ], gap='3'),
                            ]
                            ),
                            dbc.Row([],
                                    className="h-75")
                        ], fluid=True, style={"color": coloresFondo['textoBarraArriba'],
                                              'backgroundColor': coloresFondo['backgroundBarraArriba'],
                                              'height': '100vh'})],
                    ), ], style={"color": coloresFondo['textoBarraArriba'],
                                 'backgroundColor': coloresFondo['backgroundBarraArriba'],
                                 'textAlign': 'center'}, width={"size": 2, "offset": 0}),
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.Div(
                                    id=GRAFICAS,
                                    children=[
                                        lSeccion1()
                                    ]
                                )
                            ], width=True),
                        ]),
                        dbc.Row([
                            dbc.Col([
                                html.Div(
                                    children=[
                                        comentariosAyuda()
                                    ]
                                )
                            ], align="end", width=True)
                        ], align="end")
                    ], width=True)
                ], justify="start"),
            ], fluid=True)
        ]
    )


def acabarRegistro():
    UltimasSesiones = np.array([-1.0, -1.0, -1, -1, -1.0, -1.0, -1.0, -1.0])
    UltimasSesiones = np.vstack([UltimasSesiones, UltimasSesiones, UltimasSesiones, UltimasSesiones, UltimasSesiones])

    path = "usuarios/" + UsuarioAplicacion.name + ".txt"
    file = open(path, "wb")
    pickle.dump(UsuarioAplicacion, file)
    pickle.dump(UltimasSesiones, file)
    file.close()


def guardarInfUsuario():
    global tSecciones, UsuarioAplicacion, TFinSeccion, seccionActual, TInicioSeccion
    TFinSeccion = time.time()
    tSecciones[seccionActual-1] += (TFinSeccion - TInicioSeccion)


    path = "usuarios/" + UsuarioAplicacion.name + ".txt"
    file = open(path, "rb")
    UsuarioAplicacion = pickle.load(file)
    UltimasSesiones = pickle.load(file)
    file.close()

    tiempoTotal = tSecciones[0]+tSecciones[1]+tSecciones[2]+tSecciones[3]

    UltimasSesiones[1:5, :] = UltimasSesiones[0:4, :]
    global tiempoInMax, nclicks_inicio, nclicks_fin, nclicks_cambio_seccion
    nclicks = nclicks_fin - nclicks_inicio

    # Guardamos el tiempo de la última sesión
    UltimasSesiones[0, 0] = tiempoTotal
    # Guardamos el tiempo de inactividad máximo
    UltimasSesiones[0, 1] = tiempoInMax
    # Guardamos el tiempo de inactividad máximo
    UltimasSesiones[0, 2] = nclicks
    # Guardamos el número de cambios de sección por minuto
    UltimasSesiones[0, 3] = nclicks_cambio_seccion
    # Guardamos el tiempo en cada sección
    UltimasSesiones[0, 4:8] = tSecciones / np.sum(tSecciones)

    path = "usuarios/" + UsuarioAplicacion.name + ".txt"
    file = open(path, "wb")
    pickle.dump(UsuarioAplicacion, file)
    pickle.dump(UltimasSesiones, file)
    file.close()


def iniciarSesion(nombre):
    path = "usuarios/" + nombre + ".txt"
    if (os.path.isfile(path)):
        global UsuarioAplicacion
        file = open(path, "rb")
        UsuarioAplicacion = pickle.load(file)
        UltimasSesiones = pickle.load(file)

        global TUltimoClick
        TUltimoClick = time.time()

        global tSecciones, TInicioSeccion, seccionActual
        seccionActual = 1
        TInicioSeccion = time.time()
        tSecciones = [0.0] * 4

        global nclicks_cambio_seccion
        nclicks_cambio_seccion = 0

        global tipoGraficas
        sesionesValidas = 5 - np.count_nonzero(UltimasSesiones[:, 0] == -1)
        if sesionesValidas == 0:
            if UsuarioAplicacion.gltInitResult < 5:
                tipoGraficas = 0
            elif UsuarioAplicacion.gltInitResult < 7:
                tipoGraficas = 1
            elif UsuarioAplicacion.gltInitResult < 9:
                tipoGraficas = 1
            else:
                tipoGraficas = 2
            return True

        else:
            infoEntrenamiento = np.asarray([0] * 10)
            infoEntrenamiento[0] = UsuarioAplicacion.age
            infoEntrenamiento[1] = UsuarioAplicacion.gltInitResult
            infoEntrenamiento[2:10] = np.mean(UltimasSesiones[0:sesionesValidas, :], axis=0)

            infoEntrenamiento[2] = 1200
            infoEntrenamiento[3] = 120
            infoEntrenamiento[4] = 4
            infoEntrenamiento[5] = 0.1
            infoEntrenamiento[6] = 0.8
            infoEntrenamiento[7] = 0.05
            infoEntrenamiento[8] = 0.1
            infoEntrenamiento[9] = 0.05


            path = "modelos/" + "ModeloCuadrosAyuda.txt"
            file = open(path, "rb")
            modelCA = pickle.load(file)

            path = "modelos/" + "ModeloNGraficasSeccion.txt"
            file = open(path, "rb")
            modelNGS = pickle.load(file)

            path = "modelos/" + "ModeloNavegacion.txt"
            file = open(path, "rb")
            modelNAV = pickle.load(file)

            path = "modelos/" + "ModeloDificultadGraficas.txt"
            file = open(path, "rb")
            modelDG = pickle.load(file)

            path = "modelos/" + "ModeloContenidoSimplificado.txt"
            file = open(path, "rb")
            modelSIMP = pickle.load(file)


            r1 = modelCA.predict(infoEntrenamiento.reshape(1, -1))
            r2 = modelNGS.predict(infoEntrenamiento.reshape(1, -1))
            r3 = modelNAV.predict(infoEntrenamiento.reshape(1, -1))
            r4 = modelDG.predict(infoEntrenamiento.reshape(1, -1))
            r5 = modelSIMP.predict(infoEntrenamiento.reshape(1, -1))

            global addAyuda, nGraficasSeccion, navegacionAnidada, contenidoSimplificado
            if r1[0] == 1:
                addAyuda = True
            else:
                addAyuda = False

            print("Añadir cuadros de ayuda")
            print(addAyuda)
            print("")

            if r2[0] == 0:
                nGraficasSeccion = 1
            elif r2[0] == 1:
                nGraficasSeccion = 4
            else:
                nGraficasSeccion = 9

            print("Número de gráficas por sección")
            print(nGraficasSeccion)
            print("")

            if r3[0] == 1:
                navegacionAnidada = True
            else:
                navegacionAnidada = False

            print("Navegación con contenido extendido")
            print(navegacionAnidada)
            print("")

            tipoGraficas = int(r4[0])

            print("Formato de las gráficas (0-2)")
            print(tipoGraficas)
            print("")

            if r5[0] == 1:
                contenidoSimplificado = True
            else:
                contenidoSimplificado = False

            print("Simplificar contenido")
            print(contenidoSimplificado)
            print("")

            # nGraficasSeccion = 4
            # contenidoSimplificado = True
            # addAyuda = False
            # navegacionAnidada = True
            # tipoGraficas = 0

            return True

    else:
        return False

#
@app.callback(
    Output(GLOBAL, "children"),
    Input(GLOBAL, 'n_clicks')
)
def contarClicks(n):
    global nclicks_fin, nclicks_inicio, estadoAplicacion
    if estadoAplicacion == EJECCUCION:
        nclicks_fin = n
        global TUltimoClick, tiempoInMax
        if (time.time() - TUltimoClick) > tiempoInMax:
            tiempoInMax = time.time() - TUltimoClick
        TUltimoClick = time.time()

    else:
        nclicks_inicio = n
    raise PreventUpdate


# Volver al inicio
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOHOME, 'n_clicks')
)
def goHome(b1):
    global estadoAplicacion
    if estadoAplicacion == EJECCUCION:
        guardarInfUsuario()
    estadoAplicacion = HOME
    return layoutHome


# Comenzar login
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOLOGIN, 'n_clicks')
)
def gotoLogin(nclicks):
    global estadoAplicacion
    estadoAplicacion = INICIO_SESION
    return layoutInicioSesion


# Terminar Login
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_TERMINAR_LOGIN, 'n_clicks'),
    State(REGUNAME, 'value'),
)
def AcabarLogin(nclicks, r):
    if r is None:
        raise PreventUpdate
    if iniciarSesion(str(r)):
        global estadoAplicacion
        estadoAplicacion = EJECCUCION

        return layoutEjecucion()
    else:
        return layoutInicioSesionError


# Cerrar sesión
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_CLOSE_SESSION, 'n_clicks'),
)
def cerrarSesion(nclicks):
    global estadoAplicacion
    if estadoAplicacion == EJECCUCION:
        guardarInfUsuario()
        estadoAplicacion = HOME

        return layoutHome
    else:
        raise PreventUpdate


# Contar tiempos test
TinicioPregunta = 0
TFinPregunta = 0


# Comenzar registro
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOREGISTRO, 'n_clicks')
)
def gotoRegister(nclicks):
    global estadoAplicacion
    estadoAplicacion = REGISTRO
    return layoutRegistro


# Contar tiempos test
TinicioPregunta = 0
TFinPregunta = 0


# Pasar al test
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_CONTINUAR_REGISTRO, 'n_clicks'),
    [State(REGROL, 'value'),
     State(REGEDAD, 'value'),
     State(REGUNAME, 'value'), ],
)
def continuarRegistro(nclicks, c1, c2, c3):
    global estadoAplicacion
    if c1 is None:
        raise PreventUpdate
    if c2 is None:
        raise PreventUpdate
    if c3 is None:
        raise PreventUpdate
    path = "usuarios/" + str(c3) + ".txt"
    if (os.path.isfile(path)):
        return layoutRegistroError
    else:
        UsuarioAplicacion.role = c1
        UsuarioAplicacion.age = c2
        UsuarioAplicacion.name = c3
        global ContadorPreguntas
        ContadorPreguntas = 1
        global TinicioPregunta
        TinicioPregunta = time.time()
        UsuarioAplicacion.gltInitResult = 0

        return layoutTest


@app.callback(
    Output(TEST, "children"),
    Input(SIGUIENTE_PREGUNTA, 'n_clicks'),
    State(RESPUESTA, 'value'),
    prevent_initial_call=True
)
def avanzarPregunta(nclicks, r):
    if nclicks is None:
        raise PreventUpdate
    global ContadorPreguntas

    global TinicioPregunta
    global TFinPregunta
    TFinPregunta = time.time()
    if r is not None:
        if r == RespuestasCorrectas[ContadorPreguntas - 1]:
            if (TFinPregunta - TinicioPregunta) < 30:
                UsuarioAplicacion.gltInitResult += 2
            else:
                UsuarioAplicacion.gltInitResult += 1
    TinicioPregunta = time.time()

    ContadorPreguntas += 1
    if ContadorPreguntas == 2:
        return pregunta2
    elif ContadorPreguntas == 3:
        return pregunta3
    elif ContadorPreguntas == 4:
        return pregunta4
    elif ContadorPreguntas == 5:
        return pregunta5


@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_TERMINAR_REGISTRO, 'n_clicks'),
    State(RESPUESTA, 'value'),
)
def EndRegistro(nclicks, r):
    if nclicks is None:
        raise PreventUpdate
    global UsuarioAplicacion
    global TinicioPregunta
    global TFinPregunta
    TFinPregunta = time.time()
    if r is not None:
        if r == RespuestasCorrectas[4]:
            if (TFinPregunta - TinicioPregunta) < 30:
                UsuarioAplicacion.gltInitResult += 2
            else:
                UsuarioAplicacion.gltInitResult += 1
    UsuarioAplicacion.gltInitResult = UsuarioAplicacion.gltInitResult

    UsuarioAplicacion.gltInitResult = 9
    print(UsuarioAplicacion.gltInitResult)

    global tipoGraficas
    global contenidoSimplificado
    contenidoSimplificado = False
    global navegacionAnidada
    navegacionAnidada = False
    global nGraficasSeccion
    nGraficasSeccion = 1

    if UsuarioAplicacion.gltInitResult < 5:
        tipoGraficas = 0
        contenidoSimplificado = True
    elif UsuarioAplicacion.gltInitResult < 7:
        tipoGraficas = 1
    elif UsuarioAplicacion.gltInitResult < 9:
        tipoGraficas = 1
        nGraficasSeccion = 4
    else:
        tipoGraficas = 2
        nGraficasSeccion = 4
        navegacionAnidada = True

    global addAyuda
    addAyuda = True

    global TUltimoClick
    TUltimoClick = time.time()

    global TInicioSeccion
    TInicioSeccion = time.time()

    global tSecciones
    tSecciones = [0.0] * 4

    acabarRegistro()
    global estadoAplicacion
    estadoAplicacion = EJECCUCION

    global nclicks_cambio_seccion
    nclicks_cambio_seccion = 0

    return layoutEjecucion()


# Cambiar sección
@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_1, 'n_clicks'),
    prevent_initial_call=True
)
def irASeccion1(nclicks):
    global seccionActual
    if nclicks is None:
        raise PreventUpdate
    if seccionActual != 1:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 1

        global nclicks_cambio_seccion
        nclicks_cambio_seccion += 1

        return lSeccion1()
    else:
        raise PreventUpdate


@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_2, 'n_clicks'),
    prevent_initial_call=True
)
def irASeccion2(nclicks):
    global seccionActual
    if nclicks is None:
        raise PreventUpdate
    if seccionActual != 2:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 2

        global nclicks_cambio_seccion
        nclicks_cambio_seccion += 1

        return lSeccion1()
    else:
        raise PreventUpdate


@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_3, 'n_clicks'),
    prevent_initial_call=True
)
def irASeccion3(nclicks):
    global seccionActual
    if nclicks is None:
        raise PreventUpdate
    if seccionActual != 3:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 3

        global nclicks_cambio_seccion
        nclicks_cambio_seccion += 1

        return lSeccion2()
    else:
        raise PreventUpdate


@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_4, 'n_clicks'),
    prevent_initial_call=True

)
def irASeccion4(nclicks):
    global seccionActual
    if nclicks is None:
        raise PreventUpdate
    if seccionActual != 4:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 4

        global nclicks_cambio_seccion
        nclicks_cambio_seccion += 1

        return lSeccion3()
    else:
        raise PreventUpdate


# ----------------------------------------------------------------------------------
# Main
def main() -> None:
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
