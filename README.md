# Process Time Limiter

🕒Promote Responsible Gaming | ⚙️ Customizable Process List | 📆 Scheduled Execution

The **Process Time Limiter** is a Python script developed using ChatGPT that helps you manage and limit your gaming time on Windows systems. This script monitors specified game processes and enforces a daily time limit on their usage. If the time limit is exceeded, the script will terminate the game processes and display motivational quotes to encourage a healthier balance between gaming and other activities.

## Motivation

The primary motivation behind this script is to promote responsible gaming and time management. By setting and enforcing time limits on gaming sessions, users can maintain a better balance between their gaming interests and other responsibilities or activities.

## How to Use

Follow these instructions to use the Process Time Limiter:

1. **Prerequisites**: Make sure you have Python installed on your system. You will also need to install the required Python packages by running the following command in your terminal:

```bash
pip install psutil plyer
```

2. **Creating the Executable**: To create an executable for the script, you can use **PyInstaller**. Open a terminal and navigate to the directory containing the script (`ProcessTimeLimiter.py`). Run the following command:

```bash
pyinstaller --noconsole --onefile --hidden-import plyer.platforms.win.notification ProcessTimeLimiter.py
```


This will create a standalone executable file in the `dist` directory.

3. **Adding to Windows Defender Allowed Applications**: To ensure that the executable is not blocked by Windows Defender, you should add it to the list of allowed applications. Here's how:

- Open Windows Security (Windows Defender) from your system settings.
- Go to "Virus & threat protection."
- Under "Exclusions," click on "Add or remove exclusions."
- Select "Add an exclusion" and choose "Folder."
- Browse and select the directory containing the generated executable.

4. **Scheduling the Script with Task Scheduler**:

- Open the Windows Task Scheduler from the Start menu.
- In the right-hand panel, click on "Create Basic Task."
- Follow the wizard to set a name and description for the task.
- Choose "When I log in" as the trigger and proceed with the setup.
- Select "Start a program" as the action, and browse to the location of the generated executable.
- Complete the wizard, and your task will be scheduled to run whenever you log in.

Additionally, you can create another task with the trigger "At startup" to ensure the script runs when the system powers up.

## Customization

You can customize the list of processes to limit by modifying the `ProcessNames` array in the script. Simply add the names of the processes you want to restrict. The time limit can be changed by modifying the `TimeLimitMinutes` variable.

## Disclaimer

The Process Time Limiter script is a tool designed to assist users in managing their time spent on gaming. It enforces time limits on specified game processes, but its effectiveness depends on user compliance. The script is provided as-is, and the developers are not responsible for any unexpected behavior, data loss, or other issues that may arise from its use.

Remember that responsible gaming habits involve a combination of tools, self-discipline, and awareness of your own gaming habits.

## Contributing

This script is open-source, and contributions are welcome. If you encounter issues or have suggestions for improvements, feel free to submit a pull request or open an issue on the project's repository.

**Note:** Always use scripts and tools responsibly and considerately. It's important to respect the intended usage of applications and systems.
