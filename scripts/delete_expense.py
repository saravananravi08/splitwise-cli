#!/usr/bin/env python3
"""
Delete Expense from Splitwise

⚠️ SAFETY: This script will NEVER delete anything without explicit confirmation.
   It only shows what will be deleted and asks for confirmation.

Usage: 
    python3 delete_expense.py --id 123456          # Delete by ID (will confirm)
    python3 delete_expense.py --search "Coffee" --group "Trip"  # Find and show matches

This script is READ-ONLY by default - it will show you what it found
but will NOT delete until you explicitly answer 'y' to the confirmation.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from splitwise_api import (
    get_expenses,
    delete_expense,
    find_group_by_name
)


def show_expense_details(expense_id):
    """Get expense details by ID"""
    from splitwise_api import api_get
    result = api_get(f'get_expense/{expense_id}')
    expense = result.get('expense')
    if expense and expense.get('deleted_at'):
        expense = None  # Treat deleted as not found
    return expense


def main():
    parser = argparse.ArgumentParser(
        description='Find and show Splitwise expense (safe mode - no auto-delete)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # List all expenses matching "coffee" in Trip group
    python3 delete_expense.py --search "coffee" --group "Trip"
    
    # Show details of a specific expense
    python3 delete_expense.py --id 123456
    
    # Delete with confirmation
    python3 delete_expense.py --id 123456 --delete
        """
    )
    parser.add_argument('--id', '-i', type=int, help='Expense ID')
    parser.add_argument('--search', '-s', help='Search text to find expense')
    parser.add_argument('--group', '-g', help='Group name to search in')
    parser.add_argument('--delete', '-d', action='store_true', 
                        help='ACTUALLY DELETE (requires --id, asks confirmation first)')
    parser.add_argument('--limit', '-n', type=int, default=20, 
                        help='Number of expenses to search (default: 20)')
    
    args = parser.parse_args()
    
    # If --delete is used, --id is required
    if args.delete and not args.id:
        print("❌ --delete requires --id")
        print("   Example: python3 delete_expense.py --delete --id 123456")
        return
    
    # If searching
    if args.search:
        if not args.group:
            print("❌ Please specify --group when using --search")
            return
        
        groups = find_group_by_name(args.group)
        if not groups:
            print(f"❌ No group found matching '{args.group}'")
            return
        
        group_id = groups[0]['id']
        group_name = groups[0]['name']
        
        expenses = get_expenses(group_id=group_id, limit=args.limit)
        matches = [e for e in expenses if args.search.lower() in e.get('description', '').lower()]
        
        if not matches:
            print(f"❌ No expense found matching '{args.search}' in {group_name}")
            return
        
        print(f"\n📋 Found {len(matches)} expense(s) matching '{args.search}' in {group_name}:\n")
        for i, e in enumerate(matches, 1):
            date = e.get('date', '')[:10]
            cost = e.get('cost', '0')
            desc = e.get('description', '')
            print(f"  {i}. [{e.get('id')}] {date} | {desc} | ₹{cost}")
        
        print(f"\n💡 To delete one of these, run:")
        print(f"   python3 delete_expense.py --delete --id <EXPENSE_ID>")
        return
    
    # If showing by ID
    if args.id:
        expense = show_expense_details(args.id)
        
        if not expense:
            print(f"❌ Expense {args.id} not found or already deleted")
            return
        
        print(f"\n📋 Expense Details:\n")
        print(f"   ID:          {expense.get('id')}")
        print(f"   Description: {expense.get('description')}")
        print(f"   Amount:      ₹{expense.get('cost')}")
        print(f"   Date:        {expense.get('date', '')[:10]}")
        print(f"   Group ID:    {expense.get('group_id')}")
        
        if args.delete:
            print(f"\n⚠️  CONFIRM DELETION")
            print(f"   You are about to PERMANENTLY DELETE:")
            print(f"   [{expense.get('id')}] {expense.get('description')} - ₹{expense.get('cost')}")
            
            try:
                confirm = input("\n   Type 'yes' to confirm deletion: ").strip().lower()
            except EOFError:
                print("\n❌ Cancelled - no input received")
                return
            
            if confirm != 'yes':
                print("❌ Cancelled.")
                return
            
            # Now delete
            result = delete_expense(args.id)
            if result.get('success'):
                print(f"\n✅ Deleted successfully!")
            else:
                print(f"\n❌ Failed to delete: {result}")
        else:
            print(f"\n💡 To delete this expense, run:")
            print(f"   python3 delete_expense.py --delete --id {args.id}")
        return
    
    # No arguments provided
    print("❌ Please provide --id or --search")
    print("\nUsage examples:")
    print("  python3 delete_expense.py --search 'coffee' --group 'Trip'")
    print("  python3 delete_expense.py --id 123456")
    print("  python3 delete_expense.py --delete --id 123456")


if __name__ == '__main__':
    main()
