Bot to perform Instant-runoff voting on Discord.

https://en.wikipedia.org/wiki/Instant-runoff_voting#Election_procedure

Made using the amazing https://github.com/Rapptz/discord.py

Forgive me for the spaghetti code.

# Contact:

Any suggestions, questions, or anything else? Feel free to contact me, im lonely.

Contact me on Discord: #PixeledBrain#0070 or by email: pixeledbrain@gmail.com

# Instructions:

## Requirements:

#### Python and packages.

I used version 3.9.4, so I recommend using that one for less issues.
https://www.python.org/downloads/release/python-394/

then run the command on cmd:
`py -3 -m pip install -U discord.py`
to install discord.py
(If that doesn't work, check their installation guide https://discordpy.readthedocs.io/en/stable/intro.html#installing )


#### A discord application with a bot assigned.
* Create one at https://discord.com/developers/applications
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

Note:
`<VAR>` - means VAR is obligatory
`[VAR]` -  means VAR is optional

Command | Description | Permissions
------------ | ------------- | -------------
`startUp <AdminRole id> [new Prefix]` | Creates server data. Sets bot `AdminRole` (need to pass role ID), and optionally, a new prefix. | Discord "Administrator" Permission
`exit` | Removes any stored server data. | AdminRole
`createElection <candidate1>,<candidate2>[, ...]` | creates an election with the given candidates, and prints out a nice copy-pastable vote message. Opens the voting. | AdminRole
`closeElection` |  Makes people unable to vote. | AdminRole
`openElection` | Makes peolpe able to vote (if it was closed manually). | AdminRole
`electionWinner` | Calculates the election's winner, and removes the current vote. | AdminRole
`vote <candidate1>:<preference1> [candidate2>:<preference2 ...]` | Registers a vote. `preference` values should be thought of as "1st option" for value 1, "2nd option" for value 2... Not all candidates need a vote. Just delete that line if you never want to give it a vote. If a person casts more than one vote, their previous one is deleted. | Anyone
`prefix <newPrefix>` | Changes command prefix to given one. | AdminRole
`help` or `contact` | Sends a message with my Discord name for contact `PixeledBrain#0070`. | Anyone
`invite` | Invite link for my bot using this. (you can modify the link to yours in botClient.py). | Anyone
`github` | Links this page. | Anyone
`commands` | Lists commands... kinda :P | Anyone


## TODO:
- [X] Make it so that each person can only vote once per vote
- [X] Make it so that people can modify their vote if they recast it
- [X] Invite command so people can invite the bot to a server
- [X] Contact command
- [X] Github command
- [X] Add a "commands" command
- [ ] Command aliases
- [ ] Save status every so often
- [ ] Load from previous status
- [X] Remove echo command
- [ ] Make an actual `commands` command
- [X] Refactor (difference between vote and election)
- [X] Add use instructions
- [X] Change readme commands section to a table.

## TODO Maybe
- [ ] Remove vote command
- [ ] Custom command aliases per server
- [ ] Make it pretty
- [ ] Send channel id for vote collection
- [ ] Private voting? dms?
- [ ] Multiple elections per server simultaneously (with name ids?)