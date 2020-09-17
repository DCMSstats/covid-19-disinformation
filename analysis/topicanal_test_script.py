import pandas as pd
import disinfo as di
from disinfo import topicAnalysis
import re
import itertools

submissions = pd.read_csv("../test_data/example_subs.csv")

topic_anal = topicAnalysis(submissions)

topic_anal.model_LDA()
topics = topic_anal.output_topics()

print(f"shape of output is {topics.shape}")

topics.to_csv("topics.csv")

