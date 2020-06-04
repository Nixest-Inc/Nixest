#Import's necessários (List import).
import discord, random, datetime, json
from discord.ext import commands, tasks
from config import get_aio, get
from io import BytesIO
import asyncio

#Classe do plugin 'Task'
class Task(commands.Cog):
    def __init__(self, shiro):
        """
         - Funções:
          self.shiro : Puxar as informações do bot pela classe shiro.
          self.bot : Obter informações 'dict' da classe da parte 'env' com informações do bot
          self.message : Obter informações 'dict' da classe da parte 'env' com informações da presence do bot e converter-las em uma 'dict'
          self.presence : Colocar toda as atividades (jogando, ouvindo, etc) de presence do bot em uma dict.
          self.status : Colocar todo os status (online, afk, não pertube) da presence do bot em uma dict.
          self.presence : Colocar toda as tasks (funções automatizas) em uma dict.
        """
        self.shiro = shiro
        self.bot = self.shiro.env.bot           
        self.message = {'listening':self.shiro.env.bot.presence.listening,'watching':self.shiro.env.bot.presence.watching,'streaming':self.shiro.env.bot.presence.streaming,'playing':self.shiro.env.bot.presence.playing}
        self.presence = [discord.ActivityType.listening,discord.ActivityType.watching,discord.ActivityType.streaming,discord.ActivityType.playing]
        self.status = [discord.Status.online,discord.Status.dnd,discord.Status.idle]
        self.emoji = get("./json/emoji.json", simple=True)

        #self.tasks = [('change_avatar', self.change_avatar.start())]

    #Gerar gerar o url e converter o url em bytes.
    async def icon_data(self, data, color):
      data = await get_aio(f"https://img.icons8.com/{data['type']}/{data['size']}/{color.color[1]}/{data['real']}.png", res_method="read")
      return data
    
    #Evento pra quando executar a ação caso demorar gerar um erro.
    async def event_coro(self, coro):
       try:
           #Converter uma função não asyncronizada em uma.
           coro = await asyncio.wait_for(coro, timeout=10.0)
      #Caso ouver algum erro na execução em relação a demora.
       except asyncio.TimeoutError:
           return None
      #Caso ouver algum erro na execução em relação a não encontrado ou algum erro.
       except (discord.NotFound, discord.HTTPException) as e:
           return False
       else:
         #retornar a função.
         return coro    
    
    #Criar um emoji no servidor
    async def create_emoji(self, guild, name, bio):
       return await self.event_coro(guild.create_custom_emoji(name=name, image=bio))     
    
    
    @commands.command(name='tt')
    async def _modulesss(self, ctx):
        #Obter os emojis do bot.
        emoji_data = get("./json/emoji.json", simple=True)
        #Puxar todos os id's das guild quem tem os emojis do bot
        for guild in self.shiro.env.bot.emoji:    
          #Puxar as informações da guild, canais, emojis, cargos etc.
          guild = await self.shiro.fetch_guild(guild) 
          #obter todo os emojis da guild e passar por um for.
          for emoji in await guild.fetch_emojis():
              #Obter as informações do emoji
              data = emoji_data[emoji.name]
              #Criar o emoji em bytes.
              icon = await self.icon_data(data, self.shiro)
              #Deletar o emoji.
              await emoji.delete()
              #Criar um emoji novo com a image.
              emoji = await self.create_emoji(guild, emoji.name, icon)
              #Trocar o code do emoji antigo pelo novo.
              emoji_data[emoji.name].update(code=f'{emoji}')
        #Abrir o arquivo emoji.json
        with open('./json/emoji.json', 'w+') as jsonf:
           #Inserir todo os emojis no json e salvar-los e depos indenta-los.
           json.dump(emoji_data, jsonf, indent=4, sort_keys=True)
        #Inserir os novos emojis na classe pro bot.             
        self.shiro.emoji = get("./json/emoji.json")
        await ctx.send("ok")

    #Task para trocar o avatar e as cores do embed.
    @tasks.loop(minutes=2)
    async def change_avatar(self):
       try: 
           #Puxar as informações do avatar e fazer um aleátorio com elas.
           info = random.choice(self.shiro.env.bot.image)
           #Ler o avatar e converter.
           avatar = open(info.path, 'rb').read()
           #Trocar as cores do embed.
           self.shiro.color = [discord.Colour.from_rgb(*info.rgb[0]), discord.Colour.from_rgb(*info.rgb[1]), info.rgb[2]]
           #Trocar o avatar do bot.
           #await self.shiro.user.edit(avatar=avatar)
           #Puxar os emojis do json.
           emoji_data = get("./json/emoji.json", simple=True)
           for guild in self.shiro.env.bot.emoji:    
              guild = await self.shiro.fetch_guild(guild) 
              #Pegar todo os emojis da guild é passar por um for.
              for emoji in await guild.fetch_emojis():
                 #Deletar o emoji.
                 await emoji.delete()
                 #Executar a função de criar emoji e pegar o código.
                 emoji = await self.create_emoji(guild, emoji.name,(await self.icon_data(emoji_data[emoji.name], self.shiro.color[2])))
                 #Trocar o code do emoji antigo pelo novo.
                 emoji_data[emoji.name].update(code=f'{emoji}')
           
           #Abrir o arquivo down.json
           with open('./json/emoji.json', 'w+') as jsonf:
                #Inserir todo os emojis no json e salvar-los e depos indenta-los.
                json.dump(emoji_data, jsonf, indent=4, sort_keys=True)
           
           self.shiro.emoji = get("./json/emoji.json")
       
       except Exception as e:
        #Caso ouver algum erro na execução da task.
        print(e)
    
    #Task para trocar a presence do bot e a mensagem.
    @tasks.loop(minutes=10)
    async def change_presence(self):
      try:
        #Passar todos os shard do bot no 'for', e após passar usar o 'try' para executar a mudança do presence.
        for shard in self.shiro.shards:
            #Puxar uma atividade aleatoria da presence (jogando, ouvindo etc)
            activity = random.choice(self.presence)
            #Puxar uma messagem aleátoria  da presence.
            message = random.choice(self.message[activity.name]).format(website=self.bot.link.website, prefix=self.bot.prefix[0])
            #Definir o presence.
            await self.shiro.change_presence(activity=discord.Activity(type=activity, name=message + f' [{shard}]',url=self.bot.link.twitch), shard_id=shard, status=random.choice(self.status))
      except Exception as e:
        #Caso ouver algum erro na execução da task.
        print(e)


#Adicionar o plugin na lista.
def setup(shiro):
    shiro.add_cog(Task(shiro))        