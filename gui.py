import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import subprocess
import os
import pandas as pd
from datetime import datetime, timedelta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import platform
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

attendance_loading = False
loading_label = None
loading_bar = None

# ================= THEME ================= #
dark_mode = True

LIGHT_THEME = {
    "bg": "#f1f5f9",
    "sidebar": "#e2e8f0",
    "card": "#ffffff",
    "text": "#0f172a",
    "muted": "#475569",
    "accent": "#2563eb"
}

DARK_THEME = {
    "bg": "#0f172a",
    "sidebar": "#020617",
    "card": "#1e293b",
    "text": "#e5e7eb",
    "muted": "#94a3b8",
    "accent": "#38bdf8"
}


COLLEGE_WIFI_SSIDS = [
    "NetDonar"
]

def get_connected_wifi():
    system = platform.system()

    try:
        if system == "Windows":
            output = subprocess.check_output(
                ["netsh", "wlan", "show", "interfaces"],
                stderr=subprocess.DEVNULL
            ).decode()

            for line in output.split("\n"):
                if "SSID" in line and "BSSID" not in line:
                    return line.split(":")[1].strip()

        elif system == "Linux":
            return subprocess.check_output(
                ["iwgetid", "-r"]
            ).decode().strip()

    except:
        return None

    return None


def is_inside_college_wifi():
    ssid = get_connected_wifi()
    return ssid in COLLEGE_WIFI_SSIDS


# ================= PATHS ================= #
BASE_DIR = os.getcwd()
ATTENDANCE_DIR = os.path.join(BASE_DIR, "attendance")
USERS_FILE = os.path.join(BASE_DIR, "users.csv")

attendance_running = False
current_user = None
current_role = None

# ================= COLORS ================= #
BG_DARK = "#0f172a"
SIDEBAR_BG = "#020617"
CARD_BG = "#1e293b"
ACCENT = "#38bdf8"
STUDENT_ACCENT = "#22c55e"
TEXT = "#e5e7eb"
MUTED = "#94a3b8"

# ================= UTIL ================= #

def load_users():
    users = {}
    if os.path.exists(USERS_FILE):
        df = pd.read_csv(USERS_FILE)
        for _, row in df.iterrows():
            users[row["username"]] = {
                "password": row["password"],
                "role": row["role"]
            }
    return users

# ================= LOGIC ================= #

def start_attendance():
    global attendance_running

    # 🔒 Wi-Fi geofence check
    if not is_inside_college_wifi():
        messagebox.showerror(
            "Attendance Blocked",
            "You are not connected to the campus Wi-Fi network."
        )
        return

    if attendance_running:
        messagebox.showwarning(
            "Attendance",
            "Attendance already running."
        )
        return

    attendance_running = True
    status_bar.config(text="📸 Attendance running...")

    start_loading_animation()

    def run():
        subprocess.call(
            ["python", "recognize_attendance.py"],
            cwd=BASE_DIR
        )

        global attendance_running
        attendance_running = False

        root.after(0, stop_loading_animation)
        status_bar.config(text="✔ Attendance completed successfully.")

    threading.Thread(target=run, daemon=True).start()



def student_attendance_percentage(student):
    present = 0
    total = 0

    if not os.path.exists(ATTENDANCE_DIR):
        return "0%"

    for file in os.listdir(ATTENDANCE_DIR):
        if file.startswith("attendance_"):
            total += 1
            df = pd.read_csv(os.path.join(ATTENDANCE_DIR, file))
            if student in df["Name"].values:
                present += 1

    if total == 0:
        return "0%"

    return f"{round((present / total) * 100, 2)}%"


def start_loading_animation():
    global attendance_loading, loading_label, loading_bar

    attendance_loading = True

    # Clear cards area
    for w in cards.winfo_children():
        w.destroy()

    loading_label = tk.Label(
        cards,
        text="📸 Attendance Running...\nScanning faces",
        font=("Segoe UI", 16, "bold"),
        fg=ACCENT,
        bg=CARD_BG,
        pady=20
    )
    loading_label.pack(pady=20)

    loading_bar = tk.Label(
        cards,
        text="",
        font=("Consolas", 16),
        fg=TEXT,
        bg=CARD_BG
    )
    loading_bar.pack()

    animate_loading_bar()



def animate_loading_bar(step=0):
    if not attendance_loading:
        return

    bar_length = 20
    filled = step % bar_length
    bar = "█" * filled + "░" * (bar_length - filled)

    loading_bar.config(text=f"[ {bar} ]")

    root.after(150, lambda: animate_loading_bar(step + 1))
def stop_loading_animation():
    global attendance_loading
    attendance_loading = False

    for w in cards.winfo_children():
        w.destroy()

    tk.Label(
        cards,
        text="✔ Attendance Completed",
        font=("Segoe UI", 18, "bold"),
        fg="#22c55e",
        bg=CARD_BG,
        pady=30
    ).pack()


