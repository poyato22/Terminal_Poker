# Imports
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.box import DOUBLE

import os
import time
import random

from bot import Bot
from card_evaluator import find_winner

# Constants
speed = 1

suits = ['♠', '♥', '♦', '♣']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

cards = []
players = []

#Make Cards
for suit in suits:
    for rank in ranks:
        color = ["white on yellow", "white on red", "white on blue", "white on green"][suits.index(suit)]
        left = rank.ljust(2)
        right = rank.rjust(2)
        cards.append([
            "┌──────────────┐",
            f"│[{color}] {left:<2}           [/]│",
            f"│[{color}]              [/]│",
            f"│[{color}]      {suit}       [/]│",
            f"│[{color}]              [/]│",
            f"│[{color}]           {right:>2} [/]│",
            f"└──────────────┘"
        ])

random.shuffle(cards)
random.shuffle(cards)

#Print Cards
def print_card(cards):
    returned_cards = []
    for i in range(len(cards[0])):
        for card in cards:
            returned_cards.append(card[i])
        returned_cards.append("\n")

    return "".join(returned_cards[0:-1])

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def phase_change():
    global min_bet, players
    min_bet = 0

    for bot in players:
        if bot.fold == False:
            bot.put_in = 0

def add_players(num):
    global players, cards
    players.append(Bot("YOU", 100, cards = cards[-3:-1], bot=False))
    for i in range(num):
        players.append(Bot(f"Bot {i+1}", 100, cards = cards[-5-i*2:-3-i*2], bot=True))

add_players(5)

console = Console()
terminal_width = console.size.width

turn_text = ""
pot = 0
min_bet = 0
dealer = 0
BB = 10
play = True

