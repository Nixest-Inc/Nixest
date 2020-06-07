#Import's necessários (List import).
from motor import motor_asyncio
from .models import Guild

#Classe principal da Database.
class on_connect_db():
    def __init__(self, *, name, uri, bot):
        """
         - Funções:
          self.connection : Fazer a conexão com o banco de dados mongoDB através do Motor asyncio.
          self.db : Puxa informações da 'collection'.
        """
        self.roxanne = bot
        self.connection = motor_asyncio.AsyncIOMotorClient(uri)
        self.db = db = self.connection[name]
        self.guilds = db.guilds
    
    #Puxar as informações de um servidor e passar as informações pela classe Guild
    async def get_guild(self, guild_id, *, register=True):
        data = await self.guilds.find_one({"_id": guild_id})
        if data != None:
            return Guild(data, self.guilds)
        elif register:
            return await self.register_guild(guild_id)
    
    #Registrar um servidor caso o mesmo não esteja registrado no banco de dados MongoDB
    async def register_guild(self, guild_id):
        data = {
                "_id": guild_id,
                "config":{"prefix":"rx.","language":"pt_BR"},
                "disable":{"command":[],"channel":[],"role":[],"member":[]}
                }
        await self.guilds.insert_one(data)
        return Guild(data, self.guilds)            