# Wayra AI — Catálogo de datasets

**Estado:** catálogo de planificación; la incorporación al modelo exige auditoría del archivo real.  
**Cobertura objetivo:** Perú completo.

## 1. Principios del catálogo

Cada fuente debe registrar versión, periodo, frecuencia, resolución, variables, licencia, acceso, latencia, `retrieved_at`, checksum y limitaciones. Una ficha encontrada en un portal no equivale a un dataset ya integrado.

## 2. Fuentes climáticas principales

### CHIRPS v3

- **Institución:** UCSB Climate Hazards Center.
- **Producto candidato:** CHIRPS v3 diario, variante final `rnl`.
- **Variable principal:** precipitación.
- **Resolución nativa:** 0.05°.
- **Cobertura:** terrestre entre 60° N y 60° S; incluye Perú.
- **Periodo general de CHIRPS v3:** desde 1981; la variante diaria seleccionada debe auditarse antes de fijar el periodo común definitivo.
- **Formato usado por el adaptador actual:** GeoTIFF.
- **Rol Wayra:** fuente raster principal de precipitación histórica y candidata a objetivo supervisado.
- **Estado:** adaptador inicial implementado.
- **URL:** https://data.chc.ucsb.edu/products/CHIRPS/v3.0/

**Cautelas:** distinguir `final` de `prelim`, registrar la variante exacta y no asumir que la fecha de observación es fecha de publicación. La variante `rnl` depende de información de reanálisis; esta dependencia debe documentarse al interpretar modelos que también incorporen ERA5.

### ERA5-Land

- **Institución:** ECMWF / Copernicus Climate Change Service.
- **Tipo:** reanálisis terrestre.
- **Frecuencia:** horaria.
- **Distribución habitual:** cuadrícula 0.1°.
- **Variables candidatas:** temperatura a 2 m, punto de rocío a 2 m, presión superficial, viento U/V a 10 m, precipitación y otras variables terrestres.
- **Formatos:** GRIB/NetCDF y productos de series temporales según servicio.
- **Rol Wayra:** variables meteorológicas históricas complementarias.
- **Estado:** pendiente de adaptador y credenciales CDS.
- **URL:** https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land

**Cautelas:** reanálisis no significa pronóstico operativo. Las variables acumuladas requieren interpretar correctamente intervalos y unidades.

### SENAMHI — estaciones automáticas de intercambio internacional

- **Institución:** Servicio Nacional de Meteorología e Hidrología del Perú.
- **Portal:** Plataforma Nacional de Datos Abiertos.
- **Frecuencia declarada:** observaciones horarias validadas.
- **Variables descritas:** temperatura, humedad relativa, precipitación, estación, red, latitud, longitud, altitud, departamento, provincia, distrito, ubigeo, fecha y hora.
- **Recursos publicados:** CSV + diccionario XLSX + metadatos DOCX.
- **Licencia indicada en la ficha:** Open Data Commons Attribution.
- **Rol Wayra:** observación terrestre, control de calidad y comparación con productos raster.
- **Estado:** pendiente de descargar/auditar el archivo completo y su diccionario.
- **URL:** https://www.datosabiertos.gob.pe/dataset/variables-meteorologicas-de-las-estaciones-autom%C3%A1ticas-de-intercambio-internacional-servicio

**Cautelas:** una estación es puntual y no representa automáticamente una celda completa. Verificar intervalo de acumulación de lluvia, zona horaria, continuidad de series y valores faltantes.

## 3. Subsistema oceanográfico

### NOAA CPC — índices Niño

- **Institución:** NOAA Climate Prediction Center.
- **Índices candidatos:** Niño 1+2, Niño 3.4 y productos relacionados con ENOS.
- **Frecuencias:** mensual y/o semanal según serie.
- **Rol Wayra:** contexto oceánico regional como feature candidata.
- **Estado:** pendiente de adaptador versionado.
- **URL catálogo:** https://www.cpc.ncep.noaa.gov/data/indices/

**Cautelas:** conservar periodo climatológico, versión de SST, referencia temporal y fecha de disponibilidad. No mezclar versiones sin dejar rastro.

