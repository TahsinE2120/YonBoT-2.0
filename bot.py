import discord
import random
import datetime  # Zaman aşımı (Timeout) süresi hesaplamak için eklendi
from discord.ext import commands
from config import token

intents = discord.Intents.default()
intents.guilds = True           # Sunucu yapısını ve kanalları görebilmek için eklendi
intents.members = True          # Kullanıcı katılım, ayrılış ve ban işlemlerini yakalamak için
intents.message_content = True  # Mesaj içeriklerini okuyabilmek

# BOT TANIMLAMASI (// ile başlar)
bot = commands.Bot(command_prefix=['//'], intents=intents)

UYE_ROL_ISMI = "üye" # gelenlere verilecek rol
HOSGELDIN_KANAL_ISMI = "gelen-giden"  # başka kanala yazmasın diye

# KELİME FİLTRESİ
TIMEOUT_WORDS = ["mal", "salak", "aptal", "beyinsiz", "angut", "gerizekalı", "gerizekali", "dangalak", "budala", "ahmak", "ezik", "yavşak", "yavsak", "hıyar", "hiyar", "şapşal", "sapsal", "terbiyesiz", "densiz", "saygısız", "saygisiz", "bok", "boktan", "haysiyetsiz", "şerefsiz", "serefsiz", "pislik", "ukala", "kafasız", "kafasiz"]
BAN_WORDS = ["oç", "oc", "o.c", "orospu", "orospu çocuğu", "orospu cocugu", "pezevenk", "avel", "sikeyim", "skym", "sik", "sikerim", "siktir", "siktir git", "amk", "aq", "a.q", "amq", "mk", "amcık", "amcik", "amcığ", "yarrak", "yarak", "piç", "pic", "ibne", "götveren", "gotveren", "kahpe", "puşt", "pust", "sikik", "sik kafa", "ananı sikeyim", "anani sikeyim", "babanı sikeyim", "babani sikeyim", "ananı avradını", "anani avradini", "göt", "got", "yarram", "siktim", "sikiyim", "hassiktir", "hasiktir", "dalyarak", "gavat", "ibnenin", "orospu evladı", "orospu evladi", "amına koyayım", "amina koyayim", "amına koyim", "amina koyim", "ananı", "anani"]

@bot.event
async def on_ready():
    print(f'Giriş yapıldı: {bot.user.name}')

@bot.event
async def on_member_join(member):
    #OTOMATİK ROL VERME SİSTEMİ
    role = discord.utils.get(member.guild.roles, name=UYE_ROL_ISMI)
    if role:
        try:
            await member.add_roles(role)
            print(f"Başarılı: {member.name} kullanıcısına otomatik olarak '{UYE_ROL_ISMI}' rolü verildi.")
        except discord.Forbidden:
            print(f"Hata: Botun rol sırası '{UYE_ROL_ISMI}' rolünden aşağıda olduğu için rol verilemedi!")
        except Exception as e:
            print(f"Rol verme hatası: {e}")
    else:
        print(f"Hata: Sunucuda '{UYE_ROL_ISMI}' adında bir rol bulunamadı!")

    #ÖZEL KANALA HOŞ GELDİN MESAJI GÖNDERME
    welcome_channel = discord.utils.get(member.guild.text_channels, name=HOSGELDIN_KANAL_ISMI)
    
    if not welcome_channel:
        welcome_channel = member.guild.system_channel

    if welcome_channel:
        await welcome_channel.send(f"👋 Hoş geldin {member.mention}! Sunucumuza katıldığın için mutluyuz. Seninle birlikte **{member.guild.member_count}** kişi olduk! 🎉")
    #ÖZEL KANALA AYRILMA BİLDİRİMİ
@bot.event
async def on_member_remove(member):
    welcome_channel = discord.utils.get(member.guild.text_channels, name=HOSGELDIN_KANAL_ISMI)
    
    if not welcome_channel:
        welcome_channel = member.guild.system_channel

    if welcome_channel:
        await welcome_channel.send(f"📤 **{member.name}** sunucudan ayrıldı. Aramızda kalan kişi sayısı: **{member.guild.member_count}** 😔")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content_lower = message.content.lower()

    # OTOMATİK BAN KONTROLÜ (Ağır Küfürler)
    if any(ban_word in content_lower for ban_word in BAN_WORDS):
        try:
            if message.guild.me.top_role > message.author.top_role:
                await message.author.ban(reason="Otomatik Filtre: Ağır Küfür / Yasaklı Kelime")
                await message.channel.send(f"🚨 {message.author.mention}, yasaklı kelime kullandığı için otomatik olarak **banlandı**!")
                return  
            else:
                await message.channel.send("❌ Yasaklı kelime tespit edildi ancak kullanıcının rolü benden yüksek veya eşit olduğu için banlayamadım.")
        except discord.Forbidden:
            await message.channel.send("❌ Yetkim yetersiz olduğu için kullanıcıyı banlayamadım.")
        except Exception as e:
            print(f"Ban hatası: {e}")

    # OTOMATİK ZAMAN AŞIMI KONTROLÜ (Hafif Hakaretler)
    words_in_message = content_lower.split()
    if any(timeout_word in words_in_message for timeout_word in TIMEOUT_WORDS):
        try:
            if message.guild.me.top_role > message.author.top_role:
                duration = datetime.timedelta(minutes=10)
                await message.author.timeout(duration, reason="Otomatik Filtre: Hakaret / Yasaklı Kelime")
                
                await message.delete()
                await message.channel.send(f"⚠️ {message.author.mention}, yasaklı kelime kullandığın için **10 dakika zaman aşımı** uygulandı ve mesajın silindi!")
                return  
            else:
                await message.channel.send("❌ Yasaklı kelime tespit edildi ancak kullanıcının rolü benden yüksek veya eşit olduğu için zaman aşımı uygulayamadım.")
        except discord.Forbidden:
            await message.channel.send("❌ Yetkim yetersiz olduğu için zaman aşımı uygulayamadım.")
        except Exception as e:
            print(f"Timeout hatası: {e}")

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
    try:
        rolls, limit = map(int, dice.lower().split('d'))
    except ValueError:
        await ctx.send('Format hatalı! Örnek: //roll 2d6 veya !roll 2d6')
        return

    if not (1 <= rolls <= 100 and 1 <= limit <= 1000000):
        await ctx.send('Zar sayısı 1-100, zar yüzü 1-1000000 arasında olmalı.')
        return

    result = ', '.join(
        str(random.randint(1, limit))
        for _ in range(rolls)
    )
    await ctx.send(f'🎲 Sonuç: {result}')

@bot.command()
async def cf(ctx):
    result = random.choice(['Yazı', 'Tura'])
    await ctx.send(f'🪙 Sonuç: **{result}**')

bot.run(token)
