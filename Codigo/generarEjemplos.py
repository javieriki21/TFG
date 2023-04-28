import numpy
import numpy as np
import random
import pandas as pd
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
)
import pickle

np.random.seed(1000)
n = 100000

#-------------------------------------------------------------------------------------------------------------
# ENTRADAS
print("INICIO GENERACIÓN DATOS")

# Tiempo total en la aplicación
tiempoTotal = np.random.normal(3000, 1800, n)
# Tiempo máximo seguido en el que el usuario ha estado inactivo
tiempoInactividadMaximo = np.random.normal(25, 20, n)
# Número de clicks por minuto promedio
nclicks_min = np.random.normal(15, 10, n)
# Cambios de sección por minuto promedio
cambiosSeccion_min = np.random.lognormal(0, 0.5, n)
# Resultado del test original
scoreInicial = np.around(np.random.normal(5, 2, n))
# Edad del usuario
edad = np.random.normal(40, 10, n)

# Diferentes porcentajes de tiempo en cada sección
tSecciones = [0,0,0,0,0,0,0]
for i in range(n):
    tiempoSecciones = [random.uniform(0, 1) for _ in range(7)]
    tiempoSecciones /= numpy.sum(tiempoSecciones)
    tSecciones = numpy.vstack([tSecciones, tiempoSecciones])
tSecciones = tSecciones[1:,:]

# Juntar en un dataset
data = np.hstack([np.column_stack([edad, scoreInicial, tiempoTotal, tiempoInactividadMaximo, nclicks_min, cambiosSeccion_min]), tSecciones])
#np.savetxt('DatosEjemplo.txt', data)
df = pd.DataFrame(data, columns=['edad', 'Resultado del test', 'Tiempo total', 'Tiempo de inactividad máximo', 'Número de clicks por minuto',  'Cambios de sección por minuto',  '% de tiempo en 1ª sección', '% de tiempo en 2ª sección', '% de tiempo en 3ª sección', '% de tiempo en 4ª sección', '% de tiempo en 5ª sección', '% de tiempo en 6ª sección', '% de tiempo en 7ª sección'])
print("ACABADA GENERACIÓN DATOS")
print("-------------------------------------------------------------------------------------------------------------")


#-------------------------------------------------------------------------------------------------------------
# SALIDAS

# Para cada salida se tiene en cuenta varios parámetros para determinar el output de esa salida
print("INICIO CÁLCULO SALIDAS")
ayudas = [True] * len(data)
n_graficas = [1] * len(data)
tipo_graficas = ['Simple'] * len(data)
navegacion = ['Rapida'] * len(data)
for i in range(0, len(data)):
    # -------------------------------------------------------------------------------
    # Probabilidad de que el usuario necesitara comentarios de ayuda
    prob_Add_Ayuda = 0.1
    # Número de gráficos en pantalla. Se calcula entre 0 y 1 y números bajos indican menos gráficas a la vez.
    prob_Num_Graficas = 0
    # Dificultad de las gráficas. Se calcula entre 0 y 1 y números bajos indican gráficas más fáciles de comprender.
    prob_Tipo_Graficas = 0.2
    # Tipo de navegación. Se calcula entre 0 y 1 y números bajos indican navegación más intuitiva y números más altos navegación más polivalente.
    prob_Navegacion = 0.5

    # Tener en cuenta su resultado del test
    resultadoTest = data[i,1]
    if resultadoTest < 5:
        prob_Add_Ayuda += 0.6
        prob_Num_Graficas -= 0.5
        prob_Tipo_Graficas -= 0.4
        prob_Navegacion -= 0.3
    elif resultadoTest < 7:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas -= 0.1
        prob_Tipo_Graficas += 0.1
    elif resultadoTest < 9:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.1
        prob_Tipo_Graficas += 0.15
        prob_Navegacion += 0.1
    else:
        prob_Add_Ayuda -= 0.5
        prob_Num_Graficas += 0.6
        prob_Tipo_Graficas += 0.3
        prob_Navegacion += 0.3

    # Tener en cuenta el máximo tiempo que el usuario se haya quedado inactivo
    tiempo_Inactivc = data[i, 3]
    if tiempo_Inactivc < 20:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.2
        prob_Tipo_Graficas += 0.1
        prob_Navegacion += 0.1
    elif tiempo_Inactivc > 45:
        prob_Add_Ayuda += 0.2
        prob_Num_Graficas -= 0.3
        prob_Tipo_Graficas -= 0.3
        prob_Navegacion -= 0.4

    # Tener en cuenta el número de clicks por minuto
    num_clicks = data[i, 4]
    if num_clicks < 3 or num_clicks > 25:
        prob_Add_Ayuda += 0.2
        prob_Num_Graficas -= 0.2
        prob_Tipo_Graficas -= 0.2
        prob_Navegacion -= 0.3
    else:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.2
        prob_Tipo_Graficas += 0.2
        prob_Navegacion += 0.2

    # Tener en cuenta el número de cambios de sección por minuto
    n_secciones = data[i, 5]
    if n_secciones > 3:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas -= 0.2
        prob_Tipo_Graficas -= 0.1
        prob_Navegacion += 0.1
    elif n_secciones < 0.1:
        prob_Add_Ayuda += 0.05
        prob_Num_Graficas -= 0.1
        prob_Tipo_Graficas -= 0.2
        prob_Navegacion -= 0.2
    else:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.1
        prob_Tipo_Graficas += 0.2
        prob_Navegacion += 0.1

    # Tener en cuenta el tiempo en diferentes secciones. En este caso se tiene en cuenta la desviación típica para ver si hay mucha diferencia.
    # Además, se puede tener en cuenta el tiempo en diferentes tareas para realizar diferentes tareas.
    t_secciones = data[i, 6: 13]
    # print(numpy.std(t_secciones))
    if numpy.std(t_secciones) > 0.1:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas -= 0.1
        prob_Tipo_Graficas -= 0.1
        prob_Navegacion -= 0.1
    else:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.1
        prob_Tipo_Graficas -= 0.15
        prob_Navegacion += 0.1

    # Tener en cuenta la edad del usuario
    edades = data[i,0]
    if edades < 30:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas += 0.05
        prob_Tipo_Graficas -= 0.1
        prob_Navegacion += 0.1
    elif edades > 60:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas -= 0.05
        prob_Tipo_Graficas += 0.1
        prob_Navegacion -= 0.1
    else:
        prob_Add_Ayuda -= 0.1
        prob_Num_Graficas += 0.05
        prob_Tipo_Graficas += 0.1
        prob_Navegacion += 0.1

    # Tener en cuenta el tiempo en la aplicación
    tTotal = data[i, 2]
    if tTotal > 7200:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas += 0.1
        prob_Tipo_Graficas -= 0.1
        prob_Navegacion += 0.1
    elif tTotal < 300:
        prob_Add_Ayuda += 0.1
        prob_Num_Graficas -= 0.1
        prob_Tipo_Graficas -= 0.1
        prob_Navegacion += 0.1

    # Se decide si añadir cuadros de ayuda
    addAyuda = False
    if prob_Add_Ayuda > 0.7:
        addAyuda = True
    ayudas[i] = addAyuda

    # Se decide el número de gráficas por sección
    if (prob_Num_Graficas <= 0.5):
        n_graficas[i] = 0
    elif (prob_Num_Graficas <= 0.8):
        n_graficas[i] = 1
    else:
        n_graficas[i] = 2

    # Se decide el tipo de gráficas a usar
    if (prob_Tipo_Graficas <= 0.4):
        tipo_graficas[i] = 0
    elif (prob_Tipo_Graficas <= 0.7):
        tipo_graficas[i] = 1
    else:
        tipo_graficas[i] = 2

    # Se decide el tipo de navegación a usar
    if (prob_Navegacion <= 0.4):
        navegacion[i] = 0
    else:
        navegacion[i] = 1


