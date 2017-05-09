import unittest
from main_index import Interface_Tasking
from bson.objectid import ObjectId

class APIGetAdList(unittest.TestCase):

    def test_call(self):
        api = Interface_Tasking()
        api.give_one_objectid(ObjectId("58ef373294f941a5b4f24c14"))


if __name__ == '__main__':
    unittest.main()
