import os
import json
import random
from typing import Dict, Any, List, Tuple
from dotenv import load_dotenv
from groq import Groq

def generate_challenge_with_ai(difficulty: str) -> Dict[str, Any]:
    # Load environment variables
    load_dotenv()
    
    # Initialize Groq client
    client = Groq(api_key=os.environ.get("GROQ_KEY"))
    if not os.environ.get("GROQ_KEY"):
        raise ValueError("GROQ_KEY environment variable is not set. Please check your .env file.")

    # List of programming topics to ensure variety
    topics = [
        "Data Structures", "Algorithms", "Object-Oriented Programming",
        "Functional Programming", "Web Development", "Database",
        "System Design", "Testing", "Security", "Performance",
        "Concurrency", "Memory Management", "Error Handling",
        "API Design", "Design Patterns", "Code Organization",
        "Debugging", "Version Control", "Documentation", "Best Practices"
    ]

    # Select a random topic
    selected_topic = random.choice(topics)

    system_prompt = f"""You are an expert coding challenge creator. 
    Your task is to generate a unique and engaging coding question with multiple choice answers.
    The question should be appropriate for the specified difficulty level and focus on {selected_topic}.

    For easy questions: Focus on basic syntax, simple operations, or common programming concepts.
    For medium questions: Cover intermediate concepts like data structures, algorithms, or language features.
    For hard questions: Include advanced topics, design patterns, optimization techniques, or complex algorithms.

    Important guidelines:
    1. Each question must be unique and different from previous questions
    2. Give clear and concise question and options
    3. Give a detailed explanation of why the correct answer is right
    4. Give a detailed explanation of why the incorrect answers are wrong
    5. Vary the topics and concepts covered in each question
    6. Use different programming languages and frameworks in your questions
    7. Include a mix of theoretical and practical questions
    8. Make the question clear and the code snippet to be visible if the question has any
    9. Get detailed question so that the user can understand the question and the options
    10. Ensure the question is specific to {selected_topic} and not generic
    11. Make sure the incorrect answers are plausible but clearly wrong
    12. Avoid common or overused examples

    Return the challenge in the following JSON structure:
    {{
        "title": "The entire question clear and concise way",
        "correct_answer": "The correct answer text",
        "incorrect_answers": ["Wrong answer 1", "Wrong answer 2", "Wrong answer 3"],
        "explanation": "Detailed explanation of why the correct answer is right"
    }}
    """
    try:
        completion = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a unique {difficulty} difficulty coding challenge about {selected_topic}. Make sure it's different from any previous questions."}
                ],
            response_format={"type": "json_object"},
            temperature=0.9  # Higher temperature for more variety
        )

        content = completion.choices[0].message.content
        challenge_data = json.loads(content)

        required_fields = ["title", "correct_answer", "incorrect_answers", "explanation"]
        for field in required_fields:
            if field not in challenge_data:
                raise ValueError(f"Missing required field: {field}")

        # Combine and shuffle all answers
        all_answers = [challenge_data["correct_answer"]] + challenge_data["incorrect_answers"]
        random.shuffle(all_answers)
        
        # Find the index of the correct answer after shuffling
        correct_index = all_answers.index(challenge_data["correct_answer"])

        # Create the final response with shuffled options
        return {
            "title": challenge_data["title"],
            "options": all_answers,
            "correct_answer_id": correct_index,
            "explanation": challenge_data["explanation"]
        }

    except Exception as e:
        print(e)
        # Fallback question with randomized answers
        correct_answer = "my_list.append(5)"
        incorrect_answers = [
            "my_list.add(5)",
            "my_list.push(5)",
            "my_list.insert(5)"
        ]
        all_answers = [correct_answer] + incorrect_answers
        random.shuffle(all_answers)
        correct_index = all_answers.index(correct_answer)
        
        return {
            "title": "Basic Python List Operation",
            "options": all_answers,
            "correct_answer_id": correct_index,
            "explanation": "In Python, append() is the correct method to add an element to the end of a list."
        }