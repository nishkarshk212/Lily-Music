# Authored By Certified Coders © 2025
"""
Thumbnail Generator for Saregama Music Bot
Creates beautiful thumbnails with blur background and track info
"""
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
import os


def create_thumbnail(
    title: str,
    duration: str,
    views: str = "0",
    thumbnail_url: str = None,
    output: str = "thumb.png"
) -> str:
    """
    Create a beautiful thumbnail with blur background and track information
    
    Args:
        title: Song/video title
        duration: Duration of the track
        views: View count (optional)
        thumbnail_url: URL of the thumbnail image
        output: Output filename
        
    Returns:
        Path to saved thumbnail
    """
    try:
        # Download thumbnail if URL provided
        if thumbnail_url:
            response = requests.get(thumbnail_url, timeout=10)
            img = Image.open(BytesIO(response.content)).convert("RGB")
        else:
            # Create default background if no URL
            img = Image.new("RGB", (1280, 720), color=(30, 30, 30))
        
        # Resize to standard size
        img = img.resize((1280, 720))
        
        # Create blurred background
        try:
            from PIL import ImageFilter
            bg = img.filter(ImageFilter.GaussianBlur(radius=15))
        except:
            bg = img.filter(Image.BLUR)
        
        # Add dark overlay for better text visibility
        overlay = Image.new("RGBA", bg.size, (0, 0, 0, 140))
        bg.paste(overlay, (0, 0), overlay)
        
        draw = ImageDraw.Draw(bg)
        
        # Try to load fonts (fallback to default if not found)
        try:
            font_title = ImageFont.truetype("arial.ttf", 48)
            font_small = ImageFont.truetype("arial.ttf", 32)
            font_large = ImageFont.truetype("arial.ttf", 56)
        except:
            font_title = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_large = ImageFont.load_default()
        
        # Create circular album art from original image
        album_size = 320
        album = img.resize((album_size, album_size), Image.Resampling.LANCZOS)
        
        # Create circular mask
        mask = Image.new("L", (album_size, album_size), 0)
        d = ImageDraw.Draw(mask)
        d.ellipse((0, 0, album_size, album_size), fill=255)
        
        # Paste circular album art on the left side
        bg.paste(album, (80, 200), mask)
        
        # Draw gradient line under album art
        for i in range(4):
            alpha = 180 - (i * 30)
            line = Image.new("RGBA", (340, 4), (255, 255, 255, alpha))
            bg.paste(line, (80, 540 + i), line)
        
        # Add title text (wrap if too long)
        max_chars = 50
        if len(title) > max_chars:
            title_lines = [title[:max_chars], title[max_chars:max_chars*2]]
        else:
            title_lines = [title]
        
        y_position = 250
        for line in title_lines:
            draw.text((450, y_position), line, font=font_title, fill="white")
            y_position += 60
        
        # Add views count
        if views and views != "0":
            draw.text(
                (450, 380),
                f"👁️ {format_number(views)} views",
                font=font_small,
                fill="#CCCCCC"
            )
        
        # Add duration badge
        draw.text(
            (450, 440),
            f"⏱️ Duration: {duration}",
            font=font_small,
            fill="#CCCCCC"
        )
        
        # Add bot branding at bottom
        draw.text(
            (640, 650),
            "♪ SAREGAMA MUSIC ♪",
            font=font_small,
            fill="#FF69B4",
            anchor="mm"
        )
        
        # Save thumbnail
        bg.save(output, "PNG", quality=95)
        return output
        
    except Exception as e:
        print(f"[Thumbnail Error] {e}")
        # Return default thumbnail if generation fails
        return None


def format_number(num: str) -> str:
    """Format large numbers to K/M format"""
    try:
        num_int = int(num)
        if num_int >= 1000000:
            return f"{num_int/1000000:.1f}M"
        elif num_int >= 1000:
            return f"{num_int/1000:.1f}K"
        return str(num_int)
    except:
        return str(num)


