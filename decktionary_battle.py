import random
import csv

class DecktionaryBattle:
    def __init__(self):
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player1_score = 0
        self.player2_score = 0
        self.debug = False
        self.game_log = []
        self.game_number = 1
        self.playing_against_bot = False
        self.bot_difficulty = None

    def choose_opponent(self):
        # This is to choose to play against another human locally or against the computer
        print("Choose your opponent:")
        print("1. Human")
        print("2. CPU")
        while True:
            choice = input("Enter 1 for Human or 2 for CPU: ").strip()
            if choice == '1':
                self.playing_against_bot = False
                print("You chose to play against a human!")
                return
            elif choice == '2':
                self.playing_against_bot = True
                self.choose_bot_difficulty()
                print("You the difficulty:")
                print(f"{self.bot_difficulty}")
                return
            else:
                print("Invalid choice. Please Try again.")

    def choose_bot_difficulty(self):
        # Chooses difficulty (Currently only easy or expert)

        print("Choose bot difficulty:")
        print("1. Easy")
        print("2. Expert")
        while True:
            difficulty = input("Enter 1 for Easy or 2 for Expert: ").strip()
            if difficulty == '1':
                self.bot_difficulty = "easy"
                return
            elif difficulty == '2':
                self.bot_difficulty = "expert"
                return
            else:
                print("Invalid choice. Please try again.")

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(2,15)) # 2 to Ace (Ace = 14)
        deck = [(rank, suit) for suit in suits for rank in ranks if rank != 13] # This removes the kings
        random.shuffle(deck)
        return deck
    
    def log_event(self, round_num, player1_card, player2_card, winner):
        #Logs the details of the round to then be saved to a .csv file
        self.game_log.append({
            'Game': self.game_number,
            'Round': round_num,
            'Player 1 Hand': self.player1_hand.copy(),
            'Player 2 Hand': self.player2_hand.copy(),
            'Player 1 Card': player1_card,
            'Player 2 Card': player2_card,
            'Winner': f"Player {winner}",
            'Player 1 Score': self.player1_score,
            'Player 2 Score': self.player2_score
        })

    def save_log_to_csv(self, filename="game_log.csv"):
        with open(filename, 'a', newline='') as csvfile:  # Open in append mode
            fieldnames = [
                'Game', 
                'Round', 
                'Player 1 Hand', 
                'Player 2 Hand', 
                'Player 1 Card', 
                'Player 2 Card', 
                'Winner', 
                'Player 1 Score', 
                'Player 2 Score'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write header only if the file is empty
            if csvfile.tell() == 0:
                writer.writeheader()

            # Add the game number to each log entry and write to the CSV
            for log in self.game_log:
                for field in fieldnames:
                    log.setdefault(field, '')
                log['Game'] = self.game_number  # Include game number
                writer.writerow(log)

            # Add a blank row to separate games
            writer.writerow({})

        self.game_number += 1

    def log_final_scores(self):
    # Logs the final scores and game summary.
        self.game_log.append({
            'Game': self.game_number,
            'Round': 'Final',
            'Player 1 Hand': self.player1_hand.copy(),
            'Player 2 Hand': self.player2_hand.copy(),
            'Player 1 Card': '',
            'Player 2 Card': '',
            'Winner': 'Game Over',
            'Player 1 Score': self.player1_score,
            'Player 2 Score': self.player2_score
    })

    def deal_cards(self):
        self.player1_hand = [self.deck.pop() for _ in range(8)]
        self.player2_hand = [self.deck.pop() for _ in range(8)]
        if self.debug:
            print("Player 1 Hand:")
            print(self.render_cards(self.player1_hand))
            print("Player 2 Hand:")
            print(self.render_cards(self.player2_hand))
        
        self.game_log.append({
            'Round': 'Deal',
            'Player 1 Hand': self.player1_hand,
            'Player 2 Hand': self.player2_hand,
            'Winner': 'N/A'
        })

    def render_cards(self, cards):
        # This is going to change the cards from (#, *Suit*) to display a text based image of a card to look nicer when playing

        if isinstance(cards, tuple):
            cards = [cards]  # Converts single card tuple to a list

        suit_symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}
        rank_map = {11: 'J', 12: 'Q', 14: 'A'} # Maps the special cards so it doesnt appear as a number
        card_lines = [''] * 4 # For storing the actual face of the cards

        for rank, suit in cards:
            rank_str = rank_map.get(rank, str(rank)) # This changes number to a string
            suit_symbol = suit_symbols[suit]

            # Add card lines
            card_lines[0] += "┌─────┐  "
            card_lines[1] += f"|  {rank_str:<2} |  "  # Rank left-aligned
            card_lines[2] += f"|  {suit_symbol}  |  "
            card_lines[3] += f"|  {rank_str:<2} |  "
        
        card_lines.append("└─────┘  " * len(cards))

        return "\n".join(card_lines)
    
    def lead_round(self, leader, follower):
        if leader == 1:
            player1_card = self.choose_card(self.player1_hand, 1)
            player2_card = self.choose_card(self.player2_hand, 2)
        else:
            player2_card = self.choose_card(self.player2_hand, 2)
            player1_card = self.choose_card(self.player1_hand, 1)
        
        # Determines the lead suit
        self.lead_suit = player1_card[1] if leader == 1 else player2_card[1]
        print("Player 1 plays:")
        print(self.render_cards(player1_card))
        print("Player 2 plays:")
        print(self.render_cards(player2_card))
        print(f"Lead suit: {self.lead_suit}")
        
        # Initilization of the winner variable
        winner = None

        # Follow Suit Rule Check: Checks to see if anyone did not follow the suit
        if follower == 2 and player2_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.player2_hand):
            print("Player 2 broke the rules by not following suit!")
            winner = 1 # Player 1 automatically wins
        elif follower == 1 and player1_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.player1_hand):
            print("Player 1 broke the rules by not following suit!")
            winner = 2 # Player 2 automatically wins
            
        if winner is None:   
            # Determines the winner normally if no rules have been broken
            if (player2_card[1] == self.lead_suit and leader == 1) or (player1_card[1] == self.lead_suit and leader == 2):
                winner = 1 if player1_card[0] > player2_card[0] else 2
                print(f"Both players followed the suit. Winner: Player {winner}")
            else:
                winner = leader
                print(f"Player {follower} did not follow suit. Winner: {leader}")
        
        # Updates the scores
        if winner == 1:
            self.player1_score += 1
            print("Player 1 wins this round!")
        else:
            self.player2_score += 1
            print("Player 2 wins this round!")
        
        # Reveals the next card from the deck
        revealed_card = self.deck.pop()
        self.revealed_cards.append(revealed_card)
        print("Revealed Card:")
        print(self.render_cards(revealed_card))
        
        return player1_card, player2_card, winner
    
    def get_lead_suit(self):
        """Returns the lead suit for the current round"""
        return self.lead_suit

    def choose_card(self, player_hand, player_num):
        
        # This allows players or the cpu to choose a card from their hand with controls for privacy
        if self.playing_against_bot and player_num == 2:
            return self.bot_choose_card(player_hand)
        
        # Human player options
        hidden = not self.playing_against_bot # Privacy is disabled against bots (Bot cant read the screen)
        while True:
            if hidden:
                print(f"Player {player_num}'s hand is hidden. Type 'show' (s) to display it.")
            else:
                print(f"Player {player_num}'s turn. Your hand:")
                print(self.render_cards(player_hand))
        
            choice = input(f"Player {player_num}, choose an action (show/s, hide/h, or pick a card): ").lower()

            if choice in ['show', 's'] and not self.playing_against_bot:
                hidden = False
            elif choice in ['hide', 'h'] and not self.playing_against_bot:
                hidden = True
            elif choice.isdigit() and not hidden:
                card_idx = int(choice)
                if 0 <= card_idx < len(player_hand):
                    return player_hand.pop(card_idx)
                else:
                    print("Invalid card index. Please try again.")
            else:
                print("Invalid input. Please try again.")

    def bot_choose_card(self, bot_hand):
        """Logic for the bot to choose a card base on the difficulty."""
        print("Bot is choosing a card...")
        if self.bot_difficulty == "easy":
            return self.bot_easy_choice(bot_hand)
        elif self.bot_difficulty == "expert":
            return self.bot_expert_choice(bot_hand)

    def bot_easy_choice(self, bot_hand):
        random.shuffle(bot_hand) # This will shuffle the bots hand to add randomness to the pick
        return bot_hand.pop() # Picks a random card from the hand
    
    def bot_expert_choice(self, bot_hand):
        if self.lead_suit is None:
            # If there is no lead suit, play the lowest card
            return bot_hand.pop(bot_hand.index(min(bot_hand, key=lambda x: x[0])))
        
        # Filters cards in hand for the lead suit
        valid_cards = [card for card in bot_hand if card[1] == self.lead_suit]
        if valid_cards:
            return bot_hand.pop(bot_hand.index(max(valid_cards, key=lambda x: x[0]))) # Plays then highest card in suit
        else:
            return bot_hand.pop(bot_hand.index(min(bot_hand, key=lambda x: x[0]))) # Dumps lowest card

    def print_instructions(self):
    # This is to print the rules and instructions of the game.
        print("\n--- Rules of Decktionary Battle ---")
        print("""
        1. The game uses a standard deck of playing cards with Kings removed (48 cards).
        2. Each player starts with 8 cards in their hand.
        3. Player 1 always leads the first round.
        4. The player who leads sets the suit for the round (the lead suit).
        5. The other player must follow the lead suit if possible.
        6. If the player cannot follow the lead suit, they may play any card.
        7. The highest-value card in the lead suit wins the round.
        8. The player who wins the round earns a point and leads the next round.
        9. After every 8 rounds, if enough cards are left in the deck, each player is dealt 8 new cards.
        10. The game ends when:
            - One player scores 16-0 and "shoots the moon," winning with 17 points.
            - One player scores 9+ points while the other player has at least 1 point.
            - The deck runs out of cards to deal.
        11. The player with the most points at the end of the game wins.

        Instructions:
        - Players will take turns selecting cards from their hand.
        - Follow the prompts to choose a card to play each round.
        - Have fun and strategize to win!       
        """)
    
    def get_game_length(self):
        # Prompts user to choose the length of the game.
        print("Choose game length:")
        print("short (s) - Play one hand (8 rounds)")
        print("long (l) - Play the entire deck (Default)")
        while True:
            choice = input("Enter your choice (short/s or long/l}: ").lower()
            if choice in ['short', 's']:
                return "short"
            if choice in ['long', 'l']:
                return "long"
            else:
                print("Invalid input. Please type 'short' or 's' fpr a short game, or 'long' or 'l' for a long game.")

    def play_game(self):
        print("Welcome to Decktionary Battle!")
        self.print_instructions() # Runs the print_instructions
        
        # Choose opponent type
        self.choose_opponent()

        # Choose game length
        game_length = self.get_game_length()
        
        self.deal_cards() # Deals out the initial 8 cards
        
        self.lead_suit = None

        # Player 1 leads the first round
        leader = 1

        while True: # Loops until the game ends
            for round_num in range(1,9): # Play 8 rounds
                print(f"\n--- Round {round_num} ---")
                print(f"Player {leader} is leading this round.")
                player1_card, player2_card, winner = self.lead_round(leader, 2 if leader == 1 else 1)

                leader = winner

                # Logs the round        
                self.log_event(round_num, player1_card, player2_card, winner)
                
                # Checks the game-ending criteria after each round
                if self.check_game_end():
                    self.log_final_scores()
                    self.save_log_to_csv()
                    return
            
            if game_length == "short":
                print("\n--- Short game completed ---")
                self.log_final_scores()
                self.save_log_to_csv()
                break

            # Deals new cards
            if len(self.deck) >= 16:
                print("\n--- Dealing New Cards ---")
                self.deal_cards()
            else:
                print("\nNot enough cards to deal. Game over.")
                self.log_final_scores()
                self.save_log_to_csv()               
                break
        
        self.print_final_scores()
    
    def check_game_end(self):
        # Checks if the game should end based off the set rules

        # If a player has shot the moon
        if self.player1_score == 16 and self.player2_score == 0:
            self.print_final_scores("Player 1 has shot the moon and wins with 17 points!")
            return True
        if self.player2_score == 16 and self.player1_score == 0:
            self.print_final_scores("Player 2 has shot the moon and wins with 17 points!")
            return True
        
        # If a player is guaranteed to win
        if self.player1_score >= 9 and self.player2_score >= 1:
            self.print_final_scores("Player 1 is guaranteed to win. Ending game early.")
            return True
        if self.player2_score >= 9 and self.player1_score >= 1:
            self.print_final_scores("Player 2 is guaranteed to win. Ending game early.")
            return True
        
        return False # Continues game if moon or guaranteed win criteria has not been met
         
    def print_final_scores(self, message=None):   
        if message:
            print(f"\n{message}")
        print("\n--- Final Scores ---")
        print("Player 1:", self.player1_score)
        print("Player 2:", self.player2_score)

        if self.player1_score > self.player2_score:
            print("Player 1 wins the game!")
        elif self.player2_score > self.player1_score:
            print("Player 2 wins the game!")
        else:
            print("The game is a tie!")
        

game = DecktionaryBattle()
game.play_game()