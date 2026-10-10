# Prospero Shell Lab

Investigación de la interfaz de PS5 y de las dependencias necesarias para portarla a PC.

Esta primera versión identifica artefactos locales sin ejecutarlos y construye un inventario reproducible de puntos de integración publicados por etaHEN. Todavía no ejecuta SceShellUI ni contiene una reconstrucción del menú original.

## Uso

Requiere Python 3.10 o posterior, sin dependencias externas.

```console
python shell_lab.py public --output public-inventory.json
python shell_lab.py inspect RUTA_A_UN_ARCHIVO --output artifact.json
python -m unittest discover -s . -v
```

`public` fija la revisión de etaHEN antes de consultar su fuente, registra SHA-256 y enumera identificadores de integración. No copia su implementación al proyecto. `inspect` calcula el hash completo y reconoce firmas ELF, PE, ZIP y SELF; un archivo no reconocido permanece desconocido. Una firma no demuestra que el archivo sea el menú ni que pueda portarse.

## Objetivo inicial

1. Inventariar evidencias públicas y artefactos disponibles.
2. Identificar componentes Mono/PUI, recursos CXML y mecanismos de arranque.
3. Mapear cada dependencia a una implementación disponible o a un bloqueo documentado.
4. Ejecutar una pantalla aislada cuando dispongamos de los artefactos y dependencias necesarios.
5. Conectar una selección de juegos a ejecutables convertidos por AnyPS5.

## Fuentes y límites

- [etaHEN](https://github.com/etaHEN/etaHEN): modificaciones e integración con ShellUI en una consola real. GPL-3.0; su código no se incorpora a este repositorio.
- [Inyección ELF en PS5](https://reversing.codes/posts/PlayStation-5-ELF-Injection/): investigación sobre ejecución dentro de SceShellUI.
- [AnyPS5](https://github.com/boykopovar/AnyPS5): conversión de ejecutables y bibliotecas compatibles.

Los nombres extraídos son evidencia de referencias en un proyecto público, no prueba de una implementación completa de Sony. No hay archivos de firmware, claves ni recursos originales de Sony en este proyecto. Los informes de archivos locales se mantienen fuera de Git.

Código de las herramientas: licencia MIT.

