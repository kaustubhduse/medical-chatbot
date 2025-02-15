css = '''
<style>
  /* Chat container */
  .chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
    background-color: #f9f9f9;
    border-radius: 15px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
  }

  /* Chat message */
  .chat-message {
    padding: 1rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: flex-start;
    transition: transform 0.3s ease-in-out;
    max-width: 100%;
    box-sizing: border-box;
  }

  /* Hover effect on message */
  .chat-message:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }

  /* User message */
  .chat-message.user {
    background-color: #4e5b6e;
    align-self: flex-start;
    color: #f4f4f9;
    margin-left: 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 80%; /* Limit width to 80% */
  }

  /* Bot message */
.chat-message.bot {
    background-color: #3e4a55;
    align-self: flex-end; /* Align the message container to the right */
    color: #f4f4f9;
    margin-left: 20%; /* Remove any margin on the left */
    margin-right: 0; /* Ensure no margin on the right */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    max-width: 80%; /* Limit width to 80% */
    justify-content: flex-end; /* Align content to the right */
}


  /* Avatar */
  .chat-message .avatar {
    width: 15%;
    padding-right: 1rem;
  } 

  .chat-message .avatar img {
    max-width: 60px;
    max-height: 60px;
    border-radius: 50%;
    object-fit: cover;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  }

  /* Message container */
  .chat-message .message {
    width: 100%;
    padding: 0.8rem 1.5rem;
    border-radius: 12px;
    background-color: #1f2630;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    word-wrap: break-word;
    white-space: pre-wrap;
  }

  /* Responsive Design */
  @media (max-width: 768px) {
    .chat-message {
      flex-direction: column;
      align-items: flex-start;
    }

    .chat-message .avatar {
      width: 30%;
    }

    .chat-message .message {
      width: 100%;
    }
  }
</style>
'''

bot_template = '''
<div class="chat-message bot">
  <div class="avatar">
    <img src="https://i.ibb.co/cN0nmSj/Screenshot-2023-05-28-at-02-37-21.png" alt="Bot Avatar"
    style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;"
    >
  </div>
  <div class="message" style="margin-left: 20px;">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
  <div class="avatar">
    <img src="https://upload.wikimedia.org/wikipedia/en/4/45/Indian_Institute_of_Information_Technology_Vadodara_Logo.svg" alt="User Avatar">
  </div>
  <div class="message">{{MSG}}</div>
</div>
'''
