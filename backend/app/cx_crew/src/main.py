from crew import CustomerSupportCrew
import sys


def run(initial_query: str = ""):
    print("Starting Customer Support Crew...")
    support_crew = CustomerSupportCrew()
    query = initial_query

    while True:
        if not query:
            query = input("Enter a message: ")

        if query.lower() == "exit":
            break

        crew = support_crew.crew()

        result = crew.kickoff(inputs={"query": query})
        print(result)
        query = ""


if __name__ == "__main__":
    initial_query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    run(initial_query)
