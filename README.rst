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

A cog that allows users to add Steam Games to a pool. Users can add or remove Steam games to a channel's pool and then pick a random game from the pool.

Allows users to add games they'd like to play to a channel pool and then chooses a random game to play

SubCommands: 
Add: [p]gamepool add <game>

Remove: [p]gamepool remove <game>

Pick: [p]gamepool pick

This cogs looks at all the message history of a channel and looks for specific messages from the bot to generate the pool when the pick command is run. A link to the Steam page will be generated once a game is picked.

The added <game> must be one that is available on Steam and must me spelled correctly. Games can be added multiple times to the pool but duplicates will be removed on pick.
The remove command will remove all references of the <game> from the pool.

------------
Contributing
------------

If you have ideas, you can open an issue. If you have coded new features, make a PR. I'm happy to make changes to these cogs!


-------
LICENSE
-------

This repository and its cogs are protected under the MIT License.

For further information, please click `here <https://github.com/V-Shadbolt/Shadbolt-Cogs/blob/main/LICENSE>`_