import subprocess
import time

# Path to your bot script
BOT_SCRIPT = "main.py"

# Command to run your bot
COMMAND = f"python {BOT_SCRIPT}"

def start_bot():
    """Start the bot process."""
    print("Starting the bot...")
    return subprocess.Popen(COMMAND, shell=True)

def monitor_bot():
    """Monitor the bot process and restart if it crashes."""
    bot_process = start_bot()
    try:
        while True:
            # Check if the bot process is still running
            if bot_process.poll() is not None:
                print("Bot process has stopped. Restarting...")
                bot_process = start_bot()
            time.sleep(5)  # Check every 5 seconds
    except KeyboardInterrupt:
        print("Shutting down daemon...")
        bot_process.terminate()

if __name__ == "__main__":
    monitor_bot()