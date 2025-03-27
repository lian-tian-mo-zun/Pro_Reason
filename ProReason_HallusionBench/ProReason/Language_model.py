from ProReason.OpenAI_GPT4o_mini import get_gpt4o_mini_response

def get_LVLM_response(prompt,pic,system_prompt=''):
    return get_gpt4o_mini_response(prompt=prompt,pic=pic,system_prompt=system_prompt)

def get_LLM_response(prompt,system_prompt=''):
    return get_gpt4o_mini_response(prompt=prompt,system_prompt=system_prompt)