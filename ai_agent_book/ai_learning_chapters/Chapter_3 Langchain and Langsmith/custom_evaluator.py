import sys
import os
from dotenv import load_dotenv

# Step 1: Add parent folder (project root) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Step 2: Now import works fine
from utils.config_loader import load_config

# Load .env variables and config
load_dotenv()
config = load_config()
openai_key = config.openai_key

from langsmith.evaluation import EvaluationResult, run_evaluator


@run_evaluator
def check_category_match(run, example):
    """
      A simple custom evaluator that checks if the predicted category 
        contains the expected category as a substring, case-insensitively.  
    """

    predicted = run.outputs.get("category","").lower()
    expected = example.outputs.get("expected_category","").lower()

    score = 1 if expected in predicted else 0
    return EvaluationResult(
        key = "category_check",
        score = score
    )