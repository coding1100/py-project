import argparse
import os
import random
import yaml
import uuid
import requests
from dataclasses import dataclass, field
from typing import List

# Global configuration
OUTPUT_DIR = 'output'
PROBLEMS_FILE = 'problems/problems.txt'
LEADERBOARD_FILE = 'leaderboard.yaml'
PROMPT_DIR = 'prompts/mutations/'

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

@dataclass
class Problem:
    text: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    score: float = 0.0

class ProblemProcessor:
    def __init__(self, args):
        self.args = args
        self.problems: List[Problem] = []
        self.load_problems()
        self.leaderboard = {}

    def load_problems(self):
        if not os.path.exists(PROBLEMS_FILE):
            raise FileNotFoundError(f"Problem file '{PROBLEMS_FILE}' is missing.")
        
        with open(PROBLEMS_FILE, 'r') as f:
            self.problems = [Problem(line.strip()) for line in f if line.strip()]
        
        if not self.problems:
            raise ValueError("No problems loaded from file.")

    def save_processed_problem(self, problem: Problem):
        filename = os.path.join(OUTPUT_DIR, f"{problem.id}.txt")
        with open(filename, 'w') as f:
            f.write(problem.text)
        print(f"Saved processed problem: {filename}")

    def update_leaderboard(self):
        top_problems = sorted(self.problems, key=lambda x: x.score, reverse=True)[:self.args.topk_problems]
        self.leaderboard = {p.id: p.score for p in top_problems}
        
        with open(LEADERBOARD_FILE, 'w') as f:
            yaml.dump(self.leaderboard, f)
        print(f"Updated leaderboard: {self.leaderboard}")

    def mutate_problem(self, problem: Problem, prompt_template: str) -> Problem:
    # Call OpenAI API to mutate the problem
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": [{"type": "text", "text": "You are an algorithmic expert and the best coder in the world"}]
                },
                {
                    "role": "user",
                    "content": problem.text
                }
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 800
        }
        
        headers = {
            "Content-Type": "application/json",
            "api-key": os.getenv("API_KEY")
        }
        
        try:
            response = requests.post(os.getenv("OPENAI_ENDPOINT"), headers=headers, json=payload)
            response.raise_for_status()
            new_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", problem.text)
            problem.text = new_text.strip()
            print(f"Mutated problem ID {problem.id}: {problem.text}")  # Debug statement
        except requests.RequestException as e:
            print(f"Error calling OpenAI API: {e}")
        
        return problem

    def run(self):
        random.seed(self.args.seed)
        
        for round_num in range(self.args.num_rounds):
            print(f"\nProcessing round {round_num + 1}...")
            problems_to_process = random.sample(self.problems, min(self.args.num_problems, len(self.problems)))
            
            # Mutate problems
            for problem in problems_to_process:
                prompt_template = self.get_random_prompt()
                mutated_problem = self.mutate_problem(problem, prompt_template)
                mutated_problem.score = random.uniform(0, 10)  # Placeholder for a scoring mechanism
                self.save_processed_problem(mutated_problem)
            
            self.update_leaderboard()
            print(f"Round {round_num + 1} completed and leaderboard updated.")

    def get_random_prompt(self):
        prompt_files = [f for f in os.listdir(PROMPT_DIR) if f.endswith('.txt')]
        if not prompt_files:
            raise FileNotFoundError("No prompt templates found in prompts/mutations/")
        
        selected_file = random.choice(prompt_files)
        with open(os.path.join(PROMPT_DIR, selected_file), 'r') as f:
            return f.read()

def main():
    parser = argparse.ArgumentParser(description="Process problem statements.")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random operations")
    parser.add_argument("--num_rounds", type=int, required=True, help="Number of processing rounds")
    parser.add_argument("--num_problems", type=int, required=True, help="Number of problems to process per round")
    parser.add_argument("--topk_problems", type=int, required=True, help="Number of top problems to retain each round")
    parser.add_argument("--mutate_on_start", action="store_true", help="Flag to mutate on start")
    
    args = parser.parse_args()

    processor = ProblemProcessor(args)
    processor.run()

if __name__ == "__main__":
    main()