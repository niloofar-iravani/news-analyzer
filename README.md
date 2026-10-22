## News Analyzer
News Analyzer is a Python command-line application that retrieves news articles using the News API and provides basic text analysis.

# Features
- Fetch news articles by topic
- Filter articles by keyword, source, and publication date
- Analyze article text by counting words and sentences
- Identify the three most frequent words
- Save articles to a JSON file for later reading
- Handle API errors, connection issues, and invalid input

# Technologies
- Python
- News API
- Requests
- python-dotenv
- JSON
- pytest

# Setup
1. Install the required dependencies:

pip install -r requirements.txt

2. Create a .env file in the project directory and add your News API key:

NEWS_API_KEY=your_api_key_here

3. Run the application:

python news_analyzer.py

# Running Tests
Run the test suite with:

python -m pytest -v

# Security
Keep your .env file private. Never publish your API key in the repository.

## project structure and functions

### 'search_articles()'
**purpose:** It shows some topicts, which are AI, Science, Technology, and business, to the user and asks to choose one to search. It also finds the article through API.
**Output:** A list of news articles
**Error handling:** It handles API errors and connection problems.


### 'fetch_news(subject)'
**purpose:** It fetches news articles that have the given subject from the API.
**Output:** It returns a list of articles that have the given subject.
**Error handling:** It handles API errors and connection problems by raising ValueError.

### 'filter_articles()'
**purpose:** First of all, it search articles, then ask the user to choose a desired keyword, source, and date.
In try-Except, it turns the string that user has entered as a date to a year-month-day format, using datetime library.
And if the user enters a wrong string format, it raises ValueError.
Then, it builts an empty list(filtered_articles) to add filtered articles.
In for loop it checks the date, keyword, and source of articles and if they were what user wants, append them to filtered_articles.

**Output:** It returns a list of filtered articles.


### 'analyze_article(article)'
**purpose:** It turns the title, description, and content of the article to a unique string (text). If one of them was empty we use "" to prevent potential errors. It uses re library to find (.!?) and count sentences based on them.
It uses text.split() to find words and their numbers. The method of Counter from collections library finds the repeatition of each word and returns the 3 most common words.
**Output:** This function returns a dictionary (result) of the number of words, sentences, and 3 most common words.

### 'save_article(title, articles)'
**purpose:** This functionsaves a selected news article based on its title, allowing the user to read it later.
It checks the existing saved articles in a json file and saves the selected article. This allows the user to keep articles even after closing the program.
**Output:** Saves the selected article to 'saved_articles.json' and returns a list of saved articles.

### 'load_saved_articles(title)'
**purpose:** Allows the user to access previously saved news artiles. The function reads the saved articles from 'saved_articles.json' and retrieves the article that matches the given title.
**Output:** returns the saved article if it is found in the json file and if there was not such a saved article it will return None.

### "main()"
**purpose:** Runs the main program and allows the user to acces the different featurs, by showing a menu of options. Next, based on user's choice, it calls the related function or exit the program through sys.exit()
**Output:** Executes the selected action and manages the main flow of the program.


## Running Tests

**To run the tests, execute:** pytest test_project.py

## Files

- 'project.py': Contains the main program and its functions.

- 'test_project.py': Contains tests for selected functions.

- 'saved_articles.json': Stores saved articles and is created when articles are saved.

- '.env': Stores the News API key and should not be shared publicly.


