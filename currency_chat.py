from openai import OpenAI
import requests
from datetime import datetime
import json

# Initialize OpenAI client
client = OpenAI()

def get_currency_rate(currency: str, date: str) -> str:
    """Get currency exchange rate from NBP API for a specific date."""
    try:
        url = f"https://api.nbp.pl/api/exchangerates/rates/c/{currency}/{date}/?format=json"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            buy_rate = data['rates'][0]['bid']
            sell_rate = data['rates'][0]['ask']
            return f"On {date}, {currency} exchange rates were: Buy: {buy_rate} PLN, Sell: {sell_rate} PLN"
        else:
            return f"Could not fetch data for {currency} on {date}. Please check if it's a valid working day."
    except Exception as e:
        return f"Error occurred: {str(e)}"

# Define the available tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_currency_rate",
            "description": "Get the exchange rate for a specific currency on a given date from NBP (National Bank of Poland)",
            "parameters": {
                "type": "object",
                "properties": {
                    "currency": {
                        "type": "string",
                        "description": "The currency code (e.g., USD, EUR, GBP)"
                    },
                    "date": {
                        "type": "string",
                        "description": "The date in YYYY-MM-DD format"
                    }
                },
                "required": ["currency", "date"]
            }
        }
    }
]

# System message to define the assistant's behavior
system_message = """You are a helpful assistant specializing in providing currency exchange rates from the National Bank of Poland (NBP).
You can check historical exchange rates for various currencies against PLN.
You can help users by calling the get_currency_rate function with a currency code and date.
Please inform users that you can help them check currency rates for specific dates."""

def main():
    print("Welcome to the Currency Exchange Rate Assistant!")
    print("You can ask about historical currency rates from NBP (e.g., 'What was the USD rate on 2023-01-15?')")
    print("Type 'quit' to exit")
    
    # Start conversation with system message
    messages = [{"role": "system", "content": system_message}]
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        assistant_message = response.choices[0].message
        
        # Handle tool calls
        if assistant_message.tool_calls:
            messages.append({"role": "assistant", "content": assistant_message.content, "tool_calls": assistant_message.tool_calls})
            for tool_call in assistant_message.tool_calls:
                if tool_call.function.name == "get_currency_rate":
                    function_args = json.loads(tool_call.function.arguments)
                    result = get_currency_rate(
                        function_args["currency"],
                        function_args["date"]
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call.function.name,
                        "content": result
                    })
            
            # Get final response after tool call
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            assistant_message = response.choices[0].message
            
        messages.append({"role": "assistant", "content": assistant_message.content})
        print(f"\nAssistant: {assistant_message.content}")

if __name__ == "__main__":
    main()
