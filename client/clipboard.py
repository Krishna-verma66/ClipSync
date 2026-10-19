import pyperclip as ppc
import hashlib

#This script has methods to interect with OS's clipboard...


class ClipboardManager:

    def __init__(self):
        self._last_capture_text = None
        self._last_capture_hash = self._get_clipboard_hash(self.read_clipboard())


    def _get_clipboard_hash(self, text: str) -> str:
        """Calculate a SHA-256 fingerprint of clipboard text."""
        return hashlib.sha256(
            text.encode("utf-8")
        ).hexdigest()


    def read_clipboard(self) -> str:
        return ppc.paste()
    
    
    def write_clipboard(self, text) -> None:
        if text is not None:
           ppc.copy(text)
           
        self._remember(text)


    def _remember(self, text: str) -> None:
        """Update the last-observed clipboard state."""
        self._last_capture_text = text
        self._last_capture_hash = self._get_clipboard_hash(text)
        
    
    def is_new_data(self, text) -> bool:
        server_text_hash = self._get_clipboard_hash(text)
        
        if server_text_hash != self._last_capture_hash:
            return True
    
        return False


    def has_clipboard_changed(self) -> tuple[bool, str]:
        current_text = self.read_clipboard()
        current_text_hash = self._get_clipboard_hash(current_text)

        changed = current_text_hash != self._last_capture_hash

        return (changed, current_text)


    def get_clipboard_update(self) -> str | None:
        """Return new clipboard text, or None if unchanged."""
        changed, current_text = self.has_clipboard_changed()

        
        if changed:
            self._remember(current_text)
            return current_text

        return None

