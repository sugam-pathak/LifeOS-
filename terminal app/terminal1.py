import os
import json
import sys
import time
import math
from datetime import datetime, date
try:
    import readline
except ImportError:
    readline = None
APP_NAME = "LifeOS CLT"
VERSION = "0.0.1"

DATA_DIR = os.path.expanduser("~/.lifeos")
DATA_FILE = os.path.join(DATA_DIR, "data.json")
BACKUP_DIR = os.path.join(DATA_DIR, "backups")

CONFIG_FILE = os.path.join(DATA_DIR, "config.json")
COLORS_ENABLED = True
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

THEMES = {
    "green": "\033[92m",
    "blue": "\033[94m",
    "yellow": "\033[93m"
}

CURRENT_THEME = "green"
def boot_loader():
    logo = [
        "██╗     ██╗███████╗███████╗ ██████╗ ███████╗",
        "██║     ██║██╔════╝██╔════╝██╔═══██╗██╔════╝",
        "██║     ██║█████╗  █████╗  ██║   ██║███████╗",
        "██║     ██║██╔══╝  ██╔══╝  ██║   ██║╚════██║",
        "███████╗██║██║     ███████╗╚██████╔╝███████║",
        "╚══════╝╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚══════╝"
    ]

    os.system("cls" if os.name == "nt" else "clear")

    for line in logo:
        print(color(line, GREEN))
        time.sleep(0.08)
    print(color("\n Booting LifeOS CLT........\n",GREEN))

    steps = [
        "Loading core modules",
        "initializing data store",
        "Checking streaks",
        "Loading habits & tasks",
        "Applying user config",
        "System ready"

    ]

    symbols = ["|", "/", "-", "\\"]
    for i, step in enumerate(steps):
        sys.stdout.write(color(f"[ OK ] {step}\n", GREEN))
        sys.stdout.flush()
        time.sleep(0.25)
        sys.stdout.write("\r")
        sys.stdout.write(color(f"[✔] {step}\n"))
        beep()
    sys.stdout.write(color("\nProgress:"))
    for i in range(21):
        bar = "█" * i + "-" * (20 - i)
        sys.stdout.write(f"\rProgress: [{bar}]")
        sys.stdout.flush()
        time.sleep(0.15)
    print(color("\n✔ LifeOS boot complete\n", GREEN))
    time.sleep(0.5)
#----------------
def shutdown_animation():
    print(color("\n 🔻 Shutting down LifeOS CLT...\n "))

    steps = [
        "Saving user data",
        "Creating backup",
        "Stopping background tasks",
        "Relasing resources",
        "powering off system"
    ]

    symbols = ["|", "/", "-", "\\"]
    for i, step in enumerate(steps):
        for j in range(6):
            sys.stdout.write(color(f"\r[{symbols[j % 4]}] {step}"))
            sys.stdout.flush()
            time.sleep(0.08)
        sys.stdout.write(color(f"\r[✔] {step}\n"))  
        beep()
    
    sys.stdout.write(color("\nShutdown progress: "))
    for i in range(21):
        bar = "█" * i + "-" * (20 - i)
        sys.stdout.write(f"\rShutdown progress: [{bar}]")
        sys.stdout.flush()
        time.sleep(0.03)
    print(color("\n\n LifeOS safely powered off\n"))
    time.sleep(0.3)
def color(text, c=None):
    if not COLORS_ENABLED:
        return text
    if c is None:
        c = THEMES.get(CURRENT_THEME, GREEN)
    return f"{c}{text}{RESET}"

def default_config():
    return {
        "keybindings": {
            "s": "status",
            "q": "exit",
            "h": "help"
        }
    }

#-----------------------------
def calculator(expr):
    try:
        allowed = "0123456789+-*/().%^"
        for ch in expr:
            if ch not in allowed:
                raise ValueError("Invalid character")
        result = eval(expr, {"__builtins___": None}, {})
        print(color(f"Result: {result}", GREEN))
    except ZeroDivisionError:
        print(color("🔴 Error: Division by zero", RED))
    except Exception:
        print(color("🔴 Invalid expression", RED))
#------------------------------
def load_config():
    if not os.path.exists(CONFIG_FILE):
        cfg = default_config()
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
        return cfg
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)
# unty function 
#---------------------
def ensure_directories():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def today():
    return date.today().isoformat()

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def pretty_time(seconds):
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours}h {minutes}m"

