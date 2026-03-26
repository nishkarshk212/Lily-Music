# 🎨 Thumbnail Generator Usage Guide

## Overview
The thumbnail generator creates beautiful, professional-looking thumbnails with blur background effects for your music bot's now playing messages.

## Features
- ✨ Blurred background from original thumbnail
- 🎵 Circular album art overlay
- 📝 Title, duration, and views display
- 🎨 Custom branding (Saregama Music)
- 📊 Visual progress bar
- 💾 Automatic file management

## Basic Usage

### 1. Simple Thumbnail Generation

```python
from AnnieXMedia.utils import create_thumbnail

# Generate thumbnail
thumb_path = create_thumbnail(
    title="Shape of You",
    duration="3:54",
    views="5,892,341",
    thumbnail_url="https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg",
    output="downloads/custom_thumb.png"
)
```

### 2. Send Now Playing Message with Thumbnail

```python
from AnnieXMedia.utils import send_now_playing

# In your play command handler
@Client.on_message(filters.command("play"))
async def play_command(client, message):
    # ... your existing code ...
    
    # Get track details
    title = "Shape of You"
    duration = "3:54"
    thumbnail_url = "https://img.youtube.com/vi/JGwWNGJdvx8/maxresdefault.jpg"
    user = message.from_user
    
    # Send beautiful now playing message
    await send_now_playing(
        message=message,
        title=title,
        duration=duration,
        thumbnail_url=thumbnail_url,
        user=user,
        views="5892341"
    )
```

### 3. Manual Thumbnail with Custom Caption

```python
from AnnieXMedia.utils import create_thumbnail, progress_bar

# Generate thumbnail
thumb = create_thumbnail(
    title=title,
    duration=duration_min,
    views=views,
    thumbnail_url=thumbnail,
    output=f"downloads/thumb_{videoid}.png"
)

# Send message
if thumb:
    await message.reply_photo(
        photo=thumb,
        caption=f"""
**✦ STARTED STREAMING**

○ **TITLE :** `{title}`
○ **DURATION :** `{duration_min}`
○ **BY :** `{user.mention}`

**{progress_bar(current_time, total_duration)}**

🎧 Now Playing in Voice Chat
""",
        parse_mode="Markdown"
    )
```

## Function Parameters

### `create_thumbnail()`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `title` | str | ✅ Yes | - | Song/video title |
| `duration` | str | ✅ Yes | - | Duration (e.g., "3:54") |
| `views` | str | ❌ No | "0" | View count |
| `thumbnail_url` | str | ❌ No | None | YouTube thumbnail URL |
| `output` | str | ❌ No | "thumb.png" | Output filename |

### `progress_bar()`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `current` | float | ✅ Yes | - | Current playback position |
| `total` | float | ✅ Yes | - | Total duration |
| `length` | int | ❌ No | 20 | Bar length in characters |

### `send_now_playing()`

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `message` | Message | ✅ Yes | - | Pyrogram message object |
| `title` | str | ✅ Yes | - | Song title |
| `duration` | str | ✅ Yes | - | Song duration |
| `thumbnail_url` | str | ❌ No | None | Thumbnail URL |
| `user` | User | ❌ No | None | User who requested |
| `views` | str | ❌ No | "0" | View count |

## Example Output

The generated thumbnail will have:
- **Blurred background** from the original thumbnail
- **Circular album art** on the left side
- **Title text** (auto-wrapped if too long)
- **Views count** with eye emoji
- **Duration** with clock emoji
- **Bot branding** at the bottom in pink
- **White gradient line** under album art

## Error Handling

If thumbnail generation fails, the functions will:
1. Return `None` (for `create_thumbnail`)
2. Fall back to text-only message (for `send_now_playing`)
3. Log error to console

```python
try:
    thumb = create_thumbnail(title, duration, thumbnail_url=thumb_url)
    if thumb:
        await message.reply_photo(photo=thumb, caption=caption)
    else:
        await message.reply_text("🎵 Now Playing: " + title)
except Exception as e:
    print(f"Thumbnail error: {e}")
    await message.reply_text(f"Playing: {title}")
```

## Advanced: Custom Styling

You can modify the thumbnail style by editing `thumbnail_generator.py`:

```python
# Change colors
overlay = Image.new("RGBA", bg.size, (0, 0, 0, 140))  # Dark overlay
draw.text((450, 250), title, font=font_title, fill="#FF69B4")  # Pink text

# Change position
bg.paste(album, (80, 200), mask)  # (x, y) coordinates

# Add more info
draw.text((450, 500), f"Artist: {artist}", font=font_small, fill="white")
```

## Performance Tips

1. **Reuse thumbnails**: Save to cache and reuse if same video
2. **Async processing**: Generate thumbnail while downloading audio
3. **Size limits**: Keep images at 1280x720 for optimal performance
4. **Cleanup**: Delete old thumbnails from downloads folder

## Integration with Existing Code

Find where your bot sends the now playing message and replace:

**Before:**
```python
await message.reply_photo(
    photo=details["thumb"],
    caption=_["play_10"].format(title, duration)
)
```

**After:**
```python
from AnnieXMedia.utils import send_now_playing

await send_now_playing(
    message=message,
    title=details["title"],
    duration=details["duration_min"],
    thumbnail_url=details["thumb"],
    user=message.from_user
)
```

---

**Created for Saregama Music Bot** 🎵
Enhance your users' experience with beautiful thumbnails!
