'''This file contains User class and Auction class.'''
import random


class User:
    '''Class to represent a user with a secret probability of clicking an ad.'''

    def __init__(self):
        '''Generating a probability between 0 and 1 from a uniform distribution'''
        self.__probability = random.uniform(0,1)

    def __repr__(self):
        '''User object with secret probability'''
        # return str(self._probability)
        return f"User({self.__probability:.2f})"

    def __str__(self):
        '''User object with a secret likelihood of clicking on an ad'''
        return f"User has {self.__probability:.2f} chance of clicking on an ad"

    def show_ad(self):
        '''Returns True to represent the user clicking on an ad or False otherwise'''
        return self.__probability > random.uniform(0,1)


class Auction:
    '''Class to represent an online second-price ad auction'''

    def __init__(self, users, bidders):
        '''Initializing users, bidders, and dictionary 
        to store balances for each bidder in the auction'''
        if len(users) == 0:
            raise ValueError("At least 1 user is needed")
        if len(bidders) == 0:
            raise ValueError("At least 1 bidder is needed")
        self.users = users
        self.qualified_bidders = bidders
        self.balances = {bidder: 0 for bidder in self.qualified_bidders}

    def __repr__(self):
        '''Return auction object with users and qualified bidders'''
        return f"""There are {len(self.users)} users and {len(self.qualified_bidders)}
        qualified bidders"""

    def __str__(self):
        '''Return auction object with users and qualified bidders'''
        return f"""There are {len(self.users)} users and {len(self.qualified_bidders)}
        qualified bidders"""

    def _find_winner(self, bids):
        '''Search for the winning bidder, ie who has the highest bid,
            - returns the winnder's index,
            - returns winning price (2nd highest bid) '''
        if len(bids) == 1:
            return bids[0]
        sorted_bids = sorted(bids)
        highest_bids = sorted_bids[-1][0]
        winner_price = sorted_bids[-2][0]
        winner_idx_list = [idx for price, idx in sorted_bids if price == highest_bids]
        winner_idx = winner_idx_list[random.randint(0, len(winner_idx_list)-1)]
        return winner_price, winner_idx

    def execute_round(self):
        '''Executes a single round of an auction, completing the following steps:
            - random user selection
            - bids from every qualified bidder in the auction
            - selection of winning bidder based on maximum bid
            - selection of actual price (second-highest bid)
            - showing ad to user and finding out whether or not they click
            - notifying winning bidder of price and user outcome and updating balance
            - notifying losing bidders of price'''

        user_id = random.randint(0, len(self.users)-1)

        bids = []
        for idx, bidder in enumerate(self.qualified_bidders):
            # Get bids from qualified bidders
            bid = bidder.bid(user_id)
            if bid >= 0:
                bids.append((bid, idx)) # Only append (bid, index) when bid is valid

        winner_price, winner_idx = self._find_winner(bids)

        # Check if user has clicked
        click_result = self.users[user_id].show_ad()

        # Notify qualified bidders
        for idx, bidder in enumerate(self.qualified_bidders):
            if idx == winner_idx: # if idx bidder won
                bidder.notify(True, winner_price, click_result)
                self.balances[bidder] += click_result - winner_price  # Update balances for winner
                if self.balances[bidder] < -1000:
                    self.qualified_bidders.pop(idx)
            else: #if idx bidder lost
                bidder.notify(False, winner_price, None)
