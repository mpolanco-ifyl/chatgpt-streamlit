import openai
import streamlit as st
import os

# Inicializa el modelo GPT-3
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define an empty message log
message_log = []
    
def generate_response(message_log):
    # Use OpenAI's Completion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        engine="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        prompt=message_log[-1]['content'],   # The most recent user message as the prompt
        max_tokens=4024,        # The maximum number of tokens (words or subwords) in the generated response
        n=1,        # The number of responses to generate
        stop=None,              # The stopping sequence for the generated response, if any
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Extract the first response from the API response
    return response.choices[0].text.strip()

st.markdown("# OpenAI Chatbot - Escritor Fantasma")

# Add a prompt for the chatbot to start the conversation
message_log.append({"role": "assistant", "content": "Hola, soy un escritor fantasma. Estoy aquí para ayudarte a escribir lo que necesites. ¿En qué puedo ayudarte hoy?"})

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_area("You:", key=hash(str(st.session_state['past'])), default="", height=100, max_chars=None, key_up=None, help=None)

if user_input:
    # print(message_log)
    message_log.append({"role": "user", "content": user_input})
    output=generate_response(message_log)
    message_log.append({"role": "assistant", "content": output})
    #store the output
    st.session_state['past'].append(user_input)
    st.session_state['generated'].append(output)

if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')
        st.markdown(f'''**You:** {st.session_state['past'][i]}''')

# Initialize the text area for user input, or clear it if there is a new message
if 'input' not in st.session_state:
    st.session_state['input'] = ''
user_input=st.text_area("You:", value=st.session_state['input'], key='input')
st.session_state['input'] = user_input.strip()
