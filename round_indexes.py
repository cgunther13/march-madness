# Mapping for strings describing each round to an integer (for indexing)
round_dictionary = {
    0 : 'FIRST FOUR',
    1 : 'ROUND OF 64',
    2 : 'ROUND OF 32',
    3 : 'ROUND OF 16',
    4 : 'ELITE 8',
    5 : 'FINAL 4',
    6 : 'FINALS',
}

seed_pairs_by_round = {
    1 : {
        1:16, 16:1,
        8:9, 9:8,
        5:12, 12:5,
        4:13, 13:4,
        6:11, 11:6,
        3:14, 14:3,
        7:10, 10:7,
        2:15, 15:2,
    },
    2 : {
        1:8, 8:1,
        4:5, 5:4,
        3:6, 6:3,
        2:7, 7:2,
    },
    3 : {
        1:4, 4:1,
        2:3, 3:2,
    },
    4 : {
        1:2, 2:1,
    },
}
