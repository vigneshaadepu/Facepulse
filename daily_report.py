import os
import pandas as pd
import matplotlib.pyplot as plt

ATTENDANCE_DIR = "attendance"

def generate_daily_report(date_str):
    file_name = f"attendance_{date_str}.csv"
    file_path = os.path.join(ATTENDANCE_DIR, file_name)

    if not os.path.exists(file_path):
        print("No attendance data for this date")
        return

    df = pd.read_csv(file_path)

    # Print daily report in console
    print("\n📅 Daily Attendance Report:", date_str)
    print(df)
    print("\nTotal Students Present:", len(df))

    # Generate bar graph
    plt.figure(figsize=(6, 4))
    plt.bar(df["Name"], [1] * len(df))
    plt.ylabel("Present")
    plt.xlabel("Students")
    plt.title(f"Daily Attendance - {date_str}")
    plt.ylim(0, 1.5)
    plt.tight_layout()
    plt.show()
