#News analyzer
import requests
import json
import sys
from dotenv import load_dotenv
import os
from datetime import datetime
from collections import Counter
import re

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



#finding news that maches with user wants (their keyword)
def search_articles():
    print("AI")
    print("Technology")
    print("Science")
    print("Business")
    topic = input("choose a topic:")
    return fetch_news(topic)



# receiving news via API
def fetch_news(subject):
    url = "https://newsapi.org/v2/everything"

    subject = subject.strip()

    if subject.lower() not in ["ai", "technology", "science", "business"]:
        raise ValueError("Invalid subject!")
    if not NEWS_API_KEY:
        raise ValueError("API key is missing!")

    try:

        response = requests.get(url, params = {"q": subject, "language" : "en",  "apiKey" : NEWS_API_KEY}, timeout = 10)
        data = response.json()

    except requests.exceptions.RequestException as error:
        raise ValueError(f"Could not connect to News API: {error}")

    if data.get("status") == "error":
        raise ValueError(data.get("message", "News API returned an error."))
#it returns a list of articles
    return data["articles"]



#limiting news based on category, resource, date, popularity
def filter_articles():
    articles = search_articles()
    keyword = input("choose your keyword: ")
    my_source = input("choose the resource: ")
    date = input("choose the date (YYYY-MM-DD): ")
    try:
        selected_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date. Please use YYYY-MM-DD")

    filtered_articles = []
    for article in articles:
        article_date = datetime.fromisoformat(article["publishedAt"].replace("Z", "+00:00"))
        if (keyword.lower() in article["title"].lower() and my_source.lower() in article["source"]["name"].lower() and article_date.date() == selected_date):
            filtered_articles.append(article)

    return filtered_articles




#analyzing the text: Finding the number of words, reporting 3 most commen words,
#the number of sentences, the number of characters, and average word length, this function takes article that is a dictionary not the content or string
#article has title, description and content
def analyze_article(article):
    text= ((article["title"] or "")
            + " "
            + (article["description"] or "")
            + " "
            + (article["content"] or ""))
    text = text.lower()
    sentence = re.findall(r"[.!?]", text)
    sentences_count = len(sentence)
    text= re.sub(r"[^\w\s]", "", text)
    words = text.split()
    number_of_words = len(words)
    most_common_words = Counter(words).most_common(3)
    result = {"Number of words": number_of_words,
              "Number of sentences": sentences_count,
               "Most common words": most_common_words}
    return result



#Saving articles that user have chosen and returning a list of them
def save_article(title, articles):
    saved_articles = []
#if there was no saved_articles.json, as it is the first time to run the program, we have FileNotFoundError.
# Otherwise, we add the article to our list, which is saved_articles
    try:
        with open("saved_articles.json", "r", encoding="utf-8") as file:
            saved_articles = json.load(file)
    except FileNotFoundError:
        pass
#checking if the title was found or not, and whether it has been saved before or not
    found = False
    for article in articles:
        if article["title"].lower() == title.lower():
            found = True
            already_saved = False
            for saved_article in saved_articles:
                if saved_article["title"].lower() == title.lower():
                    already_saved = True
                    break
            if not already_saved:
                saved_articles.append(article)
                break
    if not found:
        raise ValueError("Article not found!")

#Until now we have not save anithing in the file, just in the memory of python
#Now save the update list to the JSON file
    with open("saved_articles.json", "w", encoding="utf-8") as file:
        json.dump(saved_articles, file, indent=4)
    if already_saved:
        print("This article is already saved.")
    else:
        print("Article saved successfully.")

    return saved_articles



# Reading news that have been chosen
def load_saved_articles(title):
    try:
        with open("saved_articles.json", "r", encoding="utf-8") as file:
            saved_articles = json.load(file)
    except FileNotFoundError:
        return None

    for article in saved_articles:
        if article["title"].lower() == title.lower():
            return article

    return None



def main():

    while True:

        print("\nNews Analyzer")
        print("1. Search news")
        print("2. Analyze article")
        print("3. Save article")
        print("4. View saved articles")
        print("5. Exit")

        action = input("Choose an option: ").strip().lower()

        if action not in [
            "1",
            "2",
            "3",
            "4",
            "5",
            "search",
            "analyze",
            "save",
            "view saved articles",
            "exit"
        ]:
            print("Not valid!")
            continue

        # Search
        elif action == "1" or action == "search":
            searched_articles = search_articles()

            if not searched_articles:
                print("No articles found.")
            else:
                print("\nArticles:")
                for number, article in enumerate(searched_articles, start=1):
                    print(f"{number}. {article['title']}")

        # Analyze
        elif action == "2" or action == "analyze":
            subject = input("What is your subject? ")

            data = fetch_news(subject)

            title = input("Enter the title of the article: ")

            result = None

            for article in data:
                if article["title"].lower() == title.lower():
                    result = analyze_article(article)
                    break

            if result is None:
                print("Article not found!")
            else:
                print("\nAnalysis:")
                print(result)

        # Save
        elif action == "3" or action == "save":
            searched_articles = search_articles()

            saved_article_title = input(
                "Which article do you want to save? "
                "Enter 'none' to cancel: "
            )

            if saved_article_title.lower() == "none":
                print("Saving cancelled.")
                continue

            save_article(saved_article_title, searched_articles)

        # View saved articles
        elif action == "4" or action == "view saved articles":
            view_title = input(
                "Enter the title of the article you want to read: "
            )

            article = load_saved_articles(view_title)

            if article is None:
                print("This article has not been saved.")
            else:
                print("\nTitle:", article["title"])
                print("Source:", article["source"]["name"])
                print("Description:", article["description"])
                print("URL:", article["url"])

        # Exit
        elif action == "5" or action == "exit":
            print("Goodbye!")
            sys.exit()


if __name__ == "__main__":
    main()


"""
def main():
    print("News analyzer", end = "\n")
    print("1. Search news", end = "\n")
    print("2. Analyze article", end = "\n")
    print("3. Save article", end = "\n")
    print("4. Vew saved articles", end = "\n")
    print("5. Exit", end = "\n")
    action = input("Choose an option: ")
    result = None

    if action.lower() not in ["1", "2", "3", "4", "5", "search", "analyze", "save", "vew saved articles", "exit"]:
        raise ValueError("Not valid!")

    elif action == "1" or action.lower() == "search" or action.lower() == "save":
#searched_articles is a list of article dictionaries
        searched_articles = search_articles()
        saved_article_title = input("which article do you want to save any? Enter none or a title: ")
        if saved_article_title.lower() == "none":
            sys.exit()
        else:
            for article in searched_articles:
                if article["title"].lower() == saved_article_title.lower():
                    result = save_article(saved_article_title, searched_articles)
                    break
            if result is None:
                    raise ValueError("Article not found!")

            print(result)


    elif action == "2" or action.lower() == "analyze":
        subject = input("What is your subject?")
#data is a list of article dictionaries
        data = fetch_news(subject)
        title = input("Enter the title of article: ")
        for article in data:
            if article["title"].lower() == title.lower():
                result = analyze_article(article)
                break
        if result == None:
            raise ValueError("Article not found!")

        print(result)

    elif action == "4" or action.lower() == "view saved articles":
        view_title = input("Enter the title of article you want to read: ")
        print(load_saved_articles(view_title))

    elif action == "5" or action.lower() == "exit":
        sys.exit("We are done!")
        before upgrade
        """













