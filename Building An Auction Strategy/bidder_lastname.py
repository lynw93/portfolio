'''This file contains bidder class'''
import random


class Bidder:
    '''Class to represent a bidder in an online second-price ad auction'''
    def __init__(self, num_users, num_rounds):
        '''Setting number of users, number of rounds, and round counter'''
        self.num_users = num_users
        self.tol_rounds = num_rounds
        self.round_cnt = 0
        self.balance = 0
        self._curr_user_id = None
        self._bidding_strategies = [BiddingStrategy() for _ in range(num_users)]

    def __repr__(self):
        '''Return Bidder object'''
        return f"Bidder with {self.balance} balance left after {self.round_cnt} round"

    def __str__(self):
        '''Return Bidder object'''
        return f"Bidder with {self.balance} balance left after {self.round_cnt} round"

    def bid(self, user_id):
        '''Returns a non-negative bid amount'''
        self.round_cnt += 1
        bid_price = self._bidding_strategies[user_id].generating_bid(
            1.0 * self.round_cnt / self.tol_rounds
        )
        self._curr_user_id = user_id
        return round(bid_price, 3)

    def notify(self, auction_winner, price, clicked = None):
        '''Updates bidder attributes based on results from an auction round'''
        if auction_winner:
            self.balance += (1 if clicked else 0) - price
        self._bidding_strategies[self._curr_user_id].update(price, clicked)


class BiddingStrategy:
    '''
    Given user history
        * Find the minimum bidding price to win compared
            to other bidders (use historical winner price)
        * Find the maximum bidding prices to reflect user-click
            probability (use historical clicked results to predict click prob)
    '''

    def __init__(self):
        self.predicted_max_bid = 0.5
        self.num_win = 0
        self.num_clicked = 0

    def update(self, winning_price, clicked):
        '''update knowledge about given user'''
        winning_price = float(winning_price)
        self.predicted_max_bid = min(winning_price, 1.0)
        if clicked is not None:  # Only needs to update the probablity of user click
            self.num_win += 1
            self.num_clicked += clicked

    def generating_bid(self, round_factor):
        '''customize bidding strategy based on given knowledge'''
        # Choose a bidding value within this range and add some randomness given those factors
        upper_limit = 1.0 if self.num_clicked == 0 else 1.0 * self.num_clicked / self.num_win
        if self.predicted_max_bid >= upper_limit:
            return upper_limit
        offset = random.uniform(0, upper_limit - self.predicted_max_bid)
        # Shift toward upper limit when reaching the end of bidding since we have higher confidence
        offset *= round_factor
        return min(self.predicted_max_bid + offset, 1.0)
