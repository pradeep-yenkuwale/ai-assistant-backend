
import datetime
from app.constants.voices import LANGUAGE_NOT_SELECTED
from app.helpers.log_helpers import update_user_search_logs
from app.helpers.model_helpers import configure_model, prepare_prompt
from app.helpers.stream_helpers import StreamingCallback
from app.lib.voice.speak_default import speak_english
from app.lib.voice.speak_local import speak_arabic

async def stream_text(input_object, language='en'):
    query = input_object["query"]
    context = input_object["context"]
    callback = StreamingCallback()
    
    print("User Input: ", input_object)

    # Load training data and configure model
    chain = configure_model(callback)
    chat_history = []
    query = prepare_prompt(query, language, context)
    print("User Query: ", query)

    # Check if there is input query passed and send to AI model
    if query and query != None:
        # Get response from the model
        result = chain({"question": query, "chat_history": chat_history, "return_only_outputs": True})
        response = result['answer']
        received_at = datetime.datetime.now(datetime.timezone.utc)
        input_object['received_at'] = received_at
        log = await update_user_search_logs(input_object, response)
        # Update chat history, which can be used to retrieve response for repeated questions
        chat_history.append((query, response))
        print("Model Response", result['answer'])
        async for message in callback.get_messages():
            print("message", message)
            yield message
    query = None

def stream_voice(input_object, audio_dir, language='en'):
    print("User Input: ", input_object)
    query = input_object["query"]
    context = input_object["context"]   
    callback = StreamingCallback()
    print("User Query: ", query)

    # Load training data and configure model
    chain = configure_model(callback)
    chat_history = []
    user_query = prepare_prompt(query, language, context)

    # Check if there is input query passed and send to AI model
    if user_query and user_query != None:
        # Get response from the model
        result = chain({"question": user_query, "chat_history": chat_history, "return_only_outputs": True})
        response = result['answer']
        received_at = datetime.datetime.now(datetime.timezone.utc)
        input_object['received_at'] = received_at
        # log = update_user_search_logs(input_object, response)
        # Update chat history, which can be used to retrieve response for repeated questions
        chat_history.append((user_query, response))
        if(language == 'en'):
            return speak_english(response, audio_dir)
        elif(language == 'ar'):
            return speak_arabic(response, audio_dir)
        else:
            return speak_english(LANGUAGE_NOT_SELECTED, audio_dir)
        
    user_query = None



def stream_voice_text(input_object, language='en'):
    query = input_object["query"]
    context = input_object["context"]
    callback = StreamingCallback()
    
    # Load training data and configure model
    chain = configure_model(callback)
    chat_history = []
    query = prepare_prompt(query, language, context)
    print("User Query: ", query)

    # Check if there is input query passed and send to AI model
    if query and query != None:
        # Get response from the model
        result = chain({"question": query, "chat_history": chat_history, "return_only_outputs": True})
        # Update chat history, which can be used to retrieve response for repeated questions
        chat_history.append((query, result['answer']))
        print("result['answer'])", result['answer'])
        return result['answer']
    query = None
