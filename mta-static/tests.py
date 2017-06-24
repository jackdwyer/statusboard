import datetime
import unittest

import lib


class TestScheduleLoader(unittest.TestCase):
    def test_parse_trip_id(self):
        inputs = [('B20161106SUN_025350_E..S04R', 'sunday'),
                  ('A20161106WKD_133300_2..S01R', 'weekday'),
                  ('B20161106WKD_059150_F..S69R', 'weekday'),
                  ('A20161106SUN_124750_1..N02R', 'sunday'),
                  ('A20161106WKD_034100_1..S02R', 'weekday'),
                  ('B20161106SAT_055350_C..N04R', 'saturday'),
                  ('A20161106SAT_033650_7..N97R', 'saturday'),
                  ('A20161106SAT_097900_7..N97R', 'saturday'),
                  ('A20161106SUN_001150_7..S97R', 'sunday'),
                  ('A20161106SAT_138550_1..N02R', 'saturday')]
        for el in inputs:
            self.assertTrue(lib.parse_trip_id(el[0]), el[1])

    def test_parse_arrive_time(self):
        inputs = ['09:30:00',
                  '03:30:30',
                  '15:33:00',
                  '24:59:00',
                  '15:11:30',
                  '12:38:30',
                  '14:51:00',
                  '10:39:00',
                  '06:32:00',
                  '14:22:00',
                  '25:13:00',
                  "26:01:30",
                  "27:01:30"]
        for el in inputs:
            self.assertTrue(isinstance(lib.parse_arrival_time(el),
                                       datetime.time))


class TestSchedule(unittest.TestCase):
    # TODO: FIX this for new data structure
    # def test_schedule_elements_are_datetime(self):
    #     schedule = lib.load_schedule()
    #     for el in schedule:
    #         self.assertTrue(isinstance(el, datetime.time))

    def test_generated_week_window(self):
        week = lib.generate_week()
        self.assertEqual(week[-1].weekday(), 5)
        self.assertEqual(len(week), 7)
        self.assertEqual(week[0].weekday(), 6)

    # def test_next_train_response(self):
    #     schedule = [
    #         datetime.datetime.strptime("01:27:00", "%H:%M:%S").time(),
    #         datetime.datetime.strptime("06:22:30", "%H:%M:%S").time(),
    #         datetime.datetime.strptime("09:02:00", "%H:%M:%S").time(),
    #         datetime.datetime.strptime("15:36:00", "%H:%M:%S").time(),
    #     ]
    #     s = tuple(schedule)
    #     now = datetime.datetime.strptime("03:30:35", "%H:%M:%S").time()
    #     response = api.get_next(now, s)
    #     self.assertTrue(response == s[1])

    #     # now = datetime.datetime.strptime("22:30:35", "%H:%M:%S").time()
    #     # response = api.get_next(s, now)
    #     # print(response)


if __name__ == '__main__':
    unittest.main()
