import unittest
from unittest.mock import patch, MagicMock
from process_problems import ProblemProcessor, Problem
import os
import yaml
import tempfile

class TestProblemProcessor(unittest.TestCase):

    def setUp(self):
        self.temp_output_dir = tempfile.TemporaryDirectory()
        self.temp_leaderboard_file = tempfile.NamedTemporaryFile(delete=False)
        
        self.args = MagicMock()
        self.args.seed = 42
        self.args.num_rounds = 1
        self.args.num_problems = 2
        self.args.topk_problems = 1
        self.args.mutate_on_start = False
        
        # Override global variables for testing
        global OUTPUT_DIR, LEADERBOARD_FILE
        OUTPUT_DIR = self.temp_output_dir.name
        LEADERBOARD_FILE = self.temp_leaderboard_file.name

    def tearDown(self):
        self.temp_output_dir.cleanup()
        os.unlink(self.temp_leaderboard_file.name)

    @patch("process_problems.requests.post")
    def test_mutate_problem(self, mock_post):
        # Setup mock response for API call
        mock_post.return_value.json.return_value = {
            "choices": [{"message": {"content": "Simplified problem statement"}}]
        }
        
        problem_processor = ProblemProcessor(self.args)
        problem = Problem("Original problem statement")

        mutated_problem = problem_processor.mutate_problem(problem, "Rephrase this problem")
        
        self.assertEqual(mutated_problem.text, "Simplified problem statement")
        mock_post.assert_called_once()

    def test_update_leaderboard(self):
        problem_processor = ProblemProcessor(self.args)
        problem_processor.problems = [Problem("Test problem", score=9.0)]
        
        problem_processor.update_leaderboard()
        
        with open(LEADERBOARD_FILE, 'r') as f:
            leaderboard_data = yaml.safe_load(f)
        
        self.assertEqual(len(leaderboard_data), 1)
        self.assertIn(problem_processor.problems[0].id, leaderboard_data)
        self.assertEqual(leaderboard_data[problem_processor.problems[0].id], 9.0)

    def test_load_problems(self):
        # Create a temporary problems.txt file
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_problems_file:
            temp_problems_file.write("Problem 1\nProblem 2\nProblem 3\n")
            temp_problems_file_path = temp_problems_file.name
        
        # Update the global PROBLEMS_FILE variable temporarily
        global PROBLEMS_FILE
        PROBLEMS_FILE = temp_problems_file_path
        
        problem_processor = ProblemProcessor(self.args)
        problem_processor.load_problems()
        
        self.assertEqual(len(problem_processor.problems), 3)
        
        os.unlink(temp_problems_file_path)  # Clean up

if __name__ == "__main__":
    unittest.main()