# FastAPI Telegram Messenger API Service

This API service is built with FastAPI and is currently in its prototype version. It is designed to process messages from Telegram Messenger, and can be integrated into Bubble (a low-code platform). It serves as a micro CRM for managing customers through various messengers.


## Features

- Receive and process messages from Telegram Messenger
- Integration with Bubble for low-code application development
- Manage customer data and interactions
- Easy to deploy and scale as a microservice

## Installation

### Prerequisites

- Python 3.10+
- pip (Python package installer)

### Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/your-repo.git
   cd your-repo

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt

3. Start the FastAPI server:
   ```bash
   uvicorn crm.openapi_server.main:app --reload

Integrating with Bubble
To integrate this API service with Bubble, follow these steps:


### In Bubble, go to the API Connector plugin.
Add a new API and configure the endpoint details (URL, method, headers, etc.).
Use Bubble's workflows and actions to call this API and process messages accordingly.


