from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import random
from fake_useragent import UserAgent


class LebenInDeutschland:
    def __init__(self, output_excel: bool = False, path: str | None = None) -> None:
        self.base_url = "https://www.einbuergerungstest-online.eu/fragen/"
        self.output_excel = output_excel
        self.path = path
        self.ua = UserAgent()

    def extract_data(self):
        questions = []
        answers = []

        for i in range(0, 10):
            url = self.base_url if i == 0 else f"{self.base_url}{i+1}/"
            print("Extracting data from", url)

            # Add a random delay between requests
            delay = random.randint(5, 15)
            print(f"Waiting for {delay} seconds before the next request...")
            time.sleep(delay)

            result = self.questions_and_answers(url)
            questions.extend(result["questions"])
            answers.extend(result["answers"])

            print(f"Successfull extracted data from {url}\n\n")

        return pd.DataFrame({"Frage": questions, "Antwort": answers})

    def questions_and_answers(
        self, url: str | None = None, questions: list = [], answers: list = []
    ) -> dict:
        headers = {"User-Agent": self.ua.random}  # Randomize user-agent
        page = requests.get(self.base_url if url is None else url, headers=headers)
        page_soup = BeautifulSoup(page.content, "html.parser")
        questions = []
        answers = []

        # Find all divs with an id that contains "frage"
        question_rows = page_soup.select("div[id*=frage]")
        
        if not question_rows:
            wait_time = random.randint(0, 10)
            print(f"No question rows found, reloading page in {wait_time} seconds")
            time.sleep(wait_time)
            page = requests.get(self.base_url if url is None else url, headers=headers)
            page_soup = BeautifulSoup(page.content, "html.parser")
            question_rows = page_soup.select("div[id*=frage]")

        if question_rows:
            for question_row in question_rows:
                question = (
                    question_row.find(class_="questions-question-text").find("p").text
                )
                questions.append(question)
                answer = question_row.find(class_="question-answer-right").text
                answers.append(answer)

        return {"questions": questions, "answers": answers}

    def save_data(self) -> None:
        df = self.extract_data()
        if self.path:
            print("Saving data... to ", self.path)
            df.to_excel(
                f"{self.path}/leben_in_deutschland.xlsx",
            )
            print("Saved to ", self.path)
        if not self.path:
            print("Saving data... to default path")
            df.to_excel(
                "leben_in_deutschland.xlsx",
            )
            print("Saved to default path")
        else:
            pass

    def run(self) -> None:
        if self.output_excel:
            self.save_data()
        else:
            print(self.extract_data())


if __name__ == "__main__":
    leben_in_deutschland = LebenInDeutschland(
        output_excel=True,
    )
    leben_in_deutschland.run()
