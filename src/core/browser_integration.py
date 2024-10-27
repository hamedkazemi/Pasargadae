import asyncio
import json
import os
import sys
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path
import websockets
from ..models.download import Download

class BrowserIntegration:
    def __init__(self, settings: dict, download_manager):
        self.settings = settings
        self.download_manager = download_manager
        self.server = None
        self.connections = set()
        
        # Get browser settings
        self.enabled_browsers = settings["browser_integration"]["enabled_browsers"]
        self.url_sniffer = settings["browser_integration"]["url_sniffer"]
        self.hotkeys = settings["browser_integration"]["hotkeys"]
        
        # Extension paths
        self.extension_paths = self._get_extension_paths()
    
    async def start(self):
        """Start the browser integration server."""
        if not self.enabled_browsers:
            return
        
        # Start WebSocket server for extension communication
        self.server = await websockets.serve(
            self.handle_connection,
            "localhost",
            8765  # Default port for extension communication
        )
    
    async def stop(self):
        """Stop the browser integration server."""
        if self.server:
            self.server.close()
            await self.server.wait_closed()
    
    async def handle_connection(self, websocket, path):
        """Handle a new browser extension connection."""
        try:
            self.connections.add(websocket)
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": "error",
                        "error": "Invalid JSON"
                    }))
                
        finally:
            self.connections.remove(websocket)
    
    async def handle_message(self, websocket, data: Dict[str, Any]):
        """Handle a message from a browser extension."""
        message_type = data.get("type")
        
        if message_type == "download_request":
            # Handle download request
            url = data.get("url")
            if not url:
                await websocket.send(json.dumps({
                    "type": "error",
                    "error": "No URL provided"
                }))
                return
            
            # Check URL against filters
            if not self._check_url_filters(url):
                await websocket.send(json.dumps({
                    "type": "error",
                    "error": "URL blocked by filters"
                }))
                return
            
            # Start download
            download = await self.download_manager.add_download(url)
            
            await websocket.send(json.dumps({
                "type": "download_started",
                "download_id": download.id
            }))
            
        elif message_type == "capture_toggle":
            # Handle URL sniffer toggle
            enabled = data.get("enabled", False)
            self.url_sniffer = enabled
            
            await websocket.send(json.dumps({
                "type": "capture_status",
                "enabled": enabled
            }))
    
    def _get_extension_paths(self) -> Dict[str, str]:
        """Get paths for browser extensions."""
        extension_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "extensions"
        )
        
        paths = {}
        for browser in self.enabled_browsers:
            ext_path = os.path.join(extension_dir, browser.lower())
            if os.path.exists(ext_path):
                paths[browser] = ext_path
        
        return paths
    
    def _check_url_filters(self, url: str) -> bool:
        """Check if URL passes the configured filters."""
        filters = self.settings["filters"]
        
        # Check blocked URLs
        for blocked in filters["url_filter"]["blocked"]:
            if blocked in url:
                return False
        
        # Check allowed URLs
        allowed = filters["url_filter"]["allowed"]
        if allowed and not any(allowed_url in url for allowed_url in allowed):
            return False
        
        # Check file type filters
        file_types = filters["file_type_filter"]
        if file_types:
            ext = os.path.splitext(url)[1].lower()
            if ext and ext not in file_types:
                return False
        
        return True
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast a message to all connected extensions."""
        if not self.connections:
            return
        
        message_json = json.dumps(message)
        await asyncio.gather(*[
            connection.send(message_json)
            for connection in self.connections
        ])
    
    def install_extension(self, browser: str) -> bool:
        """Install the download manager extension for a browser."""
        if browser not in self.extension_paths:
            return False
        
        ext_path = self.extension_paths[browser]
        
        try:
            if browser == "Chrome":
                self._install_chrome_extension(ext_path)
            elif browser == "Firefox":
                self._install_firefox_extension(ext_path)
            elif browser == "Edge":
                self._install_edge_extension(ext_path)
            return True
            
        except Exception:
            return False
    
    def _install_chrome_extension(self, path: str):
        """Install Chrome extension."""
        # Implementation depends on OS
        if sys.platform == "win32":
            # Windows registry modification
            pass
        else:
            # Linux/Mac native messaging host
            self._install_native_messaging_host("chrome")
    
    def _install_firefox_extension(self, path: str):
        """Install Firefox extension."""
        self._install_native_messaging_host("firefox")
    
    def _install_edge_extension(self, path: str):
        """Install Edge extension."""
        self._install_native_messaging_host("edge")
    
    def _install_native_messaging_host(self, browser: str):
        """Install native messaging host for browser integration."""
        manifest = {
            "name": "com.pasargadae.downloader",
            "description": "Pasargadae Download Manager",
            "path": sys.executable,
            "type": "stdio",
            "allowed_origins": [
                f"chrome-extension://*/"  # Chrome/Edge
            ] if browser in ["chrome", "edge"] else [
                f"firefox-extension://*/"  # Firefox
            ]
        }
        
        # Get native messaging hosts directory
        if sys.platform == "win32":
            base_dir = os.path.expandvars(r"%APPDATA%")
        else:
            base_dir = os.path.expanduser("~/.mozilla" if browser == "firefox" else "~/.config")
        
        # Create manifest directory
        manifest_dir = os.path.join(
            base_dir,
            "NativeMessagingHosts" if browser == "firefox" else 
            f"{browser.title()}/NativeMessagingHosts"
        )
        os.makedirs(manifest_dir, exist_ok=True)
        
        # Write manifest
        manifest_path = os.path.join(
            manifest_dir,
            "com.pasargadae.downloader.json"
        )
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
