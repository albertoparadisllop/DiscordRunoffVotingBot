import discord
import voting

defaultPrefix = "!"

class ServerData():

    def __init__(self, id, adminRole=0, prefix=defaultPrefix, electionInstance=None, electionOpen=False):
        self.id = id
        self.adminRole = adminRole
        self.electionInstance = electionInstance
        self.prefix = prefix
        self.electionOpen = electionOpen
        self.voteList = None

class VotingClient(discord.Client):

    def __init__(self,*args,**kwargs):

        self.commands = {
                     None: self.noCommand,
                     "createelection": self.createElection,
                     "vote": self.vote,
                     "removevote": self.removeVote,
                     "closeelection": self.closeElection,
                     "openelection": self.openElection,
                     "electionwinner": self.electionWinner,
                     "removeelection": self.removeElection,
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

    async def createElection(self, ctx, paramList):
        if await self.isAdmin(ctx):
            candidateString = " ".join(paramList)
            candidates = [i.strip() for i in candidateString.split(",")]
            if(self.servers[ctx.guild.id].electionInstance == None):
                self.servers[ctx.guild.id].electionInstance = voting.Voting(candidates)
                self.servers[ctx.guild.id].electionOpen = True
                self.servers[ctx.guild.id].voteList = {}
                messageList = [self.servers[ctx.guild.id].prefix+"vote"]
                for i in candidates:
                    messageList.append(f"{i}:x")
                message = "\n".join(messageList)
                await ctx.channel.send(f"Election created! Send Your votes in now with the following format (you can copy and paste, replace `x` with the priority, and remove lines): \n```\n{message}\n```\nSend `!closeElection` to close votes, and `!electionWinner` to calculate a winner!")
            else:
                await ctx.channel.send("Election already in progress!\n Use `!removeElection` to remove it, or `!electionWinner` to calculate the previous election's winner!")
    
    async def vote(self, ctx, paramList):
        if await self.isStarted(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("No election going on!")
            elif(not self.servers[ctx.guild.id].electionOpen):
                await ctx.channel.send("Election not open!")
            else:
                voteToMake = {}
                voteList = ctx.content.split("\n")[1:]
                for line in voteList:
                    parts = [i.strip() for i in line.split(":")]
                    voteToMake[int(parts[1])] = parts[0]
                try:
                    replaced = False
                    if(ctx.author.id in self.servers[ctx.guild.id].voteList.keys()):
                        self.servers[ctx.guild.id].electionInstance.removeVote(self.servers[ctx.guild.id].voteList[ctx.author.id])
                        replaced = True
                    voteID = self.servers[ctx.guild.id].electionInstance.addVote(voteToMake)
                    self.servers[ctx.guild.id].voteList[ctx.author.id] = voteID
                    if not replaced:
                        await ctx.channel.send("Vote added!")
                    else:
                        await ctx.channel.send("Vote replaced!")
                except Exception as Err:
                    await ctx.channel.send("Error adding vote :(")
                    print(Err)

    async def removeVote(self, ctx):
        if await self.isStarted(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("No election going on!")
            elif(not self.servers[ctx.guild.id].electionOpen):
                await ctx.channel.send("Election not open!")
            else:
                if(ctx.author.id in self.servers[ctx.guild.id].voteList.keys()):
                    self.servers[ctx.guild.id].electionInstance.removeVote(self.servers[ctx.guild.id].voteList[ctx.author.id])
                    del self.servers[ctx.guild.id].voteList[ctx.author.id]
                    await ctx.channel.send("Your vote was removed!")
                else:
                    await ctx.channel.send("You have not yet voted in this election!")

    async def openElection(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("Election not yet created. Run `!createElection [candidates]` to create an election!")
            elif(self.servers[ctx.guild.id].electionOpen):
                await ctx.channel.send("Election already open!")
            else:
                self.servers[ctx.guild.id].electionOpen = True
                await ctx.channel.send("Election opened!")

    async def closeElection(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("Election not yet created. Run `!createElection [candidates]` to create an election!")
            elif(not self.servers[ctx.guild.id].electionOpen):
                await ctx.channel.send("Election already closed!")
            else:
                self.servers[ctx.guild.id].electionOpen = False
                await ctx.channel.send("Election closed!")

    async def electionWinner(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("Election not yet created. Run `!createElection [candidates]` to create an election!")
            else:
                winner, endvotes = self.servers[ctx.guild.id].electionInstance.calculateResult()
                self.servers[ctx.guild.id].electionOpen = False
                self.servers[ctx.guild.id].electionInstance = None
                if winner is not None:
                    resultList = [f"{candidate} --> {votes} votes" for candidate,votes in endvotes.items()]
                    resultString = "\n".join(resultList)
                    await ctx.channel.send(f"Election winner is: **{winner}**!\nAt the time majority was achieved, results were:\n{resultString}")
                else:
                    await ctx.channel.send(f"No votes were provided. Removed election.")

    async def removeElection(self, ctx):
        if await self.isAdmin(ctx):
            if(self.servers[ctx.guild.id].electionInstance == None):
                await ctx.channel.send("Election not yet created. Nothing closed!")
            else:
                self.servers[ctx.guild.id].electionOpen = False
                self.servers[ctx.guild.id].electionInstance = None
                await ctx.channel.send("Election removed!")

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