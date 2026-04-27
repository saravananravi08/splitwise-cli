#!/usr/bin/env python3
"""
Add Expense to Splitwise
Usage: python3 add_expense.py <group_name> <description> <amount> [--split-with NAME] [--date YYYY-MM-DD] [--paid-by NAME]
"""

import sys
import argparse
from pathlib import Path

# Add scripts folder to path
sys.path.insert(0, str(Path(__file__).parent))

from splitwise_api import (
    get_current_user,
    get_groups,
    find_group_by_name,
    find_member_by_name,
    create_expense,
    print_user_info,
    print_groups
)

# Alias for convenience
api_get = __import__('splitwise_api').api_get


def get_user_id_by_name(name):
    """Get current user ID"""
    user = get_current_user().get('user', {})
    return user.get('id')


def main():
    parser = argparse.ArgumentParser(description='Add expense to Splitwise')
    parser.add_argument('description', help='Expense description')
    parser.add_argument('amount', type=float, help='Total amount')
    parser.add_argument('--group', '-g', help='Group name (partial match works)')
    parser.add_argument('--split-with', '-s', nargs='+', help='Names to split with (space separated)')
    parser.add_argument('--paid-by', '-p', help='Who paid (default: you)')
    parser.add_argument('--date', '-d', help='Date (YYYY-MM-DD, default: today)')
    parser.add_argument('--currency', '-c', default='INR', help='Currency code (default: INR)')
    parser.add_argument('--list-groups', '-l', action='store_true', help='List all groups and exit')
    
    args = parser.parse_args()
    
    # List groups and exit
    if args.list_groups:
        print_user_info()
        print_groups()
        return
    
    # Get current user
    current_user = get_current_user().get('user', {})
    current_user_id = current_user.get('id')
    current_user_name = f"{current_user.get('first_name')} {current_user.get('last_name')}"
    
    # Find group
    if not args.group:
        print("❌ Please specify a group with --group or -g")
        print("\nAvailable groups:")
        print_groups()
        return
    
    matching_groups = find_group_by_name(args.group)
    if not matching_groups:
        print(f"❌ No group found matching '{args.group}'")
        return
    if len(matching_groups) > 1:
        print(f"❌ Multiple groups match '{args.group}':")
        for g in matching_groups:
            print(f"   - {g.get('name')} (ID: {g.get('id')})")
        return
    
    group = matching_groups[0]
    group_id = group.get('id')
    group_name = group.get('name')
    members = group.get('members', [])
    
    # Determine who paid
    if args.paid_by:
        paid_matches = find_member_by_name(group_id, args.paid_by)
        if not paid_matches:
            print(f"❌ No member found matching '{args.paid_by}' in {group_name}")
            return
        if len(paid_matches) > 1:
            print(f"❌ Multiple members match '{args.paid_by}':")
            for m in paid_matches:
                print(f"   - {m.get('first_name')} {m.get('last_name')}")
            return
        payer_id = paid_matches[0].get('id')
        payer_name = f"{paid_matches[0].get('first_name')} {paid_matches[0].get('last_name')}"
    else:
        payer_id = current_user_id
        payer_name = current_user_name
    
    # Determine split participants
    split_user_ids = [payer_id]  # Start with payer
    
    if args.split_with:
        for name in args.split_with:
            matches = find_member_by_name(group_id, name)
            if not matches:
                print(f"⚠️  No member found matching '{name}' in {group_name}")
                continue
            if len(matches) > 1:
                print(f"⚠️  Multiple members match '{name}', using first one")
            member_id = matches[0].get('id')
            if member_id not in split_user_ids:
                split_user_ids.append(member_id)
    
    # Create expense
    expense = create_expense(
        group_id=group_id,
        description=args.description,
        cost=args.amount,
        paid_by_user_id=payer_id,
        split_type='equal',
        split_with_user_ids=split_user_ids,
        date=args.date,
        currency=args.currency
    )
    
    if expense:
        print(f"\n✅ Expense Added!")
        print(f"   Group: {group_name}")
        print(f"   Description: {expense.get('description')}")
        print(f"   Amount: ₹{expense.get('cost')}")
        if args.date:
            print(f"   Date: {args.date}")
        print(f"   Paid by: {payer_name}")
        
        print(f"\n💰 Split ({len(split_user_ids)} way):")
        for u in expense.get('users', []):
            name = f"{u['user'].get('first_name')} {u['user'].get('last_name')}"
            balance = float(u.get('net_balance', 0))
            if balance > 0:
                print(f"   {name}: Gets ₹{balance}")
            elif balance < 0:
                print(f"   {name}: Owes ₹{abs(balance)}")
    else:
        print("❌ Failed to create expense")


if __name__ == '__main__':
    main()
