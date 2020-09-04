import pandas as pd
import pandas_gbq
import datetime as dt
import yaml

from .pushift import pushshift


class RedditCollector():
    """
    Class to collect reddit data.
    """
    _REQUIRED_CONFIG = [
        "query",
        "start_date",
        "end_date",
        "write_to_gbq",
        "gbq_project",
        "gbq_submission_table",
        "gbq_comments_table"
    ]
    
    
    def __init__(config):
        self.pushshift = pushshift
        if isinstance(config, str):
            config = 
        
        if not isinstance(config, dict):
            raise TypeError("config must be a dict or path to a YAML config")
        
        if not all(element in config for element in self._REQUIRED_CONFIG):
            raise ValueError(f"config must contain keys: {", ".join(self._REQUIRED_CONFIG)}")

        self.config = config
        
        self.config["start_date"] = int(dt.datetime.strptime(self.config["start_date"], "%Y/%m/%d").timestamp())
        self.config["end_date"] = int(dt.datetime.strptime(self.config["end_date"], "%Y/%m/%d").timestamp())
                

    def collect_submissions(self):
        """
        Collect reddit submissions for the given configuration
        parameters and write them to Google Big Query.
        """
        gen = self.pushshift.search_submissions(
            q=self.config.["query"],
            after=self.config["start_date"],
            before=self.config["end_date"]
            )

        submissions = pd.DataFrame([obj.d_ for obj in gen])
        
        if self.config["write_to_gbq"]:
            pandas_gbq.to_gbq(
                submissions,
                self.config["gbq_submission_table"], 
                project_id=self.config["gbq_project"],
                if_exists="append"
            )
        
        else:
            return comments
        
        
    def collect_comments(self):
        """
        Collect reddit comments for the given configuration
        parameters and write them to Google Big Query.
        """
        gen = self.pushshift.search_comments(
            q=self.config.["query"],
            after=self.config["start_date"],
            before=self.config["end_date"]
            )

        comments = pd.DataFrame([obj.d_ for obj in gen])
        
        if self.config["write_to_gbq"]:
            pandas_gbq.to_gbq(
                comments,
                self.config["gbq_comments_table"], 
                project_id=self.config["gbq_project"],
                if_exists="append"
            )
        
        else:
            return comments
    