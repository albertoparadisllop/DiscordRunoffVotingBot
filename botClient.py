import discord
import voting

defaultPrefix = "!"

class ServerData():

    def __init__(self, id, adminRole=0, prefix=defaultPrefix, voteInstance=None, votingOpen=False):
        self.id = id
        self.adminRole = adminRole
        self.voteInstance = voteInstance
        self.prefix = prefix
        self.votingOpen = votingOpen
        self.voteList = None

class VotingClient(discord.Client):

    def __init__(self,*args,**kwargs):

        self.commands = {
                     None: self.noCommand,
                     "echo": self.echo,
                     "createvote": self.createVote,
                     "vote": self.vote,
                     "closevoting": self.closeVoting,
                     "openvoting": self.openVoting,
                     "calculatewinner": self.calculateWinner,
                     "removevoting": self.removeVoting,
                     "exit": self.closeBot,
                     "startup": self.startUp,
                     "prefix": self.changePrefix,
                     "invite": self.invite,
                     "github": self.githubLink,
                     "contact": self.contact,
                     "help": self.contact,
                     "commands": self.commands
                    }

        self.servers = {}

        super().__init__()

    async def run_command(self, messageText, messageContext):
        if messageContext.guild.id in self.servers:
            usedPrefix = self.servers[messageContext.guild.id].prefix
        else:
            usedPrefix = defaultPrefix

        if(messageText.startswith(usedPrefix)):
            commandInput = messageText[len(usedPrefix):].split()
            command = commandInput[0].lower()
            if(len(commandInput)>1):
                args = [i.strip() for i in commandInput[1:]]
                exitCode = await self.commands.get(command, self.noCommand)(messageContext, args)
            else:
                exitCode = await self.commands.get(command, self.noCommand)(messageContext)
            return exitCode
        else:
            return 0

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author != self.user:
            print('Message from {0.author}: {0.content}'.format(message))
            res = await self.run_command(message.content, message)


    async def echo(self, ctx, message):
        try:
            messageJoined = " ".join(message)
            await ctx.channel.send(messageJoined)
            return 1
        except:
            return -1

    async def createVote(self, ctx, paramList):
        if await self.isAdmin(ctx):
            candidateString = " ".join(paramList)
            candidates = [i.strip() for i in candidateString.split(",")]
            if(self.servers[ctx.guild.id].voteInstance == None):
                self.servers[ctx.guild.id].voteInstance = voting.Voting(candidates)
                self.servers[ctx.guild.id].votingOpen = True
                self.servers[ctx.guild.id].voteList = {}
                messageList = [self.servers[ctx.guild.id].prefix+"vote"]
                for i in candidates:
                    messageList.append(f"{i}:x")
                message = "\n".join(messageList)
                await ctx.channel.send(f"Vote created! Send Your votes in now with the following format (you can copy and paste, replace `x` with the priority): \n```\n{message}\n```\nSend `!closeVoting` to close votes, and `!calculateWinner` to calculate a winner!")
            else:
                await ctx.channel.send("Voting already in progress!\n Use `!removeVoting` to remove it, or `!calculateWinner` to calculate the previous bot's winner!")
        else:
            print("NOT ADMIN ROLE")
    
    async def vote(self, ctx, paramList):
        if await self.isStarted(ctx):
            if(self.servers[ctx.guild.id].voteInstance == None):
                await ctx.channel.send("Vote not yet created. Run `!createVote [candidates]` to create a vote!")
            elif(not self.servers[ctx.guild.id].votingOpen):
                await ctx.channel.send("Voting not open!")
            else:
                voteToMake = {}
                voteList = ctx.content.split("\n")[1:]
                for line in voteList:
                    parts = [i.strip() for i in line.split(":")]
                    voteToMake[int(parts[1])] = parts[0]
                try:
                    if(ctx.author.id in self.servers[ctx.guild.id].voteList.keys()):
                        self.servers[ctx.guild.id].voteInstance.removeVote(self.servers[ctx.guild.id].voteList[ctx.author.id])
                    voteID = self.servers[ctx.guild.id].voteInstance.addVote(voteToMake)
                    self.servers[ctx.guild.id].voteList[ctx.author.id] = voteID
                    await ctx.channel.send("Vote added!")
                except Exception:
                    await ctx.channel.send("Error adding vote :(")

    async def openVoting(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].voteInstance == None):
                await ctx.channel.send("Vote not yet created. Run `!createVote [candidates]` to create a vote!")
            elif(self.servers[ctx.guild.id].votingOpen):
                await ctx.channel.send("Vote already open!")
            else:
                self.servers[ctx.guild.id].votingOpen = True
                await ctx.channel.send("Voting opened!")

    async def closeVoting(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].voteInstance == None):
                await ctx.channel.send("Vote not yet created. Run `!createVote [candidates]` to create a vote!")
            elif(not self.servers[ctx.guild.id].votingOpen):
                await ctx.channel.send("Vote already closed!")
            else:
                self.servers[ctx.guild.id].votingOpen = False
                await ctx.channel.send("Voting closed!")

    async def calculateWinner(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].voteInstance == None):
                await ctx.channel.send("Vote not yet created. Run `!createVote [candidates]` to create a vote!")
            else:
                winner, endvotes = self.servers[ctx.guild.id].voteInstance.calculateResult()
                self.servers[ctx.guild.id].votingOpen = False
                self.servers[ctx.guild.id].voteInstance = None
                await ctx.channel.send(f"Vote winner is: **{winner}**!")

    async def removeVoting(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].voteInstance == None):
                await ctx.channel.send("Vote not yet created. Nothing closed!")
            else:
                self.servers[ctx.guild.id].votingOpen = False
                self.servers[ctx.guild.id].voteInstance = None
                await ctx.channel.send("Voting removed!")

    async def closeBot(self, ctx):
        if await self.isAdmin(ctx):
            try:
                del self.servers[ctx.guild.id]
                await ctx.channel.send("Server data deleted. Run `!startUp adminRoleId` to start the bot up again.")
                return 1
            except Exception as err:
                return -1
    
    async def noCommand(self, ctx, *args, **kwargs):
        return -1

    async def changePrefix(self, ctx, paramList):
        newPrefix = paramList[0]
        if await self.isAdmin(ctx):
            self.servers[ctx.guild.id].prefix = newPrefix
            await ctx.channel.send(f"Prefix changed to {newPrefix}")

    async def contact(self, ctx):
        await ctx.channel.send("Need any help? Contact the creator on Discord: PixeledBrain#0070")

    async def githubLink(self, ctx):
        await ctx.channel.send("Follow any possible future development of the bot on Github: <https://github.com/pixeledbrain/DiscordRunoffVotingBot>")

    async def invite(self, ctx):
        await ctx.channel.send("Invite me to a server using: <https://discord.com/oauth2/authorize?client_id=830927490482569217&permissions=347200&scope=bot>")

    async def commands(self, ctx):
        await ctx.channel.send("Look at the README for commands: <https://github.com/pixeledbrain/DiscordRunoffVotingBot> \nOr just contact the creator for help: PixeledBrain#0070 (I'll make an actual commands command someday, sorry)")

    async def startUp(self, ctx, paramList):
        newServerData = ServerData(id = ctx.guild.id)

        if len(paramList) > 0:
            newServerData.adminRole = int(paramList[0])
            if len(paramList) > 1:
                newServerData.prefix = paramList[1]
        else:
            newServerData.adminRole = ctx.guild.roles[0]

        if(ctx.author.guild_permissions.administrator):
            self.servers[ctx.guild.id] = newServerData
            await ctx.channel.send("Started vote bot for this server!")
        else:
            await ctx.channel.send("Command must be run by administrator!")

    async def isAdmin(self, ctx):
        if await self.isStarted(ctx):
            return self.servers[ctx.guild.id].adminRole in [i.id for i in ctx.author.roles]
        else:
            await ctx.channel.send("Bot not yet started up for this server. Run `!startUp adminRoleId` to start the bot up.")
            return False

    async def isStarted(self, ctx):
        return ctx.guild.id in self.servers

def run_bot(token):
    client = VotingClient()
    client.run(token)