# Example Chainlit LangGraph Azure

A project that combines Chainlit, LangGraph, and Azure services for building interactive AI applications.

Based on:
 - https://docs.chainlit.io/integrations/langchain
 - https://github.com/Azure-Samples/azure-sql-db-rag-langchain-chainlit

## Prerequisites

- Python 3.12
- Poetry (Python package manager)
- Azure account and necessary credentials

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd example-chainlit-langgraph-azure
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Set up your environment variables:
Create a `.env` file in the root directory with your Azure and other necessary credentials.
See `.env.example` for used env vars.

## Running the Project

To run the project in development mode with hot-reload enabled:

```bash
poetry run chainlit run entrypoint.py --port 8042 -w
```

This will:
- Start the Chainlit application
- Run on port 8042
- Enable watch mode (-w) for automatic reloading during development

The application will be available at `http://localhost:8042`

## Development

The project uses Poetry for dependency management. Key dependencies include:
- chainlit
- langchain
- langgraph
- Azure services integration

For more information about the technologies used, refer to the links in the "Based on" section above. 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 


