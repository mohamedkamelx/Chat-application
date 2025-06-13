# Django Chat Application

A simple real-time chat application built with Django that allows users to connect with friends and exchange messages.

## Features

- User authentication and profiles
- Friend system (add/remove friends)
- Real-time messaging between friends
- Message history and read receipts
- User search functionality
- Clean and responsive interface

## Models

The application uses three main models:
- **UserProfile**: Stores user information and profiles
- **Friends**: Manages friend relationships between users
- **Messages**: Stores chat messages with timestamps and read status

## Key Functionality

### User Management
- User registration and authentication
- Profile management
- Friend search and discovery

### Friend System
- Add friends by username
- View friends list
- Bidirectional friend relationships

### Messaging
- Send messages to friends
- View message history
- Mark messages as read/seen
- Real-time message updates

## API Endpoints

### Views
- `/` - Home page with friends list
- `/search/` - Search for users and manage friends
- `/add_friend/<username>/` - Add a user as friend
- `/chat/<username>/` - Chat interface with a specific friend

### API Endpoints
- `GET /messages/<sender_id>/<receiver_id>/` - Fetch unseen messages
- `POST /messages/` - Send a new message

## Installation

1. Clone the repository
2. Install Django and Django REST Framework:
   ```bash
   pip install django djangorestframework
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage

1. Register or login to your account
2. Search for other users and add them as friends
3. Navigate to the chat interface to start messaging
4. Messages are automatically marked as read when viewed
