import pandas as pd
import numpy as np

def generate_test_data():

    mock_data = pd.DataFrame({
    "author": ["popcornboiii", "TweetArchiveBot", "SJWagner", "TradeFlags", "TrueIndologyBot", "therealfatumbot", "DarkCrusader77"],
    "title": ["synchroneous autocompletion for rstats in vim8", 
    "White House moves to halt evictions as fears of coronavirus-fueled housing crisis grow", 
    'Fauci pushes back against minimizing of coronavirus death toll', 
    'The Gateway Pundit: US Markets Set New All-time Highs in the S&amp;P 500 and Nasdaq – Way Above What’s Needed Per One Study for Trump to Win in November',
    'Democrats are losing the fucking plot',
    'Man who lost SEVEN family members to coronavirus becomes first American dosed in Oxford’s trial',
    'Is ‘malignant narcissist’ Trump sick? Experts and former allies say he’s ‘unfit’'],
    "selftext": ['He is awful and will lead the US into a white supremacist dystopia.',
     np.nan, 
     'As the title asks. I am genuinely worried about the future of our Nation. I am not a patriotic person and am against Nationalism. I have been watching a lot of WW2 documentaries lately and the rise of Hitler and his rhetoric has seemed awfully familiar to Trumps. I would love to hear some insight on what your thoughts the future of our country will be. Thank you',
     'Biden will have a massive scandal next month. (Something to go with racism or sex crime allegations)\n\nAttempted Trump assassination before Nov 3\n\nThe house of representatives will choose the next president. They will choose Trump.',
      "Our daycare provider tested positive for Coronavirus. She has stated that she can open after 10 days which is Tuesday September 8. We were told that our kids can't come back for 14 days even if they test negative. How is that possible?\n\nThe states website is worthless for what to do and the phone line runs from 9-4 so if you work during that time you can't ask anyone. Does anyone know the guidelines? \n\nWe already burned through our pto and extra Coronavirus time off for previous exposure and are on thin ice with our jobs already.", 
      "As I\'m sure the truth for many of you is, this August\'s SAT was or would have been extremely important for your college admissions journey. However, due to both Coronavirus and the College Board\'s extreme unpreparedness and disorganization, most kids have not been able to take it since last year. \n\nThink about that. \n\nNow, I get that we have to play our part in slowing down the pandemic, but how fair is it to kids who NEED results for colleges and need to take as many tests as possible to maximize their scores through superscoring? \n\nLet me tell you what happened to me the other day. Knowing that most tests were likely to get canceled, my father and I tried to pick the most desolate test center in a Republican state. We went to Great Falls, Montana. Nearly a 2,000 dollar flight ticket combined. Why? Our test center in Last Vegas (we live in LA) got canceled shortly before the deadline, August 18.",
       "I mean if I dare say as much as, “Trump isn’t the worst president.” I get 30+ downvotes and a few rude messages. But is someone says “Trump Idiot.” I’m willing to bet that they don’t get much is any hate for it even if someone disagrees. If I said something like Trump is the best president ever I would probably be doxxed"]
    })

    return mock_data