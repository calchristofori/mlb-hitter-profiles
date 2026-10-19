# =====================================================================================
# data.py — ANNOTATED COPY FOR READING (no Python experience needed)
# =====================================================================================
# This is a copy of ~/mlb_analyst/data.py with explanations added. The code is the
# same as the real file (as of 2026-10-18); only the comments are new. Edit the real
# data.py, not this one: this copy is for learning and does not update itself.
#
# How to use it: read PART A (the Python crash course) once, then scroll through the
# code. Every time a new piece of Python appears for the first time, a comment marked
# "PYTHON:" explains it right there. Comments marked "WHAT IT DOES:" explain the
# baseball / data logic.
#
# =====================================================================================
# PART A — PYTHON CRASH COURSE (everything this file uses, with examples from it)
# =====================================================================================
#
# 1. COMMENTS AND DOCSTRINGS
#    # anything after a hash sign is a comment. Python skips it entirely.
#    """Text in triple quotes""" right under a function is a "docstring", a built-in
#    description of the function. Python stores it but does not run it.
#
# 2. VARIABLES: giving a value a name
#    min_pa = 502
#    The = sign means "store the value on the right under the name on the left".
#    It is NOT "equals" in the math sense. To COMPARE two values, Python uses ==.
#    Names are lowercase_with_underscores by habit. ALL_CAPS names (like CONNINFO)
#    are, by habit, settings that never change while the program runs.
#
# 3. TYPES OF VALUES (Python calls them "types")
#    502                 an integer (whole number)
#    0.383               a float (decimal number)
#    "xwoba" or 'xwoba'  a string (text). Single or double quotes both work.
#    True / False        booleans (yes/no values)
#    None                "no value" — Python's word for a missing number
#
# 4. STRINGS (text) — things you can do with them
#    "Season " + "2026"            -> "Season 2026"      (+ glues text together)
#    "\n"                          -> a line break        (backslash-n = new line)
#    f"{rank} of {total}"          -> "34 of 135"         (an f-string: the f before
#                                                          the quote lets you drop values
#                                                          into text inside {braces})
#    f"{0.38349:.3f}"              -> "0.383"             (after a colon inside {}, a
#                                                          "format spec": .3f = 3 decimals)
#    f"{1.4:+.1f}"                 -> "+1.4"              (+ means always show the sign)
#    "0.383"[1:]                   -> ".383"              ([1:] = from the 2nd character on)
#    "0.383".startswith("0")       -> True
#    "-0.007".replace("-0.", "-.") -> "-.007"
#    "Pete Crow".lower()           -> "pete crow"
#    "  hi  ".strip()              -> "hi"                (trims spaces at the ends)
#    "crow armstrong".split()      -> ["crow", "armstrong"]  (splits into words)
#    " | ".join(["A", "B", "C"])   -> "A | B | C"         (joins a list with a separator)
#    The things after a dot (.lower(), .split()) are "methods": functions that belong
#    to a value. You'll see them on strings, lists and dictionaries.
#
# 5. LISTS: ordered collections, written with [square brackets]
#    groups = ["fastball", "breaking", "offspeed"]
#    groups[0]      -> "fastball"     (positions start at 0, not 1)
#    groups[-1]     -> "offspeed"     (negative = count from the end)
#    groups[1:]     -> ["breaking", "offspeed"]   (a "slice": from position 1 on)
#    groups[-3:]    -> the last three items
#    len(groups)    -> 3              (len = length, how many items)
#    groups.append("other")           (adds an item to the end)
#    "breaking" in groups -> True     (is it in the list?)
#
# 6. TUPLES: like lists, but fixed once made, written with (parentheses)
#    ("EV90", "ev90", "higher")       a bundle of three related things
#    A one-item tuple needs a trailing comma: (player_id,)
#
# 7. DICTIONARIES: look things up by name, written with {key: value}
#    QUALIFIED_PA = {2020: 186}
#    QUALIFIED_PA[2020]               -> 186
#    QUALIFIED_PA.get(2026, 502)      -> 502   (.get(key, default): use the default if
#                                               the key isn't there, instead of crashing)
#    Every database row in this file is a dictionary: row["xwoba"] -> 0.383
#
# 8. SETS: a collection with no duplicates, written with {curly braces} but no colons
#    {"pete crowarmstrong", "peter crowarmstrong"}
#
# 9. COMPARISONS AND LOGIC (each gives True or False)
#    ==  equal         !=  not equal       >  >=  <  <=   bigger / smaller
#    x is None         "is x missing?" (the right way to check for None)
#    a and b           True only if both are True
#    a or b            True if either is True
#    not a             flips True/False
#    Python treats True as 1 and False as 0 when you add them up: sum([True, True, False]) = 2
#
# 10. IF / ELIF / ELSE: making decisions
#     if x is None:
#         return "—"          <- runs only when the condition is True
#     elif ...:                <- "else if": checked only if the first was False
#     else:                    <- runs when nothing above was True
#     INDENTATION MATTERS: the indented lines under "if" belong to it. Python uses
#     indentation (4 spaces) instead of brackets to show what belongs together.
#
#     One-line version (a "conditional expression"):
#     "—" if x is None else pct(x)     -> "if x is missing use a dash, otherwise format it"
#
# 11. LOOPS: doing something once per item
#     for r in rows:
#         print(r["season"])   <- runs once for each row; r is each row in turn
#     "continue" inside a loop = skip to the next item.
#
#     Unpacking in a loop — when each item is a tuple, you can name its parts:
#     for label, col, better in CONTEXT_METRICS:
#         ...  label = "EV90", col = "ev90", better = "higher" (on that turn)
#
# 12. LIST COMPREHENSIONS: a loop that builds a list, in one line
#     [r["pa"] for r in rows]                       -> a list of every row's PA
#     [r for r in rows if r["split"] == "all"]      -> only the rows where split is "all"
#     Read it as English: "r['pa'], for each r in rows".
#     Without the [brackets] (inside sum(), any(), all(), join()) it's the same idea,
#     just not stored as a list ("generator expression").
#
# 13. FUNCTIONS: named recipes
#     def pct(x):                        <- "def" defines a function named pct with
#         return f"{x * 100:.1f}%"           one input, x. Nothing runs yet.
#     pct(0.263)                         -> "26.3%"  (calling it: now it runs)
#     "return" hands a value back to whoever called the function and ends the function.
#     A function can return two things at once: return rows, min_pa
#     and the caller can catch both: league, min_pa = fetch_league(cur, 2026)
#
# 14. BUILT-IN FUNCTIONS used in this file (they come with Python)
#     len(x)      how many items          sum(x)    add them up
#     min(x)      smallest                abs(x)    drop the minus sign: abs(-0.007) = 0.007
#     round(x)    nearest whole number    str(x)    turn into text: str(34) = "34"
#     sorted(x, key=...)   sort, using "key" to say what to sort by
#     zip(a, b)   pair items up: zip([1,2], ["a","b"]) -> (1,"a"), (2,"b")
#     next(x, default)     the first item from x, or the default if there are none
#     any(x)      True if at least one is True     all(x)  True only if every one is True
#     print(x)    show x in the terminal
#
# 15. LAMBDA: a tiny unnamed function, written in one line
#     lambda r: r["season"]     means "given r, return r['season']"
#     Used with sorted() to say "sort by season".
#
# 16. IMPORTS: loading toolboxes
#     import re                      -> use its tools as re.something
#     from psycopg.rows import dict_row  -> bring in just one tool, by name
#
# 17. WITH: open something and close it automatically when done
#     with psycopg.connect(...) as conn:
#         ...                        <- connection is open in here
#     ...                            <- closed automatically here, even after an error
#
# 18. ERRORS: raise and try/except
#     raise ValueError("No MLB hitter matches 'X'.")   stops the program with a message
#     try:
#         ...risky thing...
#     except ValueError as e:                          if that error happens, do this instead
#         ...                                          (e holds the error message)
#
# 19. SQL INSIDE PYTHON (the database's own language)
#     cur.execute("SELECT * FROM main.batter_season WHERE batter_id = %s", (player_id,))
#     The text in quotes is SQL, sent to the database. %s is a blank that psycopg fills
#     in with the value after the comma (safely). SQL words:
#       SELECT columns   which columns to return (* = all)
#       FROM table       which table
#       WHERE condition  only rows where this is true
#       JOIN ... ON ...  link two tables on a shared column (like player ID)
#       ORDER BY col     sort (DESC = newest/biggest first)
#       LIMIT 1          only the first row
#       GROUP BY         combine rows into one per group (for max(), count() etc.)
#     cur.fetchall() collects every row of the answer; cur.fetchone() just the first.
#
# WHAT THIS FILE DOES (big picture)
#   name in  ->  find the player  ->  ask the database for his stats and the league's
#            ->  calculate averages, ranks, percentiles, changes  ->  format as text
#            ->  data packet out (one block of text the AI reads)
#   No AI runs here. Same name in, same packet out, every time.
#
# =====================================================================================
# PART B — THE CODE, ANNOTATED
# =====================================================================================

