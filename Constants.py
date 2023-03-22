# Player types
MANUAL = 0
RANDOM = 1
ROBERT_M_STRUPP = 2
MAUER = 3

# Player roles
PICKER = 0
PARTNER = 1
GOOD_GUY = 2

# Printed Suits
CLUBS = 3
SPADES = 2
HEARTS = 1
DIAMONDS = 0

# Sheep Suits (includes printed suits besides DIAMONDS)
TRUMP = 0
DUMMY = 5 # To make logic easier for when picker plays alone

# Face Cards
JACK = 11
QUEEN = 12
KING = 13
ACE = 14

# Phases of Simulated Games
PICKING = 0
CALLING_ACE = 1
LEADING = 2
FOLLOWING = 3