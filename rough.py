import schedule
import subprocess
import time

def run_script():
    # Replace 'script.sh' with the name of your shell script
    subprocess.call('./script.sh', shell=True)

# Schedule the script to run at 7 AM every day
schedule.every().day.at("07:00").do(run_script)

while True:
    schedule.run_pending()
    time.sleep(1)
