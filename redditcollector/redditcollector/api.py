import pandas as pd
import pandas_gbq
import datetime as dt
import yaml
from pathlib import Path
import uuid
import json

from .pushshift import pushshift


class RedditCollector():
    """
    Class to facilitate collection of reddit data for specific search terms or subreddits.
    Data can be collected between specified start and end dates.
    
    All data collections are assigned a unique identifier, which is logged in the gbq_logging_table.
    """
    _REQUIRED_CONFIG = [
        "gbq_project",
        "gbq_submissions_table",
        "gbq_comments_table",
        "gbq_logging_table",
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
                

    def collect_submissions(self, query, start_date, end_date, subreddits=None):
        """
        Collect reddit submissions for the given configuration
        parameters and write them to the Google Big Query gbq_comments_table.
        Set query to None if no query.
        
        Parameters
        ----------
        query : str or None
            search term for querying submissions. Use None to collect all data from specified subreddits.
        start_date : str
            earliest date to be queried, in "DD/MM/YYYY" format
        end_date : str
            latest date to be queried, in "DD/MM/YYYY" format
        subreddits : list, optional
            subreddits to perform query in
            
        Returns
        -------
        (str, dict)
            A unique identifier that can be used to select the data from the relevant
            BGQ table, counts of each error encountered
        
        """
        unique_id, errors = self._collect("submissions", query, start_date, end_date, subreddits)
        
        return unique_id, errors
        
        
    def collect_comments(self, query, start_date, end_date, subreddits=None):
        """
        Collect reddit comments for the given configuration
        parameters and write them to the Google Big Query gbq_submissions_table.
        Set query to None if no query.
        
        Parameters
        ----------
        query : str or None
            search term for querying comments. Use None to collect all data from specified subreddits.
        start_date : str
            earliest date to be queried, in "DD/MM/YYYY" format
        end_date : str
            latest date to be queried, in "DD/MM/YYYY" format
        subreddits : list, optional
            subreddits to perform query in
            
        Returns
        -------
        (str, dict)
            A unique identifier that can be used to select the data from the relevant
            BGQ table, counts of each error encountered
            
            
        """
        unique_id = self._collect("comments", query, start_date, end_date, subreddits)
        
        return unique_id, errors
    
    
    def _write_to_gbq(self, mode, dataframe):
        """
        Use project details from config to write to Google Big Query.
        """
        pandas_gbq.to_gbq(
            dataframe,
            self.config[f"gbq_{mode}_table"], 
            project_id=self.config["gbq_project"],
            if_exists="append"
        )
        
        
    def _collect(self, mode, query, start_date, end_date, subreddits):
        """
        Collect data from pushshift for specified mode.
        
        Data is written per subreddit per day in the query period.
        """
        if mode not in ["comments", "submissions"]:
            raise ValueError("Mode must be comments or submissions")
        if isinstance(subreddits, str) or subreddits is None:
            subreddits = [subreddits]

        unique_id = uuid.uuid4()
        
        start_date = dt.datetime.strptime(start_date, "%Y/%m/%d")
        end_date = dt.datetime.strptime(end_date, "%Y/%m/%d")
        daterange = pd.date_range(start_date, end_date)
        t_delta = dt.timedelta(days=1)
    
        logging_data = pd.DataFrame({
            "uuid": unique_id,
            "mode": mode,
            "query": query,
            "subreddits": json.dumps(subreddits),
            "query_datetime": dt.datetime.now(),
            "start_date": start_date,
            "end_date": end_date
        }, index=[0])
        self._write_to_gbq("logging", logging_data)
        print("Query uuid logged: " + str(unique_id))
        
        error_count = 0
        errors = {}
        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        for subreddit in subreddits:
            # Loop for each t_delta period between start and end
            for date in daterange:
                try:
                    gen = getattr(self.pushshift, "search_" + mode)(
                        q=query,
                        subreddit=subreddit,
                        after=int(date.timestamp()),
                        before=int((date + t_delta).timestamp())
                        )
                    start_date += t_delta

                    search_data = pd.DataFrame([obj.d_ for obj in gen]).sort_index(axis=1)
                    if not search_data.empty:
                        search_data.insert(0, "uuid", unique_id)
                        self._write_to_gbq(mode, search_data)
                except Exception as e:
                    # Store errors in errors dict, so that collection is not stopped by API errors
                    if e not in errors:
                        errors[e] = 1
                    else:
                        errors[e] += 1
                    error_count +=1
        print("Error count: ", str(error_count))
        print("Query completed successfully, returning uuid and errors")
        return unique_id, errors
        
    def query_gbq(self, sql):
        """
        Utility method to query from the projects database.
        Uses the project details from the Class configuration.
        
        Parameters
        ----------
        
        sql : str
            A valid SQL query for a database table within the gbq_project
        
        
        Returns
        -------
        pandas.DataFrame
            data returned by sql query
        
        """
        return pandas_gbq.read_gbq(sql, project_id=self.config["gbq_project"])
                                           