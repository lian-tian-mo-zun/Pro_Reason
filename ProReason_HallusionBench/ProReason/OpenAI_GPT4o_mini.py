from openai import OpenAI
import os
import base64
import mimetypes

def get_gpt4o_mini_response_pic(prompt,pic,system_prompt):
    client = OpenAI(
        api_key="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",
    )
    image_path = pic

    mime_type, _ = mimetypes.guess_type(image_path)

    if mime_type and mime_type.startswith('image'):
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read())
            encoded_image_str = encoded_image.decode('utf-8')
            data_uri_prefix = f'data:{mime_type};base64,'
            encoded_image_str = data_uri_prefix + encoded_image_str
            
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                        {
                            "role": "system","content": system_prompt,
                        },
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": encoded_image_str
                                    }
                                }
                            ]
                        }
                ],
            )
            #print(completion.usage.prompt_tokens, completion.usage.completion_tokens)
            return completion.choices[0].message.content
    else:
        print("MIME type unsupported or not found.")

def get_gpt4o_mini_response_text(prompt,system_prompt):
    client = OpenAI(
        api_key="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",
    )
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": prompt}],
    )
    #print(chat_completion.usage.prompt_tokens, chat_completion.usage.completion_tokens)
    return chat_completion.choices[0].message.content

def get_gpt4o_mini_response(prompt,pic=None,system_prompt='You are a helpful assistant.'):
    if pic!=None:
        return get_gpt4o_mini_response_pic(prompt,pic,system_prompt)
    else:
        return get_gpt4o_mini_response_text(prompt,system_prompt)