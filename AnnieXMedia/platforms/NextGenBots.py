# Authored By Certified Coders © 2025
"""
NexGenBots API Integration for YouTube Search
API Documentation: https://console.nexgenbots.xyz/dashboard
"""
import asyncio
import aiohttp
from typing import List, Dict, Optional
from AnnieXMedia import LOGGER
from config import API_KEY


class NexGenBotsSearch:
    """NexGenBots API Client for YouTube song downloads
    API: https://pvtz.nexgenbots.xyz/docs
    """
    
    def __init__(self):
        self.base_url = "https://pvtz.nexgenbots.xyz"
        self.song_url = f"{self.base_url}/song"
        self.api_key = API_KEY or "NxGBNexGenBots448436"
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession(
                headers={
                    "User-Agent": "AnnieXMusic/1.0"
                }
            )
        return self.session
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_video_download(self, video_id: str, format: str = "mp4") -> Optional[str]:
        """
        Get download URL for a specific video using NexGenBots API
        Uses the /song endpoint with format parameter to get video
        
        Args:
            video_id: YouTube video ID
            format: Desired format (mp4, webm, etc.)
            
        Returns:
            Download URL or None
        """
        if not self.api_key:
            LOGGER("NexGenBots").warning("API_KEY not configured, falling back to default")
        
        try:
            session = await self._get_session()
            
            # Use /song/{vidid} endpoint with api and format parameters
            url = f"{self.song_url}/{video_id}"
            params = {
                "api": self.api_key,
                "format": format
            }
            
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    LOGGER("NexGenBots").info(f"Got video download URL for {video_id} in {format} format")
                    return data  # Return full response for processing
                elif response.status == 401:
                    LOGGER("NexGenBots").error("Invalid API key!")
                    return None
                else:
                    LOGGER("NexGenBots").error(f"Video API error: {response.status}")
                    try:
                        error_data = await response.json()
                        LOGGER("NexGenBots").error(f"Error details: {error_data}")
                    except:
                        pass
                    return None
                    
        except asyncio.TimeoutError:
            LOGGER("NexGenBots").error("Request timeout!")
            return None
        except Exception as e:
            LOGGER("NexGenBots").error(f"Failed to get video: {e}")
            return None
    
    async def get_song_download(self, video_id: str) -> Optional[str]:
        """
        Get download URL for a specific song/video using NexGenBots API
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Download URL or None
        """
        if not self.api_key:
            LOGGER("NexGenBots").warning("API_KEY not configured, falling back to default")
        
        try:
            session = await self._get_session()
            
            # Use /song/{vidid} endpoint with api parameter
            url = f"{self.song_url}/{video_id}"
            params = {
                "api": self.api_key
            }
            
            async with session.get(url, params=params, timeout=15) as response:
                if response.status == 200:
                    data = await response.json()
                    LOGGER("NexGenBots").info(f"Got download URL for {video_id}")
                    return data  # Return full response for processing
                elif response.status == 401:
                    LOGGER("NexGenBots").error("Invalid API key!")
                    return None
                else:
                    LOGGER("NexGenBots").error(f"Song API error: {response.status}")
                    try:
                        error_data = await response.json()
                        LOGGER("NexGenBots").error(f"Error details: {error_data}")
                    except:
                        pass
                    return None
                    
        except asyncio.TimeoutError:
            LOGGER("NexGenBots").error("Request timeout!")
            return None
        except Exception as e:
            LOGGER("NexGenBots").error(f"Failed to get song: {e}")
            return None
    
    async def search(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Note: NexGenBots API does NOT provide search functionality.
        This method returns empty list. Use youtubesearchpython for search.
        
        Args:
            query: Search query
            limit: Max results
            
        Returns:
            Empty list (search not supported)
        """
        LOGGER("NexGenBots").debug("Search not supported by NexGenBots API")
        return []
    
    def _format_results(self, results: List[Dict]) -> List[Dict]:
        """Format API results to match expected format"""
        formatted = []
        
        for item in results:
            try:
                formatted_item = {
                    "id": item.get("id") or item.get("videoId"),
                    "title": item.get("title"),
                    "duration": item.get("duration") or item.get("durationText", "0:00"),
                    "thumbnail": item.get("thumbnail") or item.get("thumbnails", [{}])[0].get("url"),
                    "channel": item.get("channel") or item.get("author") or item.get("channelTitle"),
                    "views": item.get("views") or item.get("viewCount", "0"),
                    "published": item.get("published") or item.get("publishedTime", ""),
                    "link": f"https://www.youtube.com/watch?v={item.get('id') or item.get('videoId')}"
                }
                
                # Validate required fields
                if formatted_item["id"] and formatted_item["title"]:
                    formatted.append(formatted_item)
                    
            except Exception as e:
                LOGGER("NexGenBots").debug(f"Failed to format result: {e}")
                continue
        
        return formatted


# Global instance
_nexgen_instance: Optional[NexGenBotsSearch] = None


def get_nexgen_client() -> NexGenBotsSearch:
    """Get singleton instance of NexGenBots client"""
    global _nexgen_instance
    if _nexgen_instance is None:
        _nexgen_instance = NexGenBotsSearch()
    return _nexgen_instance


async def nexgen_search(query: str, limit: int = 10) -> List[Dict]:
    """
    Convenience function for searching via NexGenBots API
    
    Args:
        query: Search query
        limit: Max results
        
    Returns:
        List of formatted results
    """
    client = get_nexgen_client()
    return await client.search(query, limit)
