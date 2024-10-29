import os
import openai


class GPT3:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def call(self,
             prompt,
             engine="gpt-3.5-turbo-instruct",
             temperature=1.,
             max_tokens=30,
             top_p=1.,
             frequency_penalty=0,
             presence_penalty=0,
             logprobs=0,
             n=1):
        # Update number of API calls from file
        with open("api_calls.txt", "r") as file:
            api_calls = int(file.read())
            api_calls += 1
        with open("api_calls.txt", "w") as file:
            file.write(str(api_calls))
        return openai.Completion.create(
            engine=engine,
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            logprobs=logprobs,
            n=n)

