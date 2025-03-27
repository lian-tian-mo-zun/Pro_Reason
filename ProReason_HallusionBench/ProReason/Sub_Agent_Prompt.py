DISPATCHER_PROMPT="""The information you need is in an image, but you can't see the image right now.
At the same time, you're not capable of complex reasoning.

However, you can can consult the following two EXPERTs for help:
1. Vision Expert: You can ask him for information in the picture, for example, you could ask him, "What color is the bird in the picture?"
2. Reasoning Expert: You can ask him to get the results of complex reasoning, e.g. you can ask him, "What is the acceleration produced by a 1N force applied to a 1KG object?"

To solve this problem, which EXPERT do you think you should consult now??

Use the following format:
{
'Thought':'analyze the problem here.',
'EXPERT name':'The name of the EXPERT you choose should be one of Vision Expert and Reasoning Expert',
'Question':'Questions you want to ask the EXPERT'
}"""
def get_dispatcher_prompt(question,memory,last_expert):
    prompt=''
    prompt+='You currently need to address the following questions: \n\n'
    prompt+='"'+question+'"'
    prompt+=DISPATCHER_PROMPT
    if memory!='':
        prompt+='The last expert you chose was '+last_expert+' and the information you know currently is as follows:\n'
        prompt+=memory
    return prompt


REASONING_EXPERT_PROMPT="""You are a polytechnic college professor.
Use the following format:

Reasoning: Perform a step-by-step process of reasoning to solve a problem.
Final Answer: The final answer you get when you have finished reasoning."""
def get_reasoning_expert_prompt(question, memory):
    prompt='The following is the available information:\n'+memory+'Please solve the following problems step by step:'+question
    system_prompt=REASONING_EXPERT_PROMPT
    return prompt, system_prompt



REFEREE_PROMPT="""Return CAN_SOLVE if you think QUESTION can be resolved with known information. Otherwise return UNSOLVABLE.
Use the following format:

Thought: Conduct an analysis before you give me an answer.
Answer: the action to take, should be one of ['CAN_SOLVE', 'UNSOLVABLE']"""
def get_referee_prompt(question,memory):
    prompt='My current QUESTION that needs to be addressed is: \n'
    prompt+='"'+question+'"'
    prompt+='\n'
    prompt+='The information I know is: '
    prompt+=memory
    prompt+='\n'
    prompt+=REFEREE_PROMPT
    return prompt


SUMMARY_PROMPT="""Use the following format to solve the question:

Thought:Conduct a step by step analysis before you give me an answer.
Answer:The final answer of the question. """
SUMMARY_PROMPT_OPEN_ENDED="""Give me the answer."""
def get_summarizer_prompt(question,memory, open_ended_question):
    prompt='My current question that needs to be addressed is: \n'
    prompt+=question
    prompt+='\n'
    prompt+='I can not see the image, but I know the information in the image is as follows: \n'
    prompt+=memory
    prompt+='\n'
    if open_ended_question:
        prompt+=SUMMARY_PROMPT_OPEN_ENDED
    else:
        prompt+=SUMMARY_PROMPT
    return prompt