"""Step 1 of the hitter report workflow: build the data packet.

    python data.py "Pete Crow-Armstrong"

Everything here is deterministic: no AI. Given a player name, it pulls every number
the hitter report needs from the `mlb` database and returns it as one block of text
(the "data packet") that later goes to the model.

Design rules (agreed 2026-10-18):
- Code computes, the model judges. Code does all arithmetic (gaps, swing-decision
  score, league averages, ranks). Code does NOT apply the evaluation method
  (sample-size labels, "gap >= .030", thresholds) — that is the model's job, and
  what the evals will test.
- Numbers are formatted baseball-style here (.383, 26.3%), so the model can copy
  them exactly and the grader can check every number against the packet.
"""
# PYTHON: a triple-quoted string at the very top of a file is the file's docstring:
#         its description. It doesn't do anything when the program runs.


# -------------------------------------------------------------------------------------
# IMPORTS
# -------------------------------------------------------------------------------------
# PYTHON: "import name" loads a toolbox (a "module"). After this, its tools are used as
#         name.tool — for example re.sub(...) or sys.exit(...).

import os              # operating system tools; used to read a setting (CONNINFO below)
import re              # "regular expressions": text pattern matching; used to clean names
import sys             # terminal tools: what you typed after "python data.py", and exiting
import unicodedata     # handles accented letters, so "Acuña" can match "Acuna"
# ^ These four come built into Python.

import psycopg                        # an add-on (installed in .venv) for talking to Postgres
from psycopg.rows import dict_row     # PYTHON: "from X import Y" brings in one tool, Y,
                                      # by name. dict_row makes each database row a
                                      # dictionary, so we can write row["xwoba"].


# -------------------------------------------------------------------------------------
# SETTINGS
# -------------------------------------------------------------------------------------

CONNINFO = os.environ.get("MLB_ANALYST_CONN", "host=localhost port=5432 dbname=mlb user=mlb_analyst")
# PYTHON: a variable (name = value). The value comes from calling a function:
#         os.environ is a dictionary of the computer's settings; .get("NAME", default)
#         looks one up and falls back to the default if it isn't there.
# WHAT IT DOES: the database "address" — this computer (localhost), Postgres's usual
#         door (port 5432), the database named mlb, logging in as the read-only user
#         mlb_analyst. No setting called MLB_ANALYST_CONN exists, so the default is used.

# Qualified hitter = 3.1 PA per team game (502 PA in a 162-game season; 2020 had 60 games).
QUALIFIED_PA = {2020: 186}
# PYTHON: a dictionary with one entry: the key 2020 maps to the value 186.
DEFAULT_QUALIFIED_PA = 502
# PYTHON: an integer.
# WHAT IT DOES: together, these say "502 PA to qualify, except 186 in 2020". Used later
#         as QUALIFIED_PA.get(season, DEFAULT_QUALIFIED_PA).

