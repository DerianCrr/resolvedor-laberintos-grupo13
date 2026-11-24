from collections import deque
import random
import time

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

MAPA_NORMAL = [
    ["S", 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, "E"],
]

MAPA_LIMITE = [
    ["S", "E"],
]

MAPA_SIN_SOLUCION = [
    ["S", 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 1, 1],
    [0, 1, 0, 1, "E"],
    [0, 0, 0, 1, 1],
]


def generar_laberinto(filas, cols, semilla):
    random.seed(semilla)
    maze = []

    for f in range(filas):
        fila = []
        for c in range(cols):
            if random.random() < 0.28:
                fila.append(1)
            else:
                fila.append(0)
        maze.append(fila)

    f = 0
    c = 0
    maze[0][0] = 0

    while f < filas - 1 or c < cols - 1:
        if f == filas - 1:
            c += 1
        elif c == cols - 1:
            f += 1
        elif random.random() < 0.5:
            f += 1
        else:
            c += 1
        maze[f][c] = 0

    maze[0][0] = "S"
    maze[filas - 1][cols - 1] = "E"
    return maze


def buscar_inicio_fin(maze):
    inicio = None
    fin = None

    for f in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[f][c] == "S":
                inicio = (f, c)
            elif maze[f][c] == "E":
                fin = (f, c)
            if inicio is not None and fin is not None:
                return inicio, fin

    return inicio, fin


def reconstruir_camino(padre, fin):
    ruta = []
    actual = fin

    while actual is not None:
        ruta.append(actual)
        actual = padre[actual]

    ruta.reverse()
    return ruta


def resolver_backtracking(maze, f, c, fin, visitado, ruta):
    filas = len(maze)
    cols = len(maze[0])

    if not (0 <= f < filas and 0 <= c < cols):
        return False

    if maze[f][c] == 1 or (f, c) in visitado:
        return False

    visitado.add((f, c))
    ruta.append((f, c))

    if (f, c) == fin:
        return True

    for df, dc in DIRECCIONES:
        if resolver_backtracking(maze, f + df, c + dc, fin, visitado, ruta):
            return True

    ruta.pop()
    return False


def resolver_dfs(maze):
    inicio, fin = buscar_inicio_fin(maze)
    if inicio is None or fin is None:
        return False, [], 0

    filas = len(maze)
    cols = len(maze[0])
    pila = [inicio]
    visitado = {inicio}
    padre = {inicio: None}
    explorados = 0

    while pila:
        actual = pila.pop()
        explorados += 1

        if actual == fin:
            return True, reconstruir_camino(padre, fin), explorados

        f = actual[0]
        c = actual[1]

        for df, dc in DIRECCIONES:
            nf = f + df
            nc = c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    visitado.add((nf, nc))
                    padre[(nf, nc)] = actual
                    pila.append((nf, nc))

    return False, [], explorados


def resolver_bfs(maze):
    inicio, fin = buscar_inicio_fin(maze)
    if inicio is None or fin is None:
        return False, [], 0

    filas = len(maze)
    cols = len(maze[0])
    cola = deque([inicio])
    visitado = {inicio}
    padre = {inicio: None}
    explorados = 0

    while cola:
        actual = cola.popleft()
        explorados += 1

        if actual == fin:
            return True, reconstruir_camino(padre, fin), explorados

        f = actual[0]
        c = actual[1]

        for df, dc in DIRECCIONES:
            nf = f + df
            nc = c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    visitado.add((nf, nc))
                    padre[(nf, nc)] = actual
                    cola.append((nf, nc))

    return False, [], explorados


def mostrar_laberinto(maze, ruta=None):
    camino = set(ruta) if ruta else set()

    for f in range(len(maze)):
        linea = []
        for c in range(len(maze[0])):
            celda = maze[f][c]
            if celda == "S" or celda == "E":
                linea.append(celda)
            elif celda == 1:
                linea.append("#")
            elif (f, c) in camino:
                linea.append("*")
            else:
                linea.append(".")
        print(" ".join(linea))


def mostrar_fila(nombre, ok, pasos, explorados, tiempo):
    salida = "SI" if ok else "NO"
    col1 = nombre.ljust(13)
    col2 = salida.ljust(6)
    col3 = str(pasos).ljust(6)
    col4 = str(explorados).ljust(10)
    col5 = str(round(tiempo, 4))
    print(col1, "|", col2, "|", col3, "|", col4, "|", col5)


