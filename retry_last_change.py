from perform_code_change import perform_code_change
from state import change_requests


def retry_last_change():
    last_change = change_requests.get().strip().split("\n")[-1]
    if last_change:
        print(f"Retrying last change: {last_change}")
        perform_code_change(last_change)
    else:
        print("No previous changes to retry.")
