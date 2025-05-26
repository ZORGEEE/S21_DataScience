num_of_steps = 3

report_template = """
Report

We have made {observations} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. The probabilities are {tail_percent:.2f}% and {head_percent:.2f}%, respectively. Our forecast is that in the next {num_predictions} observations we will have: {predicted_tails} tail and {predicted_heads} heads.
"""

telegram_bot_token = ""
telegram_chat_id = ""