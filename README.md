Made using the amazing https://github.com/Rapptz/discord.py

Forgive me for the spaghetti code.

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

## Commands:

Default prefix: `!`

Note:
`<VAR>` - means VAR is obligatory
`[VAR]` -  means VAR is optional

* `echo <Text>` - I just use it to check if the bot is alive.
* `startUp <adminRole id> [new Prefix]` - Creates server data. Stores an administration role (need to pass role ID), and optionally, a new prefix.
* `exit` - Removes any stored server data
* `createVote <candidate1>,<candidate2>[, ...]` creates a vote with the given candidates, and prints out a nice copy-pastable vote message. Opens the voting.
* `closeVoting` - Makes people unable to vote
* `openVoting` - Makes peolpe able to vote (if it was closed manually)
* `calculateWinner` - Calculates the vote's winner, and removes the current vote.
* `vote <candidate1>:<preference1> [candidate2>:<preference2 ...]` - Registers a vote. `preference` values should be thought of as "1st option" for value 1, "2nd option" for value 2... Not all candidates need a vote. Just delete that line if you never want to give it a vote.
* `removeVoting` - Removes the voting without calculating a winner.
* `prefix <newPrefix>` - Changes command prefix to given one.

## TODO:
- [X] Make it so that each person can only vote once per vote
- [X] Make it so that people can modify their vote if they recast it
- [ ] Invite command so people can invite the bot to a server
- [ ] Command aliases
- [ ] Add a "commands" command
- [ ] Save status every so often?

## TODO Maybe
- [ ] Custom command aliases per server
- [ ] Make it pretty
- [ ] Send channel id for vote collection