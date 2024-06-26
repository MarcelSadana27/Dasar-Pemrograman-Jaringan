import json
from difflib import get_close_matches

def load_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
        
def chat():
    knowledge_base: dict = load_base('knowledge_base.json')

    while True:
        userinput: str = input('You: ')

        if userinput.lower() == 'quit':
            break

        best_match: str | None = find_best_match(userinput, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. What do you want to me to answer??')
            new_answer: str = input('Your Answer ("skip" to cancel): ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": userinput, "answer": new_answer})
                save_base('knowledge_base.json', knowledge_base)
                print('Bot: Thank you for your input.')


if __name__ == '__main__':
    chat()          