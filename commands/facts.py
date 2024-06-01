import requests

class FactFetcher:
    def get_random_fact(self):
        try:
            response = requests.get("https://api.popcat.xyz/fact")
            if response.status_code == 200:
                fact = response.json().get("fact")
                if fact:
                    return fact
                else:
                    return "Failed to fetch a fact."
            else:
                return "Failed to fetch a fact."
        except Exception as e:
            return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    fact_fetcher = FactFetcher()
    random_fact = fact_fetcher.get_random_fact()
    print(random_fact)
