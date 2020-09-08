import pandas as pd
import pandas_gbq
import datetime as dt
import yaml
from pathlib import Path

from .pushshift import pushshift


class RedditCollector():
    """
    Class to collect reddit data.
    """
    _REQUIRED_CONFIG = [
        "gbq_project",
        "gbq_submission_table",
        "gbq_comments_table"
    ]
    
    def __init__(self, config):
        if not isinstance(config, (dict, str)):
            raise TypeError("config must be a dict or path to a YAML config")
            
        self.pushshift = pushshift
        if isinstance(config, str):
            config_path = Path(config)
            if config_path.exists():
                with config_path.open() as f:
                    config = yaml.safe_load(f)
            else:
                raise ValueError(f"File doesn't exist at: {config_path.as_posix()}")
        
        if not all(element in config for element in self._REQUIRED_CONFIG):
            raise ValueError(f"config must contain the following keys: {', '.join(self._REQUIRED_CONFIG)}")

        self.config = config
                

    def collect_submissions(self, query, start_date, end_date, write_to_gbq=False):
        """
        Collect reddit submissions for the given configuration
        parameters and write them to Google Big Query.
        """
        submissions = self._collect("comments", query, start_date, end_date)
        
        if write_to_gbq:
            self._write_to_gbq(submissions)
        
        return submissions
        
        
    def collect_comments(self, query, start_date, end_date, write_to_gbq=False):
        """
        Collect reddit comments for the given configuration
        parameters and write them to Google Big Query.
        """
        comments = self._collect("comments", query, start_date, end_date)
        
        if write_to_gbq:
            self._write_to_gbq(comments)

        return comments
        
        
    @staticmethod
    def _parse_date_to_timestamp(date):
        return int(dt.datetime.strptime(date, "%Y/%m/%d").timestamp())
    
    def _write_to_gbq(self, dataframe):
        pandas_gbq.to_gbq(
            dataframe,
            self.config["gbq_comments_table"], 
            project_id=self.config["gbq_project"],
            if_exists="append"
        )
        
        
    def _collect(self, mode, query, start_date, end_date):
        """
        Collect data from pushshift for specified mode ("comments or "))
        """
        if mode not in ["comments", "submissions"]:
            raise ValueError("Mode must be comments or submissions")
        gen = getattr(self.pushshift, "search_" + mode)(
            q=query,
            after=self._parse_date_to_timestamp(start_date),
            before=self._parse_date_to_timestamp(end_date)
            )

        return pd.DataFrame([obj.d_ for obj in gen])
            