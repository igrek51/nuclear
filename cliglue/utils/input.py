def input_required(prompt: str) -> str:
    while True:
        inputted = input(prompt)
        if inputted:
            return inputted
