# SIMULADOR DE CPU - SIGET

# Estados posibles de un proceso
NUEVO = 0
LISTO = 1
EJECUTANDO = 2
BLOQUEADO = 3
TERMINADO = 4


# Convierte el numero del estado en un texto
def nombre_estado(estado):
    if estado == NUEVO:
        return "NUEVO"
    elif estado == LISTO:
        return "LISTO"
    elif estado == EJECUTANDO:
        return "EN EJECUCION"
    elif estado == BLOQUEADO:
        return "BLOQUEADO"
    elif estado == TERMINADO:
        return "TERMINADO"
    else:
        return "DESCONOCIDO"


# Muestra la informacion completa de un proceso
def mostrar_proceso(proceso):
    print("----------------------------------------")
    print("ID:", proceso["id"])
    print("Proceso:", proceso["nombre"])
    print("Tiempo de irrupcion:", proceso["tiempo_irrupcion"])
    print("Prioridad de alerta:", proceso["prioridad_alerta"])
    print("Tamano de datos:", proceso["tamano_datos"], "MB")
    print("Tiempo de ejecucion:", proceso["tiempo_ejecucion"])
    print("Tiempo restante:", proceso["tiempo_restante"])
    print("Estado:", nombre_estado(proceso["estado"]))


# Crea los procesos que utilizara el simulador
def crear_procesos():
    procesos = []

    procesos.append({
        "id": 1,
        "nombre": "Deteccion de accidente",
        "tiempo_irrupcion": 0,
        "prioridad_alerta": 1,
        "tamano_datos": 500,
        "tiempo_ejecucion": 5,
        "tiempo_restante": 5,
        "estado": NUEVO,
        "ya_se_bloqueo": False
    })

    procesos.append({
        "id": 2,
        "nombre": "Analisis de trafico",
        "tiempo_irrupcion": 1,
        "prioridad_alerta": 2,
        "tamano_datos": 800,
        "tiempo_ejecucion": 7,
        "tiempo_restante": 7,
        "estado": NUEVO,
        "ya_se_bloqueo": False
    })

    procesos.append({
        "id": 3,
        "nombre": "Actualizacion de semaforos",
        "tiempo_irrupcion": 2,
        "prioridad_alerta": 3,
        "tamano_datos": 300,
        "tiempo_ejecucion": 4,
        "tiempo_restante": 4,
        "estado": NUEVO,
        "ya_se_bloqueo": False
    })

    procesos.append({
        "id": 4,
        "nombre": "Generacion de estadisticas",
        "tiempo_irrupcion": 3,
        "prioridad_alerta": 4,
        "tamano_datos": 600,
        "tiempo_ejecucion": 6,
        "tiempo_restante": 6,
        "estado": NUEVO,
        "ya_se_bloqueo": False
    })

    return procesos


# Simula el bloqueo de un proceso mientras espera datos
def bloquear_proceso(proceso, tiempo_actual):
    proceso["estado"] = BLOQUEADO

    print()
    print("[Tiempo", tiempo_actual, "]", proceso["nombre"], "-> BLOQUEADO")
    print("Motivo -> Esperando datos de sensores")
    print("Tiempo de bloqueo -> 1 unidad")

    # Avanza el tiempo mientras el proceso esta bloqueado
    tiempo_actual += 1

    # Cuando termina la espera, el proceso vuelve a estar listo
    proceso["estado"] = LISTO

    print("[Tiempo", tiempo_actual, "]", proceso["nombre"], "-> LISTO")

    return tiempo_actual


# Muestra el estado actual de todos los procesos
def mostrar_estado_general(procesos):
    print()
    print("ESTADO ACTUAL DE LOS PROCESOS")
    print("----------------------------------------")

    for proceso in procesos:
        print("ID:", proceso["id"], "|", proceso["nombre"], "|", nombre_estado(proceso["estado"]))


