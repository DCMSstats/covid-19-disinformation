import unittest
from disinfo.nlp.topicMod import topicAnalysis
from disinfo.functions import generate_test_data

mock_data = generate_test_data()

topic_anal = topicAnalysis(mock_data)


class TestInstatiation(unittest.TestCase):
    def test_class_inst(self):
        self.assertIsInstance(topic_anal, topicAnalysis)

