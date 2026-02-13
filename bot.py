import discord 
import pylast 
import os 
import re 
import random
from discord.ext import tasks 
from dotenv import load_dotenv

load_dotenv()

sad= [
    'sad', 'depressive', 'melancholy', 'gloom', 'heartbreak',
    'emo','slowcore','sadcore','doom metal','shoegaze','post-rock','ballad'        
]

horrible = [
    'corridos tumbados', 'sierreno', 'corrido', 'banda', 'norteño', 'regional mexican', 'norteño',
    'reggaeton', 'urbano', 'latin urban', 'trap latino', 'dembow', 'perreo', 'reggae',
    'ranchera', 'mariachi', 'bolero'
]

class MuK(discord.Client):
    def __init__(self):

        mis_reglas = discord.Intents.default()
        mis_reglas.message_content = True
        super().__init__(intents=mis_reglas)

        self.network = pylast.LastFMNetwork(
            api_key=os.getenv("LASTFM_API_KEY"),
            api_secret=os.getenv("LASTFM_SHARED_SECRET")
        )

        self.usuarios = {} 

    async def setup_hook(self):
        self.vigilar_musica.start()

    async def on_ready(self):
        print(f'El Bot se conectó exitosamente como {self.user}')

    @tasks.loop(seconds=30)
    async def vigilar_musica(self):
        if not self.usuarios:
            return

        for discord_id, datos in self.usuarios.items():
            try:
                user_api = self.network.get_user(datos['user_fm'])
                track = user_api.get_now_playing()

                if track and track.title != datos['ultima']:
                    datos['ultima'] = track.title
                    
                    tags = [t.item.name.lower() for t in track.artist.get_top_tags(limit=5)]
                    print(f"Tags encontrados para {track.artist.name}: {tags}")
                    es_triste = any(word in tags for word in sad)
                    es_horrible = any(word in tags for word in horrible)
                    canal = self.get_channel(datos['canal'])
                    
                    if canal:
                        usuario_discord = f"<@{discord_id}>" 
                        if any(t in tags for t in horrible):
                                mensajes_queja = [
                                    f"Guácala... {usuario_discord} puso **{track.artist.name}**. Mis circuitos no soportan esto.",
                                    f"{usuario_discord}, por favor quita eso. **{track.artist.name}** está prohibido en este servidor.",
                                    f"{usuario_discord} cayó bajo escuchando **{track.title}**. Qué decepción."
                                ]
                                await canal.send(random.choice(mensajes_queja))
                        elif any(t in tags for t in sad):
                                await canal.send(f"Oye {usuario_discord}... estas escuchando (**{track.title}**). ¿estas triste? ¿Quieres un abrazo?")
                        else:
                                await canal.send(f" {usuario_discord} estás escuchando **{track.title}** de {track.artist.name}. ¡Tienes un excelente gusto!")

            except Exception as e:
                print(f"Error revisando a un usuario: {e}")
                continue







    async def on_message(self, message):
        if message.author == self.user:
            return

        txt = message.content.lower() 

        if txt.startswith('!login '):
            user_fm = txt.replace('!login ', '').strip()
            
            self.usuarios[message.author.id] = {
                'user_fm': user_fm,
                'canal': message.channel.id,
                'ultima': None
            }
            await message.channel.send(f"¡Listo {message.author.mention}! Te vinculé con: **{user_fm}**. Te vigilaré en este canal.")

        if txt.startswith('hola muk'):
            await message.channel.send(f'¡Hola {message.author.display_name}! ¿Qué se te ofrece?')

        if txt.startswith('!info '):
            artist_buscado = txt.replace('!info ', "").strip()
            try:
                artist = self.network.get_artist(artist_buscado)
                bio = artist.get_bio_summary()
                bio = re.sub(r'<[^>]*>', " ", bio).strip()
                if not bio or bio.startswith("Read more"):
                    await message.channel.send(f"El artista '**{artist_buscado}**' no existe en mis registros o no tiene biografía.")
                else:
                    await message.channel.send(bio)
            except:
                await message.channel.send(f"Híjole, hubo un error buscando a '{artist_buscado}'.")

        if txt.startswith('!rec '):
            artist_reco = txt.replace('!rec ', "").strip()
            try:
                artist = self.network.get_artist(artist_reco)
                similares = artist.get_similar(limit=5)
                nombres = [s.item.name for s in similares]
                
                if nombres:
                    lista = ", ".join(nombres)
                    await message.channel.send(f"Si te gusta **{artist_reco}**, prueba con: **{lista}**.")
                else:
                    await message.channel.send("No encontré similares.")
            except:
                await message.channel.send("Error al buscar recomendaciones.")

botMuK = MuK()
botMuK.run(os.getenv("DISCORD_TOKEN"))