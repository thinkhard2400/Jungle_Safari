from faker import Faker
import random
from datetime import datetime, timedelta, timezone
import json
from pymongo import MongoClient
from config import DATABASE_NAME, MONGO_URI

fake = Faker("ko_KR")


workout_type = ["러닝", "웨이트", "스트레칭"] 
room_status = ["start", "wait" ]

rooms = []

def create_log(start_time, end_time):
    logs = []
    current_time= start_time
    current_stat = "start"

    while True:
        # 다음 상태 변경까지 5~15분
        current_time += timedelta(
            minutes=random.randint(5, 15)
        )

        # 방 종료 시간을 넘으면 종료
        if current_time >= end_time:
            break

        logs.append({
            "type": current_stat,
            "timestamp": current_time.strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )
        })

        # start -> pause
        # pause -> start
        if current_stat == "start":
            current_stat = "pause"
        else:
            current_stat = "start"

    
    return logs;


for i in range(15):
    tmax = random.randint(2,4)
    status = random.choice(room_status)
    dateMonth = random.randint(8,10)
    dateDate = random.randint(1,30)

    hour = random.choice([0, 7, 8, 11])
    minute = random.randrange(0, 60, 5)

    duration = random.choice([30, 60, 90])

    start_datetime = datetime(
        2026,
        dateMonth,
        dateDate,
        hour,
        minute,
        tzinfo=timezone.utc
    )
    timestamp = start_datetime.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    end_datetime = start_datetime + timedelta(minutes=duration)
    members = []

    hostid = fake.user_name()
    hostname = fake.name()

    if (status == "start"):
        host_logs = create_log(start_datetime, end_datetime)
    else : 
        host_logs = []

    ## host 먼저 
    members.append(
        {
            "id": hostid,
            "name": hostname,
            "isHost": True,
            "isReady": True,
            "logs": host_logs
            
        }
    )
    ## 그다음 member 
    for j in range(tmax - 1):

        member_id = fake.user_name()
        member_name = fake.name()

        # 이 member 로그 생성
        if status == "start":
            member_logs = create_log(start_datetime, end_datetime)
            member_ready = True
        else:
            member_logs = []
            member_ready = random.choice([True, False])

        members.append({
            "id": member_id,
            "name": member_name,
            "isHost": False,
            "isReady": member_ready,
            "logs":  member_logs
        })

    rooms.append({
        "id" : fake.uuid4(),
        "type" : random.choice(workout_type),
        "time": (
            f"{start_datetime.strftime('%m/%d %H:%M')} ~ "
            f"{end_datetime.strftime('%H:%M')}"
        ),
        "name" : f"{hostname}님의 방",
        "max" : tmax ,
        "status" : status,
        "timestamp" : timestamp,
        "member" : members
    })



client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db['rooms']
collection.insert_many(rooms)