import discord
import os


intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

team_string = """team-names
"""
z = team_string.split("\n")
teams = []
for a in z:
  teams.append(a.strip())
print(teams)

@client.event
async def on_ready():
    print("Bot ready! Hi, I'm {0}".format(client.user))
    await client.change_presence(status= discord.Status.idle, activity=discord.Activity(type=discord.ActivityType.playing, name="Hackathon"))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith(">hello"):
    await message.channel.send("Hello {0} :3".format(message.author.mention))

  
  # check my id
  if message.author.id == 570072181292269569:
    # create roles
    if msg.startswith(">create all roles"):
      for team in teams:
        role = await message.guild.create_role(name=team, permissions=discord.Permissions(446713683520), mentionable=True, color=discord.Colour.from_rgb(34, 16, 41))
        await message.channel.send(f"Successfully created {role.mention}!")
    
    # create channels
    if msg.startswith(">create all channels"):
      for team in teams:
        role = discord.utils.get(message.guild.roles, name=team)
        overwrites = {
            message.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            message.author: discord.PermissionOverwrite(view_channel=True),
            role: discord.PermissionOverwrite(view_channel=True)
        }
        channel = await message.guild.create_text_channel(team, category=discord.utils.get(message.guild.categories, name="whackiest'2023 - 4"), overwrites=overwrites)

        voice_channel = await message.guild.create_voice_channel(team, category=discord.utils.get(message.guild.categories, name="whackiest'2023 - 4"), overwrites=overwrites)
        
        await message.channel.send(f"Successfully created {channel.mention} and {voice_channel.mention}!")
   
    # assign member
    if msg.startswith(">assign"):
      role = message.role_mentions[0]
      for user in message.mentions:
        await user.add_roles(role)
        await message.channel.send(f"{user.mention} has been given {role.mention}")
        await message.channel.send(f"{user.mention}, you will be able to access your private channel now, if you can't find, DM <@{570072181292269569}>")
    
    #assign mentor
    if msg.startswith(">mentor"):
      for role in message.role_mentions:
        for user in message.mentions:
          await user.add_roles(role)
          await message.channel.send(f"{user.mention} has been given {role.mention}")
    
    



client.run(os.getenv('TOKEN'))
