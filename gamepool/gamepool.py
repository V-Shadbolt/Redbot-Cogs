from redbot.core import commands
import discord
import json
from .utils import Utils
from datetime import datetime
from pathlib import Path
import random
import time

class GamePool(commands.Cog):
    """Allows users to add games they'd like to play to a channel pool and then chooses a random game to play"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def gamepool(self, ctx):
        """Create a pool of games that a channel is interested in playing together and pick a winner from the pool"""
        return
    
    @gamepool.command()
    async def add(self, ctx, *, game):
        """Add a game to the channel's Game Pool"""
        # Check if wanted game can be found on steam and write to pool
        gameInfo = await Utils.gameInfo(game)
        embed = gameInfo[0]
        gameName = gameInfo[1]
        if embed:
            # Report success to channel and add to file
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt","a+") as f:
                if gameName not in f.read():
                    await ctx.send("Added \"" + gameName + "\" to the pool. \nHere's the link:", embed=embed)
                    f.write(gameName + "\n")
                else:
                    await ctx.send("\"" + gameName + "\" is already added the pool. \nHere's the link:", embed=embed)
                    
        else:
            # Report failure to channel
            await ctx.send("There was an issue finding your game on Steam. Ensure the name is spelled correctly.")
    
    @gamepool.command()
    async def remove(self, ctx, *, game):
        """Remove a game from the channel's Game Pool"""
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        await Utils.makeFile(file)
        # Read pool to memory
        found_game = False
        with open(file, "r+") as f:
            lines = f.readlines()
        # Rewrite pool to file excluding specified game
        with open(file, "w+") as f:
            for line in lines:
                if line.strip("\n").lower() != game.lower():
                    f.write(line)
                else:
                    found_game = True
        # Check if game wasn't found in the pool
        if not found_game:
            await ctx.send("Game was not found in the pool.")
        else:
            await ctx.send("Removed \"" + game + "\" from the pool")
    
    @gamepool.command()
    async def veto(self, ctx, *, game):
        """Veto a nominated game"""
        # Create poll file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Nominations.txt"
        await Utils.makeFile(file)
        # Read poll results to memory
        found_game = False
        found_author = False
        with open(file, "r+") as f:
            lines = f.readlines()
        # Check if person already vetoed
        for line in lines:
            if str(ctx.message.author) in line:
                found_author = True
        if not found_author:
            # Rewrite poll results to file excluding specified game and add a veto note
            with open(file, "w+") as f:
                for line in lines:
                    if game.lower() not in line.lower():
                        f.write(line)
                    else:
                        f.write(str(ctx.message.author) + " has used their veto on " + game + "\n")
                        found_game = True
            # Check if game wasn't found in the pool
            if not found_game:
                await ctx.send("Game was not in the poll.")
            else:
                await ctx.send("Removed \"" + game + "\" from the nomination results.")
        else:
            await ctx.send("You've already vetoed the results of the poll.")
    
    @gamepool.command()
    async def list(self, ctx, list = True):
        """List the channel's current Game Pool"""
        game_pool = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
        await Utils.makeFile(file)
        # Read pool into memory and deduplicate games
        with open(file,"r+") as f:
            for line in f:
                if line not in game_pool:
                    game_pool.append(line.strip("\n"))
        # Check if there's nothing in memory
        if not game_pool:
            await ctx.send("No games in the pool!")
            return False
        else: 
            if list:
                # Send pool to channel and return list
                message_string = "Here's the current pool: \n"
                for i, game in enumerate(game_pool):
                    if not i:
                        message_string += str("- " + game + "\n")
                    else:
                        message_string += str("- " + game + "\n")
                await ctx.send(message_string)
            return game_pool
    
    @gamepool.command()
    async def results(self, ctx, list = True):
        """List the channel's nomination results"""
        game_pool = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Nominations.txt"
        await Utils.makeFile(file)
        # Read pool into memory and deduplicate games
        with open(file,"r+") as f:
            for line in f:
                if " has used their veto on " not in line:
                    if line not in game_pool:
                        game_pool.append(line.strip("\n"))
        # Check if there's nothing in memory
        if not game_pool:
            await ctx.send("There hasn't been a poll since the last game was picked")
            return False
        else: 
            if list:
                # Send pool to channel and return list
                message_string = "Here were the last nomination results (Game : Votes): \n"
                for i, game in enumerate(game_pool):
                    if not i:
                        message_string += str("- " + game + "\n")
                    else:
                        message_string += str("- " + game + "\n")
                await ctx.send(message_string)
            return game_pool
    
    @gamepool.command()
    async def nominate(self, ctx, *, minutes: float):
        """Nominate game(s) from the channel's game pool"""
        # Get possible choices in the pool
        game_pool = await self.list(ctx, False)
        if game_pool:
            # Create dictionary of possible Discord Emojis
            contents = []
            try:
                p = Path(__file__).with_name('simple.json')
                with p.open('r') as f:
                    contents = json.load(f)
            except Exception as e:
                print(e)
                await ctx.send("The code author made a big boo boo. Tell them to fix it for me, will ya?")
                return
            # Get list of random emojis of the same length as the game pool
            reactions = []
            i = 0
            while i < len(game_pool):
                reaction = random.choice(list(contents.values()))
                if reaction not in reactions:
                    reactions.append(reaction)
                    i = i + 1
            # Create Discord embed and link emojis to games in pool
            description = []
            for x, option in enumerate(game_pool):
                description += '\n {} {}'.format(reactions[x], option)
            embed = discord.Embed(title="Please nominate the game(s) you\'re interested in from the current pool:", description=''.join(description))
            react_message = await ctx.send(embed=embed)
            # Add emojis as reactions to poll
            for reaction in reactions[:len(game_pool)]:
                await react_message.add_reaction(reaction)
            # Add countdown timer to embed
            t_end = time.time() + round(60 * minutes)
            while time.time() < t_end:
                if ((t_end - time.time()) / 60) < 1:
                    measure = 'seconds'
                    diff = round(t_end - time.time())
                else:
                    measure = 'minutes'
                    diff = round((t_end - time.time()) / 60)
                embed.set_footer(text='Time remaining on Poll: {} {}'.format(diff, measure))
                await react_message.edit(embed=embed)
                time.sleep(5)
            # Report poll has ended
            embed.set_footer(text='Poll has ended')
            await react_message.edit(embed=embed)
            # Get final message ID and parse embed message for emoji : game pairs
            message = await ctx.channel.fetch_message(react_message.id)
            embed = message.embeds[0]
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            # Create dictionary of pairs and a dictionary for reaction counts
            opt_dict = {x.split(' ', 1)[0]: x.split(' ', 1)[1] for x in unformatted_options}
            tally = {x: 0 for x in opt_dict.keys()}
            # Count reactions
            tally = await Utils.tally(opt_dict, tally, message)
            # Create weighted list
            nominated_list = []
            for key in tally.keys():
                weight = int(tally[key])
                if weight >= 1:
                    nominated_list.append(str(opt_dict[key]) + " : " + str(tally[key]))
            # Remove previous poll results
            file = open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Nominations.txt", 'w+')
            file.close()
            # Save weighted list
            for game in nominated_list:
                with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Nominations.txt","a+") as f:
                    f.write(game + "\n")
    
    @gamepool.command()
    async def pick(self, ctx):
        """Pick a random game from the channel's Game Pool"""
        # Get possible choices in the pool
        game_pool = await self.list(ctx, False)
        if game_pool:
            # Pick random game from the pool
            game = random.choice(game_pool)
            # Pick a random host from the channel
            users = ctx.channel.members
            host = await Utils.pickHost(users)
            # Get the game info from steam
            embed = await Utils.gameInfo(game)
            # Send result to channel
            await ctx.send("I pick \"" + game + f"\" and I think {host.mention} should host! I've also removed it from the pool so it doesn't get picked again. \nHere's the link:", embed=embed)
            # Remove game from the pool by rewriting file excluding chosen game
            file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
            with open(file, "r+") as f:
                lines = f.readlines()
            with open(file, "w+") as f:
                for line in lines:
                    if line.strip("\n").lower() != game.lower():
                        f.write(line)
            # Add game and host to the winners file
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt","a+") as f:
                f.write("\"" + game + "\" on " + datetime.today().strftime('%Y-%m-%d') + " | Hosted by: " + str(host) +"\n")

    @gamepool.command()
    async def vote(self, ctx, *, minutes: float):
        """Vote for a nominated game"""
        # Get possible choices in the nominated list
        game_pool = await self.results(ctx, False)
        if game_pool:
            # Create dictionary of possible Discord Emojis
            contents = []
            try:
                p = Path(__file__).with_name('simple.json')
                with p.open('r') as f:
                    contents = json.load(f)
            except Exception as e:
                print(e)
                await ctx.send("The code author made a big boo boo. Tell them to fix it for me, will ya?")
                return
            # Get list of random emojis of the same length as the game pool
            reactions = []
            i = 0
            while i < len(game_pool):
                reaction = random.choice(list(contents.values()))
                if reaction not in reactions:
                    reactions.append(reaction)
                    i = i + 1
            # Create Discord embed and link emojis to nominated games
            description = []
            for x, option in enumerate(game_pool):
                description += '\n {} {}'.format(reactions[x], option.split(" : ", 1)[0])
            embed = discord.Embed(title="Please vote for the nominated game(s):", description=''.join(description))
            react_message = await ctx.send(embed=embed)
            # Add emojis as reactions to poll
            for reaction in reactions[:len(game_pool)]:
                await react_message.add_reaction(reaction)
            # Add countdown timer to embed
            t_end = time.time() + round(60 * minutes)
            while time.time() < t_end:
                if ((t_end - time.time()) / 60) < 1:
                    measure = 'seconds'
                    diff = round(t_end - time.time())
                else:
                    measure = 'minutes'
                    diff = round((t_end - time.time()) / 60)
                embed.set_footer(text='Time remaining on Poll: {} {}'.format(diff, measure))
                await react_message.edit(embed=embed)
                time.sleep(5)
            # Report poll has ended
            embed.set_footer(text='Poll has ended')
            await react_message.edit(embed=embed)
            # Get final message ID and parse embed message for emoji : game pairs
            message = await ctx.channel.fetch_message(react_message.id)
            embed = message.embeds[0]
            unformatted_options = [x.strip() for x in embed.description.split('\n')]
            # Create dictionary of pairs and a dictionary for reaction counts
            opt_dict = {x.split(' ', 1)[0]: x.split(' ', 1)[1] for x in unformatted_options}
            tally = {x: 0 for x in opt_dict.keys()}
            # Count user reactions in addition to initial nominations
            tally = await Utils.voteTally(opt_dict, tally, message)
            # Create weighted list
            weighted_list = []
            for key in tally.keys():
                repeat = int(tally[key])
                i = 1
                while i <= repeat:
                    weighted_list.append(str(opt_dict[key]) + " : " + str(tally[key]))
                    i += 1
            # Pick random game from the pool
            game = random.choice(weighted_list)
            game = game.split(" : ", 1)[0]
            # Pick a random host from the channel
            users = ctx.channel.members
            host = await Utils.pickHost(users)
            # Get the game info from steam
            embed = await Utils.gameInfo(game)
            # Send result to channel
            await ctx.send("I pick \"" + game + f"\" and I think {host.mention} should host! I've cleared the last nomination results and removed it from the pool so it doesn't get picked again. \nHere's the link:", embed=embed)
            # Clear last poll results
            file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Nominations.txt"
            await Utils.deleteFile(file)
            # Remove game from the pool by rewriting file excluding chosen game
            file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + ".txt"
            with open(file, "r+") as f:
                lines = f.readlines()
            with open(file, "w+") as f:
                for line in lines:
                    if line.strip("\n").lower() != game.lower():
                        f.write(line)
            # Add game and host to the winners file
            with open("GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt","a+") as f:
                f.write("\"" + game + "\" on " + datetime.today().strftime('%Y-%m-%d') + " | Hosted by: " + str(host) +"\n")

    @gamepool.command()
    async def winners(self, ctx):
        """List the channel's previous Game Pool winners"""
        winner_pool = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Read from pool into memory
        with open(file,"r+") as f:
            for line in f:
                winner_pool.append(line.strip("\n"))
        # Check if there's nothing in the pool
        if not winner_pool:
            await ctx.send("No past winners.")
        else:
            # Send pool to channel
            message_string = "Here are the past winners: \n"
            for i, winner in enumerate(winner_pool):
                if not i:
                    message_string += str("- " + winner + "\n")
                else:
                    message_string += str("- " + winner + "\n")
            await ctx.send(message_string)
    
    @gamepool.command()
    async def host(self, ctx, *, game):
        """Pick a new host for the winning game"""
        filtered_members = []
        # Create pool file if not exists
        file = "GamePool_" + str(ctx.guild.id) + "_" + str(ctx.channel.id) + "_Winners.txt"
        await Utils.makeFile(file)
        # Get possible users in the channel
        users = ctx.channel.members
        # Read from pool into memory
        with open(file, "r+") as f:
            lines = f.readlines()
        # Rewrite pool and attempt to change game host
        found_game = False
        with open(file, "w+") as f:
            # Read / write file in reverse to get most recent occurance of game
            for line in reversed(lines):
                # Only edit the most recent occurance
                if game.lower() in line.lower() and not found_game:
                    found_game = True
                    # Split line to pull the name of the previous host
                    current_line = line.split("Hosted by: ")
                    old_host = ctx.guild.get_member_named(current_line[1].strip("\n"))
                    # Create list of possible hosts excluding bot(s) and previous host
                    for user in users:
                        if user != old_host and user.bot != True:
                            filtered_members.append(user)
                    try:
                        # Pick new host and write back to file
                        new_host = random.choice(filtered_members)
                        f.write(current_line[0] + "Hosted by: " + str(new_host) + "\n")
                    except: 
                        # Use old host and write back to file
                        new_host = ""
                        f.write(current_line[0] + "Hosted by: " + str(old_host) + "\n")
                    
                else:
                    f.write(line)
        # Rewrite reversed file back in order
        with open(file, "r+") as f:
            lines = f.readlines()
        with open(file, "w+") as f:
            for line in reversed(lines):
                f.write(line)
        # Report to channel
        if not found_game:
            await ctx.send("Game was not found in the pool.")
        elif new_host != "":
            # Found new host
            try:
                await ctx.send(f"{old_host.mention} couldn't cut it huh? Let's make your new host {new_host.mention}")
            except:
                await ctx.send(str(old_host) + " couldn't cut it huh? Let's make your new host " + str(new_host))
        else:
            # No other host possible
            try:
                await ctx.send(f"There's no other hosts to choose from! You're all we got {old_host.mention}")
            except:
                await ctx.send("There's no other hosts to choose from! You're all we got " + str(old_host))
            
