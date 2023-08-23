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
TimeLimitMinutes = 45

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
    notification_thread = threading.Thread(target=show_notification, args=(f"Started Time Limiter with {TimeLimitMinutes} minutes left!",))
    notification_thread.start()
    while True:
        game_processes = [p for p in psutil.process_iter() if any(p.name().startswith(name) for name in ProcessNames)]
        if game_processes:
            break
        time.sleep(10)

    start_time = time.time()
    NotificationShown = False

    while True:
        current_time = time.time()
        running_time = current_time - start_time
        game_processes = [p for p in psutil.process_iter() if any(p.name().startswith(name) for name in ProcessNames)]
        
        if game_processes:
            if running_time >= TimeLimitMinutes * 60 * 0.1 and not NotificationShown:
                notification_thread = threading.Thread(target=show_notification, args=(f"Only {(TimeLimitMinutes * 0.1 - running_time / 60):.2f}",))
                notification_thread.start()
                NotificationShown = True

            if running_time >= TimeLimitMinutes * 60:
                random_quote = random.choice(stoic_quotes)
                notification_thread = threading.Thread(target=show_notification, args=(random_quote,))
                notification_thread.start()
                close_game_processes(ProcessNames)
                continue

        time.sleep(1)

if __name__ == "__main__":
    main()