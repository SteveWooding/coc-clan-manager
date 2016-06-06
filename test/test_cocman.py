import unittest, datetime, sys

sys.path.append('../')

from cocman.database_setup import Member
from cocman.update_database import update_member_stats

class CocmanUpdateMemberStatsTest(unittest.TestCase):
    def setUp(self):
        # Create a member with some data for each test.
        self.member = Member()
        self.member.total_donations = 1000
        self.member.total_donations_rec = 800
        self.member.current_donations = 100
        self.member.current_donations_rec = 80
        self.member.last_active_time = datetime.datetime(2016, 1, 1)

    def tearDown(self):
        # Clean up
        self.member = None

    def test_last_active_date1(self):
        # Test to make sure 'last active date' doesn't get set to the date of
        # the start of a new season.
        update_member_stats(self.member, 0, False)
        self.assertEqual(self.member.last_active_time,
                         datetime.datetime(2016, 1, 1))

    def test_last_active_date2(self):
        # Test to make sure all 'last active date' doesn't get set to the date
        # of the start of a new season.
        update_member_stats(self.member, 13, False)
        self.assertGreater(self.member.last_active_time,
                         datetime.datetime(2016, 1, 1))

    def test_total_donations1(self):
        # Test to make sure total troop donations are preserved across seasons.
        update_member_stats(self.member, 0, False)
        self.assertEqual(self.member.total_donations, 1000)
        self.assertEqual(self.member.total_donations_rec, 800)

    def test_total_donations2(self):
        # Test to make sure total troop donations are preserved across seasons.
        update_member_stats(self.member, 13, False)
        self.assertEqual(self.member.total_donations, 1013)
        self.assertEqual(self.member.total_donations_rec, 800)

    def test_total_donations_rec1(self):
        # Test to make sure total troop donations received are preserved across
        # seasons.
        update_member_stats(self.member, 0, True)
        self.assertEqual(self.member.total_donations, 1000)
        self.assertEqual(self.member.total_donations_rec, 800)

    def test_total_donations_rec2(self):
        # Test to make sure total troop donations received are preserved across
        # seasons.
        update_member_stats(self.member, 13, True)
        self.assertEqual(self.member.total_donations, 1000)
        self.assertEqual(self.member.total_donations_rec, 813)


class CocmanUpdateMemberStatsTest2(unittest.TestCase):
    def setUp(self):
        # Create a member with some data for each test.
        self.member = Member()
        self.member.total_donations = 1000
        self.member.total_donations_rec = 800
        self.member.current_donations = 0
        self.member.current_donations_rec = 0

    def test_returning_member(self):
        # Test to make sure a returning member keeps their total donations.
        update_member_stats(self.member, 0, False)
        self.assertEqual(self.member.total_donations, 1000)
        self.assertEqual(self.member.total_donations_rec, 800)

    def test_new_season(self):
        update_member_stats(self.member, 13, False)
        self.assertEqual(self.member.total_donations, 1013)
        self.assertEqual(self.member.total_donations_rec, 800)


class CocmanUpdateMemberStatsTest3(unittest.TestCase):
    def setUp(self):
        # Create a member with some data for each test.
        self.member = Member()
        self.member.total_donations = 24
        self.member.total_donations_rec = 0
        self.member.current_donations = 24
        self.member.current_donations_rec = 17

    def test_current_larger_than_total(self):
        update_member_stats(self.member, 18, True)
        self.assertEqual(self.member.total_donations, 24)
        self.assertEqual(self.member.total_donations_rec, 18)


class CocmanUpdateMemberStatsTest4(unittest.TestCase):
    def setUp(self):
        # Create a member with some data for each test.
        self.member = Member()

    def test_new_member(self):
        update_member_stats(self.member, 42, False)
        self.assertEqual(self.member.current_donations, 42)
        self.assertEqual(self.member.current_donations_rec, None)
        self.assertEqual(self.member.total_donations, 42)
        self.assertEqual(self.member.total_donations_rec, None)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(
        CocmanUpdateMemberStatsTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        CocmanUpdateMemberStatsTest2)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        CocmanUpdateMemberStatsTest3)
    unittest.TextTestRunner(verbosity=2).run(suite)

    suite = unittest.TestLoader().loadTestsFromTestCase(
        CocmanUpdateMemberStatsTest4)
    unittest.TextTestRunner(verbosity=2).run(suite)