print("FIN CÁLCULO SALIDAS")
print("-------------------------------------------------------------------------------------------------------------")

df['Cuadros de ayuda'] = ayudas
df['Número de gráficas por sección'] = n_graficas
df['Dificultad de gráficas'] = tipo_graficas
df['Complejidad navegación'] = navegacion

data = df.values

print("INICIO APRENDIZAJE")

X = data[:, 0:13].astype('float32')
# Cuadros de ayuda
print("Cuadros de ayuda")
y = data[:, 13].astype('float32')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=125
)

modelCA = GaussianNB()
modelCA.fit(X_train, y_train)
y_pred = modelCA.predict(X_test)
accuracy = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print(y_test)
matriz_confusion = confusion_matrix(y_test, y_pred, labels = [0, 1])
print(matriz_confusion)

# Número de gráficas por sección
print("")
print("Número de gráficas por sección")
y = data[:, 14].astype('float32')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=125
)

modelNGS = GaussianNB()
modelNGS.fit(X_train, y_train)
y_pred = modelNGS.predict(X_test)
accuracy = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print(y_test)
matriz_confusion = confusion_matrix(y_test, y_pred, labels = [0, 1, 2])
print(matriz_confusion)

# Dificultad de gráficas
print("")
print("Dificultad de gráficas")
y = data[:, 15].astype('float32')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=125
)

modelDG = GaussianNB()
modelDG.fit(X_train, y_train)
y_pred = modelDG.predict(X_test)
accuracy = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print(y_test)
matriz_confusion = confusion_matrix(y_test, y_pred, labels = [0, 1, 2])
print(matriz_confusion)

# Complejidad navegación
print("")
print("Complejidad navegación")
y = data[:, 16].astype('float32')
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=125
)

modelNAV = GaussianNB()
modelNAV.fit(X_train, y_train)
y_pred = modelNAV.predict(X_test)
accuracy = accuracy_score(y_pred, y_test)
f1 = f1_score(y_pred, y_test, average="weighted")

print("Accuracy:", accuracy)
print("F1 Score:", f1)
print(y_test)
matriz_confusion = confusion_matrix(y_test, y_pred, labels = [0, 1])
print(matriz_confusion)

path = "modelos/" + "ModeloCuadrosAyuda.txt"
file = open(path, "wb")
pickle.dump(modelCA, file)

path = "modelos/" + "ModeloNGraficasSeccion.txt"
file = open(path, "wb")
pickle.dump(modelNGS, file)

path = "modelos/" + "ModeloNavegacion.txt"
file = open(path, "wb")
pickle.dump(modelNAV, file)

path = "modelos/" + "ModeloDificultadGraficas.txt"
file = open(path, "wb")
pickle.dump(modelDG, file)

print("FIN APRENDIZAJE")
print("-------------------------------------------------------------------------------------------------------------")