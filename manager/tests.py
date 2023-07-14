from django.test import TestCase
from unittest import skip

from .views import RandomAssignTeamToGroup

class AssignTestCase(TestCase):

    @skip("This is not test")
    def testDict(self, dic: dict, param: int, size: int, array: list) -> bool:
        return len(dic[param]) == size and dic[param] in array

    def test_auto_assign_2_groups_2_teams(self):
        r = RandomAssignTeamToGroup()

        params = [2, 3]
        array = [4, 5]
        a = r.autoAssign(
            params,
            array
        )

        assert \
            self.testDict(a, 2, 1, array) and \
            self.testDict(a, 3, 1, array)

    def test_auto_assign_2_groups_3_teams(self):
        r = RandomAssignTeamToGroup()

        params = [2, 3]
        array = [4, 5, 6]
        a = r.autoAssign(
            params,
            array
        )

        assert \
            (self.testDict(a, 2, 2, array) and \
            self.testDict(a, 3, 1, array)) or \
            (self.testDict(a, 2, 1, array) and \
            self.testDict(a, 3, 2, array))

    def test_auto_assign_4_groups_7_teams(self):
        r = RandomAssignTeamToGroup()

        params = [2, 3, 4, 5]
        array = [6, 7, 8, 9, 10, 11, 12]
        a = r.autoAssign(
            params,
            array
        )

        assert \
            (
                self.testDict(a, 2, 2, array) and \
                self.testDict(a, 3, 2, array) and \
                self.testDict(a, 4, 2, array) and \
                self.testDict(a, 5, 1, array)
            ) or \
            (
                self.testDict(a, 2, 2, array) and \
                self.testDict(a, 3, 2, array) and \
                self.testDict(a, 4, 1, array) and \
                self.testDict(a, 5, 2, array)
            ) or \
            (
                self.testDict(a, 2, 2, array) and \
                self.testDict(a, 3, 1, array) and \
                self.testDict(a, 4, 2, array) and \
                self.testDict(a, 5, 2, array)
            ) or \
            (
                self.testDict(a, 2, 1, array) and \
                self.testDict(a, 3, 2, array) and \
                self.testDict(a, 4, 2, array) and \
                self.testDict(a, 5, 2, array)
            )

    def test_auto_assign_4_groups_8_teams(self):
        r = RandomAssignTeamToGroup()

        params = [2, 3, 4, 5]
        array = [6, 7, 8, 9, 10, 11, 12, 13]
        a = r.autoAssign(
            params,
            array
        )

        assert \
            (
                self.testDict(a, 2, 2, array) and \
                self.testDict(a, 3, 2, array) and \
                self.testDict(a, 4, 2, array) and \
                self.testDict(a, 5, 2, array)
            )