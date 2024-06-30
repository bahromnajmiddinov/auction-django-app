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
