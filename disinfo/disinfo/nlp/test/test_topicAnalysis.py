import unittest
from disinfo.nlp.topicMod import topicAnalysis
from disinfo.nlp.test.test_data import generate_test_data

mock_data = generate_test_data()

topic_anal = topicAnalysis(mock_data)

topic_anal.model_LDA()

class TestInstatiation(unittest.TestCase):
    def test_class_inst(self):
        self.assertIsInstance(topic_anal, topicAnalysis)

class TestTopicModels(unittest.TestCase):
    def test_lda(self):
        topic_anal.model_LDA()
        self.assertTrue('topic_model' in topic_anal.__dict__)
        delattr(topic_anal, 'topic_model')

    def test_nmf(self):
        topic_anal.model_NMF()
        self.assertTrue('topic_model' in topic_anal.__dict__)