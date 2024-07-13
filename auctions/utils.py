import geocoder
import pycountry

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    ip = geocoder.ip(ip)

    return ip


def code_to_country_name(code):
    try:
        country = pycountry.countries.get(alpha_2=code)
        if country:
            return country.name
        else:
            return "Country not found"
    except Exception as e:
        return str(e)


def time_scheduler(date_obj, schedule_name, auction_id, task):
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    hour = date_obj.hour
    minute = date_obj.minute 
    
    schedule, created = CrontabSchedule.get_or_create(year=year, month=month, day=day, hour=hour, minute=minute)
    task = PeriodicTask.objects.create(crontab=schedule, name=schedule_name, task='tasks.time_end', args=json.dumps((auction_id, task,)))
