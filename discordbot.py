import discord
import asyncio
import sqlite3
import random as r
from os import getenv
from dotenv import load_dotenv
from sys import argv
from discord.ext import commands

load_dotenv()
TOKEN = getenv('TOKEN')
prefix = getenv('prefix')

bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')


class messagestuff(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.channelID = 123544846521354 #place here the default channelID for the Traptalk part

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == bot.user:
            return

        # Traptalk
        if message.channel.id == 123213214465321: #channel ID where you type the messages that get send to the channel in self.channelID
            if message.author.id == 1325487654845132115: #The member ID of the people that the bot uses
                if message.content.startswith(prefix):
                    await message.delete()
                else:
                    msg = message.content
                    channel = bot.get_channel(self.channelID)
                    await channel.send(msg)

        # other on message shit
        if message.content.lower().startswith("hello trapborg"):
            await message.channel.send(
                f"Hello hello "
            )
        if message.content.lower().startswith("i like qt traps"):
            await message.channel.send(
                f"I agree :drooling_face: "
            )
        if message.content.lower() == "hey trapborg, are traps gay?":
            await message.channel.send(
                f"{message.author.mention} Of course not, traps are heterosexuality in physical form"
            )
        if message.content.lower() == "hey trapborg, are traps straight?":
            await message.channel.send(
                f"{message.author.mention} Yes!"
            )
        if message.content.lower() == "hey trapborg, do you like traps?":
            await message.channel.send(
                f"Yes! I am one myself after all.", file=discord.File("alterego.png")
            )
        if message.content.lower().startswith("good night trapborg"):
            await message.channel.send(
                f"Good night"
            )

    # TRAPTALKCOMMANDS
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def setID(self,ctx, *argv):
        self. channelID = int(argv[0])
        channel = bot.get_channel(self.channelID)
        await ctx.send(
            f"Channel ID is now set to: #{channel}"
        )

class funcommands(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.traps = [] #List the images/gifs for the qt_trap command (example "trap.png","trapgif.gif")

    @commands.command(aliases=["trap"])
    async def qt_trap(self,ctx):
        traplist = self.traps
        qttrap = r.choice(traplist)
        await ctx.send(file=discord.File(qttrap))

    @commands.command()
    async def satan(self,ctx):
        await ctx.send(file=discord.File("jigglypuff.png"))

    @commands.command()
    async def cry(self,ctx):
        await ctx.send(file=discord.File("sadferris.gif"))

    @commands.command(aliases=["imout"])
    async def nolewd(self,ctx):
        await ctx.send(file=discord.File("nolewd.gif"))

    @commands.command()
    async def bye(self,ctx):
        await ctx.send(file=discord.File("bye.gif"))

    @commands.command()
    async def FBI(self,ctx):
        await ctx.send(file=discord.File("FBI.gif"))

    @commands.command()
    async def pat(self,ctx, member: discord.Member = None):
        await ctx.send(
            f"{ctx.author.display_name} *pats* {member.display_name}", file=discord.File("pat.gif")
        )

class Usefull(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def giverole(self,ctx, member: discord.Member = None, role: discord.Role = None):
        await member.add_roles(role)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self,ctx, member: discord.Member = None, reason=None):
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.Member = None, reason=None):
        await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self,ctx, limit: int):
        await ctx.channel.purge(limit=limit)
        await ctx.message.delete()


    # PLS HELP
    @commands.command(aliases=["help"])
    async def geert_help(self,ctx):
        def help_embed():
            imout = f"{prefix}imout:    Run like the wind"
            bye = f"{prefix}bye:    Wave goodbye"
            FBI = f"{prefix}FBI:    FBI OPEN UP!!"
            pat = f"{prefix}pat:    Pat the person you mention on the head"
            satan = f"{prefix}satan:    Spawn satan"
            blackjack = f"{prefix}casino:    Small list of games"
            text = f"{imout}\n \n{bye}\n \n{FBI}\n \n{pat}\n \n{satan}\n \n{blackjack}"
            embed = discord.Embed(title="HELP", description=text)
            return ctx.send(embed=embed)
        await help_embed()