# Metrics shown in the league-context table: (label, column, which direction is better).
# "higher"/"lower" get a rank; None means there is no better direction (e.g. GB% is a
# style, not a skill), so only the league average is shown.
CONTEXT_METRICS = [
    # PYTHON: a list (the [ ... ] spread over many lines). Each item is a tuple of three
    #         strings (or two strings and None). Commas separate the items; the comma
    #         after the last item is allowed and harmless.
    # WHAT IT DOES: each tuple = (label printed in the packet, column name in the
    #         database, which direction is better).
    ("xwOBA (house)", "xwoba", "higher"),
    ("wOBA", "woba", "higher"),
    ("xSLG", "xslg", "higher"),
    ("xBA", "xba", "higher"),
    ("EV90", "ev90", "higher"),
    ("Avg EV", "avg_ev", "higher"),
    ("Hard-hit%", "hard_hit_pct", "higher"),
    ("Barrel%", "barrel_pct", "higher"),
    ("Sweet spot% (8-32°)", "sweet_spot_pct", "higher"),
    ("Pulled Air%", "pulled_fb_pct", "higher"),     # label is new; the column keeps its old name
    ("IZ Swing - Chase", "swing_score", "higher"),  # swing_score isn't stored in the database;
                                                    # add_derived() calculates it below
    ("IZ Swing%", "z_swing_pct", None),             # None (no value) = no "better" direction
    ("Chase%", "chase_pct", "lower"),               # lower is better
    ("Whiff%", "whiff_pct", "lower"),
    ("K%", "k_pct", "lower"),
    ("BB%", "bb_pct", "higher"),
    ("LA median", "median_la", None),               # a style: where he lives, not a skill
    ("LA SD", "sd_la", "lower"),                    # lower = more consistent launch
    ("GB%", "gb_pct", None),
    ("FB%", "fb_pct", None),
    ("Pull%", "pull_pct", None),
    ("Sprint speed", "sprint_speed", "higher"),
]
# WHAT IT DOES: to add a metric to the league table, add one line here. Nothing else changes.

# Same idea for the by-pitch-group league context.
PITCH_GROUP_METRICS = [
    ("Pitch share", "pitch_share", None),
    ("xwOBA (house)", "xwoba", "higher"),
    ("wOBA", "woba", "higher"),
    ("IZ Swing%", "z_swing_pct", None),
    ("Chase%", "chase_pct", "lower"),
    ("IZ Swing - Chase", "swing_score", "higher"),
    ("Whiff%", "whiff_pct", "lower"),
    ("K%", "k_pct", "lower"),
    ("EV90", "ev90", "higher"),
    ("Hard-hit%", "hard_hit_pct", "higher"),
    ("Barrel%", "barrel_pct", "higher"),
]
PITCH_GROUPS = ["fastball", "breaking", "offspeed"]
# PYTHON: a plain list of three strings, written on one line.
# WHAT IT DOES: the order the groups are displayed in.

# Season-over-season changes, computed here so the model never has to subtract.
CHANGE_METRICS = [
    # PYTHON: a list of two-item tuples, several per line. Line breaks inside [ ] are fine.
    # WHAT IT DOES: (label, column) only — a change needs no "better direction".
    ("xwOBA (house)", "xwoba"), ("wOBA", "woba"), ("BABIP", "babip"), ("EV90", "ev90"),
    ("Hard-hit%", "hard_hit_pct"), ("Barrel%", "barrel_pct"), ("Sweet spot%", "sweet_spot_pct"),
    ("Pulled Air%", "pulled_fb_pct"), ("Pull%", "pull_pct"), ("LA median", "median_la"), ("LA SD", "sd_la"),
    ("IZ Swing - Chase", "swing_score"), ("IZ Swing%", "z_swing_pct"), ("Chase%", "chase_pct"),
    ("Whiff%", "whiff_pct"), ("K%", "k_pct"), ("BB%", "bb_pct"), ("Sprint speed", "sprint_speed"),
]


# ---------------------------------------------------------------- formatting
# =====================================================================================
# FORMATTING: turning raw numbers into baseball notation
# =====================================================================================
# WHAT IT DOES: the database stores 0.383 and 0.263. Baseball people read .383 and
# 26.3%. These small functions translate. Each also turns a missing value (None)
# into "—" so the packet never shows the word "None".

def rate(x):          # .383  (wOBA, xwOBA, AVG, BABIP...)
    # PYTHON: "def rate(x):" defines a function called rate that takes one input,
    #         called x inside the function. The colon starts the function's body: every
    #         indented line below, until the indentation ends.
    if x is None:                 # PYTHON: "is None" asks "is x missing?"
        return "—"                # PYTHON: return hands back "—" and ends the function here
    s = f"{x:.3f}"                # PYTHON: f-string with a format spec — 3 decimals.
                                  #         0.383 -> "0.383"; 1.0234 -> "1.023"
    return s[1:] if s.startswith("0") else s.replace("-0.", "-.")
    # PYTHON: a one-line if/else (A if condition else B), plus three string tools:
    #         s.startswith("0")       True if the text begins with "0"
    #         s[1:]                   the text minus its first character
    #         s.replace("-0.", "-.")  swaps every "-0." for "-."
    # WHAT IT DOES: "0.383" -> ".383" (baseball style drops the leading zero).
    #         Negatives: "-0.007" doesn't start with "0", so it gets the replace instead
    #         and becomes "-.007". A value of 1 or more ("1.023") is left alone.


def signed_rate(x):   # +.023 / -.007  (gaps)
    return "—" if x is None else ("+" if x >= 0 else "-") + rate(abs(x))
    # PYTHON: two one-line if/elses, one inside the other, plus + gluing text together.
    #         Read it as: if x is missing -> "—"; otherwise -> ("+" if x is 0 or more,
    #         else "-") followed by rate() of x without its sign. abs(-0.007) = 0.007.
    # NOTE:   this function calls rate(), defined above. Functions can use each other.


def pct(x):           # 26.3%
    return "—" if x is None else f"{x * 100:.1f}%"
    # PYTHON: * is multiplication. Inside the f-string braces you can do math:
    #         {x * 100:.1f} = "multiply by 100, show 1 decimal". 0.263 -> "26.3%".


def one(x):           # 106.6  (mph, degrees, ft/s)
    return "—" if x is None else f"{x:.1f}"
    # One decimal, no % sign: 106.62 -> "106.6".


# How each column is displayed.
FORMAT = {
    # PYTHON: a dictionary spread over several lines. Keys are column names (strings);
    #         the values are the FUNCTIONS themselves (rate, one) — no parentheses, so
    #         they aren't run here, just stored, to be run later.
    "xwoba": rate, "woba": rate, "xslg": rate, "xba": rate, "avg": rate, "obp": rate,
    "slg": rate, "babip": rate, "iso": rate, "swing_score": rate,
    "ev90": one, "avg_ev": one, "median_la": one, "sd_la": one, "sprint_speed": one,
}
# WHAT IT DOES: any column NOT listed here is treated as a percentage (see fmt below).


