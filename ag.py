# ag.py
import argparse
import os
from chat import *

def main():
    parser = argparse.ArgumentParser(description="AG CLI - Chat with ZhipuAI in terminal.")
    parser.add_argument("--reset", action="store_true", help="Reset the current conversation history")
    parser.add_argument("--api-key", type=str, help="Your ZhipuAI API key (or export AG_API_KEY=\"xxx\")")
    parser.add_argument("--file", type=str, help="Path to a file to include its content in the prompt") # New argument
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("AG_API_KEY")
    if not api_key:
        print("Error: API key is required. Use --api-key or set AG_API_KEY env variable.")
        return

    if args.reset:
        reset_history()
        print("✅ new chat \n")
        return

    file_content = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            print(f"📎 Attached file: {args.file}\n")
        except FileNotFoundError:
            print(f"Error: File not found at path: {args.file}")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return

    print("👇💬~")
    try:
        while True:
            user_input = prompt("👴: ")
            if user_input.lower() in ("exit", "quit"):
                print("\n👋")
                break
            
            stream_chat(user_input, api_key, file_content=file_content) # Modified call
            file_content = None 
    except KeyboardInterrupt:
        print("\n👋")

if __name__ == "__main__":
    main()