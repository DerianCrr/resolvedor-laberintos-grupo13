Resolvedor de Laberintos - Grupo 13

Programa de consola hecho en Python 3.11 para resolver laberintos en matrices 2D. Pone a prueba y compara tres algoritmos distintos: Backtracking, DFS y BFS.

Este es nuestro proyecto final para el curso de Análisis de Algoritmos y Estrategias de Programación (Sección 21527).

Lo que hace el programa

- Comparativa entre algoritmos: Corre Backtracking, DFS y BFS al mismo tiempo sobre un mismo laberinto. Te muestra si encontraron la salida, cuántos pasos dieron, qué tantos nodos tuvieron que revisar y cuánto tardaron en milisegundos.
- Encuentra el camino más corto: Usa BFS con una cola FIFO (collections.deque) como base para asegurar que siempre dé con la ruta más rápida moviéndose en vertical y horizontal.
- Pruebas ya cargadas en el código:
  1. Un mapa normal (6x6) con varios caminos y callejones sin salida.
  2. Un caso mínimo (1x2) para probar el límite más bajo.
  3. Un laberinto sin salida (5x5) donde el final está bloqueado.
  4. Pruebas de rendimiento usando mapas generados con semillas (tamaños 10x10, 25x25 y 40x40).
  5. Opción para que ingreses tu propio laberinto a mano desde la consola, con validación para evitar errores de formato.

Qué necesitas y cómo correrlo

Como solo usamos librerías que ya vienen con Python (collections, random y time), no hace falta instalar nada aparte.

1. Revisa que tengas Python 3.10 o una versión más nueva:
   python --version

2. Baja el repositorio o descarga directamente el archivo resolvedor_laberintos.py.

3. Ábrelo desde tu terminal con este comando:
   python resolvedor_laberintos.py

Integrantes (Grupo 13 - "Los wasaa")

- Jefferson Gonzalo Núñez Martinez
- Derian Jacsel Carrasco Canayo
- Anderson Jhair Timana Damaso
- Jose Carlos Jauregui Zavaleta
- Fabricio Antonio Farfan Cruz
