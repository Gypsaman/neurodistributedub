import json
from collections import Counter
import numpy as np

questions = json.load(open('./data/quizzes.json','r'))
Topics = Counter([q['Topic'] for id,q in questions.items()])


def create_quiz(topics_selected):
    quiz_questions = []
    for topic,qty in topics_selected.items():
        selection = np.random.choice(range(Topics[topic]),qty ,replace=False)
        topic_questions = np.array([id for id,q in questions.items() if q['Topic'] == topic])
        for q in topic_questions[selection]:
            answers = np.array(questions[q]['Answers'])
            selection = np.random.choice(range(len(answers)),len(answers),replace=False)
            quiz_questions.append((q,questions[q]['Question'],[a for a in answers[selection]]))
    return quiz_questions
        

    
if __name__ == '__main__':
    Topics_selected = {'Encryption': 5, 'Blockchain': 3,"Solidity": 2}
    quiz_questions = create_quiz(Topics_selected)

    print(quiz_questions)
