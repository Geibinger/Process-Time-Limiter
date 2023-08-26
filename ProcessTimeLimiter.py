from datetime import datetime, date
import psutil
import time
import random
from plyer import notification
import threading

stoic_quotes = [
    "The obstacle is the path.",
    "Waste no more time arguing what a good man should be. Be one.",
    "You have power over your mind, not outside events. Realize this, and you will find strength.",
    "The happiness of your life depends upon the quality of your thoughts.",
    "Very little is needed to make a happy life; it is all within yourself, in your way of thinking.",
    "He who lives in harmony with himself lives in harmony with the universe.",
    "The soul becomes dyed with the color of its thoughts.",
    "The best revenge is not to be like your enemy.",
    "It does not matter what you bear, but how you bear it.",
    "The more we value things outside our control, the less control we have.",
    "Wealth consists not in having great possessions, but in having few wants.",
    "The world is only in your mind. Your mind is only in the world."
]


ProcessNames = ["League", "Riot"]
TimeLimitMinutes = 180
RemainingTimeFile = "remaining_time.txt"

def save_remaining_time(remaining_time, daily_total_time, total_time, last_save_date):
    with open(RemainingTimeFile, "w") as file:
        file.write(f"{remaining_time}\n{daily_total_time}\n{total_time}\n{last_save_date}")

def load_remaining_time():
    try:
        with open(RemainingTimeFile, "r") as file:
            lines = file.readlines()
            remaining_time = float(lines[0])
            daily_total_time = float(lines[1])
            total_time = float(lines[2])
            last_save_date = datetime.strptime(lines[3].strip(), "%Y-%m-%d").date()
            return remaining_time, daily_total_time, total_time, last_save_date
    except FileNotFoundError:
        return TimeLimitMinutes, 0, 0, date.today()

def close_game_processes(process_names):
    for process in psutil.process_iter():
        for name in process_names:
            if process.name().startswith(name):
                try:
                    process.terminate()
                except psutil.NoSuchProcess:
                    pass

def show_notification(message):
    notification.notify(
        title=f"Process Time Limit",
        message=message,
        timeout=10
    )

def main():
    remaining_time, daily_total_time, total_time, last_save_date = load_remaining_time()
    old_daily_total_time = daily_total_time
    old_total_time = total_time
    notification_thread = threading.Thread(target=show_notification, args=(f"Started Time Limiter with {remaining_time} minutes left!",))
    notification_thread.start()
    time.sleep(1)
    notification_thread.join()
    current_date = date.today()
    if current_date > last_save_date:  # Check if a new day has started
        remaining_time = TimeLimitMinutes
        last_save_date = current_date
        old_daily_total_time = 0

    TimeLeftNotificationShown = False
    QuoteNotificationShown = False
    GamesRunning = False
    FirstRun = True
    start_time = 0

    while True:
        game_processes = [p for p in psutil.process_iter() if any(p.name().startswith(name) for name in ProcessNames)]

        if game_processes:
            if FirstRun:
                start_time = time.time()
                FirstRun = False

            GamesRunning = True
            current_time = time.time()
            running_time = current_time - start_time
            remaining_time = (TimeLimitMinutes * 60 - running_time) / 60
            QuoteNotificationShown = False

            save_remaining_time(remaining_time, old_daily_total_time + running_time / 60, old_total_time + running_time / 60, last_save_date)

            if running_time >= TimeLimitMinutes * 60 * 0.75 and not TimeLeftNotificationShown:
                notification_thread = threading.Thread(target=show_notification, args=(f"{(remaining_time):.2f} minutes left!",))
                notification_thread.start()
                time.sleep(1)
                notification_thread.join()
                TimeLeftNotificationShown = True

            if remaining_time <= 0:
                if not QuoteNotificationShown:
                    random_quote = random.choice(stoic_quotes)
                    notification_thread = threading.Thread(target=show_notification, args=(random_quote,))
                    notification_thread.start()
                    time.sleep(1)
                    notification_thread.join()
                    QuoteNotificationShown = True
                close_game_processes(ProcessNames)
                remaining_time = 0
                save_remaining_time(remaining_time, old_daily_total_time + running_time / 60, old_total_time + running_time / 60, last_save_date)
                continue
        else:
            if GamesRunning:
                notification_thread = threading.Thread(target=show_notification, args=(f"Stopped Time Limiter with {remaining_time} minutes left!",))
                notification_thread.start()
                time.sleep(1)
                notification_thread.join()
                GamesRunning = False
            continue
        time.sleep(10)

if __name__ == "__main__":
    main()