# Simula el algoritmo Round Robin utilizando un quantum
def round_robin(procesos, quantum):
    print()
    print("ALGORITMO ROUND ROBIN")
    print("Quantum:", quantum)

    cola = []
    frente = 0
    tiempo_actual = 0
    procesos_terminados = 0
    cantidad_procesos = len(procesos)

    # Continua hasta terminar todos los procesos
    while procesos_terminados < cantidad_procesos:

        # Agrega a la cola los procesos que ya llegaron
        for i in range(cantidad_procesos):
            if procesos[i]["estado"] == NUEVO and procesos[i]["tiempo_irrupcion"] <= tiempo_actual:
                procesos[i]["estado"] = LISTO
                cola.append(i)

                print("[Tiempo", tiempo_actual, "]", procesos[i]["nombre"], "-> NUEVO a LISTO")

        # Si no hay procesos disponibles, avanza el tiempo
        if frente >= len(cola):
            tiempo_actual += 1
            continue

        # Obtiene el siguiente proceso de la cola
        indice = cola[frente]
        frente += 1

        procesos[indice]["estado"] = EJECUTANDO

        print()
        print("CPU ->", procesos[indice]["nombre"])
        print("Estado ->", nombre_estado(procesos[indice]["estado"]))

        tiempo_ejecutado = 0
        proceso_bloqueado = False

        # Ejecuta el proceso durante el tiempo permitido por el quantum
        while tiempo_ejecutado < quantum and procesos[indice]["tiempo_restante"] > 0:

            # El proceso 1 se bloquea una vez cuando le quedan 3 unidades
            if (procesos[indice]["id"] == 1 and
                    procesos[indice]["ya_se_bloqueo"] == False and
                    procesos[indice]["tiempo_restante"] == 3):

                procesos[indice]["ya_se_bloqueo"] = True

                tiempo_actual = bloquear_proceso(procesos[indice], tiempo_actual)

                # El proceso vuelve a la cola despues del bloqueo
                cola.append(indice)
                proceso_bloqueado = True

                break

            print("Tiempo:", tiempo_actual, "| Ejecutando:", procesos[indice]["nombre"], "| Restante:", procesos[indice]["tiempo_restante"])

            procesos[indice]["tiempo_restante"] -= 1
            tiempo_actual += 1
            tiempo_ejecutado += 1

            # Verifica si aparecieron nuevos procesos durante la ejecucion
            for i in range(cantidad_procesos):
                if procesos[i]["estado"] == NUEVO and procesos[i]["tiempo_irrupcion"] <= tiempo_actual:
                    procesos[i]["estado"] = LISTO
                    cola.append(i)

                    print("[Tiempo", tiempo_actual, "]", procesos[i]["nombre"], "-> NUEVO a LISTO")

        # Si el proceso se bloqueo, continua con el siguiente
        if proceso_bloqueado:
            mostrar_estado_general(procesos)
            continue

        # Si ya no le queda tiempo, el proceso termina
        if procesos[indice]["tiempo_restante"] == 0:

            procesos[indice]["estado"] = TERMINADO
            procesos_terminados += 1

            print()
            print("PROCESO TERMINADO:", procesos[indice]["nombre"])
            print("Estado ->", nombre_estado(procesos[indice]["estado"]))

        else:

            # Si se acaba el quantum, el proceso vuelve a la cola
            procesos[indice]["estado"] = LISTO
            cola.append(indice)

            print()
            print("Quantum terminado:", procesos[indice]["nombre"])
            print("Estado -> LISTO")

        mostrar_estado_general(procesos)

    print()
    print("ROUND ROBIN FINALIZADO")


# Simula el algoritmo de prioridad
def prioridad(procesos):
    print()
    print("ALGORITMO DE PRIORIDAD")

    tiempo_actual = 0
    procesos_terminados = 0
    cantidad_procesos = len(procesos)

    # Continua hasta terminar todos los procesos
    while procesos_terminados < cantidad_procesos:

        indice = -1

        # Busca el proceso disponible con mayor prioridad
        for i in range(cantidad_procesos):
            if (procesos[i]["estado"] != TERMINADO and
                    procesos[i]["tiempo_irrupcion"] <= tiempo_actual):

                if (indice == -1 or
                        procesos[i]["prioridad_alerta"] < procesos[indice]["prioridad_alerta"]):

                    indice = i

        # Si todavia no ha llegado ningun proceso, avanza el tiempo
        if indice == -1:
            tiempo_actual += 1
            continue

        procesos[indice]["estado"] = LISTO

        print()
        print("[Tiempo", tiempo_actual, "]", procesos[indice]["nombre"], "-> NUEVO a LISTO")

        procesos[indice]["estado"] = EJECUTANDO

        print("CPU ->", procesos[indice]["nombre"])
        print("Estado ->", nombre_estado(procesos[indice]["estado"]))

        # Ejecuta completamente el proceso seleccionado
        while procesos[indice]["tiempo_restante"] > 0:

            print("Tiempo:", tiempo_actual, "| Ejecutando:", procesos[indice]["nombre"], "| Restante:", procesos[indice]["tiempo_restante"])

            procesos[indice]["tiempo_restante"] -= 1
            tiempo_actual += 1

        # Cuando termina su ejecucion, cambia a terminado
        procesos[indice]["estado"] = TERMINADO
        procesos_terminados += 1

        print()
        print("PROCESO TERMINADO:", procesos[indice]["nombre"])
        print("Estado ->", nombre_estado(procesos[indice]["estado"]))

        mostrar_estado_general(procesos)

    print()
    print("PRIORIDAD FINALIZADO")


# Reinicia los procesos para poder ejecutar el segundo algoritmo
def reiniciar_procesos(procesos):
    for proceso in procesos:
        proceso["tiempo_restante"] = proceso["tiempo_ejecucion"]
        proceso["estado"] = NUEVO
        proceso["ya_se_bloqueo"] = False


# Programa principal
cantidad_procesos = 4

print("SIMULADOR DE CPU - SIGET")

# Crea los procesos del sistema
procesos = crear_procesos()

print()
print("PROCESOS DEL SIGET")

# Muestra la informacion inicial de cada proceso
for i in range(cantidad_procesos):
    mostrar_proceso(procesos[i])

# Define el quantum utilizado por Round Robin
quantum = 2

# Ejecuta Round Robin
round_robin(procesos, quantum)

# Reinicia los procesos antes de ejecutar el segundo algoritmo
reiniciar_procesos(procesos)

# Ejecuta el algoritmo de prioridad
prioridad(procesos)