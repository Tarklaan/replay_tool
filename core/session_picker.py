import random

def pick_random_session(sessions: dict):
    """
    Pick a random New York session.
    Returns (date, DataFrame).
    """
    date = random.choice(list(sessions.keys()))
    return date, sessions[date]
