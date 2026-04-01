#!/usr/bin/env python3
import os
import re

def fix_return_await_in_file(filepath):
    """Fix 'return await X.answer(...)' pattern in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to match: return await <something>.answer(...) or return await callback.answer(...)
    # We need to be careful not to match edit_message_text which returns Message objects
    
    # Simple pattern for .answer( with show_alert
    pattern = r'return await\s+(\w+)\.answer\(([^)]*show_alert[^)]*)\)'
    
    def replacement(match):
        obj = match.group(1)
        args = match.group(2)
        return f'await {obj}.answer({args})\n        return'
    
    new_content = re.sub(pattern, replacement, content)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Fixed: {filepath}")
        return True
    return False

# Files to fix
files_to_fix = [
    "AnnieXMedia/plugins/Manager/language.py",
    "AnnieXMedia/plugins/Manager/zombie.py", 
    "AnnieXMedia/plugins/Manager/del_msg.py",
    "AnnieXMedia/plugins/Manager/mass_actions.py",
    "AnnieXMedia/plugins/tools/dev.py",
    "AnnieXMedia/plugins/misc/tts.py",
    "AnnieXMedia/plugins/bot/settings.py",  # For remaining instances
    "AnnieXMedia/plugins/admins/speed.py",  # For remaining instances
]

base_path = "/Users/nishkarshkr/Desktop/music bot/Saregama"

for filepath in files_to_fix:
    full_path = os.path.join(base_path, filepath)
    if os.path.exists(full_path):
        fix_return_await_in_file(full_path)
    else:
        print(f"Not found: {full_path}")

print("\nDone!")
