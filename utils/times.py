from datetime import datetime, timedelta, time
from pytz import timezone

timezoneBR = timezone('America/Sao_Paulo')

def getTimeNow(format=None):

    if(format is not None):
        return datetime.now(timezoneBR).strftime(format)

    return datetime.now(timezoneBR) 

def get_seconds_to_wait(ha):

    hour_send, minute_send, days_send = ha['hour_send'], ha['min_send'], ha['days']
    time_now = getTimeNow()

    future = datetime(time_now.year, time_now.month, time_now.day, hour_send, minute_send, tzinfo=timezoneBR)
    
    if(time(time_now.hour, time_now.minute) >= time(hour_send, minute_send)):
        future += timedelta(days=1)

    weekday = future.weekday()

    if(weekday not in days_send):
        next_day = find_next_day(weekday, days_send)
        days_to_add = dist_weekdays(weekday, next_day)
        future += timedelta(days=days_to_add)

    secs_to_wait = diff_seconds(time_now, future)

    return future, secs_to_wait

def diff_seconds(d1, d2):
    diff = d2-d1
    return int(diff.total_seconds())

def find_next_day(new_day, days):
    
    days_aux = days.copy()
    days_aux.append(new_day)
    days_aux.sort()
    idx = days_aux.index(new_day) + 1

    if(idx >= len(days_aux)):
        idx = 0

    return days_aux[idx]

def dist_weekdays(day1, day2):
    return 7 - (day1 - day2)

def get_left_time(time_future):
    time_now = getTimeNow()
    time_left_secs = diff_seconds(time_now, time_future)
    hours, remainder = divmod(time_left_secs, 3600)
    minutes, seconds = divmod(remainder, 60)
    return hours, minutes, seconds