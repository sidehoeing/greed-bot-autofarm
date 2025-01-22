# Discord Bot: Autofarm with Message Parsing

This bot automates specific actions on Discord by responding to messages, processing embeds, and sending pre-configured commands in whitelisted channels. It is particularly designed for scenarios where automated interaction with Discord embeds (like games or work simulations) is necessary.

---

## Features

- **Admin Privilege Elevation**: Ensures the script runs with elevated permissions on Windows.
- **Whitelist Channel Enforcement**: Restricts bot activities to specific channel IDs.
- **Embed Parsing**: Handles and parses embeds to extract useful data, such as:
  - Money earned from work.
  - Dance directions.
  - Cooldown times.
- **Command Automation**: Sends commands based on parsed data or at regular intervals.
- **Logging and Debugging**: Outputs logs to track bot activities and debug issues.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **Discord.py**: Install using `pip install discord.py`.
- **Admin Privileges**: Required for running certain elevated commands (on Windows).
- **Token File**: A `tokens.txt` file with your bot's token stored as plain text.

---

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