def show_weekly_graph(student):
    # Clear previous content
    for w in cards.winfo_children():
        w.destroy()

    days = []
    values = []

    today = datetime.now().date()

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        days.append(day.strftime("%a"))

        file = os.path.join(ATTENDANCE_DIR, f"attendance_{day}.csv")
        if os.path.exists(file):
            df = pd.read_csv(file)
            df = df[df["Name"].str.lower() != "unknown"]
            values.append(1 if student in df["Name"].values else 0)
        else:
            values.append(0)

    fig = plt.Figure(figsize=(7, 3), dpi=100)
    ax = fig.add_subplot(111)

    ax.bar(days, values)
    ax.set_ylim(0, 1)
    ax.set_ylabel("Presence")
    ax.set_title(f"Weekly Attendance – {student}")

    canvas = FigureCanvasTkAgg(fig, master=cards)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

    status_bar.config(text=f"📊 Showing weekly attendance graph for {student}")

def toggle_theme():
    global dark_mode
    dark_mode = not dark_mode

    theme = DARK_THEME if dark_mode else LIGHT_THEME

    # Root & main
    root.configure(bg=theme["bg"])
    main.configure(bg=theme["bg"])
    header.configure(bg=theme["bg"])
    cards.configure(bg=theme["bg"])

    # Sidebar
    sidebar.configure(bg=theme["sidebar"])
    app_title.configure(bg=theme["sidebar"], fg=theme["accent"])

    for widget in menu_container.winfo_children():
        if isinstance(widget, tk.Button):
            widget.configure(
                bg=theme["sidebar"],
                fg=theme["text"],
                activebackground=theme["card"]
            )

    # Cards
    for card in cards.winfo_children():
        if isinstance(card, tk.Frame):
            card.configure(bg=theme["card"])
            for child in card.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(
                        bg=theme["card"],
                        fg=theme["text"]
                    )

    # Header text
    header_title.configure(fg=theme["text"])
    header_sub.configure(fg=theme["muted"])

    # Status bar
    status_bar.configure(
        bg=theme["sidebar"],
        fg=theme["muted"]
    )

# ================= UI ================= #

root = tk.Tk()
root.title("AI Face Recognition Attendance System")
root.geometry("1100x650")
root.configure(bg=BG_DARK)
root.resizable(False, False)
root.eval("tk::PlaceWindow . center")

# ---------- SIDEBAR ---------- #
sidebar = tk.Frame(root, bg=SIDEBAR_BG, width=220)
sidebar.pack(side="left", fill="y")

app_title = tk.Label(
    sidebar,
    text="📸 Smart\nAttendance",
    font=("Segoe UI", 18, "bold"),
    fg=ACCENT,
    bg=SIDEBAR_BG,
    pady=25
)
app_title.pack()

menu_container = tk.Frame(sidebar, bg=SIDEBAR_BG)
menu_container.pack(fill="x")

def sidebar_btn(text, cmd):
    return tk.Button(
        menu_container,
        text=text,
        font=("Segoe UI", 11),
        fg=TEXT,
        bg=SIDEBAR_BG,
        relief="flat",
        anchor="w",
        padx=25,
        pady=10,
        activebackground=CARD_BG,
        command=cmd
    )

main = tk.Frame(root, bg=BG_DARK)
main.pack(side="right", fill="both", expand=True)


# ---------- MAIN ---------- #
main = tk.Frame(root, bg=BG_DARK)
main.pack(side="right", fill="both", expand=True)

header = tk.Frame(main, bg=BG_DARK)
header.pack(fill="x", padx=30, pady=20)

header_title = tk.Label(
    header,
    text="Welcome",
    font=("Segoe UI", 24, "bold"),
    fg=TEXT,
    bg=BG_DARK
)
header_title.pack(side="left")

header_sub = tk.Label(
    header,
    text="",
    fg=MUTED,
    bg=BG_DARK
)
header_sub.pack(side="right")

cards = tk.Frame(main, bg=BG_DARK)
cards.pack(padx=30, pady=20)

def stat_card(title, value, accent=ACCENT):
    frame = tk.Frame(cards, bg=CARD_BG, width=260, height=140)
    frame.pack(side="left", padx=12)
    frame.pack_propagate(False)

    tk.Label(frame, text=title, fg=MUTED, bg=CARD_BG).pack(anchor="w", padx=15, pady=12)
    tk.Label(frame, text=value, fg=accent, bg=CARD_BG,
             font=("Segoe UI", 30, "bold")).pack(anchor="w", padx=15)

# ---------- STATUS ---------- #
status_bar = tk.Label(
    root,
    text="Checking Wi-Fi status...",
    bg=SIDEBAR_BG,
    fg=MUTED,
    anchor="w",
    padx=15
)
status_bar.pack(side="bottom", fill="x")


