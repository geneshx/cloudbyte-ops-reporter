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


if __name__ == "__main__":
    main()
    