def progress_bar(current: float, total: float, length: int = 20) -> str:
    """
    Create a visual progress bar
    
    Args:
        current: Current position
        total: Total duration
        length: Length of the bar
        
    Returns:
        Formatted progress bar string
    """
    try:
        percentage = current / total
        filled_length = int(length * percentage)
        empty_length = length - filled_length
        
        bar = "●" * filled_length + "▬" * empty_length
        return f"{bar}"
    except:
        return "▬" * length


async def send_now_playing(
    message,
    title: str,
    duration: str,
    thumbnail_url: str = None,
    user=None,
    views: str = "0"
):
    """
    Send a now playing message with thumbnail
    
    Args:
        message: Pyrogram message object
        title: Song title
        duration: Song duration
        thumbnail_url: YouTube thumbnail URL
        user: User who requested the song
        views: View count
    """
    try:
        # Generate thumbnail
        thumb_path = create_thumbnail(
            title=title,
            duration=duration,
            views=views,
            thumbnail_url=thumbnail_url,
            output=f"downloads/thumb_{title.replace(' ', '_')[:20]}.png"
        )
        
        # Format caption
        caption = f"""
**✦ STARTED STREAMING**

○ **TITLE :** `{title[:50]}`
○ **DURATION :** `{duration}`
○ **BY :** `{user.mention if user else 'Unknown'}`

**{progress_bar(0, 1)}**

🎧 Now Playing in Voice Chat
"""
        
        # Send message
        if thumb_path and os.path.exists(thumb_path):
            await message.reply_photo(
                photo=thumb_path,
                caption=caption,
                parse_mode="Markdown"
            )
        else:
            await message.reply_text(caption)
            
    except Exception as e:
        print(f"[Now Playing Error] {e}")
        # Fallback to simple text message
        await message.reply_text(
            f"🎵 **Now Playing:** `{title}`\n"
            f"⏱️ **Duration:** `{duration}`\n"
            f"👤 **Requested by:** `{user.mention if user else 'Unknown'}`"
        )


def format_number(num: str) -> str:
    """Format large numbers to K/M format"""
    try:
        num_int = int(num)
        if num_int >= 1000000:
            return f"{num_int/1000000:.1f}M"
        elif num_int >= 1000:
            return f"{num_int/1000:.1f}K"
        return str(num_int)
    except:
        return str(num)


def progress_bar(current: float, total: float, length: int = 20) -> str:
    """
    Create a visual progress bar
    
    Args:
        current: Current position
        total: Total duration
        length: Length of the bar
        
    Returns:
        Formatted progress bar string
    """
    try:
        percentage = current / total
        filled_length = int(length * percentage)
        empty_length = length - filled_length
        
        bar = "●" * filled_length + "▬" * empty_length
        return f"{bar}"
    except:
        return "▬" * length


async def send_now_playing(
    message,
    title: str,
    duration: str,
    thumbnail_url: str = None,
    user=None,
    views: str = "0"
):
    """
    Send a now playing message with thumbnail
    
    Args:
        message: Pyrogram message object
        title: Song title
        duration: Song duration
        thumbnail_url: YouTube thumbnail URL
        user: User who requested the song
        views: View count
    """
    try:
        # Generate thumbnail
        thumb_path = create_thumbnail(
            title=title,
            duration=duration,
            views=views,
            thumbnail_url=thumbnail_url,
            output=f"downloads/thumb_{title.replace(' ', '_')[:20]}.png"
        )
        
        # Format caption
        caption = f"""
**✦ STARTED STREAMING**

○ **TITLE :** `{title[:50]}`
○ **DURATION :** `{duration}`
○ **BY :** `{user.mention if user else 'Unknown'}`

**{progress_bar(0, 1)}**

🎧 Now Playing in Voice Chat
"""
        
        # Send message
        if thumb_path and os.path.exists(thumb_path):
            await message.reply_photo(
                photo=thumb_path,
                caption=caption,
                parse_mode="Markdown"
            )
        else:
            await message.reply_text(caption)
            
    except Exception as e:
        print(f"[Now Playing Error] {e}")
        # Fallback to simple text message
        await message.reply_text(
            f"🎵 **Now Playing:** `{title}`\n"
            f"⏱️ **Duration:** `{duration}`\n"
            f"👤 **Requested by:** `{user.mention if user else 'Unknown'}`"
        )
