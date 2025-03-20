''' test bidder and auction script '''

from auction_lastname import Auction, User
from bidder_lastname import Bidder


if __name__ == "__main__":
    NUM_USERS = 2

    NUM_ROUNDS = 10000
    NUM_BIDDER = 2

    users = [User() for _ in range(NUM_USERS)]
    bidders = [Bidder(NUM_USERS, NUM_ROUNDS) for i in range(NUM_BIDDER)]
    auction = Auction(users, bidders)
    print(users)

    for round_num in range(NUM_ROUNDS):
        print(auction)
        print(f'Round{round_num} = ')

        auction.execute_round()
