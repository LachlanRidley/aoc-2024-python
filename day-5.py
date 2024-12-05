from collections import defaultdict


with open("day-5.txt") as f:
    puzzle = f.read()

# make rules look up
sections = puzzle.split("\n\n")
rules = [(rule.split("|")[0], rule.split("|")[1]) for rule in sections[0].splitlines()]
rules_lookup = defaultdict(set)
for x, y in rules:
    rules_lookup[x].add(y)
rules_lookup = dict(rules_lookup)

# get updates
updates = [update.split(",") for update in sections[1].splitlines()]

# the good stuff
valid_updates = []
invalid_updates = []
for update in updates:
    update_valid = True
    for i, page in enumerate(update):
        if rules_for_page := rules_lookup.get(page):
            relevant_rules = set(rules_for_page).intersection(set(update))
            pages_left = update[i + 1 :]
            for rule in relevant_rules:
                if rule not in pages_left:
                    update_valid = False
    if update_valid:
        valid_updates.append(update)
    else:
        invalid_updates.append(update)

part_1 = sum([int(update[len(update) // 2]) for update in valid_updates])

# fix incorrectly ordered
for update in invalid_updates:
    i = 0
    while i < len(update):
        page = update[i]
        if rules_for_page := rules_lookup.get(page):
            relevant_rules = set(rules_for_page).intersection(set(update))
            pages_left = update[i + 1 :]
            while len(relevant_rules.difference(pages_left)) > 0:
                temp = update[i - 1]
                update[i - 1] = update[i]
                update[i] = temp
                i -= 1
                pages_left = update[i + 1 :]
        i += 1

part_2 = sum([int(update[len(update) // 2]) for update in invalid_updates])


print(f"Part 1: {part_1}")
print(f"Part 2: {part_2}")
