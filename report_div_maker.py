import re

def wrap_messages_in_divs(text):
    # Split the text into messages
    messages = re.split(r'\),\s*\(', text)
    
    # Remove any leading or trailing parentheses
    messages = [message.strip().strip('()') for message in messages]
    
    # Wrap each message in a div
    wrapped_messages = [f'<div class="message">{message}</div>' for message in messages if message]
    
    # Join the wrapped messages back into a string
    wrapped_text = '\n'.join(wrapped_messages)
    
    return wrapped_text

# Example text
text = """
(sender: human, message: I have a headache), 
(sender: ai, message: Okay, I understand you have a headache. To help me understand what might be causing it, could you tell me **where in your head you feel the pain most intensely?**
), 
(sender: human, message: back right), 
(sender: ai, message: Okay, the pain is most intense in the back right of your head. Can you describe the nature of the pain? Is it throbbing, sharp, dull, or something else?
), 
(sender: human, message: dull), 
(sender: ai, message: Okay, the pain in the back right of your head is dull. How long have you been experiencing this dull headache?
), 
(sender: human, message: 2 horus), 
(sender: ai, message: Okay, you've had this dull headache in the back right of your head for about 2 hours. Have you taken any medication for the headache, such as Tylenol or ibuprofen?
), 
(sender: human, message: np), 
(sender: ai, message: Okay, you've had this dull headache in the back right of your head for about 2 hours and haven't taken any medication. Have you experienced any other symptoms along with the headache, such as nausea, dizziness, or sensitivity to light or sound?
), 
(sender: human, message: no), 
(sender: ai, message: Okay, you've had this dull headache in the back right of your head for about 2 hours, haven't taken any medication, and aren't experiencing any other symptoms like nausea, dizziness, or sensitivity to light or sound.

Considering the location and nature of your headache, it could be related to muscle tension.

Has anything specific triggered the headache, such as stress, prolonged computer use, or poor posture?
), 
(sender: human, message: I was playing valorant for 26 hours straigt), 
(sender: ai, message: Okay, you've had this dull headache in the back right of your head for about 2 hours, haven't taken any medication, aren't experiencing any other symptoms, and you were playing Valorant for 26 hours straight. Prolonged screen time and gaming can certainly contribute to headaches, potentially due to eye strain or muscle tension from posture.
), 
"""

# Wrap messages in divs
if __name__ == '__main__':
    wrapped_text = wrap_messages_in_divs(text)
    print(wrapped_text)
# Print the result
