from datetime import datetime, date, timedelta
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

process_names = ["League", "Riot"]
time_limit_minutes = 180
remaining_time_file = "remaining_time.txt"

class TimeLimiter:
    def __init__(self):
        self.load_time()
        self.quote_notification_shown = False
        self.start_time = None

    def save_remaining_time(self):
        with open(remaining_time_file, "w") as file:
            file.write(f"{self.remaining_time}\n{self.daily_total_time}\n{self.total_time}\n{self.last_save_date}")

    def load_time(self):
        try:
            with open(remaining_time_file, "r") as file:
                lines = file.readlines()
                self.remaining_time = float(lines[0])
                self.daily_total_time = float(lines[1])
                self.total_time = float(lines[2])
                self.last_save_date = datetime.strptime(lines[3].strip(), "%Y-%m-%d").date()
        except FileNotFoundError:
            self.remaining_time = time_limit_minutes
            self.last_save_date = date.today()
            self.daily_total_time = 0
            self.total_time = 0

    def close_game_processes(self):
        for process in psutil.process_iter():
            for name in process_names:
                if process.name().startswith(name):
                    try:
                        process.terminate()
                    except psutil.NoSuchProcess:
                        pass

    def show_notification(self, message):
        notification_thread = threading.Thread(target=notification.notify, args=("Process Time Limit", message))
        notification_thread.start()
        time.sleep(1)
        notification_thread.join()

    def start(self):
        self.show_notification(f"Started Time Limiter with {self.remaining_time:.2f} minutes left!")

        while True:
            game_processes = [p for p in psutil.process_iter() if any(p.name().startswith(name) for name in process_names)]
            current_time = time.time()

            if game_processes:
                if self.start_time is None:
                    self.start_time = current_time

                running_time = current_time - self.start_time
                self.remaining_time = max(0, time_limit_minutes - running_time / 60)

                if running_time >= time_limit_minutes * 0.75 and not self.quote_notification_shown:
                    random_quote = random.choice(stoic_quotes)
                    self.show_notification(random_quote)
                    self.quote_notification_shown = True

                if self.remaining_time <= 0:
                    if not self.quote_notification_shown:
                        random_quote = random.choice(stoic_quotes)
                        self.show_notification(random_quote)
                        self.quote_notification_shown = True
                    self.close_game_processes()
                    self.remaining_time = 0

                # Update total times
                self.daily_total_time += running_time / 60
                self.total_time += running_time / 60

            else:
                if self.start_time is not None:
                    self.show_notification(f"Stopped Time Limiter with {self.remaining_time:.2f} minutes left!")
                    self.close_game_processes()
                self.start_time = None
                self.quote_notification_shown = False
                self.remaining_time = time_limit_minutes

            # Reset daily total time if a new day is detected
            if date.today() > self.last_save_date:
                self.daily_total_time = 0
                self.last_save_date = date.today()

            self.save_remaining_time()
            time.sleep(10)

def main():
    time_limiter = TimeLimiter()
    time_limiter.start()

if __name__ == "__main__":
    main()