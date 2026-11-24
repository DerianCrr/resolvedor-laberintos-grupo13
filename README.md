====================================================================

RESOLVEDOR DE LABERINTOS - GRUPO 13

====================================================================



Programa de consola hecho en Python 3.11 para resolver laberintos en matrices 2D. Pone a prueba y compara cinco algoritmos distintos: Backtracking, DFS, BFS, Dijkstra y A*.



Este es nuestro proyecto final para el curso de Análisis de Algoritmos y Estrategias de Programación (Sección 21527).



--------------------------------------------------------------------

LO QUE HACE EL PROGRAMA

--------------------------------------------------------------------



- Comparativa entre algoritmos: Corre Backtracking, DFS, BFS, Dijkstra y A* al mismo tiempo sobre un mismo laberinto. Te muestra si encontraron la salida, cuántos pasos dieron, qué tantos nodos tuvieron que revisar y cuánto tardaron en milisegundos.

- Encuentra el camino más corto: Usa BFS con una cola FIFO (collections.deque) como referencia óptima, junto con Dijkstra y A* (usando colas de prioridad con heapq y heurística Manhattan), para asegurar la ruta más rápida moviéndose en vertical y horizontal.

- Pruebas disponibles en el menú:

  1. Un mapa normal aleatorio con solución garantizada (6x6) con varios caminos y callejones sin salida.

  2. Un caso mínimo fijo (1x2) para probar el límite más bajo.

  3. Un laberinto aleatorio sin salida (5x5) donde el final está bloqueado.

  4. Pruebas de rendimiento usando mapas aleatorios con solución garantizada y semilla dinámica (tamaños 10x10, 25x25 y 40x40).

  5. Opción para que ingreses tu propio laberinto a mano desde la consola, con validación para evitar errores de formato.



--------------------------------------------------------------------

QUÉ NECESITAS Y CÓMO CORRERLO

--------------------------------------------------------------------



Como solo usamos librerías que ya vienen con Python (collections, heapq, random y time), no hace falta instalar nada aparte.



1. Revisa que tengas Python 3.10 o una versión más nueva:

   python --version



2. Baja el repositorio o descarga directamente el archivo resolvedor_laberintosv2.py.



3. Ábrelo desde tu terminal con este comando:

   python resolvedor_laberintosv2.py



--------------------------------------------------------------------

INTEGRANTES (GRUPO 13 - "LOS WASAA")

--------------------------------------------------------------------



- Jefferson Gonzalo Núñez Martinez

- Derian Jacsel Carrasco Canayo

- Anderson Jhair Timana Damaso

- Jose Carlos Jauregui Zavaleta

- Fabricio Antonio Farfan Cruz
