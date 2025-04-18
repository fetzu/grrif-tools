"""
GRRIF Scrobbler helper functions.

This module provides functions to scrobble GRRIF tracks to Last.fm.
"""
import time
import hashlib
import threading
from typing import Dict, Optional, Any
import requests
import titlecase

from .utils import Config, logger

class TrackScrobbler:
    """
    Class to handle scrobbling tracks to Last.fm.
    """
    def __init__(self):
        """Initialize the scrobbler with configuration and state."""
        self.config = Config()
        self.credentials = self.config.get_lastfm_credentials()
        self.current_track = None
        self.last_check_time = ""
        self.check_interval = 60  # Check for new track every 60 seconds
        
    def has_credentials(self) -> bool:
        """Check if the required Last.fm credentials are set."""
        return all([
            self.credentials['api_key'],
            self.credentials['api_secret'],
            self.credentials['session_key']
        ])
    
    def hash_request(self, params: Dict[str, str]) -> str:
        """
        Create a hash for Last.fm API authentication.
        
        Args:
            params: The parameters to hash.
            
        Returns:
            The md5 hash of the parameters and API secret.
        """
        items = sorted(params.keys())
        string = ''
        
        for item in items:
            string += item + params[item]
            
        string += self.credentials['api_secret']
        
        # Create MD5 hash
        return hashlib.md5(string.encode('utf8')).hexdigest()
    
    def scrobble_track(self, artist: str, title: str, timestamp: int) -> bool:
        """
        Scrobble a track to Last.fm.
        
        Args:
            artist: The artist name.
            title: The track title.
            timestamp: The Unix timestamp when the track started playing.
            
        Returns:
            True if scrobbling was successful, False otherwise.
        """
        if not self.has_credentials():
            logger.warning("Cannot scrobble: Last.fm credentials not set")
            return False
            
        url = "http://ws.audioscrobbler.com/2.0/"
        
        params = {
            "method": "track.scrobble",
            "api_key": self.credentials['api_key'],
            "artist": artist,
            "chosenByUser": "0",
            "sk": self.credentials['session_key'],
            "timestamp": str(timestamp),
            "track": title,
        }
        
        req_hash = self.hash_request(params)
        params["api_sig"] = req_hash
        
        try:
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            logger.info(f"Scrobbled: {artist} - {title}")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to scrobble track: {e}")
            return False
    
    def get_current_track(self) -> Optional[Dict[str, str]]:
        """
        Get the currently playing track from GRRIF.
        
        Returns:
            A dictionary with track information or None if failed.
        """
        try:
            response = requests.get("https://www.grrif.ch/live/covers.json")
            response.raise_for_status()
            
            data = response.json()[3]  # The current track is at index 3
            
            return {
                "artist": titlecase.titlecase(data.get("Artist", "")),
                "title": titlecase.titlecase(data.get("Title", "")),
                "time": data.get("Hours", "")
            }
        except (requests.RequestException, ValueError, IndexError) as e:
            logger.error(f"Error getting current track: {e}")
            return None
    
    def start_tracking(self, stop_event: threading.Event) -> None:
        """
        Start tracking the currently playing track and scrobble it.
        
        Args:
            stop_event: Event to signal when to stop tracking.
        """
        logger.info("Starting track tracking")
        
        while not stop_event.is_set():
            try:
                track_info = self.get_current_track()
                
                if track_info and track_info["time"] != self.last_check_time:
                    # New track detected
                    self.current_track = track_info
                    self.last_check_time = track_info["time"]
                    
                    # Log the currently playing track
                    logger.info(f"Now playing: {track_info['artist']} - {track_info['title']}")
                    
                    # Scrobble the track with a timestamp 30 seconds in the past
                    # This ensures the track is scrobbled correctly
                    timestamp = int(time.time() - 30)
                    self.scrobble_track(
                        track_info["artist"], 
                        track_info["title"], 
                        timestamp
                    )
            except Exception as e:
                logger.error(f"Error in track tracking: {e}")
            
            # Check for new track after interval
            for _ in range(self.check_interval):
                if stop_event.is_set():
                    break
                time.sleep(1)
        
        logger.info("Track tracking stopped")

def start_scrobbling(stream_mode: str = "0") -> None:
    """
    Start standalone scrobbling mode.
    
    Args:
        stream_mode: "0" for standalone mode.
    """
    stop_event = threading.Event()
    
    try:
        scrobbler = TrackScrobbler()
        
        if not scrobbler.has_credentials():
            print("Last.fm credentials not set. Please use 'grrif_tools scrobble settings' first.")
            return
            
        print("Starting scrobbling to Last.fm. Press Ctrl+C to stop.")
        
        # Start scrobbling in the main thread
        scrobbler.start_tracking(stop_event)
    except KeyboardInterrupt:
        print("Scrobbling stopped by user.")
    finally:
        stop_event.set()

def stop_scrobbling() -> None:
    """Placeholder for stopping scrobbling in the TUI."""
    # In the TUI implementation, this will be used to stop scrobbling
    pass