#DATABASE
class TrapDataBase(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    #CREATE/UPDATE DATABASE
    @commands.command(aliases=["updateDB"])
    @commands.has_permissions(ban_members=True)
    async def createdatabase(self, ctx):
        conn = sqlite3.connect('trap.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS points (member UNIQUE , TrapCoin INT, Daily INT)''')
        for i in ctx.guild.members:
            try:
                player = (str(i.id), '100',"0")
                c.execute("INSERT INTO points VALUES(?,?,?)", player)
                conn.commit()
            except:
                pass
        conn.close

    #BALANCE RELATED
    @commands.command()
    async def daily(self, ctx):
        conn = sqlite3.connect("trap.db")
        c = conn.cursor()
        member = str(ctx.author.id)
        t=(member,)
        c.execute("SELECT Daily FROM points WHERE member=?", t)
        value= c.fetchone()
        if value[0] == 1:
            conn.close()
            await ctx.channel.send("You already recieved your daily 100TrapCoins")
        elif value[0] == 0:
            c.execute("SELECT TrapCoin FROM points WHERE member=?", t)
            puntjes = c.fetchone()
            updatedcoins = (puntjes[0] + 100)
            t= ctx.author.id
            data =(updatedcoins, str(t))
            c.execute("UPDATE points SET TrapCoin=? , Daily=1 WHERE member=?", data)
            conn.commit()
            conn.close()
            await ctx.channel.send("You recieved your daily 100TrapCoins")

    @commands.command()
    async def balance(self, ctx):
        conn = sqlite3.connect("trap.db")
        c = conn.cursor()
        member = str(ctx.author.id)
        t=(member,)
        c.execute("SELECT TrapCoin FROM points WHERE member=?", t)
        puntjes = c.fetchone()
        Coinamount = str(puntjes[0])
        conn.close()
        await ctx.channel.send(f'{ctx.author.mention}, you have {Coinamount}TrapCoins!')

#CASINO
class Casino(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.lock = asyncio.Lock()
    
    #BLACKJACK
    @commands.command()
    async def blackjack(self, ctx):
        player = ctx.author
        player_value = 0
        dealer_value = 0

        conn = sqlite3.connect("trap.db")
        c = conn.cursor()
        member = str(ctx.author.id)
        t=(member,)

        def check(ctx):
            if ctx.author != player:
                return False
            else:
                return True
        
        def handvalue(handplayer, handdealer):
            player_value = 0
            dealer_value = 0
            for i in handplayer:
                if type(i) == int:
                    player_value += i
                elif i == "A":
                    player_value += 1
            if player_value + 10 <= 21 and "A" in handplayer:
                player_value += 10
            else:
                player_value = player_value
            for i in handdealer:
                if type(i) == int:
                    dealer_value += i
                elif i == "A":
                    dealer_value += 1
            if dealer_value + 10 <= 21 and "A" in handdealer:
                dealer_value += 10
            else:
                dealer_value = dealer_value
            return player_value, dealer_value

        def blackjack1(handplayer, handdealer):
            hand = ", ".join(str(i) for i in handplayer)
            text = (player.display_name)+", your hand: " + (hand) + "\n Hit or stand?"           
            embed = discord.Embed(title=text)
            return embed
        
        def blackjack2(handplayer, handdealer, player_value, dealer_value, bet):
            Your_Hand = ", ".join(str(i) for i in handplayer)
            Trap_Hand = ", ".join(str(i) for i in handdealer)
            if player_value > 21 and dealer_value > 21 or dealer_value == player_value:
                gamestate = "TIE"
                winnings = 0
            elif player_value == 21 and dealer_value < 21 or player_value == 21 and dealer_value > 21:
                winnings = (bet * 3)
                gamestate = f"YOU WIN \n Your winnings are {winnings}TrapCoins" 
            elif player_value > dealer_value and player_value <= 21 or dealer_value > 21:
                winnings = round(bet * 1.5)
                gamestate = f"YOU WIN \n Your winnings are {winnings}TrapCoins"            
            elif dealer_value > player_value and dealer_value <= 21 or player_value > 21:
                winnings = (0 - bet)
                gamestate = "THE DEALER WINS \n You lose " + str(bet) +"TrapCoins" 
            text = f"{player.display_name}, your hand: { Your_Hand} \n The value of your hand is: {player_value} \n \n My hand: {Trap_Hand} \n The value of my hand is: {dealer_value} \n \n{gamestate}"
            embed = discord.Embed(title=text)
            return embed, winnings

        values = ["A", 2, 3, 4, 5, 6, 7, 8, 9, 10]
        handplayer = [r.choice(values),  r.choice(values)]
        handdealer = [r.choice(values),  r.choice(values)]
        player_value, dealer_value = handvalue(handplayer, handdealer)
        hand = ", ".join(str(i) for i in handplayer)
        text = "How many TrapCoins do you want to bet?"           
        embed = discord.Embed(title=text)
        await ctx.channel.send(embed=embed)

        while True:
            try:
                answer = await bot.wait_for('message', timeout=60, check=check)
                answer = answer.content
                c.execute("SELECT TrapCoin FROM points WHERE member=?", t)
                puntjes = c.fetchone()
                Coinamount = str(puntjes[0])
                try:
                    bet = int(answer)
                    if (puntjes[0]-bet) >= 0:
                        break
                    elif (puntjes[0]-bet) < 0:
                        await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name}, you don't have that many TrapCoins! \n You have {Coinamount} Trapcoins left"))
                except ValueError:
                    await ctx.channel.send(embed=discord.Embed(title=(player.display_name)+"Invalid bet, please give a number"))
            except asyncio.TimeoutError:
                await ctx.channel.send(f"{player.display_name} Timeout: You took to long to respond!")
                return
        
        await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name} hand {hand}.\nHit or stand?"))
        
        while player_value < 21 and dealer_value < 21:         
            try:
                answer = await bot.wait_for('message', timeout=60, check=check)
                if answer.content.casefold() == "hit":
                    handplayer.append(r.choice(values))
                    if dealer_value + 10 < 17 and "A" in handdealer:
                        handdealer.append(r.choice(values))
                    elif dealer_value < 17:
                        handdealer.append(r.choice(values))
                    embed = blackjack1(handplayer, handdealer)
                    player_value, dealer_value = handvalue(handplayer, handdealer)
                    await ctx.channel.send(embed=embed)
                elif answer.content.casefold() == "stand":
                    if dealer_value + 10 <= 12 and "A" in handdealer:
                        handdealer.append(r.choice(values))
                    elif dealer_value <= 12 :
                        handdealer.append(r.choice(values))
                    break
                else:
                    await ctx.channel.send((player.display_name)+ ", please input hit or stand.")
            except asyncio.TimeoutError:
                await ctx.channel.send((player.display_name)+" Timeout: You took to long to respond!")
                return

        player_value, dealer_value = handvalue(handplayer, handdealer)
        embed, winnings = blackjack2(handplayer, handdealer, player_value, dealer_value, bet)

        updatedcoins = (puntjes[0] + winnings)
        t= player.id
        data =(updatedcoins, str(t))
        c.execute("UPDATE points SET TrapCoin=? WHERE member=?", data)
        conn.commit()
        conn.close()
        await ctx.channel.send(embed=embed)

    # ROULETTE
    @commands.command()
    async def roulette(self, ctx):
        player = ctx.author

        conn = sqlite3.connect("trap.db")
        c = conn.cursor()
        member = str(ctx.author.id)
        t=(member,)

        def check(ctx):
            if ctx.author != player:
                return False
            else:
                return True

        def spin(bet, betamount, player) :
            blacklist = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
            spinvalue = r.randint(0,36)
            spinproperties = []
            spinproperties.append(spinvalue)
            try:
                bet = int(bet)
            except:
                pass
            if ((spinvalue%2)==0):
                evenodd = "even"
            else:
                evenodd = "odd"
            spinproperties.append(evenodd)

            if spinvalue in blacklist:
                colour = "black"
                embedcolour ="Black"
            else:
                colour = "red"
                embedcolour = "Red"
            spinproperties.append(colour)

            if spinvalue > 0 and spinvalue <= 12:
                whatthird = "1st 12"
            elif spinvalue > 12 and spinvalue <= 24:
                whatthird = "2nd 12"
            elif spinvalue > 24 and spinvalue <= 36:
                whatthird = "3rd 12"
            spinproperties.append(whatthird)

            if spinvalue >=1 and spinvalue <= 18:
                half = "1 to 18"
            if spinvalue >=19 and spinvalue <= 36:
                half = "19 to 36"
            spinproperties.append(half) 
            if bet in spinproperties:
                if type(bet) == int:
                    if bet == 0 :
                        winnings = betamount*3
                        valmuntjes = str(winnings)
                    else:
                        winnings = round(betamount * 1.75)
                        valmuntjes = str(winnings)
                else:
                    if bet == "1st 12" or bet == "2nd 12" or bet == "3rd 12":
                        winnings = round(betamount * 1.5)
                        valmuntjes = str(winnings)
                    elif bet == "even" or bet == "odd" or bet == "even" or bet == "black" or bet == "red" or bet == "1 to 18" or bet == "19 to 36":
                        winnings = round(betamount * 1.25)
                        valmuntjes = str(winnings)
                gamestate = "YOU WON "
            else:
                gamestate = "YOU LOST "
                winnings = (0 - betamount)
                valmuntjes = str(betamount)
            text = f"{player.display_name}, I spun the wheel and the ball landed on: {spinvalue} {embedcolour} \n \n{gamestate}{valmuntjes}TrapCoins"
            embed = discord.Embed(title=text)
            return embed,winnings
        
        await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name}, what do you want to bet on?"), file=discord.File("roulette.png"))

        while True:
            potentialbets = ["even", "odd", "black", "red", "1st 12", "2nd 12", "3rd 12", "1 to 18", "19 to 36","0","1","2","3",'4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36']
            try:
                answer = await bot.wait_for('message', timeout=60, check=check)
                bet = answer.content.casefold()
                if bet in potentialbets:
                    break
                else:
                    await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name}, please try again with something that is on the roulette table"), file=discord.File("roulette.png"))
            except asyncio.TimeoutError:
                await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name} TIMEOUT:You took to long to respond"))
                return
        
        await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name}, how many TrapCoins do you want to bet?"))
        
        while True:
            answer = await bot.wait_for('message', timeout=200, check=check)
            answer = answer.content
            c.execute("SELECT TrapCoin FROM points WHERE member=?", t)
            puntjes = c.fetchone()
            Coinamount = str(puntjes[0])
            try:
                betamount = int(answer)
                if (puntjes[0]-betamount) >= 0:
                    break
                elif (puntjes[0]-betamount) < 0:
                    await ctx.channel.send(embed=discord.Embed(title= f"{player.display_name}, you don't have that many TrapCoins! \n You have {Coinamount}Trapcoins left"))
            except ValueError:
                await ctx.channel.send(embed=discord.Embed(title=f"{player.display_name} Invalid bet, please give a number"))

        embed,winnings = spin(bet, betamount, player)

        updatedcoins = (puntjes[0] + winnings)
        t= player.id
        data =(updatedcoins, str(t))
        c.execute("UPDATE points SET TrapCoin=? WHERE member=?", data)
        conn.commit()
        conn.close()
        await ctx.channel.send(embed=embed)

    # SLOTS
    @commands.command(aliases=["slots"])
    async def slotmachine(self,ctx):
        async with self.lock:
            count = 0
            player = ctx.author
            conn = sqlite3.connect("trap.db")
            c = conn.cursor()
            member = str(ctx.author.id)
            t=(member,)
            c.execute("SELECT TrapCoin FROM points WHERE member=?", t)
            puntjes = c.fetchone()
            if (puntjes[0]-10 < 0):
                poor = discord.Embed(title="You don't have enough TrapCoins!")
                await ctx.send(embed=poor)
                return
            embed = discord.Embed(title= f"You put in 10TrapCoins \n :100::100::100:=1500 \n :four_leaf_clover::four_leaf_clover::four_leaf_clover:=500 \n :cherries::cherries::100:=350 \n |TRAPSLOTS| \n | [0][0][0] |")
            message = await ctx.send(embed=embed)
            await asyncio.sleep(3)
            while count < 5:
                Rando_Dizzle = [":100:", ":green_apple:", ":four_leaf_clover:", ":grapes:", ":cherries:"]
                fruits = [":apple:", ":strawberry:", ":cherries:"]
                random1= r.choice(Rando_Dizzle)
                random2= r.choice(Rando_Dizzle)
                random3= r.choice(Rando_Dizzle)
                top=":100::100::100:=1500 \n :four_leaf_clover::four_leaf_clover::four_leaf_clover:=500 \n :cherries::cherries::100:=350 \n|TRAPSLOTS| \n"
                bot=f"| [{random1}][{random2}][{random3}] |"
                new_embed = discord.Embed(title=top + bot)
                await message.edit(embed=new_embed)
                count += 1
            if random1 == ":100:" and random2 == ":100:" and random3 == ":100:":
                updated_coins = (puntjes[0]+ 1490)
                text = "JACKPOT!! \n You won 1500TrapCoins"
            elif random1 in fruits and random2 in fruits and random3 == ":100:":
                if random1 == random2:
                    updated_coins = (puntjes[0]+ 340)
                    text = "You won 350TrapCoins"
                else:
                    updated_coins = (puntjes[0]+ 240)
                    text = "You won 250TrapCoins"
            elif random1 == random2 and random1 == random3:
                updated_coins = (puntjes[0]+ 490)
                text = "You won 500TrapCoins"
            else :
                updated_coins = (puntjes[0]- 10)
                text = "Sadly you won nothing"

            t= player.id
            data =(updated_coins, str(t))
            c.execute("UPDATE points SET TrapCoin=? WHERE member=?", data)
            conn.commit()
            conn.close()
            embed= discord.Embed(title=f"{player.display_name} {text}")
            await ctx.channel.send(embed=embed)

    #CASINO HELP COMMAND        
    @commands.command(aliases=["casino"])
    async def casinohelp(self, ctx):
        def casino_help():
            blackjackbois = f"{prefix}blackjack:    Play a game of blackjack with Trapborg"
            roulettebois = f"{prefix}roulette:   Try your luck at the roulette table"
            slots =f"{prefix}slots:   Play a round on the slotmachine(price=10TrapCoins)"
            dailybois =f"{prefix}daily: Get 100TrapCoins (can only be used once a day)"
            balancebois=f"{prefix}balance: Check your TrapCoin balance"
            text =f"{blackjackbois}\n \n{roulettebois}\n \n{slots}\n \n{dailybois}\n \n{balancebois}"
            embed= discord.Embed(title= "CASINO GAMES", description=text)
            return ctx.send(embed=embed)
        await casino_help()

