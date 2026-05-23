"""
setup_db.py
Run this ONCE to create and populate the movies database.
Command: python setup_db.py
"""

import sqlite3

conn = sqlite3.connect("movies.db")
cursor = conn.cursor()

# ── Create table ──────────────────────────────────────────────
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    title           TEXT NOT NULL,
    genres          TEXT NOT NULL,        -- comma-separated, e.g. "Sci-Fi,Thriller"
    release_year    INTEGER NOT NULL,
    runtime_minutes INTEGER NOT NULL,
    rating          REAL NOT NULL,        -- IMDb-style 0–10
    plot_summary    TEXT NOT NULL
)
""")

# Movie data
movies = [
    # (title, genres, year, runtime, rating, plot)
    ("The Matrix",          "Sci-Fi,Action,Thriller",       1999, 136, 8.7,
     "A hacker discovers reality is a simulation and joins a rebellion against the machines controlling humanity."),
    ("Inception",           "Sci-Fi,Thriller,Action",       2010, 148, 8.8,
     "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea."),
    ("Minority Report",     "Sci-Fi,Thriller,Action",       2002, 145, 7.7,
     "In a future where police stop crimes before they happen, a top cop is accused of a future murder he hasn't committed."),
    ("Interstellar",        "Sci-Fi,Drama,Adventure",       2014, 169, 8.6,
     "A team of explorers travels through a wormhole in space to ensure humanity's survival."),
    ("The Dark Knight",     "Action,Crime,Drama,Thriller",  2008, 152, 9.0,
     "Batman faces the Joker, a criminal mastermind who plunges Gotham City into anarchy."),
    ("Pulp Fiction",        "Crime,Drama,Thriller",         1994, 154, 8.9,
     "The lives of two mob hitmen, a boxer, a gangster, and his wife intertwine in four tales of violence."),
    ("Forrest Gump",        "Drama,Romance,Comedy",         1994, 142, 8.8,
     "The presidencies of Kennedy and Johnson through the lens of an Alabama man with an extraordinary life story."),
    ("The Shawshank Redemption", "Drama,Crime",             1994, 142, 9.3,
     "Two imprisoned men bond over years, finding solace and eventual redemption through acts of decency."),
    ("Goodfellas",          "Crime,Drama,Thriller",         1990, 146, 8.7,
     "The story of Henry Hill and his life in the mob, covering his ups and downs with the Italian-American crime syndicate."),
    ("Schindler's List",    "Drama,History,Biography",      1993, 195, 8.9,
     "In German-occupied Poland, Oskar Schindler saves the lives of more than a thousand Jewish refugees during the Holocaust."),
    ("Fight Club",          "Drama,Thriller",               1999, 139, 8.8,
     "An insomniac office worker and a soap salesman build a secret fight club that evolves into something much more sinister."),
    ("Gladiator",           "Action,Adventure,Drama",       2000, 155, 8.5,
     "A Roman general is betrayed and his family murdered by an emperor's corrupt son, so he becomes a gladiator for revenge."),
    ("The Silence of the Lambs", "Crime,Drama,Thriller",   1991, 118, 8.6,
     "A young FBI cadet must receive the help of an incarcerated cannibal killer to catch a serial killer at large."),
    ("Se7en",               "Crime,Drama,Mystery,Thriller", 1995, 127, 8.6,
     "Two detectives hunt a serial killer who uses the seven deadly sins as his motives."),
    ("The Prestige",        "Drama,Mystery,Sci-Fi,Thriller",2006, 130, 8.5,
     "Two magicians engage in a bitter rivalry that leads to obsession, betrayal, and shocking consequences."),
    ("Memento",             "Mystery,Thriller,Crime",       2000, 113, 8.4,
     "A man with short-term memory loss uses notes and tattoos to hunt his wife's murderer."),
    ("Parasite",            "Thriller,Drama,Comedy",        2019, 132, 8.5,
     "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the poor Kim clan."),
    ("Whiplash",            "Drama,Music",                  2014, 107, 8.5,
     "A promising young drummer enrolls at a cut-throat music conservatory where his dreams are both nurtured and crushed."),
    ("La La Land",          "Drama,Music,Romance",          2016, 128, 8.0,
     "A jazz pianist falls for an aspiring actress in Los Angeles as they struggle to reconcile their dreams with their relationship."),
    ("1917",                "Drama,History,War",            2019, 119, 8.3,
     "Two British soldiers are given an impossible mission to deliver a message across enemy territory during World War I."),
    ("Avengers: Endgame",   "Action,Adventure,Sci-Fi",      2019, 181, 8.4,
     "The Avengers assemble once more to undo Thanos's actions and restore order to the universe."),
    ("Mad Max: Fury Road",  "Action,Adventure,Sci-Fi",      2015, 120, 8.1,
     "In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler in search of her homeland."),
    ("The Grand Budapest Hotel","Comedy,Drama,Mystery",      2014, 100, 8.1,
     "A writer encounters a legendary concierge and the adventures they share spanning decades."),
    ("Spirited Away",       "Animation,Adventure,Fantasy",  2001, 125, 8.6,
     "A sullen 10-year-old girl wanders into a world ruled by gods, witches, and monsters, where humans are changed into beasts."),
    ("The Lion King",       "Animation,Adventure,Drama",    1994,  88, 8.5,
     "Lion cub Simba idolizes his father, but his uncle Scar plots to seize the throne by using Simba as his pawn."),
    ("Toy Story",           "Animation,Adventure,Comedy",   1995,  81, 8.3,
     "A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room."),
    ("Up",                  "Animation,Adventure,Comedy",   2009,  96, 8.2,
     "Seventy-eight-year-old Carl Fredricksen travels to Paradise Falls in his house equipped with balloons, meeting a young wilderness explorer."),
    ("WALL-E",              "Animation,Sci-Fi,Romance",     2008,  98, 8.4,
     "A robot that cleans a waste-covered Earth falls in love with another robot and follows her into outer space."),
    ("Get Out",             "Horror,Mystery,Thriller",      2017, 104, 7.7,
     "A Black man visits his white girlfriend's family estate only to discover a disturbing secret."),
    ("A Quiet Place",       "Drama,Horror,Sci-Fi",          2018,  90, 7.5,
     "A family struggles to survive in a post-apocalyptic world inhabited by blind monsters with an acute sense of hearing."),
    ("Hereditary",          "Drama,Horror,Mystery",         2018, 127, 7.3,
     "A grieving family is haunted by tragic and disturbing occurrences after the death of their secretive grandmother."),
    ("The Truman Show",     "Comedy,Drama,Sci-Fi",          1998, 103, 8.1,
     "An insurance salesman discovers his whole life is actually a reality TV show."),
    ("Eternal Sunshine of the Spotless Mind","Drama,Romance,Sci-Fi",2004,108,8.3,
     "When their relationship turns sour, a couple undergoes a medical procedure to have each other erased from their memories."),
    ("Blade Runner 2049",   "Action,Drama,Mystery,Sci-Fi",  2017, 164, 8.0,
     "Young Blade Runner K's discovery of a long-buried secret leads him to track down former Blade Runner Rick Deckard."),
    ("Ex Machina",          "Drama,Mystery,Sci-Fi,Thriller",2014, 108, 7.7,
     "A programmer is selected to evaluate an AI robot with a striking humanoid appearance."),
    ("The Social Network",  "Biography,Drama",              2010, 120, 7.8,
     "Harvard student Mark Zuckerberg creates the social networking site Facebook, but is later sued by two brothers who claimed he stole their idea."),
    ("Moneyball",           "Biography,Drama,Sport",        2011, 133, 7.6,
     "Oakland A's general manager Billy Beane attempts to assemble a baseball team on a lean budget using computer-generated analysis."),
    ("The Revenant",        "Action,Adventure,Drama",       2015, 156, 8.0,
     "A frontiersman on a fur trading expedition in the 1820s fights for survival after being mauled by a bear."),
    ("Dunkirk",             "Action,Drama,History,War",     2017, 106, 7.9,
     "Allied soldiers from Belgium, the British Commonwealth, and France are surrounded by the German Army on the beaches of Dunkirk."),
    ("Everything Everywhere All at Once","Action,Adventure,Comedy,Sci-Fi",2022,139,7.8,
     "A middle-aged Chinese-American laundromat owner must connect with parallel universe versions of herself to stop a powerful being."),
    ("Dune",                "Action,Adventure,Drama,Sci-Fi",2021, 155, 8.0,
     "A noble family becomes embroiled in a war for control over a desert planet's spice supply."),
    ("No Country for Old Men","Crime,Drama,Thriller",       2007, 122, 8.1,
     "Violence and mayhem ensue after a hunter stumbles upon a drug deal gone wrong and more than two million dollars in cash near the Rio Grande."),
    ("Joker",               "Crime,Drama,Thriller",         2019, 122, 8.4,
     "In Gotham City, mentally troubled comedian Arthur Fleck is disregarded and mistreated by society, causing him to descend into madness."),
]

cursor.executemany("""
    INSERT INTO movies (title, genres, release_year, runtime_minutes, rating, plot_summary)
    VALUES (?, ?, ?, ?, ?, ?)
""", movies)

conn.commit()
conn.close()
print(f"✅ Database created with {len(movies)} movies!")
