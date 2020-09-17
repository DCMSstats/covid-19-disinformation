from redditcollector import RedditCollector
import pandas as pd
import pandas_gbq

collector = RedditCollector(r"../redditcollector_disinfo_config.yaml")

top_subreddits = list(set(['Coronavirus', 'insanepeoplefacebook', 'newsbotbot', 'worldnews', 'conspiracywhatever', 'AskReddit', 'conspiracytheories', 'memes', 'news', 'conspiracy_commons', 'AutoNewspaper', 'teenagers', 'ConspiracyHeadlines', 'technology', 'copypasta', 'unitedkingdom', 'tradeflags', 'OutOfTheLoop', 'nottheonion', 'removalbot', 'unpopularopinion', 'China_Flu', 'JAAGNet', 'businesstalkdaily', 'ukpolitics', 'NoStupidQuestions', 'Showerthoughts', 'unremovable', 'dangerous_tech', 'videos', 'wallstreetbets', 'rant', 'TheNewsFeed', 'Wuhan_Flu', 'skeptic', 'discordservers', 'technews', 'dankmemes', 'INDEPENDENTauto', 'CoronavirusUK', 'FreeKarma4U', 'TrueOffMyChest', 'facepalm', 'CoronavirusFOS', 'BannedDotVideo', 'europe', 'explainlikeimfive', 'TooAfraidToAsk', 'FreeKarma4You', 'conspiracy', 'insanepeoplefacebook', 'AskReddit', 'teenagers', 'copypasta', 'conspiracy_commons', 'Coronavirus', 'conspiracytheories', 'memes', 'relationship_advice', 'Showerthoughts', 'JAAGNet', 'tradeflags', 'OutOfTheLoop', 'NoStupidQuestions', 'pennystocks', 'Advice', 'conspiracywhatever', 'removalbot', 'unpopularopinion', 'technology', 'wallstreetbets', 'TrueOffMyChest', 'explainlikeimfive', 'worldnews', 'rant', 'DebateRightists', 'SAtechnews', 'AutoNewspaper', 'investing', 'Romania', 'niuz', 'CoronavirusUK', 'news', 'QAnonCasualties', 'stocks', 'funny', 'skeptic', 'China_Flu', 'newsbotbot', 'facepalm', 'askscience', 'ConspiracyHeadlines', 'u_snehawiseguy', 'TooAfraidToAsk', 'newzealand', 'Wuhan_Flu', 'videos', 'CovIdiots', 'relationships', 'conspiracy', 'unitedkingdom', 'conspiracywhatever', 'AutoNewspaper', 'worldnews', 'news', 'ConspiracyHeadlines', 'uknews', 'whatisthisthing', 'Ilford', 'Coronavirus', 'badunitedkingdom', 'crimenews', 'Jokes', 'CoronavirusUK', 'unremovable', 'CasualUK', 'ukpolitics', 'BBCtech', 'JAAGNet', 'BBCauto', 'FreeKarma4You', 'INDEPENDENTauto', 'bprogramming', 'insanepeoplefacebook', 'UKNewsByABot', 'conspiracy_commons', 'Scotland', 'AskScienceDiscussion', 'britishproblems', 'biology', 'NoFilterNews', 'europe', 'HomeNetworking', 'businesstalkdaily', 'TheNewsFeed', 'GlobalNews', 'TrueOffMyChest', 'technology', 'u_jerryfranksonJF', 'myfriendwantstoknow', 'offbeat', 'Feedimo', 'JustBadNews', 'CellBoosters', 'Economics', 'belgium', 'glasgow', 'GUARDIANauto', 'CovIdiots']))


subs_query_uuid, subs_errors = collector.collect_submissions(
    query=None,
    start_date="2020/01/01",
    end_date="2020/09/15",
    subreddits=top_subreddits
)

coms_query_uuid, coms_errors = collector.collect_comments(
    query=None,
    start_date="2020/01/01",
    end_date="2020/09/15",
    subreddits=top_subreddits
)

print("Submissions errors: ", subs_errors)
print("Comments errors: ", coms_errors)
print("Submission uuid: ", subs_query_uuid)
print("Comments uuid: ", coms_query_uuid)
