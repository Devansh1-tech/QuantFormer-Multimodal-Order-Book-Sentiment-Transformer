latest_news_embedding = None

latest_news = None


def update_news(headline, embedding):

    global latest_news
    global latest_news_embedding

    latest_news = headline

    latest_news_embedding = embedding


def get_latest_embedding():

    return latest_news_embedding


def get_latest_headline():

    return latest_news