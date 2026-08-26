let serverOffset = 0;
let now;

async function measureServerClock() {
    const t1 = Date.now();

    const response = await fetch(
        "http://43.201.67.185:5000/sangmin/time",
        { cache: "no-store" }
    );

    const data = await response.json();

    const t4 = Date.now();

    const t2 = data.receivedAt / 1000000;
    const t3 = data.sentAt / 1000000;

    const rtt = (t4 - t1) - (t3 - t2);
    const offset = ((t2 - t1) + (t3 - t4)) / 2;

    return { rtt, offset };
}

function getServerNow() {
    return Date.now() + serverOffset;
}

async function getRooms() {
    const response = await fetch(
        "http://43.201.67.185:5000/sangmin/rooms"
    );

    const data = await response.json();

    return data.rooms;
}

function getServerNow() {
    return Date.now() + serverOffset;
}

async function init() {
    const result = await measureServerClock();

    serverOffset = result.offset;
    rooms = await getRooms();

    console.log("RTT:", result.rtt);
    console.log("offset:", serverOffset);

}

now = getServerNow();

let user = {
    "id": "sangmin123",
    "name": "이상민"
};

let rooms = [];

const storeReady = init();

let roomData = {
    roomId: "1a2b",
    roomName: "이상민님의 방",
    time: "08/24 23:00 ~ 23:30",
    status: "start",
    timestamp: new Date(now - 480000).toISOString(),
    members: [
        {
            id: "sangmin123",
            name: "이상민",
            isHost: true,
            isReady: true,
            logs: [
                {
                    type: "start",
                    timestamp: new Date(now - 222400).toISOString()
                }
            ]
        },
        {
            id: "minkyu",
            name: "박민규",
            isHost: false,
            isReady: true,
            logs: [
                {
                    type: "start",
                    timestamp: new Date(now - 222750).toISOString()
                }
            ]
        },
        {
            id: "haesun",
            name: "박해선",
            isHost: false,
            isReady: false,
            logs: [
                {
                    type: "start",
                    timestamp: new Date(now - 180000).toISOString()
                },
                {
                    type: "pause",
                    timestamp: new Date(now - 96000).toISOString()
                }
            ]
        }
    ]
};

