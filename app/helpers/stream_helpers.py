from langchain.callbacks.base import BaseCallbackHandler
import asyncio

class StreamingCallback(BaseCallbackHandler):
    def __init__(self, delay_ms: int = 50):  # Default delay of 100ms
        self.messages = []
        self.delay = delay_ms / 1000

    def on_llm_new_token(self, token: str, **kwargs):
        # Store each token as it is received
        self.messages.append(token)

    async def get_messages(self):
        # Yield each token stored in the list
        for msg in self.messages:
            msg = msg.replace("\n", "<br/>")
            yield f"data: {msg}\n\n"  # SSE format
            await asyncio.sleep(self.delay)  # Add delay before sending the next message

        self.messages = []

    async def get_stream_text(self, messages):
        # Yield each token stored in the list
        print("messages", messages)
        for msg in messages:
            print("msg", msg)
            msg = msg.replace("\n", "<br/>")
            yield msg #f"data: {msg}\n\n"  # SSE format
            await asyncio.sleep(self.delay)  # Add delay before sending the next message

        self.messages = []