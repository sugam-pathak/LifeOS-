# LifeOS-
A terminal-based productivity and life management system for students.
LifeOS CLT is a lightweight command-line application that helps students manage their daily lives from the terminal. It brings together task scheduling, habit tracking, study timers, XP-based motivation, and analytics into a single offline-first system.
The goal of LifeOS CLT is simple: it turns your terminal into a personal productivity dashboard.
***

**Why LifeOS CLT?**
 Most productivity tools are heavy, distracting, or rely on the cloud.

 1.Minimalism and speed

2.Offline, local data storage

3.Clear structure and discipline

4.Gamified motivation without pressure

It is especially helpful for students who already spend time in the terminal and want a system that is focused without any unnecessary UI clutter.

***

**Key Features**  
**Core System**  

Animated boot and shutdown sequence.  

Optional fast-boot mode.  

Colorized output with on/off toggle.  

Automatic data saving and backups.  

Configurable keybindings.  

**Tasks & Scheduling**  

Add tasks with due dates and times.  

Mark tasks as completed using task IDs.  

Automatic overdue detection.  

Daily task summary at startup.  

Reminder checks during runtime.  

**Habits & Consistency**  

Create and track habits.  

Increment habit completions.  

Habit-based XP rewards.  

Daily streak tracking.  

**Study Tools**  

Study timer (Pomodoro-style).  

Subject-wise session tracking.  

Study history and analytics.  

**Progress & Motivation**  

XP and level system.  

Progress bars.  

Achievement unlocking.  

Streak bonuses.  

**Utilities ** 

Built-in calculator (safe evaluation).  

Export data to JSON or CSV.  

Local configuration file.  

Fully offline operation. 
***

**Installation
Requirements**

Python 3.9 or newer

Windows, Linux, or macOS

Terminal with ANSI color support (recommended)

**Run Locally**
git clone https://github.com/yourusername/lifeos-clt.git
cd lifeos-clt
python terminal1.py

**Command Reference  
General Commands ** 
Command   Description  
help      Show help menu  
status    View level, XP, and streak  
save      Save current data  
exit      Exit LifeOS CLT  

**Task Management ** 
Command   Description  
`task add Title YYYY-MM-DD HH:MM`  Add a new task  
task done <task_id>  Mark task as completed  
tasks     List all tasks  
tasks today  List today's tasks  

**Habit Tracking ** 
Command   Description  
habit add <name>  Add a new habit  
habit done <name>  Mark habit as completed  
habits    List all habits  

**Study  **
Command   Description  
study start <subject>  Start study timer  
study stop  Stop current study session  
study stats  View study statistics  

**Utilities ** 
Command   Description  
calc <expression>  Calculator  
export json  Export data to JSON  
export csv  Export data to CSV  

**Appearance & Settings ** 
Command   Description  
color on   Enable colored output  
color off  Disable colored output  
***

**Configuration**

User configuration file location:
~/.lifeos/config.json

Example configuration:
{
  "theme": "green",
  "keybindings": {
    "q": "exit",
    "st": "status"
  }
}

**Data Storage**

All data is stored locally on your system:

~/.lifeos/data.json


Automatic backups are stored in:

~/.lifeos/backups/


When new features are added, older data files are automatically migrated to prevent data loss.

Project Structure
terminal1.py        Main application
~/.lifeos/
 ├─ data.json       User data
 ├─ config.json     User configuration
 └─ backups/        Automatic backups

***

**Design Philosophy**

LifeOS CLT is built around these principles:

Offline-first — no cloud dependency

Simple but structured

Encourages consistency, not pressure

Terminal-native experience

Student-focused productivity

Your data stays on your machine, under your control.

***

**License**

MIT License — free to use, modify, and distribute.

