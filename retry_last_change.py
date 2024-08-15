from perform_code_change import perform_code_change
from state import code_change


def retry_last_change():
    last_change = code_change.get()
    if last_change:
        print(f"Retrying last change: {last_change}")
        perform_code_change(last_change)
    else:
        print("No previous changes to retry.")
