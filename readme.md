# Urlio
Urlio is a micro URL shortener web application built using Python and Flask. It allows users to shorten long URLs and manage them efficiently. The application integrates with MongoDB for data storage and supports Google OAuth 2.0 for user authentication.

## Features
- **URL Shortening:** Convert long URLs into concise, shareable links.
- **User Authentication:** Secure login using Google OAuth 2.0.
- **URL Management:** Track and manage your shortened URLs.
- **Responsive Design:** User-friendly interface accessible across devices.

## Demo
Check out the live application here: https://urlio.vercel.app/

## Installation
### Prerequisites
- Python 3.7 or higher
- MongoDB database
- Google Cloud project with OAuth 2.0 credentials

### Clone the Repository
```bash
git clone https://github.com/soni-shashan/Micro_It_urlio_Project.git
cd Micro_It_urlio_Project
```

### Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Configure Environment Variables
Create a .env file in the root directory and add the following variables:
```env
MONGO_URI=your_mongodb_connection_string
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=your_oauth_redirect_uri
```
Replace the placeholder values with your actual credentials.

## Run the Application
```bash
python app.py
```
The application will be accessible at http://localhost:5000.

## Deployment
The application is configured for deployment on Vercel. Ensure that your vercel.json is set up correctly and that your environment variables are configured in the Vercel dashboard.