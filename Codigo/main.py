import dash.exceptions
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

LAYOUT = "layout-principal"

CONTENEDOR_01 = "contenedor-01"
CONTENEDOR_02 = "contenedor-02"
CONTENEDOR_03 = "contenedor-03"


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
UsuarioAplicacion = Usuario()
tipoGraficas = "Barras"

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
        html.Button('LOGIN', id=BOTON_GOTOLOGIN),
        html.Button('REGISTRO', id=BOTON_GOTOREGISTRO),
    ],
    style={'textAlign': 'center', 'margin': 'auto', 'padding': '50px'}
)
layoutInicioSesion = html.Div(
    className="app-div",
    children=[
        html.H1("Inicio de sesión"),
        html.Hr(),
        html.H2("Introduce usuario"),
    ],
    style={'textAlign': 'center', 'margin': 'auto', 'padding': '50px'}
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
                dbc.Col(html.Button('Continuar', id=BOTON_CONTINUAR_REGISTRO, style={'width': '200px'}),width="True", style={'textAlign': 'right'}),
            ], style={'textAlign': 'center'})
        ]),
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
        ]),
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
        ]),
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
        ]),
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
        ]),
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
        ]),
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
        dbc.Col(html.Button('Continuar', id=BOTON_TERMINAR_REGISTRO, style={'width': '200px', 'color': coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba']}),width="True", style={'textAlign': 'right'})
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
app.layout = html.Div([
    html.Div([
        dbc.Container([
                dbc.Row([
                    dbc.Col(html.I(id=BOTON_GOTOHOME, className='bi bi-house-door-fill'), style={'font-size': '2em'}, width="auto"),
                    dbc.Col(html.H1('ShadowSpect'), width="auto"),
                    dbc.Col(width=True),
                ], justify=True)
        ])
    ],style={"color": coloresFondo['textoBarraArriba'], 'backgroundColor': coloresFondo['backgroundBarraArriba']}),
    html.Div(
        id = LAYOUT,
        children=[
            layoutHome
        ],
    )
],
style={"color": coloresFondo['texto'], 'backgroundColor': coloresFondo['background'],'textAlign': 'center', 'margin': 'auto'})

# ----------------------------------------------------------------------------------
# Layout aplicación
layoutEjeccucion = html.Div(
    className="app-div",
    id = LAYOUT,
    children=[
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
    ]
)


# Volver al inicio
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOHOME, 'n_clicks')
)
def changeLayout(b1):
    estadoAplicacion = HOME
    return layoutHome

# Comenzar login
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOLOGIN, 'n_clicks')
)
def gotoLogin(nclicks):
    estadoAplicacion = INICIO_SESION
    return layoutInicioSesion

# Comenzar registro
@app.callback(
    Output(LAYOUT, "children"),
    Input(BOTON_GOTOREGISTRO, 'n_clicks')
)
def gotoRegister(nclicks):
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
def AcabarRegistro(nclicks, r):
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
    print(UsuarioAplicacion.gltInitResult)
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
    return layoutEjeccucion

# @app.callback(
#     Output(TEST, "children"),
#     Input(ANTERIOR_PREGUNTA, 'n_clicks'),
#     State(RESPUESTA, 'value'),
#     prevent_initial_call = True
# )
# def retrocederPregunta(nclicks, r):
#     if nclicks is None:
#         raise PreventUpdate
#     global ContadorPreguntas
#     print(r)
#     ContadorPreguntas -= 1
#     if ContadorPreguntas == 1:
#         if r is not None:
#             global Respuesta2
#             print(Respuesta2)
#             Respuesta2 = r
#             print(Respuesta2)
#         return pregunta1
#     elif ContadorPreguntas == 2:
#         if r is not None:
#             global Respuesta3
#             Respuesta3 = r
#         return pregunta2
#     elif ContadorPreguntas == 3:
#         if r is not None:
#             global Respuesta4
#             Respuesta4 = r
#         return pregunta3
#     elif ContadorPreguntas == 4:
#         if r is not None:
#             global Respuesta5
#             Respuesta5 = r
#         return pregunta4

# @app.callback(
#     Output(LAYOUT, "children"),
#     Input(BOTON_REGISTRO, 'n_clicks'),
#     [State(PREGUNTA1, 'value'),
#     State(PREGUNTA2, 'value'),
#     State(PREGUNTA3, 'value'),
#     State(PREGUNTA4, 'value'),],
#     prevent_initial_call = True
# )
# def comenzado(nclicks, p1, p2, p3, p4):
#     global estadoAplicacion
#     if p1 is None:
#         raise PreventUpdate
#     if p2 is None:
#         raise PreventUpdate
#     if p3 is None:
#         raise PreventUpdate
#     if p4 is None:
#         raise PreventUpdate
#     else:
#         UsuarioAplicacion.role = p1
#         UsuarioAplicacion.edad = p2
#         estadoAplicacion = EJECCUCION

# ----------------------------------------------------------------------------------
# Main
def main() -> None:
    app.run_server(debug=True)
    while True:
        estadoAplicacion = EJECCUCION
    
if __name__ == "__main__":
    main()