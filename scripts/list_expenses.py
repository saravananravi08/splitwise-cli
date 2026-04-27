#!/usr/bin/env python3
"""
List Expenses from Splitwise
Usage: python3 list_expenses.py [--group NAME] [--limit 50]
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from splitwise_api import (
    get_expenses,
    find_group_by_name,
    get_group
)


def main():
    parser = argparse.ArgumentParser(description='List Splitwise expenses')
    parser.add_argument('--group', '-g', help='Group name (partial match)')
    parser.add_argument('--limit', '-n', type=int, default=20, help='Number of expenses to show')
    args = parser.parse_args()
    
    group_id = None
    group_name = None
    
    if args.group:
        matching = find_group_by_name(args.group)
        if not matching:
            print(f"❌ No group found matching '{args.group}'")
            return
        if len(matching) > 1:
            print(f"❌ Multiple groups match '{args.group}':")
            for g in matching:
                print(f"   - {g.get('name')} (ID: {g.get('id')})")
            return
        
        group_id = matching[0].get('id')
        group_name = matching[0].get('name')
    
    # Get expenses
    expenses = get_expenses(group_id=group_id, limit=args.limit)
    
    print(f"\n{'='*60}")
    if group_name:
        print(f"📋 Expenses in {group_name}")
    else:
        print("📋 Recent Expenses")
    print('='*60)
    
    if not expenses:
        print("No expenses found.")
        return
    
    total = 0
    for e in expenses:
        date = e.get('date', '')[:10]
        desc = e.get('description', 'N/A')
        cost = float(e.get('cost', 0))
        currency = e.get('currency_code', 'INR')
        created_by = e.get('created_by', {}).get('first_name', 'Unknown')
        total += cost
        
        print(f"\n[{date}] {desc}")
        print(f"   Amount: ₹{cost} | Paid by: {created_by}")
        
        # Show split details
        users = e.get('users', [])
        if users:
            splits = []
            for u in users:
                name = u['user'].get('first_name', '')
                owed = float(u.get('owed_share', 0))
                paid = float(u.get('paid_share', 0))
                if paid > 0:
                    splits.append(f"{name} paid ₹{paid}")
                elif owed > 0:
                    splits.append(f"{name} owes ₹{owed}")
            if splits:
                print(f"   Split: {' | '.join(splits)}")
    
    print(f"\n{'='*60}")
    print(f"Total: ₹{total:.2f}")
    print('='*60)


if __name__ == '__main__':
    main()
