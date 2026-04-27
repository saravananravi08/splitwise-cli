#!/usr/bin/env python3
"""
List Groups and Members from Splitwise
Usage: python3 list_groups.py [--group NAME]
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from splitwise_api import (
    get_current_user,
    get_groups,
    get_group,
    find_group_by_name
)


def main():
    parser = argparse.ArgumentParser(description='List Splitwise groups and members')
    parser.add_argument('--group', '-g', help='Show specific group details')
    args = parser.parse_args()
    
    # Get current user
    user = get_current_user().get('user', {})
    print(f"\n👤 {user.get('first_name')} {user.get('last_name')}")
    print(f"   Email: {user.get('email')}")
    print(f"   ID: {user.get('id')}")
    
    if args.group:
        # Show specific group
        matching = find_group_by_name(args.group)
        if not matching:
            print(f"\n❌ No group found matching '{args.group}'")
            return
        
        for g in matching:
            group_id = g.get('id')
            group = get_group(group_id)
            print(f"\n📁 Group: {group.get('name')} (ID: {group_id})")
            print(f"   Created: {group.get('created_at', '')[:10]}")
            print(f"   Members ({len(group.get('members', []))}):")
            for m in group.get('members', []):
                name = f"{m.get('first_name')} {m.get('last_name')}".strip()
                print(f"      [{m.get('id')}] {name}")
    else:
        # Show all groups
        groups = get_groups().get('groups', [])
        print(f"\n📁 All Groups ({len(groups)}):")
        print("-" * 50)
        for g in groups:
            members = g.get('members', [])
            member_names = [f"{m.get('first_name','')} {m.get('last_name','')}".strip() for m in members]
            print(f"\n[{g.get('id')}] {g.get('name')}")
            print(f"   Members: {len(members)}")
            if members:
                # Show first 3 members
                preview = ", ".join(member_names[:3])
                if len(member_names) > 3:
                    preview += f" (+{len(member_names)-3} more)"
                print(f"   {preview}")


if __name__ == '__main__':
    main()
