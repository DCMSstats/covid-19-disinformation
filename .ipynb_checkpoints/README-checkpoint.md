# covid-19-disinformation
Analysing spread of covid-19 disinformation

## Getting Started 

Clone the repository
```command
git clone ssh://niall.goulding1@dcms.gov.uk@source.developers.google.com:2022/p/dcms-statistics/r/reddit-disinformation
```
You will need to install the python package in the repository. On a windows machine, open the Anaconda Prompt. On a OSX or Linux machine open the Terminal. Run:

```command
pip install -e local_path/disinfo
```

Replace `local_path` with the path to your package.

## PRAW Authentication

To access reddit you will need,

1. Client ID & Client Secret:These two values are needed to access Reddit’s API as a script application ).

2. User Agent:	A user agent is a unique identifier that helps Reddit determine the source of network requests

You may choose to provide these by passing in three keyword arguments when calling the initializer of the Reddit class: client_id, client_secret, user_agent.

```python
import praw

reddit = praw.Reddit(client_id="my client id",
                     client_secret="my client secret",
                     user_agent="my user agent")
```

This method exposes the Authentication keys publicly as they are included in the GitHub code. 

Authentication can also be provided in an `praw.ini` configuration file. To run the code in this project you will need to provide this. 
> It is recommended to use a `praw.ini` file in order to keep your authentication information separate from your code.

You can obtain this by talking to a member of the team involved in this project.
Alternatively you can provide your own authentication. To provide your own then look at the [reddit documentation](https://github.com/reddit-archive/reddit/wiki/API).

Once you have the `praw.ini` file then you need to place this file either:
* In the current working directory
* In the launching user’s config directory

The second option is the preferred method but either will work. This will vary depending on what system you run, Windows, OSC or Linux. See [PRAW Documentation](https://praw.readthedocs.io/en/latest/getting_started/configuration/prawini.html) for guidance for your system.
