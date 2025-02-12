# Currency Exchange Rate Assistant

A simple demonstration of OpenAI API integration with a custom tool for checking historical currency exchange rates from the National Bank of Poland (NBP).

## Features

- Interactive chat interface
- Integration with NBP API for currency exchange rates
- Custom tool implementation using OpenAI function calling
- Support for multiple currencies (USD, EUR, GBP, etc.)

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python packages:
  - openai
  - requests

## Installation

1. Clone the repository:
```bash
git clone git@github.com:nrafal/openai-demo.git
cd openai-demo
```
2. (Optional) Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

3. Install required packages:
```bash
# Using pip directly
pip install openai requests

# Or using requirements.txt
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key'
```

## Usage

1. Run the application:
```bash
python currency_chat.py
```

2. Example questions you can ask:
- "What was the USD rate on 2023-01-15?"
- "Can you check the EUR exchange rate for 2023-05-20?"
- "Tell me the GBP rate for 2022-12-01"

3. Type 'quit' to exit the application.

## How It Works

The application combines OpenAI's GPT model with a custom tool that fetches currency exchange rates from the NBP API. When you ask about currency rates, the assistant:

1. Understands your query using natural language processing
2. Extracts the currency and date information
3. Calls the NBP API to get the actual exchange rates
4. Presents the information in a friendly format

## API Reference

The application uses:
- OpenAI API (GPT-4)
- NBP API endpoint: `https://api.nbp.pl/api/exchangerates/rates/c/{currency}/{date}/?format=json`

## Note

The NBP API only provides data for working days. Requests for weekends or holidays may return errors.

## Azure OpenAI Setup

To use Azure OpenAI API instead of OpenAI API:

1. Update environment variables:
```bash
export AZURE_OPENAI_ENDPOINT='your-azure-endpoint'
export AZURE_OPENAI_KEY='your-azure-key'
export AZURE_OPENAI_DEPLOYMENT='your-deployment-name'
```

2. Modify the code initialization:
```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-02-15-preview",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)
```

3. Update the model name in chat completion calls:
```python
response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    # rest of the parameters remain the same
)
```