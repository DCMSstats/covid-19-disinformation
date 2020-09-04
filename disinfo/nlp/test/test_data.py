import pandas as pd
import numpy as np

def generate_test_data():

    mock_data = pd.DataFrame({
    "author": ["popcornboiii", "TweetArchiveBot", "SJWagner"],
    "title": ["synchroneous autocompletion for rstats in vim8", "White House moves to halt evictions as fears of coronavirus-fueled housing crisis grow", 'Fauci pushes back against minimizing of coronavirus death toll'],
    "selftext": ['He is awful and will lead the US into a white supremacist dystopia.', np.nan, 'As the title asks. I am genuinely worried about the future of our Nation. I am not a patriotic person and am against Nationalism. I have been watching a lot of WW2 documentaries lately and the rise of Hitler and his rhetoric has seemed awfully familiar to Trumps. I would love to hear some insight on what your thoughts the future of our country will be. Thank you' ]
    })

    return mock_data

