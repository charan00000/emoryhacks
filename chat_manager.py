class ChatSession:
    def __init__(self, user_name, user_id):
        """
        Initialize a new chat session.
        :param session_id: Unique identifier for the chat session.
        :param user_name: Name of the user in the chat session.
        """
        self.user_name = user_name
        self.user_id = user_id
        self.messages = []  # List to store messages in the session

    def add_message(self, message):
        """
        Add a message to the chat session.
        :param sender: The sender of the message (e.g., 'user' or 'bot').
        :param message: The content of the message.
        """
        self.messages.append({'user': sender, 'response': message})

    def get_history(self):
        """
        Retrieve the chat history.
        :return: List of all messages in the session.
        """
        return self.messages

    def clear_history(self):
        """
        Clear the chat history.
        """
        self.messages = []

    def __str__(self):
        """
        String representation of the chat session.
        :return: A formatted string of the chat history.
        """
        history = [f"{msg['sender']}: {msg['message']}" for msg in self.messages]
        return "\n".join(history)

