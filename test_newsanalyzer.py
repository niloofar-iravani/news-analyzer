import json
from datetime import datetime

import pytest
import news_analyzer


def test_search_articles(monkeypatch):
    # Arrange: prepare fake articles and replace user input/API call
    fake_articles = [
        {"title": "AI in Healthcare"},
        {"title": "New Technology Trends"}
    ]
#we want to rest AI
    monkeypatch.setattr("builtins.input", lambda _: "AI")
    monkeypatch.setattr(
        news_analyzer,
        "fetch_news",
        lambda subject: fake_articles
    )

    # Act: call the function being tested
    result = news_analyzer.search_articles()

    # Assert: check the expected behavior
    assert result == fake_articles


def test_filter_articles(monkeypatch):
    # Arrange: prepare fake news articles
    fake_articles = [
        {
            "title": "AI in Healthcare",
            "source": {"name": "Science Daily"},
            "publishedAt": "2026-10-08T10:30:00Z"
        },
        {
            "title": "Technology in Schools",
            "source": {"name": "Education News"},
            "publishedAt": "2026-10-08T12:00:00Z"
        },
        {
            "title": "AI in Business",
            "source": {"name": "Science Daily"},
            "publishedAt": "2026-10-07T09:00:00Z"
        }
    ]

    # Prevent filter_articles from making a real API request
    monkeypatch.setattr(
        news_analyzer,
        "search_articles",
        lambda: fake_articles
    )

    # Simulate the three answers entered by the user
    answers = iter(["AI", "Science Daily", "2026-10-08"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )

    # Act
    result = news_analyzer.filter_articles()

    # Assert: only the first article should match all three filters
    assert len(result) == 1
    assert result[0]["title"] == "AI in Healthcare"


def test_filter_articles_invalid_date(monkeypatch):
    # Arrange
    fake_articles = [
        {
            "title": "AI in Healthcare",
            "source": {"name": "Science Daily"},
            "publishedAt": "2026-10-08T10:30:00Z"
        }
    ]

    monkeypatch.setattr(
        news_analyzer,
        "search_articles",
        lambda: fake_articles
    )

    answers = iter(["AI", "Science Daily", "08-10-2026"])
    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers)
    )

    # Assert: an invalid date format should raise ValueError
    with pytest.raises(ValueError, match="Invalid date"):
        news_analyzer.filter_articles()


def test_load_saved_articles_found(tmp_path, monkeypatch):
    # Arrange: create a temporary file containing a saved article
    saved_article = {
        "title": "AI in Healthcare",
        "source": {"name": "Science Daily"},
        "description": "An article about AI.",
        "url": "https://example.com/ai"
    }

    file_path = tmp_path / "saved_articles.json"
    file_path.write_text(
        json.dumps([saved_article]),
        encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)

    # Act
    result = news_analyzer.load_saved_articles("AI in Healthcare")

    # Assert
    assert result == saved_article


def test_load_saved_articles_not_found(tmp_path, monkeypatch):
    # Arrange: create a file containing a different article
    saved_articles = [
        {
            "title": "Technology in Schools",
            "source": {"name": "Education News"},
            "description": "Technology in education.",
            "url": "https://example.com/education"
        }
    ]

    file_path = tmp_path / "saved_articles.json"
    file_path.write_text(
        json.dumps(saved_articles),
        encoding="utf-8"
    )

    monkeypatch.chdir(tmp_path)

    # Act
    result = news_analyzer.load_saved_articles("AI in Healthcare")

    # Assert
    assert result is None


def test_load_saved_articles_file_missing(tmp_path, monkeypatch):
    # Arrange: use an empty temporary directory
    monkeypatch.chdir(tmp_path)

    # Act
    result = news_analyzer.load_saved_articles("AI in Healthcare")

    # Assert
    assert result is None


