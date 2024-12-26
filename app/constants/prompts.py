GREETINGS = "hi, hello, how are you, how are you doing, hey, thank you, thanks, you are awesome, welcome, welcome to, thanks for your inputs, thank you so much, hey thank you"

FORMAT_RESPONSE = " Please generalize the response, and please add a new line after each sentence, heighlight the key or important information, and if you want to list the points, please use numeric notation for listing the points."

GENERAL_PROMPT = ".\n If you do not understand the question, ask user to provide detailed context about the query, which should include information related to trips and travel. " + FORMAT_RESPONSE

LANGUAGE_PROMPT = "\n The above is the user query, i want you to process it and convert final response to arabic language, thank you"

COMMON_QUESTION = "If you don not understand the query or question, ask for more detailed context about what is needed"

BOOKING_PROMPT = ".\n If the query or question is related to a booking or future booking, do not proceed further, just stop here and ask for more details such as booking id, source and destination details etc..."

SUGGEST_TRIPS = COMMON_QUESTION +  " which should include key inputs such as trips with seasons and the budget and interested cities to travel around, once you understand the query, seek for related information and suggest the trips and also provide available details for accomodations by considering nearby hotels with key details room types, and its pricings, having said, also generalize about people interests who have already visited the cities and visiting places." + FORMAT_RESPONSE

PEOPLE_INTERESTS = BOOKING_PROMPT + ".\n " + COMMON_QUESTION + " you may ask for people interest in places, accomodations and fights and provide a detailed information about the same." + FORMAT_RESPONSE

FUTURE_BOOKINGS = ".\n " + COMMON_QUESTION + " you may ask about the booking id, travel date or the origine and destination details." + FORMAT_RESPONSE