# PRD — XP Terminal Coding RPG

## Problema y usuario

Desarrolladores que trabajan en terminal quieren una recompensa personal por su actividad de Git, sin ceder sus datos a un servicio remoto. XP convierte commits y merges en progreso RPG guardado localmente.

## Resultado

Una herramienta instalable con `pip`, cuyos comandos funcionan en Windows, macOS y Linux con Python 3.7+ y Git. La página del producto explica con honestidad el flujo local y cómo empezar.

## Objetivos

- Instalar un comando `xp` que abra el CLI real.
- Inicializar una sola vez el personaje y los datos locales.
- Instalar hooks por repositorio que puntúen commits y merges sin interferir en Git.
- Distribuir el esquema SQLite junto al paquete.
- Presentar el producto con página estática accesible y coherente con el tema del proyecto.

## No objetivos

- Cobros, cuentas, telemetría, sincronización o leaderboard remoto.
- Cambiar fórmulas RPG, economía, clases o contenido del juego.
- Desplegar o publicar el sitio.

## Éxito

Una instalación desde paquete inicia `xp`, `xp init` es idempotente, un repo puede instalar y retirar hooks, los hooks registran commits/merges y el sitio funciona sin build ni dependencias externas.
