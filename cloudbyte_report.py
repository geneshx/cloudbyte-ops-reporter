#!/usr/bin/env python3
"""CloudByte Ops Reporter: summarise CloudByte's activity from the command line."""


def main():
    # Read the access log into a list of records (one line per event).
    records = []
    with open("cloudbyte_access.log") as f:
        for line in f:
            records.append(line)

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
        fields = record.split()
        date = fields[0][:10]
        time = fields[0][11:]
        print(f"{date} {time}  {fields[1]} {fields[2]}")
    print()

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

if __name__ == "__main__":
    main()
    