import dash.exceptions
import numpy as np
from dash import Dash, dcc, html, no_update, ctx
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
DROPDOWN_GRUPOS = "dropdown-grupos"
# DROPDOWN_FORMATOS = "dropdown-formatos"
DROPDOWN_USUARIOS = "dropdown-usuarios"
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
BARRA_LATERAL = "barra-lateral"
BOTON_SECCION_1 = "boton-seccion-1"
BOTON_SECCION_2 = "boton-seccion-2"
BOTON_SECCION_3 = "boton-seccion-3"
BOTON_SECCION_4 = "boton-seccion-4"
BOTON_SECCION_5 = "boton-seccion-5"
BOTON_SECCION_6 = "boton-seccion-6"
BOTON_SECCION_7 = "boton-seccion-7"
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
tipoGraficas = "Barras"

# Contar tiempo seccion
TInicioSeccion = 0.0
TFinSeccion = 0.0
# Contar tiempo sesión
TinicioSesion = 0.0
TFinSesion = 0.0
# Número de clicks
nclicks_inicio = 0
nclicks_fin = 0
# Número de clicks cambios sección
nclicks_cambios_inicio = 0
nclicks_cambios_fin = 0
# Tiempo inactividad máximo
tiempoInMax = 0.0
TInicioInactividad = 0.0
TFinInactividad = 0.0
# Tiempo en cada sección
tSecciones = [0.0]*7

#Preguntas
ContadorPreguntas = 1
Respuesta1 = None
Respuesta2 = None
Respuesta3 = None
Respuesta4 = None
Respuesta5 = None
RespuestasCorrectas =["D", "C", "E", "D", "C"]

app = DashProxy(prevent_initial_callbacks=True, transforms=[MultiplexerTransform()], external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Probando"

# ----------------------------------------------------------------------------------
# Importar datos
DATOS = pd.read_csv("activityOutput.csv")

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
        dbc.Button('LOGIN', id=BOTON_GOTOLOGIN),
        dbc.Button('REGISTRO', id=BOTON_GOTOREGISTRO),
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
                     ], style={'font-size': '2em'}, width="auto"),
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
                     ], style={'font-size': '2em'}, width="auto"),
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
                        value = None,
                        multi=False,
                        style={'width':'500px'}
                    ),
                    html.H2("Age"),
                    dcc.Input(
                        id=REGEDAD,
                        placeholder = "Enter your age...",
                        type='number',
                        min=1,
                        max=100,
                        step=1,
                        value = None,
                        style={'width':'500px'}
                    ),
                    html.H2("Username"),
                    dcc.Input(
                        id=REGUNAME,
                        placeholder = "Enter your username...",
                        value = None,
                        style={'width':'500px'}
                    ),
                ], style={'font-size': '2em'}, width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_CONTINUAR_REGISTRO, style={'width': '200px'}),width="True", style={'textAlign': 'right'}),
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
                        value = None,
                        multi=False,
                        style={'width':'500px'}
                    ),
                    html.H2("Age"),
                    dcc.Input(
                        id=REGEDAD,
                        placeholder = "Enter your age...",
                        type='number',
                        min=1,
                        max=100,
                        step=1,
                        value = None,
                        style={'width':'500px'}
                    ),
                    html.H2("Username"),
                    dcc.Input(
                        id=REGUNAME,
                        placeholder = "Ya existe un usuario con este nombre",
                        value = None,
                        style={'width':'500px'}
                    ),
                ], style={'font-size': '2em'}, width="auto"),
                dbc.Col(dbc.Button('Continuar', id=BOTON_CONTINUAR_REGISTRO, style={'width': '200px'}),width="True", style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ], fluid=True),
    ],
    style={'textAlign': 'left', 'margin': 'auto', 'padding': '50px'}
)

