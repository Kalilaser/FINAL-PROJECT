import random
import csv
import pandas as pd
import time
import seaborn as sns
import matplotlib.pyplot as plt

class DecktionaryBattle:
    def __init__(self):
        self.deck = self.create_deck()
        self.revealed_cards = []
        self.player_score = 0
        self.bot_score = 0
        self.game_log = pd.DataFrame(columns=[
            'Timestamp', 'Game', 'Round', 'Player Hand', 'Bot Hand', 
            'Player Card', 'Bot Card', 'Winner', 
            'Player Score', 'Bot Score', 'Bot Decision Time (s)'
        ])
        self.game_number = 1
        self.playing_against_bot = True
        self.bot_difficulty = None

    def create_deck(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = list(range(2,15)) # 2 to Ace (Ace = 14)
        deck = [(rank, suit) for suit in suits for rank in ranks if rank != 13] # Removes the kings
        random.shuffle(deck)
        return deck

    def choose_bot_difficulty(self):
        # Chooses difficulty (Currently only easy or expert)

        print("Choose bot difficulty:")
        print("1. Easy")
        print("2. Expert")
        while True:
            difficulty = input("Enter 1 for Easy or 2 for Expert: ").strip()
            if difficulty == '1':
                self.bot_difficulty = "easy"
                print("You chose Easy difficulty!")
                return
            elif difficulty == '2':
                self.bot_difficulty = "expert"
                print("You chose Expert difficulty!")
                return
            else:
                print("Invalid choice. Please try again.")
    
    def deal_cards(self):
        self.player_hand = [self.deck.pop() for _ in range(8)]
        self.bot_hand = [self.deck.pop() for _ in range(8)]
        print("Your Hand:")
        print(self.render_cards(self.player_hand))

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

    def log_event(self, round_num, player_card, bot_card, winner, bot_decision_time):
        # Events logged using Pandas
        self.game_log = pd.concat([self.game_log, pd.DataFrame([{
            'Timestamp': time.strftime('%d-%m-%Y %H:%M:%S'),
            'Game': self.game_number,
            'Round': round_num,
            'Player Hand': repr(self.player_hand),
            'Bot Hand': repr(self.bot_hand),
            'Player Card': repr(player_card),
            'Bot Card': repr(bot_card),
            'Winner': f"Player {winner}",
            'Player Score': self.player_score,
            'Bot Score': self.bot_score,
            'Bot Decision Time (s)': bot_decision_time
        }])], ignore_index=True)

    def save_log_to_csv(self, filename="game_log.csv"):
        # Deduplicate data before saving
        self.game_log = self.game_log.drop_duplicates(subset=['Timestamp', 'Game', 'Round'], keep='first')

        # Save DataFrame to CSV
        self.game_log.to_csv(filename, index=False, mode='a', header=not pd.io.common.file_exists(filename))
        print(f"Game log saved to {filename} successfully.")

    def log_final_scores(self):
        # Logs final scores and generates graphs.
        final_log = pd.DataFrame([{
            'Timestamp': time.strftime('%d-%m-%Y %H:%M:%S'),
            'Game': self.game_number,
            'Round': 'Final',
            'Player Hand': str(self.player_hand),
            'Bot Hand': str(self.bot_hand),
            'Player Card': '',
            'Bot Card': '',
            'Winner': 'Game Over',
            'Player Score': self.player_score,
            'Bot Score': self.bot_score,
            'Bot Decision Time (s)': ''
        }])

        # Concatenate the final log and deduplicate
        self.game_log = pd.concat([self.game_log, final_log], ignore_index=True)
        self.game_log = self.game_log.drop_duplicates(subset=['Timestamp', 'Game', 'Round'], keep='first')

        # Save to CSV
        self.save_log_to_csv()

        # Generate graphs
        self.generate_graphs()
    
    def lead_round(self, leader, follower):
        if leader == 1:
            player_card = self.player_choose_card(self.player_hand, 1)
            bot_card, bot_decision_time = self.bot_choose_card(self.bot_hand)
        else:
            bot_card, bot_decision_time = self.bot_choose_card(self.bot_hand)
            player_card = self.player_choose_card(self.player_hand, 1)
        
        # Determines the lead suit
        self.lead_suit = player_card[1] if leader == 1 else bot_card[1]
        print("Player plays:")
        print(self.render_cards(player_card))
        print("Bot plays:")
        print(self.render_cards(bot_card))
        print(f"Lead suit: {self.lead_suit}")
        
        # Initialization of the winner variable
        winner = None

        # Follow Suit Rule Check: Checks to see if anyone did not follow the suit
        if follower == 2 and bot_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.bot_hand):
            print("Bot broke the rules by not following suit!")
            winner = 1  # Player automatically wins
        elif follower == 1 and player_card[1] != self.lead_suit and any(card[1] == self.lead_suit for card in self.player_hand):
            print("Player broke the rules by not following suit!")
            winner = 2  # Bot automatically wins
            
        if winner is None:   
            # Determines the winner normally if no rules have been broken
            if (bot_card[1] == self.lead_suit and leader == 1) or (player_card[1] == self.lead_suit and leader == 2):
                winner = 1 if player_card[0] > bot_card[0] else 2
                print(f"Both players followed the suit. Winner: Player {winner}")
            else:
                winner = leader
                print(f"Player {follower} did not follow suit. Winner: {leader}")
        
        # Updates the scores
        if winner == 1:
            self.player_score += 1
            print("Player wins this round!")
        else:
            self.bot_score += 1
            print("Bot wins this round!")
        
        # Reveals the next card from the deck
        revealed_card = self.deck.pop()
        self.revealed_cards.append(revealed_card)
        print("Revealed Card:")
        print(self.render_cards(revealed_card))
        
        # Return player_card, bot_card, and winner
        return player_card, bot_card, winner, bot_decision_time
    
    def get_lead_suit(self):
        # Returns the lead suit for the current round
        return self.lead_suit

    def player_choose_card(self, player_hand, player_num):
        # Player card selection logic
        print("Your hand:")
        print(self.render_cards(self.player_hand))
        while True:
            try:
                choice = int(input(f"Player {player_num}, choose a card index (0-{len(player_hand)-1}): "))
                if 0 <= choice < len(player_hand):
                    return player_hand.pop(choice)
                print("Invalid choice. Try again.")
            except ValueError:
                print("Enter a valid number.")

    def bot_choose_card(self, bot_hand):
        start_time = time.time()  # Start timing
        if self.bot_difficulty == "easy":
            card = self.bot_easy_choice(bot_hand)
        elif self.bot_difficulty == "expert":
            card = self.bot_expert_choice(bot_hand)
        end_time = time.time()  # End timing
        bot_decision_time = round(end_time - start_time, 3)
        print(f"Bot decision time: {bot_decision_time} seconds")
        return card, bot_decision_time  # Ensure both values are returned for logging

    def bot_easy_choice(self, bot_hand):
        # Logic for easy bot (picks random card)
        return bot_hand.pop(random.randint(0, len(bot_hand) - 1)) 
    
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
        3. Player always leads the first round.
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
    
    def play_game(self):
        print("Welcome to Decktionary Battle!")
        self.print_instructions()  # Display instructions
        
        self.choose_bot_difficulty()  # Choose bot difficulty
        self.deal_cards()  # Initial deal of cards
        
        self.lead_suit = None
        leader = 1  # Player starts as the leader
        
        while True:  # Loop until the game ends
            for round_num in range(1, 9):  # Play 8 rounds per hand
                print(f"\n--- Round {round_num} ---")
                print(f"Player {leader} is leading this round.")
                
                # Call lead_round to handle the round logic
                player_card, bot_card, winner, bot_decision_time = self.lead_round(leader, 2 if leader == 1 else 1)
                
                # Update leader based on the round winner
                leader = winner
                
                # Log the event (including bot decision timing from lead_round)
                self.log_event(round_num, player_card, bot_card, winner, bot_decision_time)
                
                # Check if game-ending criteria are met
                if self.check_game_end():
                    self.log_final_scores()
                    self.save_log_to_csv()
                    return
            
            # Deal new cards if enough cards remain in the deck
            if len(self.deck) >= 16:
                print("\n--- Dealing New Cards ---")
                self.deal_cards()
            else:
                print("\nNot enough cards to deal. Game over.")
                self.log_final_scores()
                self.save_log_to_csv()
                break

        # Print final scores at the end of the game
        self.print_final_scores()
    
    def check_game_end(self):
        # Checks if the game should end based off the set rules

        # If a player has shot the moon
        if self.player_score == 16 and self.bot_score == 0:
            self.print_final_scores("Player has shot the moon and wins with 17 points!")
            return True
        if self.bot_score == 16 and self.player_score == 0:
            self.print_final_scores("Bot has shot the moon and wins with 17 points!")
            return True
        
        # If a player is guaranteed to win
        if self.player_score >= 9 and self.bot_score >= 1:
            self.print_final_scores("Player is guaranteed to win. Ending game early.")
            return True
        if self.bot_score >= 9 and self.player_score >= 1:
            self.print_final_scores("Bot is guaranteed to win. Ending game early.")
            return True
        
        return False # Continues game if moon or guaranteed win criteria has not been met
         
    def print_final_scores(self, message=None):   
        if message:
            print(f"\n{message}")
        print("\n--- Final Scores ---")
        print("Player:", self.player_score)
        print("Bot:", self.bot_score)

        if self.player_score > self.bot_score:
            print("Player wins the game!")
        elif self.bot_score > self.player_score:
            print("Bot wins the game!")
        else:
            print("The game is a tie!")
    
    def generate_graphs(self):
        # Generates and display graphs based on the game log.
        if self.game_log.empty:
            print("No game data to visualize!")
            return

        # Rounds Won vs. Lost
        rounds_won = len(self.game_log[self.game_log['Winner'] == 'Player 1'])
        rounds_lost = len(self.game_log[self.game_log['Winner'] == 'Player 2'])
        rounds_data = [rounds_won, rounds_lost]
        rounds_labels = ['Rounds Won', 'Rounds Lost']

        # Pie Chart
        plt.figure(figsize=(6, 6))
        plt.pie(rounds_data, labels=rounds_labels, autopct='%1.1f%%', startangle=90)
        plt.title("Rounds Won vs. Lost")
        plt.show()

        # Filter numeric rounds for graph
        self.game_log['Round'] = pd.to_numeric(self.game_log['Round'], errors='coerce')
        graph_data = self.game_log.dropna(subset=['Round'])  # Drop rows with NaN in 'Round'

        # Probability of Winning Per Round
        graph_data['Winning Probability (%)'] = graph_data.apply(
            lambda row: self.calculate_probability(row['Player Card'], row['Bot Hand']), axis=1
        )

        plt.figure(figsize=(10, 6))
        sns.lineplot(data=graph_data, x='Round', y='Winning Probability (%)', marker='o')
        plt.title("Winning Probability Per Round")
        plt.xlabel("Round")
        plt.ylabel("Winning Probability (%)")
        plt.xticks(range(1, len(graph_data) + 1))
        plt.show()

    def calculate_probability(self, player_card, bot_hand):
        # Calculates the probability of winning for the player's card.
        try:
            if isinstance(bot_hand, str):
                bot_hand = eval(bot_hand)  # Parse the list from string
            if isinstance(player_card, str):
                player_card = eval(player_card)  # Parse the tuple from string
        except (SyntaxError, NameError, ValueError) as e:
            print(f"Error parsing card data: {e}, Player Card: {player_card}, Bot Hand: {bot_hand}")
            return 0  # Default to 0 probability on parsing error

        if not isinstance(player_card, tuple) or not isinstance(bot_hand, list):
            print("Invalid data format for player_card or bot_hand.")
            return 0

        if not player_card or not bot_hand:
            return 0

        player_rank = player_card[0]
        player_suit = player_card[1]

        higher_cards = [card for card in bot_hand if card[0] > player_rank and card[1] == player_suit]

        probability = 1 - (len(higher_cards) / len(bot_hand)) if bot_hand else 0
        return round(probability * 100, 2)      

game = DecktionaryBattle()
game.play_game()