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
        # Get the current time, assuming you want to compare everything in UTC
        now = datetime.datetime.now(pytz.UTC)  # You can use another timezone if necessary

        # Ensure the reminder's time is also timezone-aware (self.time must be in UTC)
        return self.fired is False and now >= self.time