def main(): 
    global play, players, cards, round, turn_text, pot, min_bet, dealer, turn, BB, speed
    while play:
        clear()
        speed = 1
        
        for bot in players:
            bot.fold = False
            bot.put_in = 0

        #Setup
        round = "Pre-Flop"
        space = terminal_width - len(left) - len(right) - 2*int(terminal_width/3)
        turn_text = f"[bold white]{players[dealer].name} (dealer)[/]"
        console.print(Align.center(Panel(f"{round}:([yellow on dark_green]{pot:.0f}[/]){' ' * space}{turn_text}", expand=True, style="bold white", box=DOUBLE)))

        panels = [Panel(f"[bold white]Chips: {bot.chips:.0f} (0)\n", title=bot.name, box=DOUBLE) for bot in players]
        console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))
        print("\n")
        console.print(Align.center(Panel("Pre-Flop:\n"+"                                                 \n"*7, style="bold white on dark_green")))
        time.sleep(1*speed)

        #BLINDS
        for i in range(1,3):
            bot = players[(dealer+i) % len(players)]
            bot.chips -= i * BB/2
            pot += i * BB/2
            panels[(dealer+i) % len(players)] = Panel(f"Chips: {bot.chips:.0f} ({i * BB/2:.0f})\n[yellow]Bet: {i * BB/2:.0f}[/]", title=bot.name, box=DOUBLE, style="bold dark_green on black")

            clear()         
            round = "Pre-Flop"
            turn_text = f"[bold white]{bot.name} (blind) {i * BB/2:.0f}[/]"
            console.print(Align.center(Panel(f"{round}:([yellow on dark_green]{pot:.0f}[/]){' ' * space}{turn_text}", expand=True, style="bold white", box=DOUBLE)))
            console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))
            panels[(dealer+i) % len(players)] = Panel(f"[bold white]Chips: {bot.chips:.0f} ({i * BB/2:.0f})\nBet: {i * BB/2:.0f}[/]", title=bot.name, box=DOUBLE)
            
            print("\n")
            console.print(Align.center(Panel("Pre-Flop:\n"+"                                                 \n"*7, style="bold white on dark_green")))

            print("\n")
            console.print(print_card(players[0].cards))
       
            bot.put_in = i * BB/2
            time.sleep(0.3*speed)
        
        min_bet = BB
        turn = (dealer + 3) % len(players)

        check = 0
        num_players = len(players)

        round_continue = True
        #Continous Play
        while round_continue:
            wait = 6/num_players

            if num_players <= 1:
                clear()
                round_continue = False
                for bot in players:
                    if bot.fold == False:
                        bot.chips += pot
                        panels[players.index(bot)] = Panel(f"Chips: {bot.chips:.0f} ({bot.put_in:.0f})\nWon: {pot:.0f}", title=bot.name, box=DOUBLE, style="bold purple on #FFD700")
                        console.print(Align.center(Panel(f"{bot.name} wins {pot:.0f} chips!", style="bold purple on #FFD700")))
                    bot.put_in = 0
                console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))
                print("\n")
                console.print(Align.center(Panel("Round Over\n"+"                                                 \n"*7, style="bold white on dark_green")))
                pot = 0
                dealer += 1
                num_players = len(players)
                time.sleep(6*speed)
                break

            style = "bold dark_green on black"
            bot = players[turn]
            print(players)

            if bot.fold == False:
                if bot.bot == False:

                    #Player Logic
                    panels[turn] = Panel(f"Chips: {bot.chips:.0f} ({bot.put_in:.0f})\n[yellow][/]", title=bot.name, box=DOUBLE, style="bold dark_green on black")
                    turn_text = f"[bold white] YOUR TURN[/]"
                    clear()
                    console.print(Align.center(Panel(f"{round}:([yellow on dark_green]{pot:.0f}[/]){' ' * space}{turn_text}", expand=True, style="bold white", box=DOUBLE)))
                    console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))
                    print("\n")
                    if round == "Pre-Flop":
                        console.print(Align.center(Panel("Pre-Flop:\n"+"                                                 \n"*7, style="bold white on dark_green")))
                    elif round == "Flop":
                        console.print(Align.center(Panel("Flop:\n"+print_card(cards[0:3]), style="bold white on dark_green")))
                    elif round == "Turn":
                        console.print(Align.center(Panel("Turn:\n"+print_card(cards[0:4]), style="bold white on dark_green")))
                    elif round == "River":
                        console.print(Align.center(Panel("River:\n"+print_card(cards[0:5]), style="bold white on dark_green")))
                    print("\n")
                    console.print(print_card(players[0].cards))

                    while True:
                        move = input(f"{bot.name} [{bot.chips:.0f}] (Call/Check: c, Fold: f, Raise: r): ").strip()
                        try:
                            if move.lower() == "c":
                                if min_bet - bot.put_in == 0:
                                    move = "Check"
                                elif min_bet - bot.put_in < bot.chips:
                                    bot.chips -= (min_bet - bot.put_in)
                                    move = "Call: " + str(min_bet - bot.put_in)
                                    pot += (min_bet - bot.put_in)
                                    bot.put_in += (min_bet - bot.put_in)
                                elif min_bet - bot.put_in > bot.chips:
                                    move = f"All-In: ({bot.chips})"
                                    pot+= bot.chips
                                    bot.put_in += bot.chips
                                    bot.chips = 0
                                break

                            elif move.lower() == "f":
                                bot.fold = True
                                move = "Fold"
                                style = "bold red on black"
                                num_players -= 1
                                check -= 1
                                speed = speed * 0.1
                                break

                            elif move.lower() == "r":
                                if bot.chips - min_bet+bot.put_in <= 0:
                                    print("You don't have enough chips to raise.")
                                else:
                                    raise_amount = input(f"Raise amount (1-{bot.chips-min_bet+bot.put_in}): ").strip()
                                    if  int(raise_amount) <= bot.chips-min_bet+bot.put_in and int(raise_amount) > 0:
                                        bot.chips -= int(raise_amount) + min_bet - bot.put_in
                                        pot += int(raise_amount) - min_bet + bot.put_in
                                        x = bot.put_in
                                        bot.put_in += int(raise_amount) + min_bet - bot.put_in
                                        min_bet = int(raise_amount) + min_bet - x
                                        move = "Raise: " + raise_amount
                                        raise StopIteration
                                    else:
                                        print(f"Invalid raise amount. Maximum is {bot.chips-min_bet-bot.put_in}.")
                                        continue
                            else:
                                print("Invalid input. Please try again.")
                                continue
                        except ValueError:
                            print("Invalid input. Please try again.")
                            continue
                        except StopIteration:
                            break

                elif bot.bot == True:
                    move = bot.logic(bot.put_in, min_bet, bot.cards, pot, round)

                    if "Call" in move:
                        bot.put_in += int(move.split(": ")[-1]) 
                        pot += int(move.split(": ")[-1])

                    if "Fold" in move:
                        move = "Fold"
                        style = "bold red on black"
                        num_players -= 1
                        check -= 1

                    if "Raise" in move:
                        raise_amount = int(move.split(": ")[-1])
                        bot.chips -= raise_amount + min_bet - bot.put_in
                        pot += raise_amount - min_bet + bot.put_in
                        x = bot.put_in
                        bot.put_in += raise_amount + min_bet - bot.put_in
                        min_bet = raise_amount + min_bet - x

                if move != "Raise" and round == "Pre-Flop" and num_players > 1:
                    check += 1
                    if check == num_players:
                        round = "Flop"
                        check = 0
                        wait = 3
                        phase_change()
                elif move != "Raise" and round == "Flop" and num_players > 1:
                    check += 1
                    if check == num_players:
                        round = "Turn"
                        check = 0
                        wait = 3
                        phase_change()
                elif move != "Raise" and round == "Turn" and num_players > 1:
                    check += 1
                    if check == num_players:
                        round = "River"
                        check = 0
                        wait = 3
                        phase_change()
                elif move != "Raise" and round == "River" and num_players > 1:
                    check += 1
                    if check == num_players:
                        clear()
                        round_continue = False
                        win_cards = []
                        win_pannel = []
                        for bot in players:
                            if bot.fold == False:
                                win_cards.append([bot.cards,bot])
                                win_pannel.append(Panel(print_card(bot.cards), title=bot.name, box=DOUBLE, style="bold white on dark_green"))
                            bot.put_in = 0

                        winners = find_winner(win_cards, cards[0:5])
                        for winner in winners:
                            winner[0].chips += pot/len(winners)
                            panels[players.index(winner[0])] = Panel(f"Chips: {winner[0].chips:.0f} ({winner[0].put_in:.0f})\nWon: {pot:.0f}", title=winner[0].name, box=DOUBLE, style="bold purple on #FFD700")

                        for pannel in win_pannel:
                            if pannel.title in [winner[0].name for winner in winners]:
                                pannel.style = "bold purple on #FFD700"

                        console.print(Align.center(Panel(f"{' '.join([winner[0].name for winner in winners])} wins {pot:.0f} chips! ({winners[0][1]})", style="bold purple on #FFD700")))
                        console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))
                        print("\n")
                        console.print(Align.center(Panel("River:\n"+print_card(cards[0:5]), style="bold white on dark_green")))
                        print("\n")
                        console.print(Columns(win_pannel, expand=True, equal=True, padding=(0,0)))
                        pot = 0
                        dealer += 1
                        num_players = len(players)
                        time.sleep(6*speed)
                        break

                panels[turn] = Panel(f"Chips: {bot.chips:.0f} ({bot.put_in:.0f})\n[yellow]{move}[/]", title=bot.name, box=DOUBLE, style=style)

                turn_text = f"[bold white]{bot.name} {move.split(': ')[0].lower()}[/]"
                clear()
                console.print(Align.center(Panel(f"{round}:([yellow on dark_green]{pot:.0f}[/]){' ' * space}{turn_text}", expand=True, style="bold white", box=DOUBLE)))
                console.print(Columns(panels, expand=True, equal=True, padding=(0,0)))

                print("\n")
                if round == "Pre-Flop":
                    console.print(Align.center(Panel("Pre-Flop:\n"+"                                                 \n"*7, style="bold white on dark_green")))
                elif round == "Flop":
                    console.print(Align.center(Panel("Flop:\n"+print_card(cards[0:3]), style="bold white on dark_green")))
                elif round == "Turn":
                    console.print(Align.center(Panel("Turn:\n"+print_card(cards[0:4]), style="bold white on dark_green")))
                elif round == "River":
                    console.print(Align.center(Panel("River:\n"+print_card(cards[0:5]), style="bold white on dark_green")))

                print("\n")
                console.print(print_card(players[0].cards))

                panels[turn] = Panel(f"[bold white]Chips: {bot.chips:.0f} ({bot.put_in:.0f})\n{move}[/]", title=bot.name, box=DOUBLE)

                if move == "Fold":
                    panels[turn] = Panel(f"Chips: {bot.chips:.0f} ({bot.put_in:.0f})\n{move}", title=bot.name, box=DOUBLE, style=style)

                if num_players > 1:
                    time.sleep(wait*speed)
                else:
                    time.sleep(1*speed)

            turn = (turn+1) % len(players)
            
main()
