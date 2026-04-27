# Splitwise CLI - Quick Reference

## Installation
```bash
splitwise user              # Show user
splitwise groups            # List groups
splitwise groups show "MyGroup"  # Group details
```

## Expenses
```bash
splitwise expenses "Trip"           # List Trip expenses
splitwise show 123456               # Show expense
splitwise search "coffee"           # Search
splitwise comments 123456           # Show comments
```

## Add Expense
```bash
# Equal split
splitwise add "Dinner" 500 --group "Trip"

# Split with specific people
splitwise add "Coffee" 150 --split-with "John"

# Custom amounts
splitwise add "Groceries" 1000 \
  --split-with "John" "Jane" \
  --type exact --amounts 600 400

# Different payer and date
splitwise add "Taxi" 200 --paid-by "Jane" --date 2026-04-20
```

## Delete Expense (Safe!)
```bash
splitwise delete 123456          # Preview
splitwise delete 123456 --yes     # Confirm
```

## Balances & Info
```bash
splitwise balances               # All balances
splitwise balances "MyGroup"     # Group balances
splitwise friends               # List friends
splitwise categories            # Categories
splitwise currencies            # Currencies
```

## Find Group & Member IDs
```bash
splitwise groups              # Lists all groups with IDs
splitwise members "Trip"     # Lists all members in a group
```

Use `splitwise members <groupname>` to find member IDs for your groups.
