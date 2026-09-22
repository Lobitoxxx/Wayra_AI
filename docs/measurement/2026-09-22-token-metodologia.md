---
tipo: medicion
estado: vigente
fecha: 2026-09-22
tags: [tokens, medicion]
---

# Metodología de medición de tokens — Wayra AI

Objetivo: verificar si el entorno reduce el consumo de contexto del agente. **No se atribuirá ahorro sin métricas comparables.**

## Procedimiento tradicional (T)
1. Exploración extensa del repositorio (glob/lectura de múltiples archivos) para cada tarea.

## Procedimiento optimizado (O)
1. Consultar [[../knowledge/00-index]] y recuperar solo notas pertinentes.
2. Consultar Graphify (grafo) para relaciones de código cuando exista.
3. Leer código solo para verificar detalles.

## Métricas a comparar (por tarea equivalente)
- Tokens **de entrada** (usados por el agente).
- Tokens en **consultas/extracción semántica** (grafo).
- Número de **archivos inspeccionados**.
- Volumen de **información recuperada**.
- **Precisión** de las respuestas (revisión humana).

## Reglas
- Costo de **construcción del grafo** se registra por separado del costo de consultas posteriores.
- Si OpenCode no ofrece métricas de uso reales, se informa: "ahorro todavía **no verificado**".

## Estado actual (2026-09-22)
- Metodología definida. **Sin métricas aún** (el entorno se está instalando y no hay código).
- Proyecto piloto al terminar F2: registrar métricas de la tarea "implementar adaptador CHIRPS".
- Resultados se guardarán en `docs/measurement/resultados/`.