### NOAA — RONI

- **Rol:** indicador relativo de ENOS.
- **Estado:** candidato; validar el producto oficial vigente y su método de revisión antes de integrarlo.

**Cautelas:** los valores recientes pueden ser revisados. Para experimentos retrospectivos se debe documentar si se usa la serie consolidada actual o una reconstrucción de disponibilidad histórica.

### IMARPE — temperatura superficial del mar

- **Institución:** Instituto del Mar del Perú.
- **Cobertura declarada en datos abiertos:** mediciones de laboratorios costeros desde 1970 hasta 2026 según el recurso consultado.
- **Campos publicados:** fecha de medición, laboratorio costero, temperatura superficial; existen recursos de coordenadas/diccionario asociados.
- **Licencia indicada:** Open Data Commons Attribution.
- **Rol Wayra:** observación costera peruana independiente de los índices agregados NOAA.
- **Estado:** pendiente de adaptador/auditoría.
- **Portal:** https://www.datosabiertos.gob.pe/

### IMARPE — anomalía de TSM

- **Campos publicados:** fecha, laboratorio, anomalía de temperatura.
- **Rol:** feature oceanográfica candidata y análisis histórico costero.
- **Estado:** pendiente.

### IMARPE — salinidad superficial

- **Periodo declarado en recurso consultado:** 1995–2026 aproximadamente.
- **Rol:** variable de investigación complementaria; no forma parte del MVP obligatorio.
- **Estado:** opcional.

## 4. Geografía

### geoBoundaries — PER-ADM0

- **Rol actual:** máscara nacional de Perú.
- **Formato en repositorio:** GeoJSON.
- **Estado:** incorporado en `data/external/geoboundaries/PER-ADM0/`.
- **Uso:** rasterización sobre la malla 0.1°.
- **URL:** https://www.geoboundaries.org/

Para departamentos/provincias/distritos se recomienda evaluar límites oficiales o referenciales compatibles con UBIGEO y registrar el año de vigencia.

## 5. Fuentes para peligros naturales — extensión futura

### INDECI / SINPAD

- **Contenido:** emergencias y daños con desagregación territorial según producto.
- **Rol:** construir eventualmente etiquetas/eventos históricos para modelos de peligros independientes.
- **Estado:** fuera del MVP de precipitación.
- **Portal:** https://www.datosabiertos.gob.pe/

No usar registros de emergencia como sinónimo automático de lluvia extrema: el evento, fecha, ubicación, reporte y mecanismo causal deben validarse.

### INAIGEM

- **Contenido identificado:** datasets especializados de vigilancia hidrometeorológica/glaciar.
- **Rol:** futura investigación de peligros glaciares.
- **Estado:** fuera del MVP.

### CENEPRED / SIGRID

- **Contenido:** escenarios y estudios oficiales de riesgo/peligro.
- **Rol:** contexto cartográfico y metodológico; no debe confundirse con una predicción de Wayra AI.

## 6. Contrato de auditoría por dataset

Antes de pasar una fuente a Silver, completar:

| Campo | Obligatorio |
|---|---|
| proveedor/producto | sí |
| URL oficial | sí |
| licencia/condiciones | sí |
| versión | cuando exista |
| periodo efectivo observado | sí |
| frecuencia | sí |
| resolución espacial | cuando aplique |
| variables originales | sí |
| unidades | sí |
| nulos y códigos especiales | sí |
| duplicados | sí |
| timestamps/zona horaria | sí |
| latencia/publicación | cuando pueda verificarse |
| checksum local | sí |
| schema/diccionario | sí |
| transformaciones Silver | sí |

## 7. Priorización

1. CHIRPS: consolidar serie temporal y pruebas.
2. SENAMHI: auditar CSV/diccionario y cobertura real.
3. ERA5-Land: implementar adquisición y variables meteorológicas.
4. NOAA: importar índices con versión y referencia temporal.
5. IMARPE: integrar TSM/anomalías como subsistema separado.
6. INDECI/INAIGEM/CENEPRED: mantener como extensiones de peligros, sin bloquear la rúbrica principal.
