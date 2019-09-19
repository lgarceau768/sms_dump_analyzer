class SMS:
    date = ''
    number = ''
    message = ''
    type = ''

    def __init__(self, date, number, message, type):
        self.date = date
        self.number = number
        self.message = message
        self.type = type

    def get_date(self):
        return self.date
    
    def get_number(self):
        return self.number

    def get_message(self):
        return self.message

    def get_type(self):
        return self.type

    def __str__(self):
        return 'Text on: %s |  type: %s  |  phone number: %s  |  message: %s' % (self.date, self.type, self.number, self.message)

    # compares number
    def compare(self, otherSMS):
        if self.get_number() == otherSMS.get_number():
            return 1
        else:
            return 0