import random
from datetime import datetime, timezone
from pymongo import MongoClient
from config import DATABASE_NAME, MONGO_URI

userdata = []
umonth = [4,5,6,7]

for cmonth in umonth:

    # 월별 운동 횟수 16~20회
    workout_count = random.randint(16, 20)

    # 해당 월에서 운동할 날짜를 중복 없이 뽑음
    max_day = 30 if cmonth in [4,6] else 31

    workout_days = random.sample(
        range(1, max_day + 1),
        workout_count
    )

    for day in workout_days:

        hour = random.choice([0, 7, 8, 11])
        minute = random.randrange(0, 60, 5)

        date = datetime(
            2026,
            cmonth,
            day,
            hour,
            minute,
            tzinfo=timezone.utc
        )

        # 10분 ~ 20분 사이, 밀리초 정수
        workout_time = random.randint(
            10 * 60 * 1000,
            20 * 60 * 1000
        )

        userdata.append({
            "date": date.strftime("%Y-%m-%dT%H:%M:%S.000Z"),
            "time": workout_time
        })

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db['userdata']
collection.insert_many(userdata)