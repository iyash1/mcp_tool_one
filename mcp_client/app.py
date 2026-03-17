import asyncio
import os
from dotenv import load_dotenv
from colorama import Fore, Style, init

print(f"{Fore.YELLOW}➡️ Starting the MCP Client... {Style.RESET_ALL}")     

# ------------------------------------
# Load environment variables
# ------------------------------------
print(f"{Fore.YELLOW}➡️ Loading environment variables... {Style.RESET_ALL}")

load_dotenv()
init(autoreset=True)

# Set environment variables (especially useful for LangChain integrations)
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError(f"{Fore.RED} ➡️__OPENAI_API_KEY not found in environment variables. ❌ {Style.RESET_ALL}")
else:
    print(f"""{Fore.GREEN}➡️ All API keys loaded successfully. ✅ {Style.RESET_ALL}""")

# ---------------------------------------------
# Import services after environment is set up
# ---------------------------------------------
from services.get_schema import get_schema
from services.client_agent import call_services

# ---------------------------------------------
# Main interactive loop
# ---------------------------------------------
async def main():
    print(f"{Fore.CYAN}\n Welcome to the MCP Client! This client will connect to the MCP Server and interact with the AI Tutor tool. {Style.RESET_ALL}")
    while True:
        print(f""" {Fore.CYAN}
        Select a service from below : 
        1. Get AI Tutor Schema
        2. Use AI Tutor
        3. Exit
        {Style.RESET_ALL}""")
        choice = input(f"{Fore.YELLOW}Enter your choice (1, 2 or 3): {Style.RESET_ALL}")
        match choice:
            case "1":
                get_schema()
            case "2":
                await call_services()
            case "3":
                print(f"{Fore.GREEN}Exiting the MCP Client. Goodbye!{Style.RESET_ALL}")
                break
            case _:
                print(f"{Fore.RED}Invalid choice. Please enter 1, 2 or 3.{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(main())
