#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""

def count_and_rank(records, get_key):
    """Return (count, key) pairs for the records, ranked most-frequent first."""
    counts = {}
    for record in records:
        key = get_key(record)
        counts[key] = counts.get(key, 0) + 1

    pairs = [(count, key) for key, count in counts.items()]
    pairs.sort(key=by_count_then_name)
    return pairs

"""
    pairs = []
    for key, count in counts.items():
        pairs.append((count, key))
    pairs.sort(key=by_count_then_name)
    return pairs
"""

def by_count_then_name(pair):
    """Sort key: busiest first, ties broken A-to-Z by name."""
    count, name = pair          # "name" is whatever was ranked: a username or an hour
    return (-count, name)       # busiest first (negated count), ties A->Z by name

def get_user(record):
    return record.split()[1]

def get_hour(record):
    return record.split()[0][11:13]

def get_action(record):
    return record.split()[2]

def main():
    # ... the log reading, header, and event lines stay unchanged ...

# def main():
    # Read the access log into a list of records (one line per event).
    with open("cloudbyte_access.log") as f:
        records = [line for line in f]

    """
    records = []
    with open("cloudbyte_access.log") as f:
        for line in f:
            records.append(line)
    """

    # Header: how many events, and the span from the first to the last.
    total = len(records)
    first_timestamp = records[0].split()[0]
    last_timestamp = records[-1].split()[0]
    first = f"{first_timestamp[:10]} {first_timestamp[11:]}"
    last = f"{last_timestamp[:10]} {last_timestamp[11:]}"

    print("CloudByte Access Report")
    print(f"{total} events from {first} to {last}")
    print()

    # One reformatted line per event.
    for record in records:
        timestamp, username, action = record.split()
        date = timestamp[:10]
        time = timestamp[11:]
        print(f"{date} {time}  {username} {action}")

        """
        fields = record.split()
        date = fields[0][:10]
        time = fields[0][11:]
        print(f"{date} {time}  {fields[1]} {fields[2]}")
        """
    print()

    # Most active users.
    user_pairs = count_and_rank(records, get_user)
    print("Most active users")
    for rank, (count, username) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {username}: {count} events")
    print()

    # Busiest hours.
    hour_pairs = count_and_rank(records, get_hour)
    print("Busiest hours")
    for count, hour in hour_pairs:
        print(f"  {hour}:00  {count} events")

    print()

    # Activity by type.
    action_pairs = count_and_rank(records, get_action)
    print("Activity by type")
    for rank, (count, action) in enumerate(action_pairs, start=1):
        print(f"  {rank}. {action}: {count} events")

    print()

    # Most active logins (login events only).
    logins = [r for r in records if get_action(r) == "login"]
    login_pairs = count_and_rank(logins, get_user)
    print("Most active logins")
    for rank, (count, username) in enumerate(login_pairs, start=1):
        print(f"  {rank}. {username}: {count} events")

    print()

    # Activity for one user (that person's events only).
    person = "alice"
    person_events = [r for r in records if get_user(r) == person]
    person_pairs = count_and_rank(person_events, get_action)
    print(f"Activity for {person}")
    for rank, (count, action) in enumerate(person_pairs, start=1):
        print(f"  {rank}. {action}: {count} events")

"""
    # Count how many events each user generated.
    user_counts = {}
    for record in records:
        username = record.split()[1]
        user_counts[username] = user_counts.get(username, 0) + 1

    # print(user_counts)

    # Rank the users from most to least active.
    user_pairs = []
    for username, count in user_counts.items():
        user_pairs.append((count, username))
    user_pairs.sort(reverse=True)
    # print(user_pairs)

    print("Most active users")
    print()

    for rank, (count, name) in enumerate(user_pairs, start=1):
        print(f"  {rank}. {name}: {count} events")
"""

if __name__ == "__main__":
    main()
    