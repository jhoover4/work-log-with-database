from datetime import datetime


class HelperFunctions:
    @staticmethod
    def date_check(date_str):
        """Dates must be in DD/MM/YYYY format"""

        date_good = True

        try:
            datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            date_good = False

        return date_good

    @staticmethod
    def time_check(time_str):
        """Times must be in minutes format"""

        time_good = True

        try:
            datetime.strptime(time_str, "%M")
        except ValueError:
            time_good = False

        return time_good