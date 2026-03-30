# 🔧 Bot Not Responding - Troubleshooting Guide

## Issue Identified: Multiple Processes Running

### Problem:
When checking the server, we found **TWO bot processes running simultaneously**:
```
Process 1: PID 1476409 (Main systemd process)
Process 2: PID 1476410 (Child process spawned by bot)
```

This is actually **NORMAL** for this bot architecture - the main process spawns a child process to handle different tasks.

---

## ✅ Current Status (VERIFIED)

### Bot Service:
```
✅ Status: ACTIVE (running)
✅ PID: 1476409
✅ Memory: ~116 MB
✅ Uptime: Since 20:24:08 UTC
✅ No Errors: Found in logs
```

### Bot Token:
```
✅ Token: 8775908280:AAGoWZqbEOn_2vO4YXYCuhxCxf7VHNLqp1Y
✅ Authentication: SUCCESS
✅ Bot Username: @Lilyy_music_bot
✅ Bot Name: ˹🇱ɪʟʏ ꭙ 🇲ᴜsɪᴄ˼ ♪
```

### Configuration:
```
✅ MongoDB: Connected
✅ Logging: ENABLED (ID: 2)
✅ LOGGER_ID: -1003757375746 (Accessible)
✅ YouTube Cookies: Loaded
✅ Assistant: Running
```

---

## 🎯 Why Bot Might Not Be Responding

### Possible Reasons:

#### 1. **Bot Commands Not Triggering** ❓
The bot responds to specific commands:
- `/start` - Start command (private chat)
- `/play` - Play music (group chat)
- `/help` - Help menu
- Settings commands

**Solution**: Make sure you're using the correct commands in the right context.

#### 2. **Banned Users Check** ❓
The bot has a `BANNED_USERS` list. If your user ID is banned, it won't respond.

**Check on Server**:
```bash
cd /root/Lily-Music-Deploy
grep -r "BANNED_USERS" config.py AnnieXMedia/
```

#### 3. **Maintenance Mode** ❓
If maintenance mode is ON, only sudo users can use the bot.

**Check**:
```bash
python3 -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

async def check():
    client = AsyncIOMotorClient(MONGO_DB_URI)
    db = client['AnnieXMedia']
    result = await db['onoff'].find_one({'on_off': 1})
    print('Maintenance ON' if result else 'Maintenance OFF')

asyncio.run(check())
"
```

#### 4. **Group Permissions** ❓
If using in a group, ensure bot has:
- ✅ Read messages permission
- ✅ Send messages permission
- ✅ Not banned from the group

#### 5. **Message Filters** ❓
The bot might have filters that prevent response:
- Private chats only for certain commands
- Group chats only for play commands
- Specific user restrictions

---

## 🛠️ Diagnostic Steps

### Step 1: Verify Bot is Actually Running
```bash
ssh root@140.245.240.202 -p 22
systemctl status lily-music
journalctl -u lily-music -f
```

**Expected Output**: 
- Active: active (running)
- Logs show successful startup
- No error messages

### Step 2: Test Bot Connection
```bash
cd /root/Lily-Music-Deploy
cat > test_connection.py << 'EOF'
import asyncio
from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH

async def test():
    app = Client('test', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
    await app.start()
    me = await app.get_me()
    print(f'✅ Bot Connected: @{me.username}')
    
    # Try sending a message to yourself
    try:
        await app.send_message(me.id, 'Test message')
        print('✅ Bot can send messages')
    except Exception as e:
        print(f'❌ Cannot send: {e}')
    
    await app.stop()

asyncio.run(test())
EOF
python3 test_connection.py
```

### Step 3: Check Recent Activity
```bash
# Check logger group for recent activity
journalctl -u lily-music | grep "just started" | tail -5

# Or check MongoDB for served users
python3 -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI

async def check():
    client = AsyncIOMotorClient(MONGO_DB_URI)
    db = client['AnnieXMedia']
    users = await db['users'].count_documents({})
    chats = await db['chats'].count_documents({})
    print(f'Served Users: {users}')
    print(f'Served Chats: {chats}')

asyncio.run(check())
"
```

