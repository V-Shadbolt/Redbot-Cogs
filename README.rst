================================================
Redbot cogs for Red-DiscordBot authored by V-Shadbolt
================================================

This is my cog repo for the redbot, a multifunctional Discord bot!

------------
Installation
------------

Primarily, make sure you have `downloader` loaded.

.. code-block:: ini

    [p]load downloader

Next, let's add my repository to your system.

.. code-block:: ini

    [p]repo add Shadbolt https://github.com/V-Shadbolt/Shadbolt-Cogs

To install a cog, use this command, replacing <cog> with the name of the cog you wish to install:

.. code-block:: ini

    [p]cog install Shadbolt <cog>

-------------------
Available cogs list
-------------------

This list of cogs is not up to date. At the time of writing there is 1.

**GamePool:**

A cog that allows users to add Steam Games to a pool. Users can add or remove Steam games to a channel's pool, look at the current pool, see previous pool winners, and pick a new winner.

SubCommands: 

Add: [p]gamepool add <game>

Remove: [p]gamepool remove <game>

Veto: [p]gamepool veto <game>

List: [p]gamepool list

Results: [p]gamepool results

Nominate: [p]gamepool nominate <minute(s)>

Pick: [p]gamepool pick

Vote: [p]gamepool vote <minute(s)>

Winners: [p]gamepool winners

Host: [p]gamepool host <game>

This cog writes the pool(s) to a text file when add, remove, or pick commands are run. A link to the Steam page will be generated once a game is picked.

The added <game> must be one that is available on Steam and must be spelled correctly. If it is missspelled you will get an error. Games can be added multiple times to the pool but duplicates will be removed on pick.

The remove command will remove all references of the <game> from the pool.

This cog also implements a voting system. If the channel does not want to pick a completely random game, the channel can run the nominate command which will invoke a poll. Users can react to the poll to nominate the game(s) they'd be interested in playing. Results are saved to a text file. If a user really dislikes a game, they can veto it with the veto command but they can only do so once per nomination poll. The results command prints the results of the poll. Once select game(s) have been nominated, the channel can run the vote command. This will invoke a final poll for users to add additional weight for the bot to consider before making it's final choice.

------------
Contributing
------------

Open that PR! Always happy to improve the cogs.


-------
LICENSE
-------

This repository and its cogs are protected under the MIT License.

For further information, please click `here <https://github.com/V-Shadbolt/Shadbolt-Cogs/blob/main/LICENSE>`_