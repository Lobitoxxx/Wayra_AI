---
tipo: visión
estado: decidido
fecha: 2026-09-22
tags: [wayra, vision, objetivos]
---

# Visión del proyecto — Wayra AI

## Qué es
**Wayra AI** es una plataforma **open source** de análisis climático y predicción de precipitaciones para el **Perú**, construida por un pipeline reproducible y auditable: ingesta de datos reales → preprocesado geoespacial → ingeniería de características → modelos ML (regresión y clasificación) → API → web.

## Objetivo general
Provever **predicción de lluvia a próxima día** (retrospectiva / validada) por celda de malla (~0.1°) sobre todo el territorio peruano, con trazabilidad completa (observación → publicación → recuperación → emisión).

## Objetivos específicos
1. Dataset maestro auténtico (no inventado) con múltiples fuentes internacionales y nacionales.
2. Modelo de **regresión**: precipitación del día siguiente (`precipitation_next_day_mm`).
3. Modelo de **clasificación**: umbral de lluvia extrema (percentil a validar según metodología SENAMHI/ENFEN).
4. Comparación sistemática con **LazyPredict** y baseline ingenuo explícito.
5. Trazabilidad temporal (sin fuga) y espacial sobre malla.
6. API y frontend en español, con disclaimers; **sin** reemplazar a SENAMHI/ENFEN ni emitir alertas.

## Alcance (resumen)
- **Dentro**: cobertura nacional; modos retrospectivo (implementable) y operativo (**deshabilitado por decisión**).
- **Fuera**: pronóstico como alerta de inundación, reemplazo de entidades oficiales, datos inventados.

Detalles y estado de requisitos: [[02-requirements]]. Compromisos técnicos: [[08-decisions]]. Arquitectura: [[03-architecture]].