#-------------------------------
def default_data():
    return {
        "tasks": {},
        "achievements": [],
        "meta": {
            "created": now(),
            "version": VERSION
        },
        "stats":{
            "xp": 0,
            "level": 1,
            "streak": 0,
            "last_active": today()
        },
        "study": {
            "sessions": [],
            "subjects": {}
        },
        "habits": {},
        "goals": {},
        "history": {}

    }
#------------------------------
ACHIEVEMENTS = {
    "First Habit": lambda d: len(d["habits"]) >= 1,
    "task Master": lambda d: sum(
        t["done"] for day in d["tasks"].values() for t in day
    ) >=5,
    "Focused Learner": lambda d: d["stats"]["level"] >= 3,
}

COMMANDS = [
    "help", "help task", "help habit",
    "status", "save", "exit",
    "task add", "task done", "tasks",
    "habit add", "habit done", "habits",
    "study", "xp", "achievements",
    "color on", "color off"
]
def Pomodoro(minutes, data):
    print(color(f"🧠 Study started: {minutes} minutes",GREEN))
    time.sleep(minutes * 60)
    add_xp(data, minutes * 2)
    print(color(" ⏰ Pomodoro complete! Take a break. ", GREEN))
def check_achievements(data):
    for name, rule in ACHIEVEMENTS.items():
        if name not in data["achievements"] and rule(data):
            data["achievements"].append(name)
            print(color(f"🏆 Achievement unlocked: {name}", GREEN))
def load_data():
    ensure_directories()

    if not os.path.exists(DATA_FILE):
        data = default_data()
        save_data(data)
        return data

    with open(DATA_FILE,"r") as f:
        data = json.load(f)

    defaults = default_data()

    for key in defaults:
        if key not in data:
            data[key] = defaults[key]

    return data
#------------------------
def save_data(data):
    ensure_directories()
    with open(DATA_FILE,"w") as f:
        json.dump(data, f, indent=2)

def backup_data():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(BACKUP_DIR, f"backup_{ts}.json")
        with open(DATA_FILE, "r") as src:
            with open(backup_file, "w") as dst:
                dst.write(src.read())
#-------------------
def completer(text, state):
    matches = [c for c in COMMANDS if c.startswith(text)]
    return matches[state] if state < len(matches) else None
#---------------------------
def add_task(data, title, due):
    task_id = str(int(time.time()))
    data["tasks"][task_id] = {
        "title": title,
        "due":due,
        "done": False,
        "created": now()
    }
    add_xp(data, 10)
    print(color(f"Task added [{task_id}]: {title}",GREEN))
#task_status -------
def task_status(task):
    if task["done"]:
        return "✔", GREEN
    
    due_dt = datetime.strptime(task["due"], "%Y-%m-%d %H:%M")
    now_dt = datetime.now()

    if due_dt < now_dt:
        return "🔴", RED
    elif due_dt.date() == date.today():
    
        return "🟡", YELLOW
    else:
        return "⏳", RESET

#list task
def list_tasks(data, today_only=False):
    print(color("\n TASKS", GREEN))

    if not data["tasks"]:
        print(color("No tasks found", YELLOW))
        return
    
    today_date = today()

    for tid, task in data["tasks"].items():
        if today_only and not task["due"].startswith(today_date):
            continue
        icon, col = task_status(task)
        print(color(f"{col}[{icon}] {tid} | {task['title']} → {task['due']}{RESET}, col"))
#task complete ---------------
def complete_task(data, task_id):
    task = data["tasks"].get(task_id)

    if not task:
        print(color("🔴 Task ID not found", RED))
        return

    if task["done"]:
        print(color("⚠ Task already completed", YELLOW))
    task["done"] = True
    add_xp(data, 20)
    print(color(f"🏆 Task completed: {task['title']}", GREEN))
# XP & level

def xp_needed(level):
    return level * 150

def xp_bar(xp, level, length=20):
    needed = xp_needed(level)
    filled = int((xp / needed) * length)
    bar = "█" * filled + "-" * (length - filled)
    return f"[{bar}] {xp}/{needed}"

