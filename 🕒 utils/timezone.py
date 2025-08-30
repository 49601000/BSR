from datetime import datetime, timezone, timedelta

def convert_to_utc_range(start_date, end_date):
    JST = timezone(timedelta(hours=9))
    #begin_dt = datetime.combine(start_date, datetime.min.time()).replace(tzinfo=JST)
    #end_dt = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=JST)

    # 時間を固定：開始は0:00:00、終了は23:59:59
    begin_dt = datetime.combine(start_date, time(0, 0, 0)).replace(tzinfo=JST)
    end_dt = datetime.combine(end_date, time(23, 59, 59)).replace(tzinfo=JST)

    begin_time = begin_dt.astimezone(timezone.utc).isoformat()
    end_time = end_dt.astimezone(timezone.utc).isoformat()

    return begin_time, end_time
