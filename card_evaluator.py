import time
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
RANK_VALUES = {r: i+2 for i, r in enumerate(RANKS)}
HAND_NAMES = [
    "High Card", "One Pair", "Two Pair", "Three of a Kind",
    "Straight", "Flush", "Full House", "Four of a Kind",
    "Straight Flush", "Royal Flush"
]

def get_combinations(lst, k):
    if k == 0:
        return [[]]
    if len(lst) < k:
        return []
    return get_combinations(lst[1:], k) + [[lst[0]] + x for x in get_combinations(lst[1:], k-1)]

def count(items):
    d = {}
    for i in items:
        d[i] = d.get(i, 0) + 1
    return d

def parse_card(card):
    suit = card[0]
    rank = card[1:]
    if rank == '14':
        rank = 'A'
    return rank, suit

def is_straight(values):
    vals = sorted(set(values))
    for i in range(len(vals) - 4):
        if vals[i+4] - vals[i] == 4:
            return True, vals[i+4]
    if set([14, 2, 3, 4, 5]).issubset(vals):
        return True, 5
    return False, 0

def evaluate_hand(cards):
    ranks = []
    suits = []
    for c in cards:
        r, s = parse_card(c)
        ranks.append(r)
        suits.append(s)

    values = [RANK_VALUES[r] for r in ranks]
    val_count = count(values)
    suit_count = count(suits)
    is_flush = any(suit_count[s] >= 5 for s in suit_count)
    is_str, high_str = is_straight(values)

    if is_flush and is_str:
        if high_str == 14:
            return (9, [14])
        return (8, [high_str])

    for v in val_count:
        if val_count[v] == 4:
            kicker = max([x for x in values if x != v])
            return (7, [v, kicker])

    trips = [v for v in val_count if val_count[v] == 3]
    pairs = [v for v in val_count if val_count[v] == 2]

    if trips and pairs:
        return (6, [max(trips), max(pairs)])
    if len(trips) >= 2:
        t = sorted(trips, reverse=True)
        return (6, [t[0], t[1]])

    if is_flush:
        return (5, sorted(values, reverse=True)[:5])
    if is_str:
        return (4, [high_str])
    if trips:
        kick = sorted([v for v in values if v != trips[0]], reverse=True)[:2]
        return (3, [trips[0]] + kick)
    if len(pairs) >= 2:
        p = sorted(pairs, reverse=True)
        kicker = max([v for v in values if v not in p])
        return (2, [p[0], p[1], kicker])
    if pairs:
        kick = sorted([v for v in values if v != pairs[0]], reverse=True)[:3]
        return (1, [pairs[0]] + kick)
    return (0, sorted(values, reverse=True)[:5])


def normalize_card(card):
    suit_map = {'♠': 'S', '♥': 'H', '♦': 'D', '♣': 'C'}
    rank = card[:-1]
    suit = card[-1]
    return suit_map[suit] + rank

def convert_players(players):
    converted_players = []
    for hand in players:
        card1 = normalize_card(hand[0])
        card2 = normalize_card(hand[1])
        player_id = hand[2]  # or just use an index if you prefer
        converted_players.append([card1, card2, player_id])
    return converted_players

def find_winner(win_cards, center):
    pre_community = []
    for card in center:
        pre_community.append(str(card[1].split("]")[1].split("[")[0].strip())+str(card[3].split("]")[1].split("[")[0].strip()))

    pre_players = []
    for player in win_cards:
        player_bucket = []
        for card in player[0]:
            player_bucket.append(str(card[1].split("]")[1].split("[")[0].strip())+str(card[3].split("]")[1].split("[")[0].strip()))
        player_bucket.append(player[1])
        pre_players.append(player_bucket)

    community = [normalize_card(c) for c in pre_community]
    players = convert_players(pre_players)
    results = []
    for p in players:
        cards = p[:2] + community
        best = (0, [])
        for combo in get_combinations(cards, 5):
            score = evaluate_hand(combo)
            if score > best:
                best = score
        results.append((best, p[2], cards))

    best_score = max(r[0] for r in results)
    winners = [r for r in results if r[0] == best_score]

    return [[w[1],HAND_NAMES[w[0][0]],w[0][1]] for w in winners]


