# MuK - El Bot Crítico de Música para Discord

**MuK** es un bot de Discord impulsado por Python que se conecta a la API de **Last.fm**. Su propósito principal no es solo mostrar lo que estás escuchando, sino **juzgarte por ello**. 

MuK vigilará tus *scrobbles* en tiempo real y reaccionará dependiendo del género musical: te ofrecerá un abrazo si andas escuchando música deprimente, se quejará amargamente si pones música cuestionable (como reggaetón o corridos tumbados), y te felicitará si tienes buen gusto. Además, funciona como una enciclopedia musical básica.

## Características Principales

* **Vigilancia en Tiempo Real:** Revisa qué estás escuchando en Last.fm cada 30 segundos.
* **Respuestas Basadas en Géneros (Tags):**
    * **Modo Sad:** Si detecta géneros como *shoegaze, emo, sadcore* o *doom metal*, te preguntará si estás bien.
    * **Modo Hater:** Si detecta *corridos, reggaeton, banda* o *trap latino*, se quejará públicamente de tus gustos musicales.
    * **Modo x:** Si la música no cae en las listas anteriores, te felicitará por tu excelente gusto.
* **Información de Artistas:** Obtén un resumen biográfico de cualquier artista.
* **Recomendaciones:** Descubre artistas similares basados en la base de datos de Last.fm.

## Requisitos Previos

Para correr este bot, necesitarás tener instalado **Python 3.8+** y las siguientes librerías:

```bash
pip install discord.py pylast python-dotenv
```

Además, necesitarás crear credenciales en dos plataformas:
1.  Un **Token de Bot de Discord** (desde el [Discord Developer Portal](https://discord.com/developers/applications)).
2.  Una **API Key y Shared Secret de Last.fm** (desde [Last.fm API Accounts](https://www.last.fm/api/account/create)).

## Instalación y Configuración

1. Clona este repositorio o descarga el script principal.
2. Crea un archivo llamado `.env` en la misma carpeta que tu script de Python.
3. Añade tus credenciales al archivo `.env` con el siguiente formato:

```env
DISCORD_TOKEN=tu_token_de_discord_aqui
LASTFM_API_KEY=tu_api_key_de_lastfm_aqui
LASTFM_SHARED_SECRET=tu_shared_secret_de_lastfm_aqui
```

4. Ejecuta el bot:

```bash
python nombre_de_tu_archivo.py
```

## Comandos del Bot

| Comando | Descripción |
| :--- | :--- |
| `!login <usuario_lastfm>` | Vincula tu cuenta de Discord con tu usuario de Last.fm. El bot empezará a vigilar tus reproducciones en el canal donde uses este comando. |
| `hola muk` | Un simple saludo para comprobar que el bot está vivo y respondiendo. |
| `!info <artista>` | Busca y muestra un resumen biográfico del artista especificado (en inglés, extraído de Last.fm). |
| `!rec <artista>` | Te da una lista de 5 artistas similares recomendados para que amplíes tu repertorio. |

## Personalización

Si quieres cambiar los géneros que el bot odia o considera tristes, simplemente edita las listas `sad` y `horrible` al principio del código fuente:

```python
sad = [ 'sad', 'depressive', 'shoegaze', 'post-rock', ... ]
horrible = [ 'corridos tumbados', 'reggaeton', 'banda', ... ]
```
*Nota: Los tags deben estar en minúsculas y coincidir con las etiquetas (tags) utilizadas por los usuarios en Last.fm.*
