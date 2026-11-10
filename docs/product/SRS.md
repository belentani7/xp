# SRS — XP Terminal Coding RPG

## Interfaces

- Python 3.7+, stdlib en tiempo de ejecución; setuptools solo para empaquetar.
- `xp` y `python -m engine` invocan el mismo CLI.
- `xp init [--name NAME]` crea el personaje de forma idempotente; no reinicia datos existentes.
- `xp install-hooks` instala hooks en el repositorio actual; `xp uninstall-hooks` los quita solo si pertenecen a XP.
- Los datos permanecen en `~/.xp/player.db`; sin red ni datos sensibles.
- El sitio raíz es HTML/CSS/JS estático, español, adaptable, accesible y sin build.

## Requisitos funcionales

1. Distribución wheel/sdist incluye CLI, motor y esquema; consola script apunta a una función importable.
2. Arranque automático nunca reemplaza un personaje existente.
3. Hooks usan `sys.executable`, argumentos del proceso y consultas Git acotadas; errores internos no hacen fallar commits.
4. Desinstalar hooks conserva hooks previos ajenos a XP y rechaza sobrescribirlos al instalar.
5. Landing explica bucle de juego, comandos e instalación reproducible; los enlaces tienen destino real.

## Calidad

No introducir dependencias runtime, llamadas de red, secrets ni cambios de economía. Asegurar foco visible, contraste, controles táctiles, reducción de movimiento, semántica y estados de error comprensibles.