def fmt(col, x):
    # PYTHON: a function with two inputs, separated by a comma.
    return FORMAT.get(col, pct)(x)
    # PYTHON: two steps in one line.
    #         FORMAT.get(col, pct) -> look up the column's formatter, or use pct if missing.
    #         (...)(x)             -> run whatever function came back, on x.
    # EXAMPLES: fmt("ev90", 106.6)     -> FORMAT gives one  -> one(106.6)   -> "106.6"
    #           fmt("chase_pct", 0.331) -> not listed, pct  -> pct(0.331)  -> "33.1%"


def change(col, new, old):
    """Difference between two seasons, in the column's display units (+.048, +4.4 pts, +1.4)."""
    # PYTHON: the triple-quoted line above is this function's docstring (its description).
    if new is None or old is None:     # PYTHON: "or" — True if either one is missing
        return "—"
    d = new - old                      # PYTHON: - is subtraction. d now holds the difference.
    if FORMAT.get(col) is rate:        # PYTHON: "is" here checks "is it the same function as rate?"
        return signed_rate(d)          #   a rate stat: show like +.048
    if FORMAT.get(col) is one:         #   mph / degrees / ft/s?
        return f"{d:+.1f}"             #   show like +1.4 (the + in the spec forces a sign)
    return f"{d * 100:+.1f} pts"       #   otherwise a percentage: +4.4 pts
    # PYTHON: because each "if" ends with "return", the function stops at the first match.
    #         The last line only runs if neither "if" matched — so no "else" is needed.
    # WHAT IT DOES: Chase% going from 41.8% to 33.1% shows as "-8.7 pts" (percentage
    #         POINTS), which is different from "-8.7 percent".


def table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    # PYTHON: a list of two strings — the first two lines of a markdown table.
    #         " | ".join(headers)  glues the header names with " | " between them:
    #                              ["Season", "PA"] -> "Season | PA" -> "| Season | PA |"
    #         "---|" * len(headers) repeats text: "---|" * 2 -> "---|---|"
    out += ["| " + " | ".join(str(v) for v in r) + " |" for r in rows]
    # PYTHON: += means "add to what's already there". The right side is a list
    #         comprehension — "for each row r in rows, build one line of text".
    #         Inside it, (str(v) for v in r) turns every value in the row into text,
    #         because join() can only glue text, not numbers.
    return "\n".join(out)
    # PYTHON: joins all the lines with "\n" (a line break) into one block of text.


# ---------------------------------------------------------------- database
# =====================================================================================
# DATABASE: finding the player and asking for stats
# =====================================================================================
# Most functions here take "cur" — a cursor. Think of it as an open phone line to the
# database: cur.execute("SQL question") asks; cur.fetchall() / cur.fetchone() collect
# the answer. (See PART A #19 for what the SQL words mean.)

def _norm(s):
    # PYTHON: a name starting with _ is a habit meaning "a helper, only used in this file".
    # WHAT IT DOES: "normalize" a name so different spellings compare as equal.
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    # PYTHON: "method chaining" — each .something() runs on the result of the one before,
    #         left to right:
    #         s or ""                -> if s is missing (None), use empty text instead.
    #                                   ("a or b" gives a if a has a value, else b.)
    #         normalize("NFKD", ...) -> splits accented letters: "ñ" -> "n" + accent mark
    #         .encode("ascii", "ignore").decode() -> keep only plain letters (drops accents)
    #         .lower()               -> lowercase
    return re.sub(r"[^a-z ]", "", s).strip()
    # PYTHON: re.sub(pattern, replacement, text) replaces every match of the pattern.
    #         r"[^a-z ]" means "any character that is NOT a lowercase letter or a space".
    #         (The r before the quote means "raw string": backslashes are kept as typed.)
    #         Replacing with "" deletes them. .strip() trims spaces at the ends.
    # EXAMPLES: "Pete Crow-Armstrong" -> "pete crowarmstrong"
    #           "Ronald Acuña Jr."    -> "ronald acuna jr"


def resolve_player(cur, name):
    """Turn a name into one player_id. Only players with MLB hitting seasons count.
    A workflow must not guess: if the name is ambiguous, stop and list the options."""
    cur.execute("""
        SELECT p.player_id, p.full_name, coalesce(p.use_name, p.first_name) AS use_name,
               p.last_name, max(b.season) AS last_season
        FROM main.players p JOIN main.batter_season b ON b.batter_id = p.player_id
        GROUP BY 1, 2, 3, 4""")
    # PYTHON: a triple-quoted string can span many lines — handy for long SQL.
    # WHAT IT DOES (the SQL in plain English): "For every player who appears in
    #         batter_season (at least one MLB hitting season), give me his ID, full name,
    #         the first name he goes by (use_name if he has one, else first_name — that's
    #         what coalesce does), last name, and his most recent season."
    #         "p" and "b" are short nicknames for the two tables. JOIN links them on the
    #         player ID. GROUP BY 1, 2, 3, 4 makes it one row per player.
    q = _norm(name)        # clean up the name you typed, the same way
    hits = []              # PYTHON: [] is an empty list. We'll add matches to it.
    for r in cur.fetchall():
        # PYTHON: a for loop. cur.fetchall() returns every row; r is each row in turn.
        names = {_norm(r["full_name"]), _norm(f"{r['use_name']} {r['last_name']}")}
        # PYTHON: a set (curly braces, no colons) of two cleaned names.
        #         Inside an f-string that uses double quotes, use single quotes for
        #         dictionary keys: r['use_name'].
        # WHAT IT DOES: his two possible names — full name, and goes-by + last name.
        if q in names:
            hits.append((0, r))                       # exact match
            # PYTHON: .append() adds one item to the list. The item is a tuple: (score, row).
            # WHAT IT DOES: what you typed equals one of his names. Score 0 = best.
        elif all(any(t in n for n in names) for t in q.split()):
            hits.append((1, r))                       # partial match
            # PYTHON: "elif" = else-if. Read the condition from the inside out:
            #         q.split()              -> the words you typed: ["crow", "armstrong"]
            #         t in n                 -> is word t found inside name n? (for text,
            #                                   "in" means "appears somewhere inside")
            #         any(... for n in names) -> True if the word is in EITHER of his names
            #         all(... for t in ...)   -> True only if that holds for EVERY word
            # WHAT IT DOES: every word you typed appears in his name. Score 1.
    if not hits:
        # PYTHON: "not hits" is True when the list is empty (an empty list counts as False).
        raise ValueError(f"No MLB hitter matches '{name}'.")
        # PYTHON: raise stops the program with an error and message (see PART A #18).
        #         The bottom of the file catches it and prints the message cleanly.
    best = min(h[0] for h in hits)
    # PYTHON: h[0] is the first part of each (score, row) tuple — the score.
    #         min(...) finds the smallest: 0 if there was any exact match, else 1.
    hits = [r for rank, r in hits if rank == best]
    # PYTHON: a list comprehension with unpacking and a filter. For each (rank, r) tuple,
    #         keep r only if its rank equals the best. This replaces the old hits list.
    # WHAT IT DOES: an exact match always beats partial matches.
    if len(hits) > 1:
        opts = "; ".join(f"{r['full_name']} (id {r['player_id']}, last season {r['last_season']})" for r in hits)
        # PYTHON: build one line per candidate, joined with "; ".
        raise ValueError(f"'{name}' matches more than one hitter: {opts}. Be more specific.")
        # WHAT IT DOES: the "19 Smiths" case — stop instead of guessing.
    return hits[0]
    # PYTHON: hits[0] = the first (and only) item. Lists count from 0.


