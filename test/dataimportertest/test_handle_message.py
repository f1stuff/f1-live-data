import json

from fastf1.utils import to_datetime

from dataimporter.importer import fix_json
from dataimporter.message_handler import handle_message


def test_gap_to_leader_and_interval_to_pos_ahead():
    msg = "['TimingData', {'Lines': {'63': {'GapToLeader': '+44.163', 'IntervalToPositionAhead': {'Value': '+1.667'}}}}, '2023-03-05T16:08:38.509Z']"
    msg = fix_json(msg)
    cat, msg, dt = json.loads(msg)
    dt = to_datetime(dt)
    points = handle_message(cat, msg, dt)
    assert len(points) == 2
    assert points[0]._name == "gapToLeader"
    assert points[1]._name == "intervalToPositionAhead"

    assert "driver" in points[0]._tags
    assert points[0]._tags["driver"] == "RUS"

    assert "GapToLeader" in points[0]._fields
    assert points[0]._fields["GapToLeader"] == 44.163

    assert "IntervalToPositionAhead" in points[1]._fields
    assert points[1]._fields["IntervalToPositionAhead"] == 1.667


def test_lapped_car():
    msg = "['TimingData', {'Lines': {'20': {'GapToLeader': '1 L', 'IntervalToPositionAhead': {'Value': '+15.040'}}}}, '2023-03-05T16:08:38.509Z']"
    msg = fix_json(msg)
    cat, msg, dt = json.loads(msg)
    dt = to_datetime(dt)
    points = handle_message(cat, msg, dt)
    assert len(points) == 2
    assert points[0]._name == "gapToLeader"
    assert points[1]._name == "intervalToPositionAhead"

    assert "driver" in points[0]._tags
    assert points[0]._tags["driver"] == "MAG"


def test_number_laps():
    msg = "['TimingData', {'Lines': {'10': {'NumberOfLaps': 7, 'Sectors': {'2': {'Value': '25.040'}}, 'Speeds': {'FL': {'Value': '285'}}, 'LastLapTime': {'Value': '1:41.134'}}}}, '2023-03-05T15:15:33.534Z']"
    msg = fix_json(msg)
    cat, msg, dt = json.loads(msg)
    dt = to_datetime(dt)
    points = handle_message(cat, msg, dt)
    assert len(points) == 2
    assert points[1]._name == "numberOfLaps"

    assert "NumberOfLaps" in points[1]._fields
    assert points[1]._fields["NumberOfLaps"] == 7

