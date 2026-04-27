# Splitwise CLI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/)

> **Manage Splitwise expenses from your terminal.** Track shared bills, split expenses with friends, manage group expenses, and view balances - all without opening a browser.

## ✨ Features

- ➕ Add expenses with equal or custom splits
- 👥 Split bills between friends, roommates, or travel groups
- 💰 View who owes whom with balance tracking
- 🔍 Search through expense history
- 🛡️ Safe delete with confirmation prompts
- 🎨 Beautiful colored terminal output
- ⚡ Fast and lightweight

## 🚀 Quick Start

### 1. Clone & Install

```bash
# Clone the repository
git clone https://github.com/saravananravi08/splitwise-cli.git
cd splitwise-cli

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy the example env file
cp .env.example .env

# Edit .env with your Splitwise credentials
# Get them from: https://secure.splitwise.com/apps
nano .env
```

Your `.env` should look like:
```env
SPLITWISE_CONSUMER_KEY=your_consumer_key
SPLITWISE_CONSUMER_SECRET=your_consumer_secret
SPLITWISE_ACCESS_TOKEN=your_access_token
SPLITWISE_ACCESS_SECRET=your_access_token_secret
DEFAULT_CURRENCY=INR
```

### 3. Run

```bash
# View help
python3 splitwise --help

# Check it works
python3 splitwise user
```

## 📦 Global CLI Installation

### Option 1: Add to PATH (Recommended)

```bash
# Create a symlink in ~/bin
ln -s ~/path/to/splitwise-cli/splitwise ~/bin/splitwise

# Add to ~/.bashrc for persistence
echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Now use from anywhere
splitwise user
splitwise groups
```

### Option 2: Install with pip

```bash
# Install in development mode
pip install -e .

# Or copy the script directly
cp splitwise /usr/local/bin/splitwise
chmod +x /usr/local/bin/splitwise
```

### Option 3: Homebrew (macOS/Linux)

```bash
# Coming soon
brew install splitwise-cli
```

## 📋 Commands

| Command | Description |
|---------|-------------|
| `splitwise user` | Show current user info |
| `splitwise groups` | List all groups |
| `splitwise groups show <name>` | Show group details |
| `splitwise members <group>` | List group members |
| `splitwise expenses [group]` | List expenses |
| `splitwise add <desc> <amount>` | Add expense |
| `splitwise show <id>` | Show expense details |
| `splitwise delete <id>` | Delete expense (safe) |
| `splitwise search <text>` | Search expenses |
| `splitwise balances` | Show all balances |
| `splitwise friends` | List friends |
| `splitwise categories` | List categories |
| `splitwise currencies` | List currencies |

## 💡 Usage Examples

### Add Expenses

```bash
# Equal split with all group members
splitwise add "Dinner" 500 --group "Trip"

# Split with specific people
splitwise add "Coffee" 150 --group "Trip" --split-with "Friend1"

# Custom exact amounts
splitwise add "Groceries" 1000 --group "Trip" \
  --split-with "Friend1" "Friend2" \
  --type exact --amounts 600 400
# Friend1 owes 600, Friend2 owes 400

# Different payer and date
splitwise add "Taxi" 200 --group "Trip" --paid-by "Friend2" --date 2026-04-20
```

### View & Search

```bash
splitwise groups                      # List all groups
splitwise members "Trip"             # List group members
splitwise expenses "Trip"            # List expenses
splitwise show 123456               # Show expense details
splitwise search "dinner"           # Search expenses
```

### Balances

```bash
splitwise balances                    # All balances across friends
splitwise balances "Trip"           # Balances in specific group
```

### Delete (Safe!)

```bash
splitwise delete 123456           # Preview what will be deleted
splitwise delete 123456 --yes    # Confirm and delete
```

## 🔧 Setup API Credentials

### 1. Register Your App

1. Go to [Splitwise Developer Portal](https://secure.splitwise.com/apps)
2. Click **Register your application**
3. Fill in details:
   - Name: `My Splitwise CLI`
   - Callback URL: `http://localhost`
4. Click **Register**
5. Copy **Consumer Key** and **Consumer Secret**

### 2. Get Access Token

You'll receive OAuth tokens during the authorization flow. For testing, you can generate an API key directly from the app page.

### 3. Configure

```bash
cp .env.example .env
# Edit .env with your credentials
```

## 🔒 Security

- ✅ API credentials stored locally in `.env` (not committed to git)
- ✅ `.gitignore` ensures secrets are never pushed
- ✅ Delete commands always require confirmation
- ✅ No data sent to third parties

## 🛠️ Requirements

- Python 3.6+
- `requests`
- `requests-oauthlib`
- `python-dotenv`

Install with:
```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Contributions welcome! Please:
- Fork the repository
- Create a feature branch
- Submit a pull request

## 📄 License

MIT License - feel free to use, modify, and distribute.

## 🔗 Related

- [Splitwise API Documentation](https://dev.splitwise.com/)
- [Official Splitwise App](https://www.splitwise.com/)
- [Python SDK](https://github.com/namaggarwal/splitwise)

---

**Made with ❤️ for Splitwise users who love the terminal**

**Keywords:** splitwise, expense tracker, bill splitter, expense sharing, roommate expenses, trip expenses, command line expense manager, split bills, shared expenses, personal finance, CLI tool