def add_derived(rows):
    """The two computed numbers: swing-decision score and the wOBA - xwOBA gap."""
    for r in rows:
        r["swing_score"] = None if r["z_swing_pct"] is None or r["chase_pct"] is None else r["z_swing_pct"] - r["chase_pct"]
        # PYTHON: assigning to r["swing_score"] ADDS a new entry to the row dictionary.
        #         The right side is a one-line if/else: None if either input is missing,
        #         otherwise the subtraction.
        # WHAT IT DOES: IZ Swing - Chase. 0.691 - 0.331 = 0.360, shown later as ".360".
        r["gap"] = None if r["woba"] is None or r["xwoba"] is None else r["woba"] - r["xwoba"]
        # WHAT IT DOES: wOBA - xwOBA. .406 - .383 = +.023.
    return rows
    # PYTHON: the dictionaries were changed in place, then the same list is returned.
    # WHAT IT DOES: every fetch function below runs its results through this, so these
    #         two numbers exist on every row.


def fetch_seasons(cur, player_id):
    cur.execute("SELECT * FROM main.batter_season WHERE batter_id = %s ORDER BY season, split", (player_id,))
    # PYTHON: the second input, (player_id,), is a one-item tuple — the comma makes it a
    #         tuple. psycopg puts its value where %s is.
    # WHAT IT DOES: "every column (*) of every batter_season row for this player, sorted
    #         by season, then split" — each season has three rows: 'all' (full season),
    #         'vs_lhp' and 'vs_rhp'.
    return add_derived(cur.fetchall())
    # PYTHON: functions can be nested: fetchall() runs first, its result goes into
    #         add_derived(), and that result is returned.


def fetch_pitch_groups(cur, player_id, first_season):
    cur.execute("""SELECT * FROM main.batter_pitch_group_season
                   WHERE batter_id = %s AND season >= %s ORDER BY season""", (player_id, first_season))
    # PYTHON: two blanks (%s, %s), filled in order from the two-item tuple.
    # WHAT IT DOES: his fastball / breaking / offspeed rows from first_season on.
    #         get_hitter_data() passes latest season minus 2, so: the last three seasons.
    return add_derived(cur.fetchall())


def fetch_league_pitch_groups(cur, season, min_pa):
    """Pitch-group rows for every qualified hitter (qualified on full-season PA)."""
    cur.execute("""
        SELECT g.* FROM main.batter_pitch_group_season g
        JOIN main.batter_season b ON b.season = g.season AND b.batter_id = g.batter_id AND b.split = 'all'
        WHERE g.season = %s AND b.pa >= %s""", (season, min_pa))
    # WHAT IT DOES: pitch-group rows for everyone in this season, but only for hitters
    #         whose FULL season had at least min_pa (502) PA. The JOIN attaches each
    #         pitch-group row (nickname g) to that hitter's full-season row (nickname b)
    #         so the query can check his season PA. This is the comparison group behind
    #         "vs. fastballs, he ranks 53rd of 135".
    return add_derived(cur.fetchall())


def fetch_current_team(cur, player_id):
    """Latest 40-man roster row (players.current_team_name is often stale)."""
    cur.execute("""
        SELECT r.date, r."STATUS" AS status, t.team_full_name, t.venue_name
        FROM main.rosters_40man_daily r
        LEFT JOIN main.mlbteams t ON t.team_id = r."ORG" AND t.season = extract(year FROM r.date)::int
        WHERE r."MLBAMID" = %s ORDER BY r.date DESC LIMIT 1""", (player_id,))
    # WHAT IT DOES: "find this player's roster entries, newest first (DESC), and give me
    #         only the first one (LIMIT 1): the date, his status (Active, Injured...),
    #         the team's full name and home park."
    #         The roster table only stores a team ID ("ORG"), so the LEFT JOIN looks up
    #         the team name in mlbteams for that year. "LEFT" = keep the roster row even
    #         if no team name is found. "AS status" renames a column in the answer.
    #         Uppercase column names ("STATUS", "ORG", "MLBAMID") need double quotes in
    #         Postgres — that's why the SQL here is wrapped in triple quotes: so the
    #         double quotes inside don't end the Python string.
    return cur.fetchone()
    # PYTHON: fetchone() returns one row, or None if there are no rows (not on a roster).


def fetch_league(cur, season):
    """Every qualified hitter's full-season row, for league averages and ranks."""
    min_pa = QUALIFIED_PA.get(season, DEFAULT_QUALIFIED_PA)
    # WHAT IT DOES: 502, unless the season is 2020 (186).
    cur.execute("SELECT * FROM main.batter_season WHERE season = %s AND split = 'all' AND pa >= %s",
                (season, min_pa))
    # PYTHON: a function call can continue on the next line while inside its parentheses.
    # WHAT IT DOES: every full-season row with 502+ PA — the 135 qualified hitters of 2026.
    return add_derived(cur.fetchall()), min_pa
    # PYTHON: returns TWO values at once. The caller catches both:
    #         league, min_pa = fetch_league(cur, 2026)


