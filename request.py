import openai
import os
import sys
import time

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")
model = os.getenv("OPENAI_MODEL")

systemMessage = """ You are a helpful github assistant. 
                    You will respond to users in a markdown friendly format. 
                    You should provide an explination to you r solution as well as a code snippet
                """

def main(input,attempt=0):
    try:
        res = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": systemMessage},
                {"role": "user", "content": input},
            ]
        )

        print(res["choices"][0]["message"]["content"])
        return res["choices"][0]["message"]["content"]
    except openai.error.RateLimitError as e:
        time.sleep(10)
        if attempt < 3:
            attempt+=1
            return main(input,attempt=attempt)
        else:
            raise Exception("Rate limit exceeded. Retry attempts failed")


if __name__ == "__main__":
    main(sys.argv[1])