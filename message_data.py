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
        gmt_plus_3 = pytz.timezone('Etc/GMT-3')
        now = datetime.datetime.now(gmt_plus_3)

        if self.time.tzinfo is None:
            self.time = gmt_plus_3.localize(self.time)

        return self.fired is False and now >= self.time