def fetch_data_through(cur, season):
    cur.execute("SELECT max(game_date) AS d FROM main.mlb_games WHERE game_type = 'R' AND season = %s", (season,))
    # WHAT IT DOES: the latest date of any regular-season ('R') game that season.
    return cur.fetchone()["d"]
    # PYTHON: fetchone() gives a one-row dictionary; ["d"] pulls out its one value.


# ---------------------------------------------------------------- packet sections
# =====================================================================================
# PACKET SECTIONS: each function returns one section of the packet as text
# =====================================================================================

def section_seasons(full):
    # WHAT IT DOES: "full" = his full-season rows, one per season. Builds four tables.
    core = table(
        ["Season", "Team", "Age", "PA", "xwOBA (house)", "EV90", "Pulled Air%", "IZ Swing - Chase",
         "Whiff%", "LA median", "LA SD"],
        [[r["season"], r["teams"], r["age"], r["pa"], fmt("xwoba", r["xwoba"]), fmt("ev90", r["ev90"]),
          fmt("pulled_fb_pct", r["pulled_fb_pct"]), fmt("swing_score", r["swing_score"]),
          fmt("whiff_pct", r["whiff_pct"]), fmt("median_la", r["median_la"]), fmt("sd_la", r["sd_la"])]
         for r in full])
    # PYTHON: one call to table(headers, rows), spread over several lines.
    #         Input 1: a list of header strings.
    #         Input 2: a list comprehension that makes a list OF LISTS — one inner list
    #                  per season ("for r in full"), each holding that season's values.
    # WHAT IT DOES: the core table — the method's first-look metrics, one row per season.
    #         Each number goes through fmt() so it prints baseball-style.
    results = table(
        ["Season", "PA", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "BABIP", "AVG", "OBP", "SLG", "HR", "Sprint speed (ft/s)"],
        [[r["season"], r["pa"], fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]),
          fmt("babip", r["babip"]), fmt("avg", r["avg"]), fmt("obp", r["obp"]), fmt("slg", r["slg"]),
          r["hr"], fmt("sprint_speed", r["sprint_speed"])] for r in full])
    # WHAT IT DOES: results vs. expected — actual outcomes next to the house model's.
    contact = table(
        ["Season", "PA", "BBE", "xBA", "xSLG", "Avg EV", "Hard-hit%", "Barrel%", "Sweet spot%",
         "GB%", "LD%", "FB%", "PU%", "Pull%", "Oppo%"],
        [[r["season"], r["pa"], r["bbe"], fmt("xba", r["xba"]), fmt("xslg", r["xslg"]), fmt("avg_ev", r["avg_ev"]),
          pct(r["hard_hit_pct"]), pct(r["barrel_pct"]), pct(r["sweet_spot_pct"]), pct(r["gb_pct"]),
          pct(r["ld_pct"]), pct(r["fb_pct"]), pct(r["pu_pct"]), pct(r["pull_pct"]), pct(r["oppo_pct"])]
         for r in full])
    # WHAT IT DOES: contact quality and batted-ball shape. pct() is used directly because
    #         all of these are percentages.
    swing = table(
        ["Season", "PA", "Pitches", "IZ Swing%", "Chase%", "IZ Swing - Chase", "Whiff%", "K%", "BB%"],
        [[r["season"], r["pa"], r["pitches"], pct(r["z_swing_pct"]), pct(r["chase_pct"]),
          fmt("swing_score", r["swing_score"]), pct(r["whiff_pct"]), pct(r["k_pct"]), pct(r["bb_pct"])]
         for r in full])
    # WHAT IT DOES: swing decisions.
    return ("## Seasons (full season, every MLB season on record)\n\n### Core (method's first look)\n\n" + core
            + "\n\n### Results vs. expected\n\n" + results
            + "\n\n### Contact quality and batted-ball shape\n\n" + contact
            + "\n\n### Swing decisions\n\n" + swing)
    # PYTHON: + glues the pieces of text together. The outer ( ) lets the expression
    #         continue across lines. "\n\n" = a blank line.
    # WHAT IT DOES: the four tables under markdown headings (## and ###).


def context_table(player_row, league, metrics, qualified):
    """Player value, league average and rank for each metric."""
    # WHAT IT DOES: the "how does he compare" logic, used for the full-season table AND
    #         each pitch group. Inputs: his row; all qualified hitters' rows; which
    #         metric list to use; and True/False for whether he has 502+ PA.
    rows = []
    for label, col, better in metrics:
        # PYTHON: unpacking in a loop — each tuple's three parts get their own names.
        #         On the first turn: label="xwOBA (house)", col="xwoba", better="higher".
        values = [r[col] for r in league if r[col] is not None]
        # PYTHON: list comprehension with a filter: every qualified hitter's value for
        #         this metric, skipping missing ones.
        avg = sum(values) / len(values) if values else None
        # PYTHON: / is division. "if values else None": an empty list counts as False,
        #         so this avoids dividing by zero when there are no values.
        # WHAT IT DOES: league average = total / count (each hitter counts once).
        mine = player_row[col]                 # his own value
        if better and qualified and mine is not None:
            # PYTHON: "and" — all three must be True. "better" counts as True when it is
            #         "higher" or "lower", and False when it is None.
            # WHAT IT DOES: rank only if the metric has a better direction, he's
            #         qualified, and his value exists.
            rank = 1 + sum(v > mine if better == "higher" else v < mine for v in values)
            # PYTHON: for each value v, a True/False ("is this hitter better than him?").
            #         sum() counts the Trues (True = 1). Add 1 for his own spot.
            # WHAT IT DOES: 33 hitters with a higher EV90 than his 106.6 -> rank 34.
            #         Ties aren't counted as better, so tied hitters share a rank.
            rank_s = f"{rank} of {len(values)}"    # -> "34 of 135"
            # share of qualified hitters he ranks ahead of: 100 = best, 0 = worst
            pctile_s = str(round(100 * (len(values) - rank) / (len(values) - 1))) if len(values) > 1 else "—"
            # PYTHON: parentheses control the order of math, as in algebra. round() gives
            #         a whole number; str() turns it into text.
            # WHAT IT DOES: percentile. With 135 hitters, rank 1 -> 100, rank 135 -> 0.
            #         Rank 34: (135 - 34) / (135 - 1) = 101 / 134 = 0.754 -> 75.
        else:
            rank_s = pctile_s = "—"
            # PYTHON: a = b = "—" sets both variables to the same value at once.
        rows.append([label, fmt(col, mine), fmt(col, avg), rank_s, pctile_s])
        # WHAT IT DOES: one finished row: label, his value, league avg, rank, percentile.
    return table(["Metric", "Player", "Qualified avg", "Player rank", "Percentile"], rows)


