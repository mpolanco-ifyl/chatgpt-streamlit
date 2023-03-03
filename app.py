import openai
import streamlit as st
import os

# Inicializa el modelo GPT-3
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Define an empty message log
message_log = []
    
def generate_response(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        # max_tokens=4096,        # The maximum number of tokens (words or subwords) in the generated response
        # stop=None,              # The stopping sequence for the generated response, if any (not used here)
        temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

st.markdown("# OpenAI Chatbot - Escritor Fantasma")

# Add a prompt for the user to start the conversation
message_log.append({"role": "user", "content": "Quiero que actúes como escritor fantasma"})
output = generate_response(message_log)
message_log.append({"role": "assistant", "content": output})
st.markdown(f'''**AI:** {output}''')

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
user_input=st.text_area("You:",key='input')


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
        # message(st.session_state["generated"][i], key=str(i))
        st.markdown(f'''**AI:** {st.session_state["generated"][i]}''')
        # message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        st.markdown(f'''**You:** {st.session_state['past'][i]}''')


