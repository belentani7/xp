# XP — Terminal Coding RPG

**Convierte tu actividad de Git en progreso RPG.** Cada commit suma experiencia; fixes, features y merges pueden desbloquear niveles, equipo, logros y fragmentos de historia.

XP guarda tu personaje localmente en SQLite. No crea cuentas ni envía telemetría. Funciona en Windows, macOS y Linux con Python 3.7+ y Git.

## Instalar

Instala desde el repositorio oficial:

    python -m pip install git+https://github.com/belentani7/xp.git

Crea tu personaje:

    xp init --name Ada
    xp status
    xp class

El comando de inicialización es seguro de repetir: conserva el personaje y el progreso que ya existan.

## Activar XP en un repositorio

Desde cada repositorio donde quieras registrar actividad:

    cd mi-proyecto
    xp install-hooks

Los hooks locales registran commits y merges y no bloquean Git si XP encuentra un error. Si ya hay un hook de otra herramienta, XP se detiene y lo conserva. Para quitar solo los hooks de XP:

    xp uninstall-hooks

La integración es opt-in por repositorio; la instalación del paquete no modifica tus repositorios.

## Comandos

| Comando | Acción |
| --- | --- |
| `xp status` | Muestra personaje, nivel, estadísticas y racha |
| `xp quest` | Muestra misiones y progreso |
| `xp achievements` | Lista logros |
| `xp class [nombre]` | Consulta o elige Warrior, Mage, Rogue o Healer |
| `xp items` / `xp equip [objeto]` | Explora y equipa objetos |
| `xp log [N]` | Muestra las últimas ganancias de XP |
| `xp streak` | Muestra tu racha de actividad |
| `xp combat [bug]` | Inicia un combate manual |
| `xp lore` | Muestra la historia desbloqueada |
| `xp leaderboard` | Muestra tu personaje y entradas locales compartidas |
| `xp help` | Ayuda completa |

El leaderboard es local: XP no proporciona un servicio en línea. Puedes compartir manualmente `~/.xp/leaderboard.json`.

## Privacidad y datos

- La base de datos del personaje está en `~/.xp/player.db`.
- La integración Git se instala solo cuando ejecutas `xp install-hooks` en un repositorio.
- No hay cuentas, sincronización remota, telemetría ni dependencias de ejecución externas.

## Desarrollo

Desde el checkout:

    python -m engine --help
    python -m pytest -q
    python setup.py sdist bdist_wheel

El sitio estático se sirve desde `index.html` y `site/index.html`; no requiere build. La distribución usa setuptools para empaquetar el CLI, el motor y el esquema SQLite.

## Licencia

MIT. Consulta [LICENSE](LICENSE).

La historia de Studio 7 empieza en el primer commit. El sistema recuerda.


## Producto
Véase `plataforma/OFERTA.md`, `plataforma/precios.json`, `plataforma/ONEPAGER.md`.
