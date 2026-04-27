"""
Splitwise API Helper Module
Provides easy-to-use functions for interacting with Splitwise API
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv
from requests_oauthlib import OAuth1
import requests

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Get credentials
CONSUMER_KEY = os.getenv('SPLITWISE_CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('SPLITWISE_CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('SPLITWISE_ACCESS_TOKEN')
ACCESS_SECRET = os.getenv('SPLITWISE_ACCESS_SECRET')
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'INR')

BASE_URL = 'https://secure.splitwise.com/api/v3.0'


def get_auth():
    """Returns OAuth1 authentication object"""
    return OAuth1(
        client_key=CONSUMER_KEY,
        client_secret=CONSUMER_SECRET,
        resource_owner_key=ACCESS_TOKEN,
        resource_owner_secret=ACCESS_SECRET
    )


def api_get(endpoint, params=None):
    """Make GET request to Splitwise API"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.get(url, auth=get_auth(), params=params or {})
    return response.json()


def api_post(endpoint, data):
    """Make POST request to Splitwise API"""
    url = f"{BASE_URL}/{endpoint}"
    response = requests.post(url, auth=get_auth(), data=data)
    return response.json()


# ============== User Functions ==============

def get_current_user():
    """Get current authenticated user"""
    return api_get('get_current_user')


def get_user(user_id):
    """Get user by ID"""
    return api_get(f'get_user/{user_id}')


# ============== Group Functions ==============

def get_groups():
    """Get all groups for the current user"""
    return api_get('get_groups')


def get_group(group_id):
    """Get specific group with members"""
    data = api_get(f'get_group/{group_id}')
    return data.get('group')


def get_group_members(group_id):
    """Get members of a specific group"""
    group = get_group(group_id)
    return group.get('members', []) if group else []


def find_group_by_name(name):
    """Find group by partial name match"""
    groups = get_groups().get('groups', [])
    name_lower = name.lower()
    return [g for g in groups if name_lower in g.get('name', '').lower()]


def find_member_by_name(group_id, name):
    """Find member in a group by name (partial match)"""
    members = get_group_members(group_id)
    name_lower = name.lower()
    matches = [m for m in members if name_lower in f"{m.get('first_name','')} {m.get('last_name','')}".lower()]
    return matches


# ============== Expense Functions ==============

def create_expense(
    group_id,
    description,
    cost,
    paid_by_user_id,
    split_type='equal',
    split_with_user_ids=None,
    split_ratios=None,
    date=None,
    currency=None,
    details=None
):
    """
    Create an expense in a group
    
    Args:
        group_id: ID of the group
        description: What the expense is for
        cost: Total amount
        paid_by_user_id: User ID who paid
        split_type: 'equal' or 'exact'
        split_with_user_ids: List of user IDs to split with (including payer)
        split_ratios: Dict of {user_id: amount} for 'exact' split type
        date: Date in YYYY-MM-DD format
        currency: Currency code (e.g., 'INR')
        details: Additional notes
    
    Returns:
        Created expense object
    """
    currency = currency or DEFAULT_CURRENCY
    users = []
    
    if split_type == 'equal' and split_with_user_ids:
        split_amount = cost / len(split_with_user_ids)
        for i, uid in enumerate(split_with_user_ids):
            users.append({
                f'users__{i}__user_id': uid,
                f'users__{i}__paid_share': cost if uid == paid_by_user_id else '0',
                f'users__{i}__owed_share': str(split_amount)
            })
    elif split_type == 'exact' and split_ratios:
        for i, (uid, paid, owed) in enumerate(split_ratios.items()):
            users.append({
                f'users__{i}__user_id': uid,
                f'users__{i}__paid_share': str(paid),
                f'users__{i}__owed_share': str(owed)
            })
    
    # Flatten users dict
    flat_users = {}
    for u in users:
        flat_users.update(u)
    
    data = {
        'group_id': group_id,
        'cost': str(cost),
        'description': description,
        'currency_code': currency,
        **flat_users
    }
    
    if date:
        data['date'] = date
    if details:
        data['details'] = details
    
    result = api_post('create_expense', data)
    return result.get('expenses', [{}])[0] if result.get('expenses') else None


def get_expenses(group_id=None, limit=100):
    """Get expenses, optionally filtered by group"""
    params = {'limit': limit}
    if group_id:
        params['group_id'] = group_id
    result = api_get('get_expenses', params)
    expenses = result.get('expenses', [])
    # Ensure all expenses are dicts (API sometimes returns strings)
    return [e if isinstance(e, dict) else {'id': e} for e in expenses]


def get_expense_by_id(expense_id):
    """Get a specific expense by ID"""
    result = api_get(f'get_expense/{expense_id}')
    return result.get('expenses', [None])[0] if result.get('expenses') else None


def find_expense_by_description(group_id, search_text, limit=20):
    """Find expenses by description in a group"""
    expenses = get_expenses(group_id=group_id, limit=limit)
    search_lower = search_text.lower()
    return [e for e in expenses if search_lower in e.get('description', '').lower()]


def update_expense(expense_id, **kwargs):
    """Update an existing expense. Returns the updated expense."""
    data = {'id': str(expense_id), **kwargs}
    result = api_post('update_expense', data)
    return result


def delete_expense(expense_id):
    """
    Delete an expense by ID.
    Returns: {'success': True} if deleted successfully
    
    Example:
        result = delete_expense(123456)
        if result.get('success'):
            print('Deleted!')
    """
    data = {'id': str(expense_id)}
    result = api_post('delete_expense', data)
    return result


# ============== Utility Functions ==============

def print_user_info():
    """Print current user info"""
    user = get_current_user().get('user', {})
    print(f"\n👤 {user.get('first_name')} {user.get('last_name')}")
    print(f"   Email: {user.get('email')}")
    print(f"   ID: {user.get('id')}")


def print_groups():
    """Print all groups"""
    groups = get_groups().get('groups', [])
    print(f"\n📁 Groups ({len(groups)}):")
    for g in groups:
        members = g.get('members', [])
        print(f"   [{g.get('id')}] {g.get('name')} - {len(members)} members")


def print_group_details(group_id):
    """Print group with all members"""
    group = get_group(group_id)
    if not group:
        print("Group not found!")
        return
    
    print(f"\n📁 Group: {group.get('name')} (ID: {group.get('id')})")
    print("   Members:")
    for m in group.get('members', []):
        name = f"{m.get('first_name')} {m.get('last_name')}".strip()
        print(f"      [{m.get('id')}] {name}")


def print_balances(group_id):
    """Print balances in a group"""
    group = get_group(group_id)
    if not group:
        return
    
    print(f"\n💰 Balances in {group.get('name')}:")
    for m in group.get('members', []):
        balances = m.get('balance', [])
        for b in balances:
            amount = float(b.get('amount', 0))
            if amount != 0:
                currency = b.get('currency_code', '')
                direction = '+' if amount > 0 else ''
                print(f"   {m.get('first_name')} {direction}{amount} {currency}")


# Make module directly executable for testing
if __name__ == '__main__':
    print_user_info()
    print_groups()