const workoutRecords = [

    {
        date: "2026-09-02T12:15:00.000Z",
        time: 1275000
    },

    {
        date: "2026-09-04T08:15:00.000Z",
        time: 1260000
    },

    {
        date: "2026-09-06T12:05:00.000Z",
        time: 6165000
    },

    {
        date: "2026-09-07T12:00:00.000Z",
        time: 4080000
    },

    {
        date: "2026-09-09T09:00:00.000Z",
        time: 3600000
    },

    {
        date: "2026-09-11T11:10:00.000Z",
        time: 4440000
    },

    {
        date: "2026-09-12T12:50:00.000Z",
        time: 1380000
    },

    {
        date: "2026-09-12T12:45:00.000Z",
        time: 1800000
    },

    {
        date: "2026-09-13T08:40:00.000Z",
        time: 990000
    },

    {
        date: "2026-09-13T08:45:00.000Z",
        time: 1875000
    },

    {
        date: "2026-09-14T13:40:00.000Z",
        time: 3975000
    },

    {
        date: "2026-09-15T12:35:00.000Z",
        time: 2100000
    },

    {
        date: "2026-09-15T09:10:00.000Z",
        time: 1980000
    },

    {
        date: "2026-09-16T12:20:00.000Z",
        time: 4005000
    },

    {
        date: "2026-09-18T11:20:00.000Z",
        time: 3480000
    },

    {
        date: "2026-09-20T12:30:00.000Z",
        time: 1320000
    },

    {
        date: "2026-09-20T09:35:00.000Z",
        time: 2640000
    },

    {
        date: "2026-09-21T13:05:00.000Z",
        time: 6000000
    },

    {
        date: "2026-09-23T10:55:00.000Z",
        time: 2490000
    },

    {
        date: "2026-09-25T11:05:00.000Z",
        time: 5415000
    },

    {
        date: "2026-09-27T13:50:00.000Z",
        time: 1065000
    },

    {
        date: "2026-09-28T12:50:00.000Z",
        time: 5505000
    },

    {
        date: "2026-09-30T11:50:00.000Z",
        time: 2400000
    },

    {
        date: "2026-10-02T09:45:00.000Z",
        time: 1155000
    },

    {
        date: "2026-10-02T08:15:00.000Z",
        time: 2160000
    },

    {
        date: "2026-10-03T13:15:00.000Z",
        time: 3315000
    },

    {
        date: "2026-10-04T08:10:00.000Z",
        time: 4380000
    },

    {
        date: "2026-10-05T09:30:00.000Z",
        time: 5445000
    },

    {
        date: "2026-10-07T11:25:00.000Z",
        time: 4080000
    },

    {
        date: "2026-10-09T09:05:00.000Z",
        time: 2025000
    },

    {
        date: "2026-10-11T09:00:00.000Z",
        time: 4440000
    },

    {
        date: "2026-10-12T10:20:00.000Z",
        time: 1290000
    },

    {
        date: "2026-10-14T10:45:00.000Z",
        time: 3645000
    },

    {
        date: "2026-10-16T12:45:00.000Z",
        time: 4740000
    },

    {
        date: "2026-10-18T11:50:00.000Z",
        time: 5655000
    },

    {
        date: "2026-10-19T11:30:00.000Z",
        time: 1200000
    },

    {
        date: "2026-10-21T09:05:00.000Z",
        time: 5760000
    },

    {
        date: "2026-10-23T08:25:00.000Z",
        time: 3540000
    },

    {
        date: "2026-10-25T12:10:00.000Z",
        time: 4050000
    },

    {
        date: "2026-10-26T08:05:00.000Z",
        time: 6075000
    },

    {
        date: "2026-10-28T09:50:00.000Z",
        time: 2250000
    },

    {
        date: "2026-10-30T10:35:00.000Z",
        time: 3195000
    },

    {
        date: "2026-11-01T11:35:00.000Z",
        time: 3480000
    },

    {
        date: "2026-11-04T08:55:00.000Z",
        time: 2055000
    },

    {
        date: "2026-11-06T13:10:00.000Z",
        time: 3750000
    },

    {
        date: "2026-11-08T10:10:00.000Z",
        time: 3390000
    },

    {
        date: "2026-11-09T10:50:00.000Z",
        time: 1065000
    },

    {
        date: "2026-11-09T10:40:00.000Z",
        time: 2460000
    },

    {
        date: "2026-11-11T10:15:00.000Z",
        time: 4830000
    },

    {
        date: "2026-11-13T10:50:00.000Z",
        time: 3060000
    },

    {
        date: "2026-11-15T09:30:00.000Z",
        time: 3780000
    },

    {
        date: "2026-11-16T12:35:00.000Z",
        time: 1560000
    },

    {
        date: "2026-11-18T10:35:00.000Z",
        time: 1680000
    },

    {
        date: "2026-11-18T13:45:00.000Z",
        time: 2415000
    },

    {
        date: "2026-11-20T13:25:00.000Z",
        time: 5580000
    },

    {
        date: "2026-11-22T09:05:00.000Z",
        time: 1920000
    },

    {
        date: "2026-11-25T09:35:00.000Z",
        time: 4500000
    },

    {
        date: "2026-11-27T11:50:00.000Z",
        time: 2085000
    },

    {
        date: "2026-11-27T08:50:00.000Z",
        time: 1515000
    },

    {
        date: "2026-11-30T13:15:00.000Z",
        time: 3675000
    },

    {
        date: "2026-12-02T13:25:00.000Z",
        time: 1215000
    },

    {
        date: "2026-12-04T11:55:00.000Z",
        time: 6300000
    },

    {
        date: "2026-12-06T09:10:00.000Z",
        time: 1365000
    },

    {
        date: "2026-12-09T09:45:00.000Z",
        time: 5865000
    },

    {
        date: "2026-12-13T10:10:00.000Z",
        time: 3600000
    },

    {
        date: "2026-12-14T08:55:00.000Z",
        time: 4365000
    },

    {
        date: "2026-12-15T09:30:00.000Z",
        time: 5280000
    },

    {
        date: "2026-12-16T08:20:00.000Z",
        time: 2520000
    },

    {
        date: "2026-12-18T12:25:00.000Z",
        time: 2340000
    },

    {
        date: "2026-12-20T08:55:00.000Z",
        time: 2445000
    },

    {
        date: "2026-12-21T12:40:00.000Z",
        time: 4320000
    },

    {
        date: "2026-12-23T12:10:00.000Z",
        time: 3375000
    },

    {
        date: "2026-12-27T09:45:00.000Z",
        time: 720000
    },

    {
        date: "2026-12-28T09:35:00.000Z",
        time: 3570000
    },

    {
        date: "2026-12-30T08:25:00.000Z",
        time: 4350000
    },

    {
        date: "2027-01-01T11:05:00.000Z",
        time: 4980000
    },

    {
        date: "2027-01-03T09:20:00.000Z",
        time: 840000
    },

    {
        date: "2027-01-03T12:35:00.000Z",
        time: 3180000
    },

    {
        date: "2027-01-04T08:35:00.000Z",
        time: 2550000
    },

    {
        date: "2027-01-08T12:15:00.000Z",
        time: 4230000
    },

    {
        date: "2027-01-10T12:35:00.000Z",
        time: 3825000
    },

    {
        date: "2027-01-11T12:20:00.000Z",
        time: 6600000
    },

    {
        date: "2027-01-13T11:10:00.000Z",
        time: 4095000
    },

    {
        date: "2027-01-15T10:05:00.000Z",
        time: 1635000
    },

    {
        date: "2027-01-15T08:15:00.000Z",
        time: 2220000
    },

    {
        date: "2027-01-17T09:55:00.000Z",
        time: 4020000
    },

    {
        date: "2027-01-18T10:10:00.000Z",
        time: 5385000
    },

    {
        date: "2027-01-20T08:30:00.000Z",
        time: 5265000
    },

    {
        date: "2027-01-22T09:10:00.000Z",
        time: 4335000
    },

    {
        date: "2027-01-24T10:30:00.000Z",
        time: 2160000
    },

    {
        date: "2027-01-25T13:25:00.000Z",
        time: 1515000
    },

    {
        date: "2027-01-26T11:55:00.000Z",
        time: 1110000
    },

    {
        date: "2027-01-29T12:20:00.000Z",
        time: 3480000
    },

    {
        date: "2027-01-31T09:05:00.000Z",
        time: 960000
    }

];