def ejecutar_prueba(titulo, maze, mostrar_mapa=True):
    filas = len(maze)
    cols = len(maze[0])
    print("\n---", titulo, "(" + str(filas) + "x" + str(cols) + ") ---")

    if mostrar_mapa:
        print("Mapa inicial (S=inicio, E=salida, #=muro, .=libre):")
        mostrar_laberinto(maze)

    t0 = time.perf_counter()
    inicio, fin = buscar_inicio_fin(maze)
    vis_bt = set()
    ruta_bt = []
    if inicio is not None and fin is not None:
        ok_bt = resolver_backtracking(maze, inicio[0], inicio[1], fin, vis_bt, ruta_bt)
    else:
        ok_bt = False
    t_bt = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    ok_dfs, ruta_dfs, exp_dfs = resolver_dfs(maze)
    t_dfs = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    ok_bfs, ruta_bfs, exp_bfs = resolver_bfs(maze)
    t_bfs = (time.perf_counter() - t0) * 1000

    pasos_bt = len(ruta_bt) - 1 if ok_bt else 0
    pasos_dfs = len(ruta_dfs) - 1 if ok_dfs else 0
    pasos_bfs = len(ruta_bfs) - 1 if ok_bfs else 0

    print("\nAlgoritmo     | Salida | Pasos  | Explorados | Tiempo (ms)")
    print("----------------------------------------------------------")
    mostrar_fila("Backtracking", ok_bt, pasos_bt, len(vis_bt), t_bt)
    mostrar_fila("DFS", ok_dfs, pasos_dfs, exp_dfs, t_dfs)
    mostrar_fila("BFS", ok_bfs, pasos_bfs, exp_bfs, t_bfs)

    if ok_bfs:
        if mostrar_mapa:
            print("\nRuta mas corta (BFS con '*'):")
            mostrar_laberinto(maze, ruta_bfs)
            print("Coordenadas:", ruta_bfs)
        else:
            print("\nRuta optima BFS:", pasos_bfs, "pasos")
    else:
        print("\nAviso: la salida 'E' es inaccesible, este laberinto no tiene solucion.")


def ingresar_laberinto():
    filas = int(input("Numero de filas: "))
    cols = int(input("Numero de columnas: "))
    print("Ingresa cada fila separada por espacios: S (inicio), E (salida), 0 (libre), 1 (muro)")
    print("Nota: solo se permite una 'S' y una 'E' en todo el laberinto.")

    maze = []
    cuenta_s = 0
    cuenta_e = 0

    for f in range(filas):
        while True:
            texto = input("Fila " + str(f + 1) + ": ").strip().upper()
            partes = texto.split()

            if len(partes) != cols:
                print("Debes ingresar exactamente", cols, "valores.")
                continue

            fila = []
            s_en_fila = 0
            e_en_fila = 0
            valido = True

            for valor in partes:
                if valor == "0" or valor == "1":
                    fila.append(int(valor))
                elif valor == "S":
                    if cuenta_s + s_en_fila >= 1:
                        print("Solo se permite una 'S' (inicio) en todo el laberinto. Cambia la fila.")
                        valido = False
                        break
                    s_en_fila += 1
                    fila.append(valor)
                elif valor == "E":
                    if cuenta_e + e_en_fila >= 1:
                        print("Solo se permite una 'E' (salida) en todo el laberinto. Cambia la fila.")
                        valido = False
                        break
                    e_en_fila += 1
                    fila.append(valor)
                else:
                    print("Simbolo no valido:", valor)
                    valido = False
                    break

            if valido:
                cuenta_s += s_en_fila
                cuenta_e += e_en_fila
                maze.append(fila)
                break

    if cuenta_s != 1 or cuenta_e != 1:
        print("Error: el mapa debe tener exactamente una 'S' y una 'E'.")
        return None

    return maze


while True:
    print("\n=== RESOLVEDOR DE LABERINTOS - GRUPO 13 ===")
    print("1. Caso normal (6x6)")
    print("2. Caso limite (1x2)")
    print("3. Caso sin solucion (5x5)")
    print("4. Comparativa de rendimiento (10x10, 25x25 y 40x40)")
    print("5. Ingresar laberinto manualmente")
    print("0. Salir")

    op = input("Opcion: ").strip()

    if op == "1":
        ejecutar_prueba("CASO NORMAL", MAPA_NORMAL, True)
    elif op == "2":
        ejecutar_prueba("CASO LIMITE", MAPA_LIMITE, True)
    elif op == "3":
        ejecutar_prueba("CASO SIN SOLUCION", MAPA_SIN_SOLUCION, True)
    elif op == "4":
        mapa_10 = generar_laberinto(10, 10, 10)
        mapa_25 = generar_laberinto(25, 25, 20)
        mapa_40 = generar_laberinto(40, 40, 30)
        ejecutar_prueba("PEQUENO (seed 10)", mapa_10, False)
        ejecutar_prueba("MEDIANO (seed 20)", mapa_25, False)
        ejecutar_prueba("GRANDE (seed 30)", mapa_40, False)
    elif op == "5":
        lab = ingresar_laberinto()
        if lab is not None:
            ejecutar_prueba("LABERINTO MANUAL", lab, True)
    elif op == "0":
        print("Programa finalizado.")
        break
    else:
        print("Opcion no valida.")
