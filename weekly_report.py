import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

ATTENDANCE_DIR = "attendance"

def generate_weekly_graph(student_name):
    today = datetime.now().date()
    dates = []
    presence = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        file_name = f"attendance_{day}.csv"
        file_path = os.path.join(ATTENDANCE_DIR, file_name) 

        dates.append(day.strftime("%Y-%m-%d"))

        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            if student_name in df["Name"].values:
                presence.append(1)
            else:
                presence.append(0)
        else:
            presence.append(0)

    # Plot graph
    plt.figure(figsize=(8, 4))
    plt.plot(dates, presence, marker="o")
    plt.yticks([0, 1], ["Absent", "Present"])
    plt.xlabel("Date")
    plt.ylabel("Attendance")
    plt.title(f"Weekly Attendance Report - {student_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
