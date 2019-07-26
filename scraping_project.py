import requests
import random
from bs4 import BeautifulSoup
from csv import reader, writer


def scrape_quotes():
    with open("quotes.csv", "w", encoding='utf-8', newline='') as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerow(["quote", "name", "href"])
        response = requests.get("http://quotes.toscrape.com/")
        response.encoding = 'utf-8'

        while response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            articles = soup.find_all(class_="quote")
            for article in articles:
                quote = article.select(".text")[0].get_text()
                name = article.select(".author")[0].get_text()
                href = article.find("a")["href"]
                csv_writer.writerow([quote, name, href])

            try:
                next = soup.nav.find(class_="next").find("a")["href"]
                print(next)
            except AttributeError:
                print("end of pages")
                break
            response = requests.get(f"http://quotes.toscrape.com{next}")
            response.encoding = 'utf-8'


def the_game():
    print("The quote guessing game!")
    print("**Rules of the game**\n You will have 4 tries \n After an incorrect guess you will receive a hint about the author")
    print("**************************\n")

    with open("quotes.csv", encoding='utf-8') as file:
        read = reader(file)
        qoutes_list = []
        for row in read:
            qoutes_list.append(row)

        count = 4
        qoute_number = random.randint(1, len(qoutes_list))
        print(f"Who authored this quote: {qoutes_list[qoute_number][0]}")
        response = requests.get(
            f"http://quotes.toscrape.com{qoutes_list[qoute_number][2]}")
        soup_about = BeautifulSoup(response.text, "html.parser")
        guess = input("Your answer: ")
        if guess == qoutes_list[qoute_number][1]:
            print("Correct! You win!")
            question = input("Play again? y/n: ")
            the_game() if question == 'y' else quit()

        else:
            count -= 1
            born_date = soup_about.find(class_="author-born-date").get_text()
            print(f"Incorrect! You have {count} tries left.")
            print(f"Here's a hint: The author was born in {born_date}")
            guess = input("Your answer: ")
            if guess == qoutes_list[qoute_number][1]:
                print("Correct! You win!")
                question = input("Play again? y/n: ")
                the_game() if question == 'y' else quit()
            else:
                count -= 1
                born_location = soup_about.find(
                    class_="author-born-location").get_text()
                print(f"Incorrect! You have {count} tries left.")
                print(f"Here's a hint: The author was born in {born_location}")
                guess = input("Your answer: ")
                if guess == qoutes_list[qoute_number][1]:
                    print("Correct! You win!")
                    question = input("Play again? y/n: ")
                    the_game() if question == 'y' else quit()
                else:
                    count -= 1
                    author_desc = soup_about.find(
                        class_="author-description").get_text()
                    description = (
                        author_desc[0:500] + '...').replace(qoutes_list[qoute_number][1], "<The Author>")
                    print(f"Incorrect! You have {count} tries left.")
                    print(f"Here's a final hint: {description}")
                    guess = input("Your answer: ")
                    if guess == qoutes_list[qoute_number][1]:
                        print("Correct! You win!")
                        question = input("Play again? y/n: ")
                        the_game() if question == 'y' else quit()
                    else:

                        print(
                            f"You are out of tries. It was {qoutes_list[qoute_number][1]}. Better luck next time!")
                        question = input("Play again? y/n: ")
                        the_game() if question == 'y' else quit()


the_game()
