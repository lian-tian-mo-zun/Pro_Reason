import re

from ProReason.Language_model import get_LVLM_response
from ProReason.Language_model import get_LLM_response

from ProReason.Sub_Agent_Prompt import get_dispatcher_prompt
from ProReason.Sub_Agent_Prompt import get_reasoning_expert_prompt
from ProReason.Sub_Agent_Prompt import get_referee_prompt
from ProReason.Sub_Agent_Prompt import get_summarizer_prompt

def extract_final_answer(text,symbol='Final Answer:'):
    start_index = text.find(symbol) + len(symbol)
    answer = text[start_index:].lstrip()
    return answer

def extract_dict(input_str, split_s="':'"):
    string = re.search(r'\{(.*)\}', input_str, re.DOTALL).group(0)
    lines = string.splitlines()
    lines=lines[1:-1]
    my_dict={}
    for i in range(0,len(lines)):
        split_line=lines[i].split(split_s)
        if i<(len(lines)-1):
            my_dict[split_line[0][1:].replace("'",'')]=split_line[1][:-2]
        else:
            my_dict[split_line[0][1:].replace("'",'')]=split_line[1][:-1]
    return my_dict

class ProReason_Agent:
    def __init__(self, max_attempt_num=8, LVLM_cot=True ,open_ended_question=True) -> None:
        self.max_attempt_num=max_attempt_num
        self.LVLM_cot=LVLM_cot
        self.open_ended_question=open_ended_question
    
    def dispatcher(self, Question, memory, last_expert):
        prompt=get_dispatcher_prompt(question=Question, memory=memory, last_expert=last_expert)
        return get_LLM_response(prompt=prompt)

    def vision_expert(self, question,picture_path):
        return get_LVLM_response(prompt=question,pic=picture_path)

    def reasoning_expert(self, question, memory):
        prompt,system_prompt=get_reasoning_expert_prompt(question=question, memory=memory)
        return get_LLM_response(prompt=prompt,system_prompt=system_prompt)

    def referee(self, Question, memory):
        prompt=get_referee_prompt(question=Question, memory=memory)
        return get_LLM_response(prompt=prompt)

    def summarizer(self, Question, memory):
        prompt=get_summarizer_prompt(question=Question, memory=memory, open_ended_question=self.open_ended_question)
        return get_LLM_response(prompt=prompt)
    
    def run_dispatcher(self, Question, memory, last_expert):
        dispatcher_response=self.dispatcher(Question, memory, last_expert)
        try:
            choice_dict=extract_dict(dispatcher_response)
        except:
            try:
                choice_dict=extract_dict(dispatcher_response,"': '")
            except:
                return 'fail'
        try:
            expert_name=choice_dict['EXPERT name']
            question=choice_dict['Question']
            if expert_name in ['Vision Expert','Reasoning Expert']:
                return choice_dict
            else:
                return 'fail'
        except:
            return 'fail'



    def run_ProReason(self, Question, pic):
        if pic==None:
            return get_LLM_response(Question)
        memory=''
        last_expert=''

        for i in range(0,self.max_attempt_num):
            #run dispatcher
            choice_dict=self.run_dispatcher(Question,memory,last_expert)
            if choice_dict=='fail':
                continue
        
            #run vision or reasoning expert, and add the answer to the memory
            try:
                if choice_dict['EXPERT name']=='Vision Expert':
                    if self.LVLM_cot:
                        answer=self. vision_expert(question='Please answer the following questions step by step:\n'+choice_dict['Question'], picture_path=pic)
                    else:
                        answer=self. vision_expert(question=choice_dict['Question'], picture_path=pic)
                if choice_dict['EXPERT name']=='Reasoning Expert':
                    reasoning_answer=self.reasoning_expert(question=choice_dict['Question'],memory=memory)
                    answer=extract_final_answer(reasoning_answer)
                memory+=answer+'\n'
                last_expert=choice_dict['EXPERT name']
            except:
                continue

            #run referee
            judgement=self.referee(Question=Question,memory=memory)
            if 'Answer: CAN_SOLVE' in judgement:
                memory+=judgement
                final_answer=self.summarizer(Question=Question,memory=memory)
                if self.open_ended_question:
                    return final_answer
                else:
                    extracted_fianl_answer=extract_final_answer(final_answer,"Answer:")
                    return extracted_fianl_answer
            else:
                continue
        return get_LVLM_response(prompt=Question,pic=pic)