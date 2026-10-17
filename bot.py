import discord
import random
from discord.ext import commands
from config import token

#çalışması için izinler
intents = discord.Intents.default()
intents.members = True          # Kullanıcıları listelemek ve banlamak için
intents.message_content = True  # Mesaj içeriklerini okuyabilmek

#BOT TANIMLAMASI (// ile başlar)
bot = commands.Bot(command_prefix=['//'], intents=intents)

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.event
async def on_message(message):
    # Botların kendi mesajlarına cevap vermesini engeller
    if message.author.bot:
        return

    # Eğer mesaj botun ön eklerinden biriyle başlıyorsa, onu komut olarak işle
    if message.content.startswith(tuple(bot.command_prefix)):
        await bot.process_commands(message)
    

@bot.command()
async def merhaba(ctx):
    await ctx.send("Merhaba! Ben senin asistan botunum, Nasıl yardımcı olabilirim :)")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None):
    if member:
        if ctx.author.top_role <= member.top_role:
            await ctx.send("Eşit veya daha yüksek rütbeli bir kullanıcıyı banlamak mümkün değildir!")
        else:
            await ctx.guild.ban(member)
            await ctx.send(f"Kullanıcı {member.name} banlandı")
    else:
        await ctx.send("Bu komut banlamak istediğiniz kullanıcıyı işaret etmelidir. Örneğin: `//ban @user`")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Bu komutu çalıştırmak için yeterli izniniz yok.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("Kullanıcı bulunamadı!")

@bot.command()
async def about(ctx):
    await ctx.send('Bu bot kullanıcı banlayabilir,kumar komutları kullanabilir')

@bot.command()
async def roll(ctx, dice: str):
    # Girilen zar bilgisini d harfinden ayırır ("2d6" -> rolls = 2, limit = 6)
    try:
        rolls, limit = map(int, dice.lower().split('d'))
    except ValueError:
        await ctx.send('Format hatalı! Örnek: //roll 2d6 veya !roll 2d6')
        return

    # Zar sayısını ve zar yüzünü sınırlandırır
    if not (1 <= rolls <= 100 and 1 <= limit <= 1000000):
        await ctx.send('Zar sayısı 1-100, zar yüzü 1-1000000 arasında olmalı.')
        return

    # Rastgele zar atma işlemi
    result = ', '.join(
        str(random.randint(1, limit))
        for _ in range(rolls)
    )
    await ctx.send(f'🎲 Sonuç: {result}')

@bot.command()
async def cf(ctx):
    # Yazı veya tura sonucunu rastgele seçer
    result = random.choice(['Yazı', 'Tura'])
    await ctx.send(f'🪙 Sonuç: **{result}**')

bot.run(token)
