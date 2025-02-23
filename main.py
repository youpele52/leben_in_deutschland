from bs4 import BeautifulSoup
import requests
import pandas as pd


class LebenInDeutschland:
    def __init__(self, output_excel: bool = False, path: str | None = None) -> None:
        self.base_url = "https://www.einbuergerungstest-online.eu"
        self.url = "https://www.einbuergerungstest-online.eu/fragen/"
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.content, "html.parser")
        self.output_excel = output_excel
        self.path = path

    def extract_data(self) -> None:
        page = requests.get(self.url)
        page_soup = BeautifulSoup(page.content, "html.parser")
        rows = page_soup.find_all(class_="row")
        questions = []
        answers = []
        indices = []

        if rows:
            for i, row in enumerate(rows):
                question_row = page_soup.find(class_="row", id=f"frage-{i+1}")
                if question_row:
                    question = (
                        question_row.find(class_="questions-question-text")
                        .find("p")
                        .text
                    )
                    questions.append(question)

                    answer = question_row.find(class_="question-answer-right").text
                    answers.append(answer)
                    indices.append(i + 1)

        return pd.DataFrame(
            {
                "Index": indices,
                "Frage": questions,
                "Antwort": answers,
            }
        )

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
        pp = self.extract_data()
        print(pp)
        if self.output_excel:
            self.save_data()


if __name__ == "__main__":
    leben_in_deutschland = LebenInDeutschland(
        output_excel=True,
    )
    leben_in_deutschland.run()
