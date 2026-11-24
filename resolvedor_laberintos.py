from collections import deque
import heapq
import random
import time

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]

MAPA_LIMITE = [
    ["S", "E"],
]


def existe_camino_bfs(maze):
    inicio, fin = buscar_inicio_fin(maze)
    if inicio is None or fin is None:
        return False

    filas = len(maze)
    cols = len(maze[0])
    cola = deque([inicio])
    visitado = {inicio}

    while cola:
        actual = cola.popleft()
        if actual == fin:
            return True

        f, c = actual
        for df, dc in DIRECCIONES:
            nf, nc = f + df, c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    visitado.add((nf, nc))
                    cola.append((nf, nc))

    return False


def generar_laberinto(filas, cols, semilla=None, con_solucion=True, prob_muro=0.28):
    if semilla is None:
        semilla = random.SystemRandom().randint(1, 10**9)
    rng = random.Random(semilla)

    while True:
        maze = [
            [1 if rng.random() < prob_muro else 0 for _ in range(cols)]
            for _ in range(filas)
        ]

        if con_solucion:
            f, c = 0, 0
            maze[f][c] = 0
            while f < filas - 1 or c < cols - 1:
                if f == filas - 1:
                    c += 1
                elif c == cols - 1:
                    f += 1
                elif rng.random() < 0.5:
                    f += 1
                else:
                    c += 1
                maze[f][c] = 0

        maze[0][0] = "S"
        maze[filas - 1][cols - 1] = "E"

        if filas == 1 and cols == 1:
            return maze, semilla

        tiene_camino = existe_camino_bfs(maze)
        if con_solucion and tiene_camino:
            return maze, semilla
        if not con_solucion and not tiene_camino:
            return maze, semilla


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

        f, c = actual
        for df, dc in DIRECCIONES:
            nf, nc = f + df, c + dc
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

        f, c = actual
        for df, dc in DIRECCIONES:
            nf, nc = f + df, c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    visitado.add((nf, nc))
                    padre[(nf, nc)] = actual
                    cola.append((nf, nc))

    return False, [], explorados


def resolver_dijkstra(maze):
    inicio, fin = buscar_inicio_fin(maze)
    if inicio is None or fin is None:
        return False, [], 0

    filas = len(maze)
    cols = len(maze[0])
    cola = [(0, inicio)]
    dist = {inicio: 0}
    visitado = set()
    padre = {inicio: None}
    explorados = 0

    while cola:
        costo, actual = heapq.heappop(cola)
        if actual in visitado:
            continue
        visitado.add(actual)
        explorados += 1

        if actual == fin:
            return True, reconstruir_camino(padre, fin), explorados

        f, c = actual
        for df, dc in DIRECCIONES:
            nf, nc = f + df, c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    nuevo_costo = costo + 1
                    if nuevo_costo < dist.get((nf, nc), float("inf")):
                        dist[(nf, nc)] = nuevo_costo
                        padre[(nf, nc)] = actual
                        heapq.heappush(cola, (nuevo_costo, (nf, nc)))

    return False, [], explorados


def heuristica_manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def resolver_a_estrella(maze):
    inicio, fin = buscar_inicio_fin(maze)
    if inicio is None or fin is None:
        return False, [], 0

    filas = len(maze)
    cols = len(maze[0])
    cola = [(heuristica_manhattan(inicio, fin), 0, inicio)]
    g_costo = {inicio: 0}
    visitado = set()
    padre = {inicio: None}
    explorados = 0

    while cola:
        _, g, actual = heapq.heappop(cola)
        if actual in visitado:
            continue
        visitado.add(actual)
        explorados += 1

        if actual == fin:
            return True, reconstruir_camino(padre, fin), explorados

        f, c = actual
        for df, dc in DIRECCIONES:
            nf, nc = f + df, c + dc
            if 0 <= nf < filas and 0 <= nc < cols:
                if maze[nf][nc] != 1 and (nf, nc) not in visitado:
                    nuevo_g = g + 1
                    if nuevo_g < g_costo.get((nf, nc), float("inf")):
                        g_costo[(nf, nc)] = nuevo_g
                        f_costo = nuevo_g + heuristica_manhattan((nf, nc), fin)
                        padre[(nf, nc)] = actual
                        heapq.heappush(cola, (f_costo, nuevo_g, (nf, nc)))

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

    t0 = time.perf_counter()
    ok_dij, ruta_dij, exp_dij = resolver_dijkstra(maze)
    t_dij = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    ok_ast, ruta_ast, exp_ast = resolver_a_estrella(maze)
    t_ast = (time.perf_counter() - t0) * 1000

    pasos_bt = len(ruta_bt) - 1 if ok_bt else 0
    pasos_dfs = len(ruta_dfs) - 1 if ok_dfs else 0
    pasos_bfs = len(ruta_bfs) - 1 if ok_bfs else 0
    pasos_dij = len(ruta_dij) - 1 if ok_dij else 0
    pasos_ast = len(ruta_ast) - 1 if ok_ast else 0

    print("\nAlgoritmo     | Salida | Pasos  | Explorados | Tiempo (ms)")
    print("----------------------------------------------------------")
    mostrar_fila("Backtracking", ok_bt, pasos_bt, len(vis_bt), t_bt)
    mostrar_fila("DFS", ok_dfs, pasos_dfs, exp_dfs, t_dfs)
    mostrar_fila("BFS", ok_bfs, pasos_bfs, exp_bfs, t_bfs)
    mostrar_fila("Dijkstra", ok_dij, pasos_dij, exp_dij, t_dij)
    mostrar_fila("A*", ok_ast, pasos_ast, exp_ast, t_ast)

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
    print("1. Caso normal aleatorio con solucion (6x6)")
    print("2. Caso limite fijo (1x2)")
    print("3. Caso aleatorio SIN solucion (5x5)")
    print("4. Comparativa de rendimiento aleatoria con solucion (10x10, 25x25 y 40x40)")
    print("5. Ingresar laberinto manualmente")
    print("0. Salir")

    op = input("Opcion: ").strip()

    if op == "1":
        mapa_1, seed_1 = generar_laberinto(6, 6, con_solucion=True, prob_muro=0.28)
        ejecutar_prueba(f"CASO NORMAL (seed {seed_1})", mapa_1, True)
    elif op == "2":
        ejecutar_prueba("CASO LIMITE", MAPA_LIMITE, True)
    elif op == "3":
        mapa_3, seed_3 = generar_laberinto(5, 5, con_solucion=False, prob_muro=0.45)
        ejecutar_prueba(f"CASO SIN SOLUCION (seed {seed_3})", mapa_3, True)
    elif op == "4":
        mapa_10, seed_10 = generar_laberinto(10, 10, con_solucion=True, prob_muro=0.28)
        mapa_25, seed_25 = generar_laberinto(25, 25, con_solucion=True, prob_muro=0.28)
        mapa_40, seed_40 = generar_laberinto(40, 40, con_solucion=True, prob_muro=0.28)
        ejecutar_prueba(f"PEQUENO (seed {seed_10})", mapa_10, False)
        ejecutar_prueba(f"MEDIANO (seed {seed_25})", mapa_25, False)
        ejecutar_prueba(f"GRANDE (seed {seed_40})", mapa_40, False)
    elif op == "5":
        lab = ingresar_laberinto()
        if lab is not None:
            ejecutar_prueba("LABERINTO MANUAL", lab, True)
    elif op == "0":
        print("Programa finalizado.")
        break
    else:
        print("Opcion no valida.")