def section_changes(full):
    """Change between consecutive seasons, for the last three seasons."""
    recent = full[-3:]
    # PYTHON: slice from the third-to-last item to the end = the last three seasons.
    if len(recent) < 2:
        return "## Season-over-season changes\n\nOnly one MLB season on record."
    pairs = list(zip(recent, recent[1:]))
    # PYTHON: zip pairs items up by position:
    #           recent      = [2024, 2025, 2026]
    #           recent[1:]  = [2025, 2026]
    #           zip(...)    -> (2024, 2025), (2025, 2026)
    #         list(...) turns the pairs into a list.
    headers = ["Metric"] + [f"{a['season']} → {b['season']}" for a, b in pairs]
    # PYTHON: + on two lists joins them into one list. Result: ["Metric", "2024 → 2025",
    #         "2025 → 2026"].
    rows = [[label] + [change(col, b[col], a[col]) for a, b in pairs] for label, col in CHANGE_METRICS]
    # PYTHON: a list comprehension INSIDE a list comprehension. Outer: one row per metric
    #         in CHANGE_METRICS. Inner: for each season pair, change(new=b, old=a).
    # WHAT IT DOES: e.g. ["EV90", "+3.3", "+1.4"].
    note = ("Computed from the season rows above (later season minus earlier). "
            "Rates in points of .001 (+.048); percentages in percentage points (+4.4 pts); EV90, LA and sprint speed in mph / degrees / ft/s. "
            "PA by season: " + ", ".join(f"{r['season']} {r['pa']}" for r in recent) + ".")
    # PYTHON: strings written next to each other inside parentheses are glued together
    #         automatically — a way to write a long sentence across several lines.
    return f"## Season-over-season changes\n\n{note}\n\n" + table(headers, rows)


def section_league(player_row, league, min_pa):
    season = player_row["season"]
    qualified = player_row["pa"] >= min_pa
    # PYTHON: a comparison produces True or False, which can be stored in a variable.
    note = (f"League = the {len(league)} qualified hitters in {season} ({min_pa}+ PA); league average is the simple "
            "mean of their values. Rank 1 = best; shown only for metrics with a clear better direction"
            + ("." if qualified else f", and not shown here because this player had {player_row['pa']} PA (not qualified)."))
    # WHAT IT DOES: the explanation above the table. If he isn't qualified, it adds why
    #         there are no ranks (what you saw in Nick Sogard's packet).
    return f"## {season} league context\n\n{note}\n\n" + context_table(player_row, league, CONTEXT_METRICS, qualified)
    # WHAT IT DOES: heading + note + the comparison table, using the full-season metric list.


def section_pitch_groups(groups, league, latest, min_pa):
    """Last three seasons by pitch group, then league context per group for the latest season."""
    if not groups:
        return "## By pitch group\n\nNo pitch-group rows in the database."
    groups = sorted(groups, key=lambda r: (r["season"], PITCH_GROUPS.index(r["pitch_group"])))
    # PYTHON: sorted(list, key=...) returns a sorted copy. key says what to sort by;
    #         here a lambda (a one-line function, PART A #15) that returns a tuple:
    #         (season, group position). Tuples sort by the first item, then the second.
    #         PITCH_GROUPS.index("breaking") -> 1 (its position in the list).
    # WHAT IT DOES: order rows by season, then fastball -> breaking -> offspeed.
    seasons = table(
        ["Season", "Group", "Pitches", "Share", "IZ Swing%", "Chase%", "IZ Swing - Chase", "Whiff%",
         "PA ending", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "K%", "BBE", "EV90", "Hard-hit%", "Barrel%"],
        [[r["season"], r["pitch_group"], r["pitches"], pct(r["pitch_share"]), pct(r["z_swing_pct"]),
          pct(r["chase_pct"]), fmt("swing_score", r["swing_score"]), pct(r["whiff_pct"]), r["pa"],
          fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]), pct(r["k_pct"]), r["bbe"],
          fmt("ev90", r["ev90"]), pct(r["hard_hit_pct"]), pct(r["barrel_pct"])] for r in groups])
    # WHAT IT DOES: one table, one row per season x group (up to nine rows).
    season = latest["season"]
    qualified = latest["pa"] >= min_pa
    parts = [
        "## By pitch group",
        "Fastball = four-seam, sinker, cutter, two-seam. Breaking = slider, sweeper, curveball, knuckle curve, "
        "slurve, slow curve. Offspeed = changeup, splitter, forkball.\n\n"
        "Two ways of counting: Pitches, Share, IZ Swing%, Chase% and Whiff% count every pitch of the group he saw. "
        "\"PA ending\" and everything after it count only plate appearances whose last pitch was in the group.",
        "### Seasons\n\n" + seasons,
    ]
    # PYTHON: a list of three text pieces. (\" inside a string is a literal double quote.)
    #         More pieces get added in the loop below; all are joined at the end.
    for g in PITCH_GROUPS:
        mine = next((r for r in groups if r["season"] == season and r["pitch_group"] == g), None)
        # PYTHON: next(candidates, None) returns the first matching row, or None if none.
        # WHAT IT DOES: his row for this group in the latest season.
        if mine is None:
            continue
            # PYTHON: continue = skip the rest of this turn and go to the next group.
        lg = [r for r in league if r["pitch_group"] == g]
        # WHAT IT DOES: the league's rows for this same group only.
        parts.append(f"### {season} vs. {g} — league context ({len(lg)} qualified hitters, {min_pa}+ season PA)\n\n"
                     + context_table(mine, lg, PITCH_GROUP_METRICS, qualified))
        # WHAT IT DOES: the same comparison logic as the full-season table, per group.
    return "\n\n".join(parts)


