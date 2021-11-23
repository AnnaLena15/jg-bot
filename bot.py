import asyncio
import random
import datetime
import dotenv
import discord
from discord import Member, Guild, User
from discord.ext import commands


client: commands.Bot = commands.Bot(command_prefix="j.")

extensions = [
    "commands"
]
#########################################################################

antworten = ['Ja', 'Nein', 'Vielleicht', 'Wahrscheinlich', 'Sieht so aus', 'Sehr wahrscheinlich',
             'Sehr unwahrscheinlich']

autoroles = {
    658960248345853952: {'memberroles': [667129769397059596, 667129722995474460], 'botroles': [667129686131736586]},
    643782995869827092: {'memberroles': [], 'botroles': []}
}

now = datetime.datetime.now()
current = now.strftime("%Y-%m-%d %H:%M:%S")
deathquotes = [
    'Du wixxer']

badwordlist = open("badwordlist.txt", "r").read().split()


@client.event
async def on_ready():
    print('Wir sind eingeloggt als User {}'.format(client.user.name))
    client.loop.create_task(status_task())


async def status_task():
    colors = [discord.Colour.red(), discord.Colour.orange(), discord.Colour.gold(), discord.Colour.green(),
              discord.Colour.blue(), discord.Colour.purple()]
    while True:
        await client.change_presence(activity=discord.Game('Jugendstelle'), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game('Dein Community Netzwerk'), status=discord.Status.online)
        await asyncio.sleep(5)
        guild: Guild = client.get_guild(658960248345853952)
        if guild:
            role = guild.get_role(662606175862521856)
            if role:
                if role.position < guild.get_member(client.user.id).top_role.position:
                    await role.edit(colour=random.choice(colors))


def is_not_pinned(mess):
    return not mess.pinned


@client.event
async def on_member_join(member):
    guild: Guild = member.guild
    if not member.bot:
        embed = discord.Embed(title='Willkommen auf Jugendstelle {} <a:tut_herz:662606955520458754>'.format(member.name),
                              description='Wir heißen dich herzlich Willkommen auf unserem Server!', color=0x22a7f0)
        try:
            if not member.dm_channel:
                await member.create_dm()
            await member.dm_channel.send(embed=embed)
        except discord.errors.Forbidden:
            print('Es konnte keine Willkommensnachricht an {} gesendet werden.'.format(member.name))
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['memberroles']:
            for roleId in autoguild['memberroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)
    else:
        autoguild = autoroles.get(guild.id)
        if autoguild and autoguild['botroles']:
            for roleId in autoguild['botroles']:
                role = guild.get_role(roleId)
                if role:
                    await member.add_roles(role, reason='AutoRoles', atomic=True)


@client.event
async def on_message(message):
    await client.process_commands(message)
    if '!help' in message.content:
        await message.channel.send('**Hilfe zum Jugendstelle Bot**\r\n'
                                   '!help - Zeigt diese Hilfe an')

    if message.author == client.user: #no real reason for this, the bot is never going to call itself, but it takes 5 seconds to implement so i might as well
        return
    if message.content == 'hallo bot':
        response = f'hallo Mensch {message.author}'
        print(f'sent {response}')
        await message.channel.send(response)

    for word in badwordlist:
        #add 'eyes' reaction when a banned word is said and log it to file and console
        if word in message.content.lower():
            print(f'{message.author} Sagte ein Böses wort, {random.choice(deathquotes)}.')
            """with open("log.txt", "a") as f:
                f.write(f'{datetime.datetime.now()}: {message.author.id} als {message.author} in server {message.guild} sagte ein gesperrtes wort in der nachricht \'{message.content}\'\n' )
                f.close()"""
            await message.delete()
            role = message.guild.get_role(906542845287084065)
            msg = await message.channel.send(f"{message.author} sagte {word} Dies wird Gespeichert")
            await msg.add_reaction('<:kanna8:910887432860340254>')
            channel = await client.fetch_channel(912490324935450685)
            msg = await channel.send(f"{message.author} sagte {word} {role.mention}")
            await msg.add_reaction('<:kanna8:910887432860340254>')


            return

    if message.content.startswith('j.ban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.ban()
                await message.channel.send(f'Member {member.name} gebannt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
    if message.content.startswith('j.unban') and message.author.guild_permissions.ban_members:
        args = message.content.split(' ')
        if len(args) == 2:
            user: User = discord.utils.find(lambda m: args[1] in m.user.name, await message.guild.bans()).user
            if user:
                await message.guild.unban(user)
                await message.channel.send(f'User {user.name} entbannt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')
    if message.content.startswith('j.kick') and message.author.guild_permissions.kick_members:
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                await member.kick()
                await message.channel.send(f'Member {member.name} gekickt.')
            else:
                await message.channel.send(f'Kein user mit dem Namen {args[1]} gefunden.')

    if message.content.startswith('j.clear'):
        if message.author.permissions_in(message.channel).manage_messages:
            args = message.content.split(' ')
            if len(args) == 2:
                if args[1].isdigit():
                    count = int(args[1]) + 1
                    deleted = await message.channel.purge(limit=count, check=is_not_pinned)
                    await message.channel.send('{} Nachrichten gelöscht.'.format(len(deleted) - 1))
    if message.content.startswith('!8ball'):
        args = message.content.split(' ')
        if len(args) >= 2:
            frage = ' '.join(args[1:])
            mess = await message.channel.send('Ich versuche deine Frage `{0}` zu beantworten.'.format(frage))
            await asyncio.sleep(2)
            await mess.edit(content='Ich kontaktiere das Orakel...')
            await asyncio.sleep(2)
            await mess.edit(content='Deine Antwort zur Frage `{0}` lautet: `{1}`'.format(frage,
                                                                                         random.choice(antworten)))


@client.command()
async def userinfo(ctx: commands.Context, *, member: discord.Member = None):
    if not member:
        member = ctx.author

    embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                          description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                          color=0x22a7f0)
    embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                    inline=True)
    embed.add_field(name='Rollen', value=member.top_role, inline=False)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text='Jugendstelle Nutezrinformation.')
    mess = await ctx.send(embed=embed)
    # await mess.add_reaction(":KExclaim:")
    await mess.add_reaction('<a:KExclaim:910887898398748724>')

if __name__ == "__main__":
    for ext in extensions:
        client.load_extension(ext)
    client.run('')


"""
 if message.content.startswith('j.userinfo'):
        args = message.content.split(' ')
        if len(args) == 2:
            member: Member = discord.utils.find(lambda m: args[1] in m.name, message.guild.members)
            if member:
                embed = discord.Embed(title='Userinfo für {}'.format(member.name),
                                      description='Dies ist eine Userinfo für den User {}'.format(member.mention),
                                      color=0x22a7f0)
                embed.add_field(name='Server beigetreten', value=member.joined_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                embed.add_field(name='Discord beigetreten', value=member.created_at.strftime('%d/%m/%Y, %H:%M:%S'),
                                inline=True)
                rollen = ''
                for role in member.roles:
                    if not role.is_default():
                        rollen += '{} \r\n'.format(role.mention)
                if rollen:
                    embed.add_field(name='Rollen', value=rollen, inline=True)
                embed.set_thumbnail(url=member.avatar_url)
                embed.set_footer(text='Ich bin ein EmbedFooter.')
                mess = await message.channel.send(embed=embed)
                await mess.add_reaction('🚍')
                await mess.add_reaction('a:tut_herz:662606955520458754')
"""