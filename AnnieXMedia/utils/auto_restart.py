# Authored By Certified Coders © 2025
"""
Auto Restart Module for Saregama Music Bot
Handles scheduled restarts with cleanup and notifications
"""
import asyncio
import os
import sys
import shutil
from datetime import datetime, timedelta
from AnnieXMedia import app, userbot, LOGGER
from AnnieXMedia.core.call import StreamController
from config import LOGGER_ID
import config


class AutoRestart:
    """Manages auto-restart functionality with cleanup and notifications"""
    
    def __init__(self):
        self.restart_interval = 6 * 60 * 60  # 6 hours in seconds
        self.is_restarting = False
        
    async def start_restart_scheduler(self):
        """Start the background task for scheduled restarts"""
        LOGGER("AnnieXMedia").info(f"Auto-restart scheduler started (interval: {self.restart_interval // 3600} hours)")
        await asyncio.sleep(self.restart_interval)
        await self.perform_auto_restart()
        
    async def perform_auto_restart(self):
        """Perform the complete restart process"""
        if self.is_restarting:
            return
            
        self.is_restarting = True
        LOGGER("AnnieXMedia").info("Starting auto-restart process...")
        
        try:
            # Step 1: Send restart notifications
            await self.send_restart_notifications()
            
            # Step 2: Clean up cache and downloads
            await self.cleanup_cache()
            
            # Step 3: Update git repository
            await self.update_git_repo()
            
            # Step 4: Stop current services gracefully
            await self.stop_services()
            
            # Step 5: Restart the bot
            self.restart_bot()
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error during auto-restart: {e}")
            self.is_restarting = False
            # Schedule next restart even if this one failed
            asyncio.create_task(self.start_restart_scheduler())
    
    async def send_restart_notifications(self):
        """Send restart notification messages"""
        try:
            # Message for private chats (users)
            private_msg = """
🎶 ˢᵃʳᵉᵍᵃᵐᵃ ᴹᵘˢⁱᶜ ⁱˢ ᵇᵃᶜᵏ ᵒⁿˡⁱⁿᵉ! 😎

ᴵ ʲᵘˢᵗ ᵗᵒᵒᵏ ᵃ ˢᵐᵃˡˡ ⁿᵃᵖ ᵃⁿᵈ ʳᵉˢᵗᵃʳᵗᵉᵈ ᵐʸ ᵐᵘˢⁱᶜᵃˡ ᵇʳᵃⁱⁿ 🧠🎧
ᴺᵒʷ ᴵ'ᵐ ᶠʳᵉˢʰ ᵃⁿᵈ ʳᵉᵃᵈʸ ᵗᵒ ᵖˡᵃʸ ʸᵒᵘʳ ᶠᵃᵛᵒʳⁱᵗᵉ ˢᵒⁿᵍˢ ᵃᵍᵃⁱⁿ.

ˢᵉⁿᵈ /play ᵃⁿᵈ ˡᵉᵗ ᵗʰᵉ ˢᵃ ᴿᵉ ᴳᵃ ᴹᵃ ᵛⁱᵇᵉˢ ᵇᵉᵍⁱⁿ 🎤🔥
"""
            
            # Message for group chats
            group_msg = """
🚨 ᴬᵗᵗᵉⁿᵗⁱᵒⁿ ᴹᵘˢⁱᶜ ᴸᵒᵛᵉʳˢ!

ˢᵃʳᵉᵍᵃᵐᵃ ᴹᵘˢⁱᶜ ʰᵃˢ ʳᵉˢᵗᵃʳᵗᵉᵈ ᵃⁿᵈ ⁱˢ ᵇᵃᶜᵏ ⁱⁿ ᵗʰᵉ ᵍʳᵒᵘᵖ 😎
ᴰᴶ ⁱˢ ᵒⁿˡⁱⁿᵉ ᵃᵍᵃⁱⁿ 🎧

ᴳʳᵒᵘᵖ ˢⁱˡᵉⁿᵗ? ᴺᵒᵗ ᵃⁿʸᵐᵒʳᵉ.
ˢᵉⁿᵈ /play ᵃⁿᵈ ˡᵉᵗ ᵗʰᵉ ᵖᵃʳᵗʸ ˢᵗᵃʳᵗ 🔥🎶
"""
            
            # Message for log channel
            log_msg = """
🟢 ˢᵃʳᵉᵍᵃᵐᵃ ᴹᵘˢⁱᶜ ᴿᵉˢᵗᵃʳᵗᵉᵈ ˢᵘᶜᶜᵉˢˢᶠᵘˡˡʸ

ˢʸˢᵗᵉᵐ ʳᵉᵇᵒᵒᵗ ᶜᵒᵐᵖˡᵉᵗᵉᵈ ⚙️
ᴹᵘˢⁱᶜ ᵉⁿᵍⁱⁿᵉ ˡᵒᵃᵈᵉᵈ 🎧
ⱽᵒⁱᶜᵉ ᶜʰᵃᵗ ᵐᵒᵈᵘˡᵉ ʳᵉᵃᵈʸ 🎶
ᴬˡˡ ˢᵉʳᵛⁱᶜᵉˢ ʳᵘⁿⁿⁱⁿᵍ ⁿᵒʳᵐᵃˡˡʸ.

ᴮᵒᵗ ⁱˢ ⁿᵒʷ ʳᵉᵃᵈʸ ᵗᵒ ˢᵗʳᵉᵃᵐ ˢᵒⁿᵍˢ 🚀
"""
            
            # Send to log channel
            try:
                await app.send_message(
                    config.LOGGER_ID,
                    log_msg.strip()
                )
                LOGGER("AnnieXMedia").info("Log message sent successfully")
            except Exception as e:
                LOGGER("AnnieXMedia").error(f"Failed to send log message: {e}")
                
            # Store messages for sending after restart
            self.pending_messages = {
                "private": private_msg.strip(),
                "group": group_msg.strip(),
                "log": log_msg.strip()
            }
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error sending notifications: {e}")
    
    async def cleanup_cache(self):
        """Clean up cache and download directories"""
        try:
            LOGGER("AnnieXMedia").info("Starting cache cleanup...")
            
            # Directories to clean
            cleanup_dirs = [
                "downloads",
                "cache",
                "couples",
            ]
            
            for dir_name in cleanup_dirs:
                dir_path = os.path.join(os.path.dirname(__file__), "..", "..", dir_name)
                if os.path.exists(dir_path):
                    # Remove all files in directory
                    for filename in os.listdir(dir_path):
                        file_path = os.path.join(dir_path, filename)
                        try:
                            if os.path.isfile(file_path):
                                os.unlink(file_path)
                            elif os.path.isdir(file_path):
                                shutil.rmtree(file_path)
                        except Exception as e:
                            LOGGER("AnnieXMedia").warning(f"Error cleaning {file_path}: {e}")
                    
                    LOGGER("AnnieXMedia").info(f"Cleaned {dir_name} directory")
            
            # Clean specific temp files
            temp_patterns = [
                "*.jpg",
                "*.png",
                "*.mp3",
                "*.mp4",
            ]
            
            LOGGER("AnnieXMedia").info("Cache cleanup completed")
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error during cache cleanup: {e}")
    
    async def update_git_repo(self):
        """Update git repository if changes exist"""
        try:
            LOGGER("AnnieXMedia").info("Checking for git updates...")
            
            # Check if .git directory exists
            git_dir = os.path.join(os.path.dirname(__file__), "..", "..", ".git")
            if not os.path.exists(git_dir):
                LOGGER("AnnieXMedia").info("Not a git repository, skipping update")
                return
            
            # Pull latest changes
            process = await asyncio.create_subprocess_exec(
                "git", "pull", "origin", "main", "--ff-only",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=os.path.dirname(os.path.dirname(__file__))
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                if stdout and b"Already up to date" not in stdout:
                    LOGGER("AnnieXMedia").info(f"Git updated: {stdout.decode()}")
                else:
                    LOGGER("AnnieXMedia").info("Git repository already up to date")
            else:
                LOGGER("AnnieXMedia").warning(f"Git pull failed: {stderr.decode()}")
                
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error updating git repo: {e}")
    
    async def stop_services(self):
        """Gracefully stop bot services"""
        try:
            LOGGER("AnnieXMedia").info("Stopping services gracefully...")
            
            # Stop voice chats
            try:
                await StreamController.stop_stream_all()
            except:
                pass
            
            # Give time for disconnection
            await asyncio.sleep(2)
            
            LOGGER("AnnieXMedia").info("Services stopped")
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error stopping services: {e}")
    
    def restart_bot(self):
        """Restart the bot process"""
        try:
            LOGGER("AnnieXMedia").info("Restarting bot process...")
            
            # Set restart flag in environment
            os.environ["RESTART_REASON"] = "auto_restart_6h"
            os.environ["RESTART_TIME"] = str(datetime.now().timestamp())
            
            # Restart using python executable
            python = sys.executable
            script = os.path.abspath(__file__)
            main_script = os.path.join(os.path.dirname(script), "__main__.py")
            
            # Close current processes
            os.execl(python, python, main_script)
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error restarting bot: {e}")
            self.is_restarting = False
    
    async def send_post_restart_messages(self):
        """Send restart completion messages to active chats"""
        try:
            if not hasattr(self, 'pending_messages'):
                return
                
            # Get list of active chats from database
            from AnnieXMedia.utils.database import get_active_chats
            
            active_chats = await get_active_chats()
            
            for chat_id in active_chats[:10]:  # Limit to first 10 chats
                try:
                    # Determine chat type
                    chat = await app.get_chat(chat_id)
                    
                    if chat.type == "private":
                        msg = self.pending_messages.get("private")
                    else:
                        msg = self.pending_messages.get("group")
                    
                    if msg:
                        await app.send_message(chat_id, msg)
                        await asyncio.sleep(0.5)  # Small delay
                        
                except Exception:
                    continue
            
            # Clear pending messages
            delattr(self, 'pending_messages')
            
        except Exception as e:
            LOGGER("AnnieXMedia").error(f"Error sending post-restart messages: {e}")


# Global instance
auto_restart = AutoRestart()


async def start_auto_restart():
    """Initialize auto-restart scheduler"""
    LOGGER("AnnieXMedia").info("Initializing auto-restart scheduler (6 hours interval)...")
    asyncio.create_task(auto_restart.start_restart_scheduler())


async def check_restart_status():
    """Check if bot was restarted and send appropriate messages"""
    try:
        restart_reason = os.environ.get("RESTART_REASON")
        
        if restart_reason == "auto_restart_6h":
            LOGGER("AnnieXMedia").info("Bot restarted via auto-restart scheduler")
            
            # Send post-restart messages
            await auto_restart.send_post_restart_messages()
            
            # Clear restart flags
            os.environ.pop("RESTART_REASON", None)
            os.environ.pop("RESTART_TIME", None)
            
            # Schedule next restart
            await start_auto_restart()
            
    except Exception as e:
        LOGGER("AnnieXMedia").error(f"Error checking restart status: {e}")
