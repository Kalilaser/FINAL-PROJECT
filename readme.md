# Decktionary Battle

## A Python impementation of a simple 2-player card game.

* This game uses a standard deck of playing cards, with the Kings removed
    – This results in a deck with 48 cards.
* The game starts with the deck face down (shuffled), and eight cards are dealt to each player.
* The players keep their cards “in hand” (meaning they can see them), and private (meaning the
other player can’t see them).
* One player starts by playing a card. This is called “leading”.
* Whatever suit (hearts, diamonds, clubs, or spades) the player leads with, the other player must
follow, if possible.
* If the second player cannot play a card in the same suit, they can play any card they wish.
* The highest-value card that is in the “lead” suit wins that round, and that player earns a point.
* The player who wins the point gets to lead in the next round.
* After every round, one of the cards in the deck is removed and shown to both players. This has
no effect on scoring or points, other than giving players information about what cards the other
player might have.
* After the players have played all eight of their cards, they are each dealt eight more cards.
* Ending the game:
    * If the game ends 16-0, the player with zero points has “shot the moon”, and immediately scores 17 points, making them the winner.
    * The player with the most points at the end of the game wins.
    * If one player has 9 or more points in the middle of the game, and the other player has at least 1 point, the game can be ended early instead of playing through the entire deck, since there is no way the other player can still win.

Below is the updated section for the readme.md file, formatted to include information about the advanced features, bot difficulty selection, and the logic behind the easy and expert bot levels. You can copy and paste this directly into your existing readme.

# Advanced Features Added
* This implementation of Decktionary Battle includes several advanced features to enhance gameplay and analysis:

## Bot Difficulty Selection:

### Players can choose between two levels of bot difficulty:
* Easy: The bot plays randomly, selecting any card from its hand.
* Expert: The bot strategically selects cards based on the game's lead suit. It prioritizes playing the highest-value card in the lead suit or, if it cannot follow the suit, the lowest-value card from its hand.

## Game Logging:

### The game records all actions and outcomes to a .csv file (game_log.csv), which includes:
* Timestamps for every round.
* Detailed information about cards played, winner of the round, and scores.
* Bot decision-making time for each turn.

## Graphical Analysis:
* At the end of the game, two graphs are generated:
    * Pie Chart: Displays the percentage of rounds won vs. rounds lost by the player.
    * Line Graph: Shows the probability of the player winning each round based on the cards played and remaining bot cards.
* Winning Probability Calculation:
    * A feature calculates the likelihood of the player's card winning against the bot's hand during each round. This is based on the lead suit and the remaining cards in the bot's hand.
## Bot Decision Timing:
* Measures and logs the time taken for the bot to make its decision, giving insight into computational efficiency for each difficulty level.
