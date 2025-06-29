import datetime

class ExamScheduler:
    def __init__(self):
        self.exams = {}

    def normalize_time_format(self, time_str):
        try:
            start_str, end_str = time_str.split('-')
            start = datetime.datetime.strptime(start_str.strip(), "%H:%M")
            end = datetime.datetime.strptime(end_str.strip(), "%H:%M")

            if start >= end:
                return None

            return f"{start.strftime('%H:%M')}-{end.strftime('%H:%M')}"
        except ValueError:
            return None

    def add_exam(self, subject, date, time, room):
        time = self.normalize_time_format(time)
        if not time:
            print("Invalid time format. Please enter like 9:00-11:00 or 08:00-10:00.")
            return

        conflict = self.check_conflict(date, time)
        if conflict != "No conflict.":
            print(f"Cannot add exam: {conflict}")
        else:
            self.exams[(subject, date)] = {"time": time, "room": room}
            print(f"Exam for {subject} on {date} scheduled successfully.")

    def view_exams(self):
        if not self.exams:
            print("No exams scheduled.")
            return
        for (subject, date), details in sorted(self.exams.items(), key=lambda x: (x[1]['time'], x[0][1])):
            print(f"{subject} on {date} at {details['time']} in Room {details['room']}")

    def update_exam(self, subject, date, new_date=None, new_time=None, new_room=None):
        key = (subject, date)
        if key in self.exams:
            current = self.exams[key]
            date_to_check = new_date if new_date else date
            time_to_check = new_time if new_time else current["time"]

            if new_time:
                normalized = self.normalize_time_format(new_time)
                if not normalized:
                    print("Invalid time format. Please enter like 9:00-11:00 or 08:00-10:00.")
                    return
                new_time = normalized
                time_to_check = new_time

            temp_exam = self.exams.pop(key)

            conflict = self.check_conflict(date_to_check, time_to_check)
            if conflict != "No conflict.":
                print(f"Cannot update exam: {conflict}")
                self.exams[key] = temp_exam  # Restore original
                return

            new_key = (subject, new_date if new_date else date)

            updated_exam = {
                "time": new_time if new_time else current["time"],
                "room": new_room if new_room else current["room"]
            }

            self.exams[new_key] = updated_exam
            print(f"Exam for {subject} updated successfully.")
        else:
            print("Exam not found!")

    def delete_exam(self, subject, date):
        key = (subject, date)
        if key in self.exams:
            del self.exams[key]
            print(f"Exam for {subject} on {date} deleted.")
        else:
            print("Exam not found!")

    def check_conflict(self, date, new_time):
        try:
            new_start_str, new_end_str = new_time.split('-')
            new_start = datetime.datetime.strptime(new_start_str.strip(), "%H:%M")
            new_end = datetime.datetime.strptime(new_end_str.strip(), "%H:%M")

            if new_start >= new_end:
                return "Start time must be before end time."
        except ValueError:
            return "Invalid time format."

        for (subject, exam_date), details in self.exams.items():
            if exam_date == date:
                try:
                    existing_start_str, existing_end_str = details["time"].split('-')
                    existing_start = datetime.datetime.strptime(existing_start_str.strip(), "%H:%M")
                    existing_end = datetime.datetime.strptime(existing_end_str.strip(), "%H:%M")
                except ValueError:
                    continue

                if new_start < existing_end and new_end > existing_start:
                    return f"Conflict with {subject} exam on {exam_date} at {details['time']}"

        return "No conflict."


scheduler = ExamScheduler()

while True:
    print("\n=== Exam Time Scheduler ===")
    print("A: Add Exam")
    print("V: View Exams")
    print("U: Update Exam")
    print("D: Delete Exam")
    print("X: Exit")

    choice = input("What do you want to do: ").strip().lower()

    if choice == "a":
        subject = input("Enter subject: ")
        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (e.g., 9:00-11:00): ")
        room = input("Enter the assigned room: ")
        scheduler.add_exam(subject, date, time, room)

    elif choice == "v":
        scheduler.view_exams()

    elif choice == "u":
        subject = input("Enter subject: ")
        date = input("Enter current exam date (YYYY-MM-DD): ")
        new_date = input("Enter new date (YYYY-MM-DD) or press enter to skip: ")
        new_time = input("Enter new time (e.g., 9:00-11:00) or press enter to skip: ")
        new_room = input("Enter new assigned room or press enter to skip: ")
        scheduler.update_exam(subject, date, new_date or None, new_time or None, new_room or None)

    elif choice == "d":
        subject = input("Enter subject: ")
        date = input("Enter exam date to delete (YYYY-MM-DD): ")
        scheduler.delete_exam(subject, date)

    elif choice == "x":
        print("Exiting Exam Scheduler.")
        break

    else:
        print("Invalid choice. Please try again.")