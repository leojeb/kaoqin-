# import pandas as pd
import datetime as dt


class datetime_UDF(dt.datetime):

    def __cmp__(self, other):
        if self.month == other.month:
            if self.day == other.day:
                if self.hour == other.hour:
                    if self.minute == other.minute:
                        return 0
                    else:
                        return cmp(self.minute, other.minute)
                else:
                    return cmp(self.hour, other.hour)

            else:
                return cmp(self.day, other.day)
        else:
            return cmp(self.month, other.month)


print(datetime_UDF.strptime("21-09-10 09:10", "%y-%m-%d %H:%M"))
list = [datetime_UDF.strptime("21-09-11 09:10", "%y-%m-%d %H:%M"),
        datetime_UDF.strptime("21-09-10 09:10", "%y-%m-%d %H:%M")]
list1 = [dt.datetime.strptime("21-09-10 09:11", "%y-%m-%d %H:%M"),
        dt.datetime.strptime("21-09-10 09:10", "%y-%m-%d %H:%M")]
print(sorted(list))
print(sorted(list1))

