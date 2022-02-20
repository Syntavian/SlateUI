def exception(_message: str) -> None:
    """Print an error message to the terminal."""
    print(f"Error: {_message}")

def exit_exception(_message: str) -> None:
    """Print an error message to the terminal and exit the application."""
    exception(f"{_message} Exiting.")
    exit()