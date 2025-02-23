import random
from flask import Blueprint, flash, redirect, render_template, session, url_for

black_jack_bp = Blueprint("black_jack", __name__)

# Setup where starting hands are built
@black_jack_bp.route("/set_up", methods=['GET','POST'])
def set_up():    
    deck=build_deck()   # Creating deck
    session["deck"]=deck # Saving deck in session
    session["player_hand"] = [draw_card(), draw_card()] # Saving player hand in session
    session["computer_hand"] = [draw_card()] # Saving computer hand in session
    return redirect(url_for("black_jack.play_black_jack"))

# "Game board"
@black_jack_bp.route("/play_black_jack", methods=['GET','POST'])
def play_black_jack():
    session["player_score"]=calculate(session["player_hand"])
    session["computer_score"]=calculate(session["computer_hand"])    
    return render_template("black_jack.html")  

#Build deck
def build_deck():
    #Create a list with all cards in the deck
    deck=[f"hearts {i}" for i in range(2,11)] +\
         ["hearts knight","hearts queen","hearts king","hearts ace"] +\
         [f"diamonds {i}" for i in range(2,11)] +\
         ["diamonds knight","diamonds queen","diamonds king","diamonds ace"] +\
         [f"clubs {i}" for i in range(2,11)] +\
         ["clubs knight","clubs queen","clubs king","clubs ace"] +\
         [f"spades {i}" for i in range(2,11)] +\
         ["spades knight","spades queen","spades king","spades ace"]
    # Shuffle the deck 
    random.shuffle(deck) 
    return deck

# Draw card and remove it from deck in session, so that every card only can be drawn once
@black_jack_bp.route("/draw_card", methods=['POST'])
def draw_card():         
    return session["deck"].pop()

# Method to draw card to player hand, callable from front end
@black_jack_bp.route("/add_card", methods=['POST'])
def add_card():
    new_hand = session["player_hand"][:] # Copy player hand to new list to make sure it's stored as a list
    new_hand.append(draw_card()) # Add new card
    session["player_hand"]=new_hand
    session["player_score"]=calculate(session["player_hand"]) # Check new score
    if session["player_score"] > 21: 
        check_score() 
    return render_template("black_jack.html")

# Draw card method for computer hand
def computer_draw_card():    
    new_hand = session["computer_hand"][:]
    new_hand.append(draw_card())
    session["computer_hand"]=new_hand
    session["computer_score"]=calculate(session["computer_hand"])
    if session["computer_score"] > 21:
        check_score()     
    return render_template("black_jack.html")
        

# Controls computer after player clicked "Stand"
@black_jack_bp.route("/computer_move", methods=['GET','POST'])
def computer_move():
    score=calculate(session["computer_hand"]) # Check score
    player_score=calculate(session["player_hand"])
    if score < 17 and player_score<=21: # Conditions for computer to draw new card
        computer_draw_card()
        score=calculate(session["computer_hand"])
        if score < 17 and player_score<=21: 
            return redirect(url_for("black_jack.computer_move")) # Repeats method           
    check_score() # Checks result when conditions are met
    return redirect(url_for("black_jack.play_black_jack"))

def check_sum(sum,card): # Calculates the numeric value from a card   
    value=card.split()[1]
    if value == "knight" or value == "queen" or value == "king":
        return 10
    elif value == "ace":
        if sum<=10:
            return 11
        else:
            return 1
    else:
        return int(value)

def calculate(cards): # Calculates the sum in a hand
    sum=0
    for c in cards:        
        sum+=check_sum(sum,c)
    return sum

@black_jack_bp.route("/check_score", methods=['GET']) # Checks who won
def check_score():
    player_sum=session["player_score"]
    computer_sum=session["computer_score"]
    if player_sum>21:
        flash("You're thick, Computer wins!") 
    elif computer_sum>21:
        flash("Computer's thick, player wins!")        
    else:
        if player_sum>computer_sum:
            flash("Player wins!")
        elif player_sum == computer_sum:
            flash("It's a draw!")
        elif player_sum<computer_sum:
            flash("Computer wins!")
    return redirect(url_for("home"))




 
       
