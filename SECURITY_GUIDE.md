# 🔒 Security Guide - Protecting Your Credentials

## ⚠️ CRITICAL: Never Commit These Files!

### 1. **Environment File (.env)**
Contains sensitive credentials that should NEVER be public:
- `API_ID` & `API_HASH` - Your Telegram API credentials
- `BOT_TOKEN` - Your Telegram bot authentication
- `MONGO_DB_URI` - Database connection string with password
- `STRING_SESSION` - User session (gives access to your account!)
- `OWNER_ID`, `SUDO_USERS` - Admin user IDs
- Any API keys or passwords

### 2. **Session Files**
- `*.session` - Pyrogram session files (account access)
- `*.session-journal` - Session journal files

### 3. **Logs**
- `log.txt` - May contain sensitive information

---

## ✅ Safe to Commit

These files are safe and necessary for the repository:
- Source code (`.py` files)
- Configuration files (without secrets)
- `requirements.txt` - Dependencies list
- `.gitignore` - Git ignore rules
- `README.md` - Documentation
- `.env.example` - Template showing required variables (no real values)
- Asset files (images, fonts in AnnieXMedia/assets/)

---

## 🛡️ How We Protected This Repository

### What's in .gitignore:
```
.env                    # Environment variables
*.session              # Session files
*.session-journal      # Session journals
log.txt                # Logs
cache/                 # Cache files
downloads/             # Downloaded files
__pycache__/           # Python cache
.DS_Store              # Mac OS files
```

### Using .env.example:
We've created a `.env.example` file that shows what environment variables are needed without exposing actual values. Users can copy this template and fill in their own credentials.

---

## 📋 Setup Instructions for Users

When someone clones this repository, they should:

1. **Copy the example file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env with their credentials:**
   ```bash
   nano .env
   ```

3. **Required variables:**
   - `API_ID` - Get from https://my.telegram.org
   - `API_HASH` - Get from https://my.telegram.org
   - `BOT_TOKEN` - Get from @BotFather on Telegram
   - `OWNER_ID` - Your Telegram user ID
   - `MONGO_DB_URI` - MongoDB connection string
   - `STRING_SESSION` - Generate using session generator
   - Other variables as needed

4. **NEVER commit .env to Git!**

---

## 🚨 If You Accidentally Committed Secrets

### Immediate Actions:

1. **Rotate/Change ALL exposed credentials immediately:**
   - Get new API_ID and API_HASH from my.telegram.org
   - Get new BOT_TOKEN from BotFather
   - Change MongoDB password and get new connection string
   - Generate new STRING_SESSION

2. **Remove secrets from git history:**
   ```bash
   # Install BFG Repo-Cleaner
   brew install bfg
   
   # Remove .env file from all commits
   bfg --delete-files .env
   
   # Or remove specific patterns
   bfg --replace-text passwords.txt
   
   # Force push cleaned history
   git push --force
   ```

3. **Check GitHub Secret Scanning:**
   GitHub may have already detected and blocked the secrets. Check:
   - Go to your repository Settings
   - Click "Code security and analysis"
   - Check "Secret scanning" alerts

---

## 🔍 Checking for Leaked Secrets

### Before pushing, always check:

1. **What files will be committed:**
   ```bash
   git status
   ```

2. **Search for potential secrets:**
   ```bash
   grep -r "sk-" . --include="*.py"
   grep -r "password" . --include="*.py"
   grep -r "token" . --include="*.py"
   grep -r "api_key" . --include="*.py"
   ```

3. **Check git diff:**
   ```bash
   git diff --cached
   ```

---

## 📝 Best Practices

### DO ✅:
- Use environment variables for all secrets
- Keep `.env` file in `.gitignore`
- Use `.env.example` as a template
- Rotate credentials regularly
- Use strong, unique passwords
- Enable 2FA where possible
- Use separate credentials for development and production

### DON'T ❌:
- Never commit `.env` files
- Never hardcode credentials in source code
- Never share your session strings
- Never use the same token across multiple projects
- Never store passwords in plain text
- Never commit database URLs with credentials

---

## 🆘 Emergency Contacts

If you think your credentials have been compromised:

1. **Telegram Bot Token:** Contact @BotFather immediately
2. **Telegram API:** Revoke and recreateate at my.telegram.org
3. **MongoDB:** Change password and regenerate connection string
4. **Heroku:** Regenerate API key in account settings

---

## 🔐 Additional Security Measures

### For Production Deployment:

1. **Use environment variables on server:**
   ```bash
   export API_ID=your_id
   export API_HASH=your_hash
   ```

2. **Use secret management tools:**
   - HashiCorp Vault
   - AWS Secrets Manager
   - Azure Key Vault
   - Doppler

3. **Enable GitHub Secret Scanning:**
   - Go to repo Settings > Code security and analysis
   - Enable "Secret scanning"

4. **Use pre-commit hooks:**
   ```bash
   pip install detect-secrets
   detect-secrets scan --baseline .secrets.baseline
   ```

---

**Remember:** Security is everyone's responsibility. Always double-check before committing!