#GIVEAWAY
class Giveaway(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.msg = None
        self.entries =[]

    @commands.command(aliases=["giveaway"])
    @commands.has_permissions(ban_members=True)
    async def creategiveaway(self,ctx):
        creator = ctx.author
        channelID = None
        giveitem = None
        duration = None
        channel=None

        def check(ctx):
            if ctx.author != creator:
                return False
            else:
                return True
        if self.msg != None:
            await ctx.send(f"Sorry, my small femboy body can only handle one giveaway at the time.")
            return

        while channel==None:
            await ctx.send(
                f" `What is the giveaway channel ID? `"
            )
            answer = await bot.wait_for('message', timeout=60, check=check)
            try:
                channelID = int(answer.content)
                channel = bot.get_channel(channelID)
            except ValueError:
                await ctx.send(
                    f"That is not a channelID"
                )

        await ctx.send(
            f"The giveaway will be in #{channel} \n`What is the prize?`"
        )

        answer = await bot.wait_for('message', timeout=60, check=check)
        giveitem = answer.content
        await ctx.send(
            f"You'll be giving away {giveitem}! \n`What is the duration people can enter in seconds?`"
        )
        while True:
            try:
                answer = await bot.wait_for('message', timeout=60, check=check)
                duration = int(answer.content)
                embed = discord.Embed(title=f"A give away for {giveitem}", description=f"click the :tada: reaction of this message to enter")
                msg = await channel.send(embed=embed)
                await msg.add_reaction("\U0001F389")
                break
            except:
                await ctx.send("That is not a valid time")
        
        self.msg=msg      
            
        await asyncio.sleep(duration-60)
        await channel.send(embed=discord.Embed(title=f"One more minute to enter the {giveitem} giveaway "))
        await asyncio.sleep(60)
        if not self.entries:
            await channel.send(embed=discord.Embed(title=f"There are no entries so no winner"))
        else:
            winnerid=r.choice(self.entries)
            winner= bot.get_user(int(winnerid))
            await channel.send(embed=discord.Embed(title=f"The winner for {giveitem} is {winner}"))
            await channel.send(winner.mention)
            self.entries=[]
            self.msg = None
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if self.msg == None:
            pass
        elif payload.message_id == self.msg.id and payload.member != bot.user and payload.emoji.name == "\U0001F389":
            if payload.member.id in self.entries:
                pass
            else:
                self.entries.append(payload.member.id)
        else:
            pass
    
# ERRORHANDLING
@bot.event
async def on_command_error(command, *arg, **kwargs):
    print(arg[0])
    
@bot.event
async def on_error(on_message, *arg, **kwargs):
    print(arg[0])

# MEMBER JOINING/BOTBOOT
@bot.event
async def on_member_join(member):
    conn = sqlite3.connect('trap.db')
    c = conn.cursor()
    player=(str(member.id), '100', '0')
    try:
        c.execute("INSERT INTO points VALUES(?,?, ?)", player)
        conn.commit()
    except:
        pass
    conn.close
    for channel in member.guild.channels:
        if str(channel) == "misschien-mtg-talk":
            await channel.send(
                f"{member.name}, welcome to the server my dude"
            )
        if str(channel) == "games-journo-pro":
            await channel.send(
                f"{member.name}, I welcome you to the Council of the Gay Frogs"
            )

            
@bot.event
async def on_ready():
    print("Ret-2-Go")
    print('-------')
    customstatus = discord.Game(f"{prefix}casino")
    await bot.change_presence(activity=customstatus)

async def dailypointreset():
    while True:
        conn = sqlite3.connect("trap.db")
        c = conn.cursor()
        c.execute("UPDATE points SET Daily = 0 ")
        conn.commit()
        conn.close()
        await asyncio.sleep(86400)

bot.add_cog(messagestuff(bot))
bot.add_cog(Usefull(bot))
bot.add_cog(funcommands(bot))
bot.add_cog(Casino(bot))
bot.add_cog(Giveaway(bot))
bot.add_cog(TrapDataBase(bot))
bot.loop.create_task(dailypointreset())
bot.run(TOKEN)
