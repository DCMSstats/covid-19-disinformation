import unittest
from disinfo.nlp.redditText import redditText
from disinfo.nlp.test.test_data import generate_test_data


mock_data = generate_test_data()

reddit_text = redditText(mock_data)

class TestInstatiation(unittest.TestCase):
    def test_class_inst(self):
        self.assertIsInstance(reddit_text, redditText)



if __name__ == '__main__':
    unittest.main()
