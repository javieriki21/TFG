import numpy
import numpy as np
import random

# np.random.seed(1000)
n = 10

#-------------------------------------------------------------------------------------------------------------
# ENTRADAS

# Tiempo total en la aplicación
tiempoTotal = np.random.normal(50, 30, n)
# Tiempo máximo seguido en el que el usuario ha estado inactivo
tiempoInactividadMaximo = np.random.normal(20, 30, n)
# Número de clicks por minuto promedio
nclicks_min = np.random.normal(15, 10, n)
# Cambios de sección por minuto promedio
cambiosSeccion_min = np.random.lognormal(0, 0.5, n)
# Resultado del test original
scoreInicial = np.around(np.random.normal(5, 2, n))

# Diferentes porcentajes de tiempo en cada sección
tSecciones = [0,0,0,0,0,0,0]
for i in range(n):
    tiempoSecciones = [random.uniform(0, 1) for _ in range(7)]
    tiempoSecciones /= numpy.sum(tiempoSecciones)
    tSecciones = numpy.vstack([tSecciones, tiempoSecciones])
tSecciones = tSecciones[1:,:]

# Juntar en un dataset
data = np.hstack([np.column_stack([tiempoTotal, tiempoInactividadMaximo, nclicks_min, scoreInicial, cambiosSeccion_min]), tSecciones])
#np.savetxt('DatosEjemplo.txt', data)



#-------------------------------------------------------------------------------------------------------------
# SALIDAS

# Para cada salida se tiene en cuenta varios parámetros para determinar el output de esa salida

ayudas = np.empty([len(data)])
for i in range(0, len(data)):
    # -------------------------------------------------------------------------------
    # Calcular probabilidad de que el usuario necesitara comentarios de ayuda
    prob_Add_Ayuda = 0.1
    # Tener en cuenta su resultado del test
    resultadoTest = data[i,3]
    if resultadoTest < 5:
        prob_Add_Ayuda += 0.4
    elif resultadoTest < 7:
        prob_Add_Ayuda += 0.1
    elif resultadoTest < 9:
        prob_Add_Ayuda -= 0.1
    else:
        prob_Add_Ayuda -= 0.3

    # Tener en cuenta el máximo tiempo que el usuario se haya quedado inactivo
    tiempo_Inactivc = data[i, 1]
    if tiempo_Inactivc < 20:
        prob_Add_Ayuda -= 0.05
    elif tiempo_Inactivc > 45:
        prob_Add_Ayuda += 0.2

    # Tener en cuenta el número de clicks por minuto
    num_clicks = data[i, 2]
    if num_clicks < 3 or num_clicks > 25:
        prob_Add_Ayuda += 0.1
    else:
        prob_Add_Ayuda -= 0.05

    # Tener en cuenta el número de cambios de sección por minuto
    n_secciones = data[i, 4]
    if n_secciones > 3:
        prob_Add_Ayuda += 0.1
    elif n_secciones < 0.1:
        prob_Add_Ayuda += 0.05
    else:
        prob_Add_Ayuda -= 0.05

    addAyuda = False
    if (prob_Add_Ayuda > random.uniform(0, 1)):
        addAyuda = True
    ayudas[i] = addAyuda

    print(addAyuda)
    print("probabilidad:" + str(prob_Add_Ayuda))
    print("tiempo inactivo:" + str(tiempo_Inactivc))
    print("resultado test:" + str(resultadoTest))
    print("número de clicks:" + str(num_clicks))
    print("número de cambios de secciones:" + str(n_secciones))
    print("")

data = np.c_[ data, ayudas ]
print(data)