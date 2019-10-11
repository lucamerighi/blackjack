#! /usr/bin/python3

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
import random

def load_cards():
    suits = ['C', 'D', 'H', 'S']
    faces = ['J', 'Q', 'K']

    for suit in suits:
        #Load cards from 2 to 10
        for value in range(2, 11):
            filename = './src/cards/{}{}.png'.format(str(value), suit)
            image = tk.PhotoImage(file=filename)
            cards.append([value, image])
        #Load aces
        filename = './src/cards/A{}.png'.format(suit)
        image = tk.PhotoImage(file=filename)
        cards.append([1, image])
        #Load faces
        for face in faces:
            filename = './src/cards/{}{}.png'.format(face, suit)
            image = tk.PhotoImage(file=filename)
            cards.append([10, image])


# Main window
root = tk.Tk()
root.geometry('640x480')
root.title('Blackjack')
root.config(bg='green', padx=5)

# Result GUI
result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, bg='green', font='Helvetica 12 bold').grid(row=0, column=0, columnspan=3, sticky='ew')

# Dealer GUI
center_frame = tk.Frame(root, bg='green')
center_frame.grid(row=1, column=0, rowspan=2, columnspan=3)
tk.Label(center_frame, text='Dealer', font='Helvetica 12 bold', bg='green').grid(row=0, column=0)
dealer_score = tk.StringVar()
tk.Label(center_frame, textvariable=dealer_score, font='Helvetica 12 bold').grid(row=1, column=0)
dealer_card_frame = tk.Frame(center_frame, bg='green')
dealer_card_frame.grid(row=0, column=1, rowspan= 2, sticky='ew')

# Player GUI
tk.Label(center_frame, text='Player', font='Helvetica 12 bold').grid(row=2, column=0)
player_score = tk.StringVar()
player_score_label = tk.Label(center_frame, textvariable=player_score, font='Helvetica 12 bold')
player_score_label.grid(row=3, column=0)
player_card_frame = tk.Frame(center_frame, bg='green')
player_card_frame.grid(row=2, column=1, rowspan= 2, sticky='ew')

# Draws a card from the deck
def deal_card(frame):
    card = deck.pop(0)
    tk.Label(frame, image=card[1], bg='green').pack(side='left')
    return card

# Adds a card to the player frame
def deal_player():
    player_hand.append(deal_card(player_card_frame))
    score = score_hand(player_hand)
    player_score.set(score)
    if score > 21:
        result_text.set('Dealer Won!')
        card_btn.config(state='disabled')
        stop_btn.config(state='disabled')
        dealer_wins.set(dealer_wins.get() + 1)

# Adds cards to the dealer frame until soft 17
def deal_dealer():
    global player_wins, dealer_wins
    card_btn.config(state='disabled')
    score = score_hand(dealer_hand)
    while score < 17:
        dealer_hand.append(deal_card(dealer_card_frame))
        score = score_hand(dealer_hand)
        dealer_score.set(score)
    if score > 21:
        result_text.set('Player Won!')
        player_wins.set(player_wins.get() + 1)
    elif score > int(player_score.get()):
        result_text.set('Dealer Won!')
        dealer_wins.set(dealer_wins.get() + 1)
    elif score == int(player_score.get()):
        result_text.set('Draw!')
    else:
        result_text.set('Player Won!')
        player_wins.set(player_wins.get() + 1)


# Calculates the score of a hand
def score_hand(hand):
    has_ace = False
    score = 0
    for card in hand:
        value = card[0]
        if card[0] == 11:
            value = 11
            has_ace = True
        score += value
        if score > 21 and has_ace:
            score -= 10
            has_ace = False
    return score


# Resets the board
def new_game():
    global dealer_card_frame
    global player_card_frame
    dealer_card_frame.destroy()
    dealer_card_frame = tk.Frame(center_frame, background='green')
    dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)
    player_card_frame.destroy()
    player_card_frame = tk.Frame(center_frame, background="green")
    player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

    result_text.set("")
    card_btn.config(state='normal')
    stop_btn.config(state='normal')

    player_hand.clear()
    dealer_hand.clear()

    deck = list(cards)
    random.shuffle(deck)

    deal_player()
    dealer_hand.append(deal_card(dealer_card_frame))
    dealer_score.set(score_hand(dealer_hand))
    deal_player()

# Button GUI
btn_frame= tk.Frame(root, bg='green')
btn_frame.grid(row=3, column=0, columnspan=3, sticky='w')
card_btn = tk.Button(btn_frame, text='Card', command=deal_player)
card_btn.grid(row=0, column=0)
stop_btn = tk.Button(btn_frame, text='Stop', command=deal_dealer)
stop_btn.grid(row = 0, column=1)
new_game_btn = tk.Button(btn_frame, text='New Game', command=new_game)
new_game_btn.grid(row=0, column=2)

# Wins
wins_frame = tk.Frame(root, bg='green')
wins_frame.grid(row=4, column=0, sticky='w')
player_wins = tk.IntVar()
dealer_wins = tk.IntVar()
player_wins.set(0)
dealer_wins.set(0)
tk.Label(wins_frame, text='Dealer Wins: ', bg='green').grid(row=0, column=0)
dealer_wins_label = tk.Label(wins_frame, textvariable=dealer_wins, bg='green')
dealer_wins_label.grid(row=0, column=1)
tk.Label(wins_frame, text='Player Wins: ', bg='green').grid(row=0, column=2)
player_wins_label = tk.Label(wins_frame, textvariable=player_wins, bg='green')
player_wins_label.grid(row=0, column=3)

for btn in btn_frame.winfo_children():
    btn.grid_configure(padx=5, pady=10)

for child in center_frame.winfo_children():
    child.config(bg='green')

# Load cards and shuffle deck
cards = []
load_cards()
deck = list(cards)
random.shuffle(deck)

player_hand = []
dealer_hand = []

new_game()
root.mainloop()