pregunta1 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 1"),width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'), style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
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
            value = Respuesta1,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta2 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 2"),width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'), style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
            ], style={'width': True})
        ], fluid=True),
        html.Img(src="assets/test2.png"),
        dcc.Dropdown(
            id=RESPUESTA,
            placeholder="Elija una respuesta...",
            options=[
                {'label': "A) The student acceptance rate has grown over the years", 'value': "A"},
                {'label': "B) The number of accepted students has decreased over the years", 'value': "B"},
                {'label': "C) It was more difficult to be accepted to the program in 2007 than in previous years", 'value': "C"},
                {'label': "D) Based on the chart, the acceptance rate will decrease further in 2008", 'value': "D"},
                {'label': "E) None of the above", 'value': "E"},
            ],
            value = Respuesta2,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta3 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 3"),width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'), style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
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
            value = Respuesta3,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta4 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 4"),width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(id=SIGUIENTE_PREGUNTA, className='bi bi-arrow-right'), style={'font-size': '2em', 'color': coloresFondo['botonActivado']}, width="auto"),
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
            value = Respuesta4,
            multi=False,
            style={'textAlign': 'left'}
        ),
    ]
)
pregunta5 = html.Div(
    [
        dbc.Container([
            dbc.Row([
                dbc.Col(html.I(className='bi bi-arrow-left'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.H5("Pregunta 5"),width="auto"),
                dbc.Col(width=True),
                dbc.Col(html.I(className='bi bi-arrow-right'), style={'font-size': '2em', 'color': coloresFondo['botonDesactivado']}, width="auto"),
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
            value = Respuesta5,
            multi=False,
            style={'textAlign': 'left'}
        ),
        dbc.Col(dbc.Button('Continuar', id=BOTON_TERMINAR_REGISTRO, style={'width': '200px', 'color': coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba']}),width="True", style={'textAlign': 'right'})
    ]
)
layoutTest = html.Div(
    className="app-div",
    children=[
        html.H1("Graph Literacy Test"),
        html.Hr(),
        html.H4("Este test sirve para tomar una estimación inicial del nivel de entenidimiento de gráficos del usuario"),
        html.Div(
            id = TEST,
            children=[
                pregunta1
            ]
        )
    ],
    style={'textAlign': 'center', 'margin': 'auto', 'padding': '50px'}
)

layoutSeccion1 = html.Div()
layoutSeccion2 = html.Div()
layoutSeccion3 = html.Div()
layoutSeccion4 = html.Div()
layoutSeccion5 = html.Div()
layoutSeccion6 = html.Div()
layoutSeccion7 = html.Div()

# ----------------------------------------------------------------------------------
# Barchart
def barchartRender() -> html.Div:
    @app.callback(
        Output(BAR_CHART, "children"),
        [Input(DROPDOWN_GRUPOS, "value"),
        Input(DROPDOWN_USUARIOS, "value")]
    )
    def update_bar_chart(grupo: str, usuario:str) -> html.Div():
        global tipoGraficas
        usuarios_grupo = DATOS.query("group == @grupo").query("user == @usuario")
        if(tipoGraficas == "Barras"): fig = px.bar(usuarios_grupo, x="task_id", y="value", color="metric")
        if(tipoGraficas == "Funnel"): fig = px.funnel(usuarios_grupo, x="task_id", y="value", color="metric")
        if(tipoGraficas == "Cajas"): fig = px.box(usuarios_grupo, x="task_id", y="value", color="metric")
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
# Layout global
app.layout = html.Div(
    id = GLOBAL,
    children = [
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.Container([
                            dbc.Row([
                                dbc.Col(html.I(id=BOTON_GOTOHOME, className='bi bi-house-door-fill'), style={'font-size': '2em'}, width="auto"),
                                dbc.Col(html.H1('ShadowSpect Dashboard'), width="auto"),
                                dbc.Col(width=True),
                                dbc.Col(html.I(id=BOTON_CLOSE_SESSION, className='bi bi-power'), style={'font-size': '2em'}, width="auto")
                            ], justify=True)
                    ], fluid=True)
                    ]),
            ], width=True,style={"color": coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba']})
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
style={"color": coloresFondo['texto'], 'backgroundColor': coloresFondo['background'],'textAlign': 'center', 'margin': 'auto'})

# ----------------------------------------------------------------------------------
# Layout aplicación
layoutEjeccucion = html.Div(
    className="app-div",
    id = LAYOUT,
    children=[
        dbc.Container([
            dbc.Row([
                dbc.Col([html.Div(
                    id = BARRA_LATERAL,
                    children=[dbc.Container([
                        dbc.Row([
                            dbc.Stack([
                                html.H1(),
                                html.H1(),
                                dbc.Button('Seccion 1', id=BOTON_SECCION_1),
                                dbc.Button('Seccion 2', id=BOTON_SECCION_2),
                                dbc.Button('Seccion 3', id=BOTON_SECCION_3),
                                dbc.Button('Seccion 4', id=BOTON_SECCION_4),
                                dbc.Button('Seccion 5', id=BOTON_SECCION_5),
                                dbc.Button('Seccion 6', id=BOTON_SECCION_6),
                                dbc.Button('Seccion 7', id=BOTON_SECCION_7),
                            ], gap='3'),
                        ]
                        ),
                        dbc.Row([],
                            className="h-75")
                    ], fluid=True, style={"color": coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba'],'height':'100vh'})],
                ),], style={"color": coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba'],
                                   'textAlign': 'center'}, width={"size":2,"offset":0 }),
                dbc.Col([
                    html.Div(
                        id = GRAFICAS,
                        children =[
                        html.H1("GRAFICAS"),
                        html.Hr(),
                        html.Div(
                            id=CONTENEDOR_01,
                            className="contenedor-dropdown",
                            children=[
                                dropdownRender()
                            ]
                        ),
                        html.Div(
                            id=CONTENEDOR_03,
                            className="contenedor-dropdown",
                            children=[
                                dropdownRender3()
                            ]
                        ),
                        barchartRender()
                    ])
                ], width = True)
            ], justify= "start"),
        ], fluid=True)
    ]
)


def acabarRegistro():
    UltimasSesiones = np.array([-1.0, -1.0, -1, -1, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0])
    UltimasSesiones = np.vstack([UltimasSesiones, UltimasSesiones, UltimasSesiones, UltimasSesiones, UltimasSesiones])

    path = "usuarios/" + UsuarioAplicacion.name + ".txt"
    file = open(path, "wb")
    pickle.dump(UsuarioAplicacion, file)
    pickle.dump(UltimasSesiones, file)
    file.close()

def guardarInfUsuario():
    global TinicioSesion, TFinSesion, UsuarioAplicacion
    TFinSesion = time.time()
    tiempoTotal = TFinSesion - TinicioSesion

    path = "usuarios/" + UsuarioAplicacion.name + ".txt"
    file = open(path, "rb")
    UsuarioAplicacion = pickle.load(file)
    UltimasSesiones = pickle.load(file)
    file.close()

    if tiempoTotal < 5:
        return

    UltimasSesiones[1:5, :] = UltimasSesiones[0:4, :]
    global tiempoInMax, nclicks_inicio, nclicks_fin, nclicks_cambios_inicio, nclicks_cambios_fin, tSecciones
    nclicks = nclicks_fin - nclicks_inicio
    nCambSecc = nclicks_cambios_fin - nclicks_cambios_inicio

    # Guardamos el tiempo de la última sesión
    UltimasSesiones[0, 0] = tiempoTotal
    # Guardamos el tiempo de inactividad máximo
    UltimasSesiones[0, 1] = tiempoInMax
    # Guardamos el tiempo de inactividad máximo
    UltimasSesiones[0, 2] = nclicks
    # Guardamos el número de cambios de sección por minuto
    UltimasSesiones[0, 3] = nCambSecc
    # Guardamos el tiempo en cada sección
    UltimasSesiones[0, 4:11] = tSecciones

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
        print(UsuarioAplicacion.name)
        print(np.around(UltimasSesiones, decimals=3))

        global tSecciones, TInicioSeccion, seccionActual
        seccionActual = 1
        TInicioSeccion = time.time()
        tSecciones = [0.0]*7

        sesionesValidas = 5 - np.count_nonzero(UltimasSesiones[:, 0] == -1)
        if sesionesValidas == 0:
            global tipoGraficas
            if UsuarioAplicacion.gltInitResult < 5:
                tipoGraficas = "Barras"
            elif UsuarioAplicacion.gltInitResult < 7:
                tipoGraficas = "Cajas"
            elif UsuarioAplicacion.gltInitResult < 9:
                tipoGraficas = "Cajas"
            else:
                tipoGraficas = "Funnel"
            return True

        else:
            infoEntrenamiento = np.asarray([0]*13)
            infoEntrenamiento[0] = UsuarioAplicacion.age
            infoEntrenamiento[1] = UsuarioAplicacion.gltInitResult
            infoEntrenamiento[2:13] = np.mean(UltimasSesiones[0:sesionesValidas, :], axis=0)
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

        global TinicioSesion
        TinicioSesion = time.time()
        return layoutEjeccucion
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


#Contar tiempos test
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


#Contar tiempos test
TinicioPregunta = 0
TFinPregunta = 0

# Pasar al test
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_CONTINUAR_REGISTRO, 'n_clicks'),
    [State(REGROL, 'value'),
    State(REGEDAD, 'value'),
    State(REGUNAME, 'value'),],
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
    prevent_initial_call = True
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
    global tipoGraficas
    if UsuarioAplicacion.gltInitResult < 5:
        tipoGraficas = "Barras"
    elif UsuarioAplicacion.gltInitResult < 7:
        tipoGraficas = "Cajas"
    elif UsuarioAplicacion.gltInitResult < 9:
        tipoGraficas = "Cajas"
    else:
        tipoGraficas = "Funnel"

    acabarRegistro()
    global estadoAplicacion
    estadoAplicacion = EJECCUCION

    global TinicioSesion
    TinicioSesion = time.time()
    return layoutEjeccucion

# Cambiar sección
@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_1, 'n_clicks')
)
def irASeccion1(nclicks):
    global seccionActual
    if seccionActual != 1:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 1
        return layoutSeccion1

@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_2, 'n_clicks')
)
def irASeccion2(nclicks):
    global seccionActual
    if seccionActual != 2:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 2
        return layoutSeccion2

@app.callback(
    Output(GRAFICAS, "children"),
    Input(BOTON_SECCION_3, 'n_clicks')
)
def irASeccion3(nclicks):
    global seccionActual
    if seccionActual != 3:
        global TInicioSeccion, TFinSeccion, tSecciones
        TFinSeccion = time.time()
        tSecciones[seccionActual - 1] = tSecciones[seccionActual - 1] + (TFinSeccion - TInicioSeccion)
        TInicioSeccion = time.time()
        seccionActual = 3
        return layoutSeccion3

# ----------------------------------------------------------------------------------
# Main
def main() -> None:
    app.run_server(debug=True)
    
if __name__ == "__main__":
    main()