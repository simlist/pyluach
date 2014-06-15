

def is_leap(year):
    if (( (7*year) + 1) % 19) < 7:
        return True
    return False
    
    
def elapsed_days(year):
    months_elapsed = (
                      (235 * ((year-1) / 19)) + (12 * ((year-1) % 19)) + 
                      (7 * ((year-1) % 19) + 1) / 19
                      )
    parts_elapsed = 204 + 793*(months_elapsed%1080)
    hours_elapsed = 5 + 12*months_elapsed + 793*(months_elapsed/1080) + parts_elapsed/1080
    conjunction_day = 1 + 29*months_elapsed + hours_elapsed/24
    conjunction_parts = 1080 * (hours_elapsed%24) + parts_elapsed%1080
    
    if (
        (conjunction_parts >= 19440) or
        (
            (conjunction_day % 7 == 2) and (conjunction_parts >= 9924) and 
           (not is_leap(year))
         ) or
        (
            (conjunction_day % 7 == 1) and
         conjunction_parts >= 16789 and is_leap(year - 1)
         )
        ):
        alt_day = conjunction_day + 1
    
    else:
        alt_day = conjunction_day
        
    if (alt_day % 7) in (0, 3, 5):
        alt_day += 1
    
    return alt_day


def days_in_year(year):
    return elapsed_days(year + 1) - elapsed_days(year)


def long_cheshvan(year):
    """Returns True if Cheshvan has 30 days"""
    return days_in_year(year) % 10 == 5


def short_kislev(year):
    """Returns True if Kislev has 29 days"""
    return days_in_year(year) % 10 == 3


def month_length(year, month):
    """Months start with Nissan (Nissan is 1 and Tishrei is 7"""
        
    if month in (1, 3, 5, 7, 11):
        return 30
    elif month in (2, 4, 6, 10, 13):
        return 29
    elif month == 12:
        return 30 if is_leap(year) else 29
    elif month == 8:   # if long Cheshvan return 30, else return 29
        return 30 if long_cheshvan(year) else 29
    elif month == 9:   # if short Kislev return 29, else return 30
        return 29 if short_kislev(year) else 30

    