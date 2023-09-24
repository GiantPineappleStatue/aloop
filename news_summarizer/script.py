import json
import requests
from newspaper import Article
from langchain.schema import HumanMessage
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
}

def fetch_article_content(url: str) -> str:
    session = requests.Session()
    response = session.get(url, headers=HEADERS, timeout=10)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch article at {url}")

    article = Article(url)
    article.download()
    article.parse()

    return article.title, article.text

def generate_prompt(title: str, text: str) -> str:
    template = """
    You are a very good assistant that summarizes online articles.
    Here's the article you want to summarize.
    ==================
    Title: {article_title}
    {article_text}
    ==================
    Write a summary of the previous article.
    """
    return template.format(article_title=title, article_text=text)

def get_summary(prompt: str) -> str:
    messages = [HumanMessage(content=prompt)]
    chat = ChatOpenAI(model_name="gpt-4", temperature=0)
    return chat(messages).content

def main():
    article_url = "https://www.artificialintelligence-news.com/2022/01/25/meta-claims-new-ai-supercomputer-will-set-records/"
    try:
        article_title, article_text = fetch_article_content(article_url)
        prompt = generate_prompt(article_title, article_text)
        summary = get_summary(prompt)
        print(summary)
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
