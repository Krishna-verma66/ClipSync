from termcolor import colored

def read_console_command(lock) -> str | None:
    with lock:
        text = colored("ClipSync>>>", "blue")
        command = input(text).strip()
        return command.upper()
        

def show_help():
    help_text = """
==================================================
                  ClipSync Help
          Peer-to-Peer Clipboard Sync
==================================================

GENERAL COMMANDS
----------------
help
    Show this help information.

devices
    Show nearby devices discovered on the local network.

connect <device>
    Connect to a discovered device using its number or IP.
    Example: connect 1
             connect 192.168.1.10

disconnect
    Disconnect from the currently connected device.

status
    Show the current connection and synchronization status.

CLIPBOARD SYNCHRONIZATION
-------------------------
sync on
    Enable clipboard synchronization.

sync off
    Disable clipboard synchronization.

HISTORY
-------
history
    Show clipboard synchronization history.

DEVICE SETTINGS
---------------
rename <name>
    Change this device's display name.
    Example: rename My-Laptop

exit
    Stop ClipSync and close the application.

==================================================
Notes:
- Both devices should run ClipSync on the same local network.
- Allow ClipSync through the firewall if device discovery fails.
- Only connect to devices you trust.
==================================================
"""

    colored_text = colored(help_text, "yellow")

    print(colored_text)
