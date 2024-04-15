import random 
import time    
import threading 

def print_header(title):   # Function to print the header
    print("\n" + "-"* len(title))
    print(title)
    print("-" * len(title) + "\n")

def select_difficulty():    # Function to select the difficulty level
    print("Select a difficulty level:")
    print("1. Easy (1-50)")
    print("2. Medium (1-100)")
    print("3. Hard (1-200)")
    difficulty = int(input("Enter the difficulty level (1/2/3): "))
    if difficulty == 1:
        return 50
    elif difficulty == 2:
        return 100
    elif difficulty == 3:  
        return 200
    else:
        print("Invalid difficulty level! Please try again.")
        return select_difficulty()

def get_input(prompt, timeout):  # Function to get input with a timeout
    input_queue = []
    def take_input():
        input_queue.append(input(prompt))
    thread = threading.Thread(target=take_input)
    thread.start()
    thread.join(timeout)
    if thread.is_alive():
        print("\nTime's up!")
        thread.join()  # Ensure thread finishes execution
        return None
    return input_queue[0] if input_queue else None

def guessing_game():  # Function to play the guessing game
    print_header("Guessing Game")  
    max_number = select_difficulty()  
    number = random.randint(1, max_number)  # Generate a random number between 1 and 100
    guess = None  
    attempts = 0  
    max_attempt = 10  

    # Timed mode setup
    timed_mode = input("Do you want to play in timed mode? (yes/no): ").lower() == "yes"
    if timed_mode:
        time_limit = 30
        start_time = time.time()
        end_time = start_time + time_limit
    else:
        time_limit = None
        start_time = None
        end_time = None    

    # Game loop 
    while guess != number and attempts < max_attempt: 
        if timed_mode and time.time() > end_time:
            print(f"\n✗ Sorry! Time's up! The number was {number}.")
            return
        
        remaining_time = int(end_time - time.time()) if timed_mode else None
        if remaining_time is not None and remaining_time <= 0:
            print(f"\n✗ Sorry! Time's up! The number was {number}.")
            break

        guess = get_input(f"Guess a number between 1 and {max_number}: ", 
                          remaining_time) if timed_mode else int(input(f"Guess a number between 1 and {max_number}: "))
        if guess is None:
            break  # Exit if time is up and no input was received

        guess = int(guess)
        attempts += 1    

        if guess < number:  
            print("-> Too low!\n")
        elif guess > number: 
            print("-> Too high!\n")

        print(f"You have {max_attempt - attempts} attempts left!")

        if timed_mode: # Display the remaining time
            remaining_time = max(0, int(end_time - time.time()))
            if remaining_time == 0:
                print(f"\n✗ Time's up! The number was {number}.")
                return  # End the function if the time is up
            print(f"Time remaining: {remaining_time} seconds")

    if guess == number: 
        print(f"\n✓ Congratulations! You guessed the number in {attempts} attempts!")

    if guess != number:  
        print(f"\n✗ Sorry! You have reached the maximum number of attempts. The number was {number}.")

guessing_game()  # Call the guessing_game function to play the game
