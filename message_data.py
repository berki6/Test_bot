import datetime
import pytz


class ReminderData:
    def __init__(self, row):
        self.reminder_id = row[0]
        self.chat_id = row[1]
        self.message = row[2]
        self.time = row [3]
        self.fired = row[4]

    def __repr__(self):
        return "Message:  {0}; At Time:  {1}".format(self.message, self.time.strftime('%d/%m/%Y %H:%M'))

    def should_be_fired(self):
        # Get the current time in UTC for comparison
        now_utc = datetime.datetime.now(pytz.UTC)

        # Ensure self.time is aware; if it is naive, localize it to UTC
        if self.time.tzinfo is None:
            self.time = pytz.UTC.localize(self.time)  # Localize to UTC

        # Debug: Print current time in UTC and reminder time for clarity
        print(f"Now (UTC): {now_utc}")
        print(f"Reminder time (UTC): {self.time}")

        # Compare the current UTC time to the reminder time
        return self.fired is False and now_utc >= self.time