def add_xp(data, amount):
    data["stats"]["xp"] += amount
    while data["stats"]["xp"] >= xp_needed(data["stats"]["level"]):
        data["stats"]["xp"] -= xp_needed(data["stats"]["level"])
        data["stats"]["level"] += 1
        data["history"].setdefault(today(), 0)
        data["history"][today()] += amount

        print(color(f"🏆 LEVEL UP → Level {data['stats']['level']}", GREEN))
        check_achievements(data)

#streak Handaling 
#------------------------------

def update_streak(data):
    last = data["stats"]["last_active"]
    if last != today():
        data["stats"]["streak"] += 1
        data["stats"]["last_active"] = today()
        add_xp(data, 25)

#command router 
#-----------------------------------------------------
def show_help():
    print(color("\n📘 AVAILABLE COMMANDS", GREEN))
    print("  help                 Show this help menu")
    print("  status               Show level, XP, streak")
    print("  save                 Save data manually")
    print("")
    print("  📅 TASKS")
    print("  task add <text>      Add a daily task")
    print("  task done <number>   Complete a task")
    print("  tasks                List today's tasks")
    print("")
    print("  🌱 HABITS")
    print("  habit add <name>     Add a habit")
    print("  habit done <name>    Complete a habit")
    print("  habits               List all habits")
    print("")
    print("  🧠 STUDY")
    print("  study <minutes>      Start Pomodoro timer")
    print("")
    print("  📈 ANALYTICS")
    print("  xp                   View XP history")
    print("  achievements         View unlocked achievements")
    print("")
    print("  🎨 SETTINGS")
    print("  color on             Enable colors")
    print("  color off            Disable colors")
    print("")
    print("  calc <expr>      Calculator (ex: calc 2+3*4)")
    print("")
    print("  exit                 Save, backup & exit\n")
    print("")
    print("  task add <title> | <date time>   Add task")
    print("")
    print("  tasks                            List all tasks")
    print("")
    print("  tasks today                      List today's tasks")
    print("")
    print("  task done <id>                   Complete task")
def daily_summary(data):
    task_date = today()
    tasks = data["tasks"].values()

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    overdue = sum(
        1 for t in tasks
        if not t["done"] and datetime.strptime(t["due"], "%Y-%m-%d %H:%M") < datetime.now()

    )

    print(color("\n DAILY SUMMARY", GREEN))
    print(F"Tasks total : {total}")
    print(f"Completed   : {done}")
    print(color(f"Overdue    : {overdue}", RED if overdue else GREEN))
# remainders checking
def check_reminders(data):
    now_dt = datetime.now()

    for task in data["tasks"].values():
        if task["done"]:
            continue

        due_dt = datetime.strptime(task["due"], "%Y-%m-%d %H:%M")
        diff = (due_dt - now_dt).total_seconds()

        if 0 < diff <= 600:
            print(color(f"Reminder: {task['title']} due at {task['due']}", YELLOW))

#status  ------
def status(data):
    stats = data["stats"]
    print("\n 📊 STATUS")
    print(f"Level: {stats['level']}")
    print(color(xp_bar(stats['xp'], stats['level']), GREEN))
    print(f"Streak: {stats['streak']} days")
    print(f"Last active: {stats['last_active']}\n")

