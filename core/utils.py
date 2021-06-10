import pytz

timezone = pytz.timezone('Asia/Ho_Chi_Minh')


def localize_datetime(datetime):
    return timezone.localize(datetime)
