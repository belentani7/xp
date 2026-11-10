# Design — XP como producto local instalable

## Intención

Convertir el RPG local ya existente en una herramienta que se pueda instalar, iniciar y conectar de forma segura a repos Git, con una página que explique exactamente qué ofrece.

## Decisiones y enfoques

- **Distribución:** se conserva el motor y se mueve la interfaz CLI al paquete `engine`; `xp` y `python -m engine` quedan como lanzadores ligeros. Alternativa descartada: empaquetar el archivo ejecutable raíz como `data_files`, porque la ruta depende del sistema y del entorno de instalación.
- **Persistencia e integración:** SQLite bajo `~/.xp`; hooks Python por repositorio con invocación aislada y restauración segura. Alternativa descartada: hooks globales, por su alcance implícito sobre repositorios ajenos.
- **Sitio:** HTML estático autocontenido, acorde a negro, rojo, oro y cyan del canon. Alternativa descartada: framework/build externo, incompatible con despliegue sin build y sin necesidad funcional.

## Alcance y límites

Objetivos: comando instalable, inicio no destructivo, integración Git explícita, distribución reproducible, landing informativa y pruebas de contrato. No objetivos: pagos, servicio en nube, multiplayer, analítica ni cambio de mecánicas.

## Restricciones

Python 3.7+, sin dependencias runtime; Windows/macOS/Linux; datos locales; conservar compatibilidad con el ejecutable y hooks históricos donde sea posible. No modificar CI, secretos ni reglas protegidas.

## Arquitectura propuesta

`engine.cli` será la interfaz de comandos; `engine.rpg` seguirá siendo dominio/persistencia; el esquema pasa a ser un recurso incluido con `engine`. El CLI administra hooks locales de Git que invocan módulos Python con `sys.executable`. El sitio se entrega como archivos estáticos existentes.

## Criterios de aceptación

Los contratos de CLI, paquete, inicialización, hooks y landing se cubren con pruebas GWT; `python -m pytest -q` y una construcción de distribución deben completarse correctamente.
