#import's necessários
from config import Shiro, env, emoji
import discord

#Definir algumas coisas na classe da shiro como prefix, shards, game etc.
kitsune = Shiro(
             command_prefix=env.bot.prefix, 
             env=env,
             emoji=emoji,
             activity=discord.Game(f'with senko | s.help'),
             help_command=None,
             shard_ids=[int(x) for x in range(1)],
             shard_count=int(1)
             )
#Evento para puxar a classe da shiro e executar o token.
if __name__ == "__main__":
    kitsune.run(env.app.token)