def handle_command(cmd, data):
    global COLORS_ENABLED
    if cmd == "help task":
        print(color("\n📅 TASK COMMANDS", GREEN))
        print("task add <text>       Add a task for today ")
        print("task done <number>    Mark task as completed")
        print("tasks                 List today's tasks\n")
        return

    if cmd == "help habit":
        
        print(color("\n TASK COMMANDS", GREEN))
        print("habit add <name>     Add a new habit")
        print("habit done <name>    Complete a habit")
        print("habits               List all habits\n")
        return

    if cmd == "help":
        show_help()
    elif cmd == "status":
        status(data)
    elif cmd == "save":
        save_data(data)
        backup_data()
        print(color("💾 Data saved & backed up. Goodbye!", GREEN))
    elif cmd == "color off":
        COLORS_ENABLED = False
        print("Color disabled")
    elif cmd == "color on":
        COLORS_ENABLED = True
        print(color("Colors enabled",GREEN))
    elif cmd.startswith("calc"):
        expr = cmd.replace("calc","", 1).strip()
        if not expr:
            print(color("⚠ Usage: calc <expression>", YELLOW))
            return
        calculator(expr)
    elif cmd.startswith("habit add"):
        name = cmd.replace("habit add", "").strip()
        if not name:
            print(color("Habit name required", YELLOW))
            return
        data["habits"][name] = {"count": 0}
        add_xp(data,10)
        print(color(f"🌱 Habit '{name}' added", GREEN))
    elif cmd.startswith("habit done"):
        name = cmd.replace("habit done", "").strip()
        if name not in data["habits"]:
            print(color("Habit not found", RED))
            return
        data["habits"][name]["count"] += 1
        add_xp(data,15)
        print(color(f"✔ Habit '{name}' completed", GREEN))
    elif cmd == "habits":
        print(color("\n🌱 HABITS", GREEN))
        for h, v in data["habits"].items():
            print(f"- {h}: {v['count']} times")

    elif cmd == "xp":
        print(color("\n 📈 XP ANALYTICS",GREEN))
        for d, xp in data["history"].items():
            print(f"{d}:{xp} XP")
    elif cmd == "achievements":
        print(color( "\n 🏆 ACHIEVEMENTS", GREEN))
        for a in data["achievements"]:
            print(f"- {a}")
    elif cmd.startswith("study"):
        mins = cmd.replace("study", "").strip()
        if not mins.isdigit():
            print(color("usage: study 25",YELLOW))
        Pomodoro(int(mins), data)
    elif cmd == "export json":
        with open("lifeos_export.json", "w") as f:
            json.dump(data, f, indent=2)
        print(color(" Exported to lifeos_export.json", GREEN))
    elif cmd == "export csv":
        import csv
        with open("xp_history.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Date",  "xp"])
            for d, xp in data["history"].items():
                writer.writerow([d, xp])
        print(color("Exported to xp_history.csv", GREEN))
    elif cmd.startswith("task add"):
        rest = cmd.replace("task add", "", 1).strip()

        if not rest:
            print(color("⚠ Task title required", YELLOW))
            return

        if "|" in rest:
            title, due = rest.split("|", 1)
            due = due.strip()

        else:
            title = rest
            due = f"{today()} 23:59"

        add_task(data, title.strip(), due)

    elif cmd == "tasks":
        list_tasks(data)
    elif cmd == "tasks today":
        list_tasks(data, today_only=True)
    elif cmd.startswith("task done"):
        task_id = cmd.replace("task done", "").strip()
        if not task_id:
            print(color("⚠ Usage: task done <task_id>", YELLOW))
            return
        complete_task(data, task_id)
    else:
        print(color("⚠ Unknown command. Type 'help'", YELLOW))
#--------------------
def spinner(duration=2):
    symbols = ["|", "/", "-", "\\"]
    end_time = time.time() + duration

    i = 0
    while time.time() < end_time:
        sys.stdout.write("\r" + symbols[i % len(symbols)] + " Loading...")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1    
    sys.stdout.write("\r✔ Done            \n ")

#-------------------------
def progress_bar(total=20, delay=0.05):
    for i in range(total + 1):
        filled = "#" * i
        empty = "-" * (total - i)
        sys.stdout.write(f"\r[{filled}{empty}]")
        sys.stdout.flush()
        time.sleep(delay)
    print()
#-------------------------
def beep():
    try:
        if os.name == "nt":
            import winsound
        else:
            print("\a", end="")
    except:
        pass
#main loop

def main():
    boot_loader()
    data = load_data()
    update_streak(data)
    config = load_config()
    daily_summary(data)
    print(f"\n{APP_NAME} v{VERSION}")
    print("Type 'help' to begin.\n")
    if readline:
        readline.set_completer(completer)
        readline.parse_and_bind("tab: complete")
    while True:
        try:
            cmd = input("> ").strip()
        except KeyboardInterrupt:
            print("\nExiting safely.")
            save_data(data)
            backup_data()
            shutdown_animation()
            break
        check_reminders(data)
        cmd = config["keybindings"].get(cmd, cmd)
        if cmd == "exit":
            save_data(data)
            backup_data()
            shutdown_animation()
            break

        handle_command(cmd, data)


if __name__ == "__main__":
    main()

#--------------------------------------------------------
#the code is fnished. this program is helpful for the students 
#code to help students 