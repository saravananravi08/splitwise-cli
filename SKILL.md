---
name: splitwise
description: Manage Splitwise expenses and groups via API. Use when you need to add, update, or retrieve bills, expenses, groups, or member balances from Splitwise. Keywords - splitwise, expense, bill, split, group, money, roommate, friends, trip expenses.
---

# Splitwise Tools

## ⚠️ SAFETY RULES (MANDATORY)

1. **NEVER delete, update, or create anything without explicit user permission**
2. **Always show what will be changed BEFORE making changes**
3. **Wait for explicit confirmation ("yes" or "confirm") before destructive actions**
4. **If unsure, ask the user first**

## CLI Tool (Recommended)

```bash
cd ~/splitwise-tools
splitwise user              # Show current user
splitwise groups            # List all groups
splitwise groups show "MyGroup"  # Group details
splitwise expenses "MyGroup" # List expenses
splitwise balances          # All balances
splitwise balances "MyGroup" # Group balances
splitwise friends           # List friends
splitwise members "Trip" # List group members
splitwise categories        # List categories
splitwise currencies        # List currencies
splitwise show 123456       # Show expense
splitwise add "Dinner" 500 --group "Trip"
splitwise delete 123456      # Safe delete (shows first)
splitwise delete 123456 --yes  # Confirm delete
```

## Add Expense Examples

```bash
# Equal split with all group members
splitwise add "Dinner" 500 --group "MyGroup"

# Equal split with specific people
splitwise add "Coffee" 150 --group "MyGroup" --split-with "Friend"

# Custom exact amounts (Friend1 owes 600, Friend2 owes 400)
splitwise add "Groceries" 1000 --group "MyGroup" \
  --split-with "Friend1" "Friend2" \
  --type exact --amounts 600 400

# Different payer and date
splitwise add "Taxi" 200 --group "MyGroup" --paid-by "Friend2" --date 2026-04-20

# Default group is non-group expenses
splitwise add "Coffee" 150 --split-with "Friend"
```

## All Commands

| Command | Description |
|---------|-------------|
| `splitwise user` | Show current user info |
| `splitwise groups` | List all groups |
| `splitwise groups show "Name"` | Show group details |
| `splitwise expenses "Group"` | List expenses in group |
| `splitwise expenses` | List recent expenses |
| `splitwise show <id>` | Show expense details |
| `splitwise add <desc> <amount>` | Add expense |
| `splitwise delete <id>` | Show delete preview (safe) |
| `splitwise delete <id> --yes` | Confirm and delete |
| `splitwise search <text>` | Search expenses |
| `splitwise balances` | All balances across friends |
| `splitwise balances "Group"` | Balances in a group |
| `splitwise friends` | List all friends |
| `splitwise categories` | List expense categories |
| `splitwise currencies` | List supported currencies |
| `splitwise comments <id>` | Show expense comments |

## Find IDs

Use `splitwise groups` and `splitwise members <group>` to find IDs.

## Tips

- Use partial name matching: `--group "Bangalore"` matches "Bangalore Food Expense"
- Dates format: `YYYY-MM-DD`
- Default currency is INR
- Expenses split equally by default
- Balances show who owes whom
