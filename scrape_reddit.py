#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 19 17:03:23 2020

@author: josh

This pipeline takes an a topic or topics (any number equal or greater than 1) and returns the new comments for each subbredit where the topic was found

"""

import disinfo as di
import praw
import pandas as pd
import pandas_gbq

#Takes command line arguments
options= di.get_arguments()

#Assigns options to variables
topics_list = options.topics
number_comments = int(options.comments)

# Warning messages if no file name or no file directory given.
#For dev purposes and checking script works, command line can be run without having to save results.
if options.name and not options.csv:
    print("WARNING: File name was given but directory was not given. Use -csv or -gbq to save results. Results will not saved.",'\n',"Use -h or --help for support.")
elif options.csv and not options.name:
    print("No name given to .csv file. File will be called reddit_database.csv.","\n","WARNING: This will overwrite any other file named reddit_database.csv")
elif not options.csv and not options.name and not options.gbq:
    print("WARNING: No flag to save results to a file format was given. Results will not be saved" '\n',"Use -h or --help for support or go to https://github.com/WMDA/social-media-analysis")

# Prints ouput of what topics are being searched for, number of comments limited to and how comments are sorted, default is new.
if options.sort:
    di.print_output(topics_list,number_comments,options.sort)
else:
    di.print_output(topics_list,number_comments)

#Calls reddit functions from reddit.py
#Sorts comments out either by -s input or default is new.
reddit = praw.Reddit("reddit")
subs_array = di.get_subreddit_names(reddit, topics_list)
if options.sort:
    database = di.get_subreddit_data(reddit, subs_array, number_comments,options.sort)
else:
    database = di.get_subreddit_data(reddit, subs_array, number_comments)

# Assigns results to csv (-csv) or gbq (-gbq & -n) if those options are selected.
if options.csv and not options.name:
    database.to_csv("%s/reddit_database.csv" % options.csv, encoding='utf-8', index=False)
elif options.csv and options.name:
    database.to_csv("%s/%s.csv" % (options.csv,options.name), encoding='utf-8', index=False)
elif options.gbq:
    database.to_gbq('%s.reddit_table' %options.name,'%s' %options.gbq, chunksize=None, if_exists='append')
