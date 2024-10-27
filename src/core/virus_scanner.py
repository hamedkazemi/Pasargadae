import asyncio
import subprocess
import shlex
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.download import Download
from ..repositories.download_repository import DownloadRepository

class VirusScanner:
    def __init__(self, settings: dict):
        self.settings = settings
        self.repository = DownloadRepository()
        
        # Get antivirus settings
        self.enabled = settings["security"]["antivirus_scanning"]
        self.pre_scan_command = settings["security"].get("pre_scan_command", "")
        self.post_scan_command = settings["security"].get("post_scan_command", "")
        self.custom_commands = settings["security"].get("custom_commands", "")
    
    async def scan_file(self, download: Download) -> Dict[str, Any]:
        """Scan a file for viruses."""
        if not self.enabled:
            return {"status": "disabled"}
        
        try:
            # Run pre-scan command if configured
            if self.pre_scan_command:
                pre_result = await self._run_command(
                    self.pre_scan_command,
                    download.save_path
                )
                if pre_result["status"] == "error":
                    return pre_result
            
            # Run main scan
            result = await self._run_command(
                self.custom_commands or "clamscan {file}",
                download.save_path
            )
            
            # Run post-scan command if configured
            if self.post_scan_command:
                post_result = await self._run_command(
                    self.post_scan_command,
                    download.save_path
                )
                if post_result["status"] == "error":
                    result["post_scan_error"] = post_result["error"]
            
            # Log scan result
            await self.repository.add_event(
                download.id,
                "virus_scan",
                result
            )
            
            return result
            
        except Exception as e:
            error_result = {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            
            # Log error
            await self.repository.add_event(
                download.id,
                "virus_scan_error",
                error_result
            )
            
            return error_result
    
    async def _run_command(self, command: str, file_path: str) -> Dict[str, Any]:
        """Run a virus scan command."""
        try:
            # Replace {file} placeholder with actual path
            command = command.replace("{file}", shlex.quote(file_path))
            
            # Run command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Wait for result with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=300  # 5 minutes timeout
                )
            except asyncio.TimeoutError:
                if process.returncode is None:
                    process.kill()
                return {
                    "status": "error",
                    "error": "Scan timeout after 5 minutes",
                    "timestamp": datetime.now().isoformat()
                }
            
            # Process result
            result = {
                "status": "clean" if process.returncode == 0 else "infected",
                "command": command,
                "return_code": process.returncode,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "timestamp": datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "command": command,
                "timestamp": datetime.now().isoformat()
            }
