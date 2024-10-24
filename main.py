from w2c_fetch_repos import fetch_repositories

def main():
    while True: 
        print("\n--- VUDENC - Version 1.0 ---")
        print("1. Exit")
        print("2. Create corpus with Python code")

        choice = input("Enter your choice: ")

        if choice == "1":   
            print("Exiting...")
            break
        elif choice == "2":
            fetch_repositories()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()