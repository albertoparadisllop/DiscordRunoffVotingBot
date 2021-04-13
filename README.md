Bot to perform [Instant-runoff voting](https://en.wikipedia.org/wiki/Instant-runoff_voting#Election_procedure) on Discord.



Made using the amazing [discord.py](https://github.com/Rapptz/discord.py)

Forgive me for the spaghetti code.

# Contact:

Any suggestions, questions, or anything else? Feel free to contact me, I'm lonely.

Contact me on Discord: `@PixeledBrain#0070` or by email: pixeledbrain@gmail.com

# Instructions:

## Use a pre-existing bot:

To invite my instance of this bot, use this link:

https://discord.com/oauth2/authorize?client_id=830927490482569217&permissions=347200&scope=bot

It will probably be offline though, if you want to use it, feel free to poke me on Discord `@PixeledBrain#0070`

## Requirements:

#### Python and packages.

I used version 3.9.4, so I recommend using that one for less issues.
[Download here.](https://www.python.org/downloads/release/python-394/)

then run the command on cmd:
`py -3 -m pip install -U discord.py`
to install discord.py
(If that doesn't work, check out [their installation guide](https://discordpy.readthedocs.io/en/stable/intro.html#installing))


#### A discord application with a bot assigned.
* Create one at the [Discord developer website](https://discord.com/developers/applications)
* Click on New Application, give it a name (this is not the user name for the bot)
* Click on the `Bot` tab on the left.
* Add a bot, give it a name.
* Copy the bot's token, replace "TOKENHERE" in "runBot.bat" with the token

To invite that bot to a server, you need an invite link.
* Go over to the `OAuth2` tab in your application's page.
* Tick `bot` in the `scopes` category.
* On the `permissions` category, tick the following:
	* View Channels
	* Send Messages
	* Embed Links
	* Read Message History
	* Use External Emojis
	* Add Reactions
* Copy the link at the bottom of the `scopes` section.

That link will be used to invite the bot to different servers.

## Running the bot

If you're on windows, you can just run the "runBot.bat" file to run the bot (assuming the correct token has been placed in the file, as described in the section above)

You can also run the bot directly from the command line by running the command:

`python main.py TOKEN`

Replacing `TOKEN` with your bot's token.

## Closing the bot

`Ctrl+C` on your keyboard with the CMD window focused should close the bot. Closing the whole CMD window will probably work too.

## Use example

After having done set up the bot, and have it in a server, while online, an example use case could be the following:

1. Copy the role ID for whatever role you want to make the bot administrator role, people with this role will be able to manage elections.
2. Send a message on Discord with `!startUp ROLEID`, replacing "ROLEID" with the role id you copied earlier.
3. To create an election, run `!createElection option1,option2,option3`. You can replace the options, or add and remove more.
4. Copy the command example the bot provides, and on each line, replace "x" with your desired preference. You can remove lines for votes you dont want to make.
5. Once everyone has voted, run `!electionWinner` to get a result. This gets rid of the election.
6. Go back to step 3 if you want to set up another one.

## Commands:

Default prefix: `!`

Note that commands are not case-sensitive, but any parameters are.

Notes:
`<VAR>` - means VAR is obligatory
`[VAR]` -  means VAR is optional

Al `AdminRole` permissions can also be run by users with a role that gives them the "Administrator" permission on Discord.

Command | Description | Permissions | Example
------------ | ------------- | ------------- | -------------
`startUp <AdminRole id> [new Prefix]` | Creates server data. Sets bot `AdminRole` (need to provide role ID, not name), and optionally, a new prefix. | Discord "Administrator" Permission | `!startUp 556940676495835146 $`
`exit` | Removes any stored server data. | AdminRole | `!exit`
`createElection <c1>,<c2>[, ...]` | creates an election with the given candidates, and prints out a nice copy-pasteable vote message. Opens the voting. | AdminRole | `!createElection candidate1,candidate2,candidate3`
`closeElection` |  Makes people unable to vote. | AdminRole | `!closeElection`
`openElection` | Makes peolpe able to vote (if it was closed manually). | AdminRole | `!openElection`
`electionWinner` | Calculates the election's winner, and removes the current vote. | AdminRole  | `!electionWinner`
`vote <c1>:<pr1> [c2>:<pr2 ...]` | Registers a vote. `preference` values should be thought of as "1st option" for value 1, "2nd option" for value 2... Not all candidates need a vote. If a person casts more than one vote, their previous one is deleted. | Anyone  | -
`removeVote` | Removes the caller's vote | Anyone | `!removeVote`
`prefix <newPrefix>` | Changes command prefix to given one. | AdminRole | `!prefix $`
`help` or `contact` | Sends a message with my Discord name for contact `PixeledBrain#0070`. | Anyone | `!help`
`invite` | Invite link for my bot using this. (you can modify the link to yours in botClient.py). | Anyone | `!invite`
`github` | Links this page. | Anyone | `!github`
`commands` | Lists commands... kinda :P | Anyone | `!commands`


## TODO:
- [X] Make it so that each person can only vote once per vote
- [X] Make it so that people can modify their vote if they recast it
- [X] Invite command so people can invite the bot to a server
- [X] Contact command
- [X] GitHub command
- [X] Add a "commands" command
- [ ] Command aliases
- [ ] Save status every so often
- [ ] Load from previous status
- [X] Remove echo command
- [ ] Make an actual `commands` command
- [X] Refactor (difference between vote and election)
- [X] Add use instructions
- [X] Change readme commands section to a table.
- [X] Put each component into its own folder.
- [X] Make it so Administration role can do all commands too (change isAdmin function) (In case wrong role id is provided)
- [X] Flake8 compliant


## TODO Maybe
- [X] Remove vote command
- [X] Show vote results
- [ ] Custom command aliases per server
- [ ] Make it pretty
- [ ] Send channel id for vote collection
- [ ] Private voting? dm?
- [ ] Multiple elections per server simultaneously (with name ids?)
- [ ] Make AdminRole optional?
- [ ] Fix up code for bot class.
