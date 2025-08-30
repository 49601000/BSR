from datetime import datetime, timezone, timedelta

def convert_to_utc_range(start_date, end_date):
    JST = timezone(timedelta(hours=9))
    begin_dt = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=JST)
    end_dt = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=JST)

    begin_time = begin_dt.astimezone(timezone.utc).isoformat()
    end_time = end_dt.astimezone(timezone.utc).isoformat()

    return begin_time, end_time