def update_wifi_status():
    ssid = get_connected_wifi()

    if ssid and ssid in COLLEGE_WIFI_SSIDS:
        status_bar.config(
            text=f"📍 Campus Wi-Fi Connected ({ssid}) | Secure Mode",
            fg="#22c55e"
        )
    elif ssid:
        status_bar.config(
            text=f"❌ Outside Campus Wi-Fi ({ssid}) | Attendance Blocked",
            fg="#ef4444"
        )
    else:
        status_bar.config(
            text="❌ No Wi-Fi Detected | Attendance Blocked",
            fg="#ef4444"
        )

    root.after(5000, update_wifi_status)



# ================= DASHBOARD LOADERS ================= #

def load_admin_dashboard():
    header_title.config(text="👨‍💼 Admin Dashboard")
    header_sub.config(text=datetime.now().strftime("%A, %d %B %Y"))

    for w in menu_container.winfo_children():
        w.destroy()

    sidebar_btn("📸 Start Attendance", start_attendance).pack(fill="x")
    sidebar_btn(
    "📊 View Student Graph",
    lambda: show_weekly_graph(
        simpledialog.askstring("Student", "Enter student name:")
    )
).pack(fill="x")

    sidebar_btn("🚪 Logout", load_login_screen).pack(fill="x", pady=20)

    for w in cards.winfo_children():
        w.destroy()

    stat_card("👥 Total Students", "—")
    stat_card("📊 Reports", "Available")
    stat_card("🔐 System", "Secure")


def load_student_dashboard(student):
    
    header_title.config(text=f"👩‍🎓 Welcome, {student}")
    header_sub.config(text="Student Dashboard")

    for w in menu_container.winfo_children():
        w.destroy()

    sidebar_btn("📸 Mark Attendance", start_attendance).pack(fill="x")
    sidebar_btn(
    "📊 My Weekly Attendance",
    lambda: show_weekly_graph(student)
    ).pack(fill="x")

    sidebar_btn("🚪 Logout", load_login_screen).pack(fill="x", pady=20)

    for w in cards.winfo_children():
        w.destroy()

    stat_card("📅 Attendance %", student_attendance_percentage(student), STUDENT_ACCENT)
    stat_card("📍 Campus Status", "Verified", STUDENT_ACCENT)
    stat_card("🔐 Access Level", "Student", STUDENT_ACCENT)

# ================= LOGIN ================= #

def load_login_screen():
    global current_user, current_role
    current_user = None
    current_role = None

    # Clear sidebar + cards
    for w in menu_container.winfo_children():
        w.destroy()
    for w in cards.winfo_children():
        w.destroy()

    header_title.config(text="🔐 Secure Login")
    header_sub.config(text="AI-Based Attendance System")

    login_frame = tk.Frame(cards, bg=CARD_BG, width=420, height=340)
    login_frame.pack(pady=40)
    login_frame.pack_propagate(False)

    tk.Label(
        login_frame,
        text="Welcome Back",
        font=("Segoe UI", 18, "bold"),
        fg=TEXT,
        bg=CARD_BG
    ).pack(pady=(25, 10))

    # Username
    tk.Label(login_frame, text="Username", fg=MUTED, bg=CARD_BG).pack(anchor="w", padx=40)
    username_entry = tk.Entry(login_frame, width=28)
    username_entry.pack(pady=5)

    # Password
    tk.Label(login_frame, text="Password", fg=MUTED, bg=CARD_BG).pack(anchor="w", padx=40)
    password_entry = tk.Entry(login_frame, width=28, show="*")
    password_entry.pack(pady=5)

    error_label = tk.Label(
        login_frame,
        text="",
        fg="#ef4444",
        bg=CARD_BG,
        font=("Segoe UI", 10)
    )
    error_label.pack(pady=8)

    def attempt_login(role):
        global current_user, current_role
        user = username_entry.get().strip()
        pwd = password_entry.get().strip()

        users = load_users()

        if user in users and users[user]["password"] == pwd and users[user]["role"] == role:
            current_user = user
            current_role = role
            error_label.config(text="")

            if role == "admin":
                load_admin_dashboard()
            else:
                load_student_dashboard(user)
        else:
            error_label.config(text="Invalid username or password")

    tk.Button(
        login_frame,
        text="Login as Admin",
        width=22,
        bg=ACCENT,
        fg="black",
        command=lambda: attempt_login("admin")
    ).pack(pady=(10, 6))

    tk.Button(
        login_frame,
        text="Login as Student",
        width=22,
        bg=STUDENT_ACCENT,
        fg="black",
        command=lambda: attempt_login("student")
    ).pack()

    tk.Label(
        login_frame,
        text="🔒 Secured by AI Face Recognition & Wi-Fi",
        fg=MUTED,
        bg=CARD_BG,
        font=("Segoe UI", 9)
    ).pack(pady=15)

    tk.Button(
    header,
    text="🌙 / ☀",
    command=toggle_theme,
    bg=SIDEBAR_BG,
    fg=TEXT,
    relief="flat",
    font=("Segoe UI", 12)
).pack(side="right", padx=10)

# ================= START ================= #
toggle_theme()   # apply theme on startup

load_login_screen()
root.mainloop()