def section_splits(splits, season):
    label = {"vs_lhp": "vs LHP", "vs_rhp": "vs RHP"}
    # PYTHON: a small dictionary to translate database names into display names.
    rows = [[label[r["split"]], r["pa"], fmt("woba", r["woba"]), fmt("xwoba", r["xwoba"]), signed_rate(r["gap"]),
             fmt("ev90", r["ev90"]), pct(r["whiff_pct"]), pct(r["k_pct"]), pct(r["bb_pct"])]
            for r in splits]
    # PYTHON: label[r["split"]] — look up r["split"] (e.g. "vs_lhp") in the label
    #         dictionary, giving "vs LHP". A lookup inside a lookup.
    if not rows:
        return f"## {season} platoon splits\n\nNo split rows in the database."
    return (f"## {season} platoon splits\n\n"
            + table(["Split", "PA", "wOBA", "xwOBA (house)", "wOBA - xwOBA", "EV90", "Whiff%", "K%", "BB%"], rows))


# ---------------------------------------------------------------- the packet
# =====================================================================================
# THE MAIN FUNCTION: runs everything above, in order
# =====================================================================================
# report.py calls data.get_hitter_data("Pete Crow-Armstrong") and gets the packet back.
# Every function above only runs when this one calls it.

def get_hitter_data(name):
    """Return the data packet (markdown text) for one hitter."""
    with psycopg.connect(CONNINFO, autocommit=True, row_factory=dict_row) as conn, conn.cursor() as cur:
        # PYTHON: "with ... as name:" (PART A #17) opens the database connection (conn)
        #         and a cursor (cur); both close automatically when the indented block
        #         ends. Two things opened in one "with", separated by a comma.
        #         The inputs after CONNINFO are "keyword arguments": name=value pairs that
        #         set options. autocommit=True = run each question on its own (we only
        #         read); row_factory=dict_row = rows come back as dictionaries.
        player = resolve_player(cur, name)                 # 1. find the player (or stop)
        rows = fetch_seasons(cur, player["player_id"])     # 2. all his season rows
        full = [r for r in rows if r["split"] == "all"]    # 3. keep only full-season rows
        latest = full[-1]                                  # 4. his most recent season ([-1] = last)
        splits = [r for r in rows if r["season"] == latest["season"] and r["split"] != "all"]
        #                                                  # 5. that season's vs LHP / vs RHP rows
        team = fetch_current_team(cur, player["player_id"])          # 6. current team and park
        league, min_pa = fetch_league(cur, latest["season"])         # 7. qualified hitters
        # PYTHON: catching the TWO values fetch_league returns into two names.
        groups = fetch_pitch_groups(cur, player["player_id"], latest["season"] - 2)
        #                                                  # 8. his pitch groups, last 3 seasons
        league_groups = fetch_league_pitch_groups(cur, latest["season"], min_pa)
        #                                                  # 9. the league's pitch groups
        data_through = fetch_data_through(cur, latest["season"])     # 10. last game date
    # PYTHON: the indentation ends here, so the database connection closes now.
    #         Everything below works with data already pulled into memory.

    team_s = (f"{team['team_full_name']} (40-man roster as of {team['date']}, status: {team['status']})"
              if team else f"{latest['teams']} (from {latest['season']} stats; not on a current 40-man roster)")
    # PYTHON: a one-line if/else across two lines. "if team" is True when a roster row
    #         was found (a row counts as True; None counts as False).
    # WHAT IT DOES: the team line — his latest roster team, or a fallback that says so.
    header = "\n".join([
        f"# Data packet: {player['full_name']}",
        "",
        f"- Player ID: {player['player_id']}",
        f"- Position: {latest['pos']} · Bats {latest['bats']} / Throws {latest['throws']}",
        f"- Age: {latest['age']} in {latest['season']} (age as of June 30 of that season)",
        f"- Current team: {team_s}",
        f"- Home venue: {team['venue_name'] if team and team['venue_name'] else '—'}",
        f"- Latest season: {latest['season']} · data through {data_through} (MLB regular season only)",
    ])
    # PYTHON: a list of lines joined with line breaks. The "" is an empty line.
    # WHAT IT DOES: the header block at the top of the packet.
    notes = "\n".join([
        "## Notes on the data",
        "",
        "- Rates are per plate appearance or per batted ball; \"—\" means the value is not available.",
        "- xwOBA, xSLG, xBA come from a house expected-stats model (validated against Statcast; typical "
        "difference 3–7 points of xwOBA). Call them \"(house model)\".",
        "- IZ Swing - Chase is in-zone swing rate minus chase rate (higher is better).",
        "- Pull% and Oppo% are approximate (about 4 points above Statcast); fine for trends.",
        "- FB% uses the Statcast definition: popups are counted separately (PU%), so it runs well below FanGraphs' FB%.",
        "- Sprint speed: about 27 ft/s is average, 30+ elite.",
        "- Park factors are NOT in the database, so park effects cannot be checked.",
    ])
    # WHAT IT DOES: reading notes at the end of the packet (your FB% line is the fifth).
    return "\n\n".join([header, section_seasons(full), section_changes(full), section_league(latest, league, min_pa),
                        section_splits(splits, latest["season"]),
                        section_pitch_groups(groups, league_groups, latest, min_pa), notes]) + "\n"
    # PYTHON: each section_...() function is called right here, inside the list; each
    #         returns its text, and join() glues them with blank lines between.
    # WHAT IT DOES: the finished packet — the one block of text Claude reads.


# =====================================================================================
# RUNNING FROM THE TERMINAL
# =====================================================================================
if __name__ == "__main__":
    # PYTHON: __name__ is a special variable Python sets automatically. It equals
    #         "__main__" only when this file is run directly (python data.py "Name").
    #         When report.py imports data.py, it doesn't, so this block is skipped.
    if len(sys.argv) != 2:
        sys.exit('usage: python data.py "Player Name"')
        # PYTHON: sys.argv is a list of what you typed: ["data.py", "Pete Crow-Armstrong"].
        #         != 2 means "not exactly two items". sys.exit() prints the message and stops.
    try:
        print(get_hitter_data(sys.argv[1]))
        # PYTHON: sys.argv[1] = the second item = the player name. print() shows the packet.
    except ValueError as e:
        sys.exit(str(e))
        # PYTHON: try/except (PART A #18): if resolve_player() raised a ValueError (no
        #         match, or several), print just its message instead of a long error dump.