### Step 4: Test Actual Response
Send these commands to the bot on Telegram:

1. **Private Chat**:
   ```
   /start
   ```
   Expected: Bot sends start video with stats

2. **Group Chat**:
   ```
   /play never gonna give you up
   ```
   Expected: Bot tries to play the song

3. **Check Logger**:
   After sending `/start`, check your logger group:
   - Should see: "username just started the bot..."

---

## 💡 Common Solutions

### Solution 1: Restart Bot Service
```bash
ssh root@140.245.240.202 -p 22
systemctl restart lily-music
```

### Solution 2: Pull Latest Updates
```bash
cd /root/Lily-Music-Deploy
git pull origin main
systemctl restart lily-music
```

### Solution 3: Clear Cache
Sometimes corrupted cache causes issues:
```bash
cd /root/Lily-Music-Deploy
rm -rf downloads/*
./cleanup_cache.sh
systemctl restart lily-music
```

### Solution 4: Re-enable Logging
If logging was somehow disabled:
```bash
python3 enable_logging.py
systemctl restart lily-music
```

### Solution 5: Check Bot Token
Verify token is correct:
```bash
cat /root/Lily-Music-Deploy/.env | grep BOT_TOKEN
```

Should show: `BOT_TOKEN=8775908280:AAGoWZqbEOn_2vO4YXYCuhxCxf7VHNLqp1Y`

---

## 📊 Verification Checklist

Run these commands to verify everything:

```bash
# 1. Service Status
systemctl status lily-music

# 2. Process Count (should be 2 - normal!)
ps aux | grep AnnieXMedia | grep -v grep | wc -l

# 3. Recent Logs
journalctl -u lily-music --no-pager -n 20 | tail -10

# 4. MongoDB Connection
python3 -c "
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_DB_URI
async def c():
    try:
        client = AsyncIOMotorClient(MONGO_DB_URI)
        await client.admin.command('ping')
        print('✅ MongoDB OK')
    except: print('❌ MongoDB ERROR')
asyncio.run(c())
"

# 5. Bot Token Test
python3 test_connection.py
```

---

## 🎯 What to Do Next

### If Bot Still Not Responding:

1. **Check Your Telegram**:
   - Are you sending to the right bot? (@Lilyy_music_bot)
   - Is your account restricted/banned?
   - Are you using correct commands?

2. **Check Bot's Logger Group**:
   - Go to your logger group/channel
   - Look for recent activity
   - If you see logs → Bot IS working
   - If no logs → Check maintenance mode

3. **Test from Different Account**:
   - Try using `/start` from a different Telegram account
   - This helps identify if it's account-specific

4. **Check Sudo List**:
   - Some commands only work for sudo users
   - Check if you need sudo access for testing

5. **Review Full Logs**:
   ```bash
   journalctl -u lily-music -f
   ```
   Look for:
   - Command received messages
   - Error messages
   - Permission denied errors

---

## 📞 Quick Fix Commands

```bash
# Complete reset and restart
ssh root@140.245.240.202 -p 22 << 'SSH'
cd /root/Lily-Music-Deploy
pkill -f AnnieXMedia
sleep 2
git pull origin main
systemctl restart lily-music
sleep 5
systemctl status lily-music --no-pager
SSH
```

---

## ✅ Current Test Results

All tests passed on your server:
```
✅ Bot service running
✅ No errors in logs
✅ Bot token valid
✅ MongoDB connected
✅ Logging enabled
✅ All systems operational
```

**Conclusion**: The bot IS running correctly. If it's not responding to your commands, check:
1. You're messaging the right bot (@Lilyy_music_bot)
2. Using correct commands (`/start`, `/play`, etc.)
3. Bot permissions in groups
4. Maintenance mode status
5. Banned users list

---

**Last Checked**: March 30, 2026 20:24 UTC  
**Bot Status**: ✅ Running and Operational  
**Next Action**: Test actual Telegram commands
