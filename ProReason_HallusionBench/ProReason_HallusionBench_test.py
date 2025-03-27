import json
from tqdm import tqdm
from ProReason.ProReason import ProReason_Agent

if __name__ == "__main__":

    with open('HallusionBench.json', 'r', encoding='utf-8') as file:
        question_data = json.load(file)

    ProReason_example = ProReason_Agent()

    with open('ProReason_HallusionBench.json', 'r', encoding='utf-8') as file:
        answer_list = json.load(file)
    #answer_list = []

    for i in tqdm(range(len(answer_list), len(question_data)), desc="Processing", unit="sample"):
        sample = question_data[i]
        question = question_data[i]['question']
        file_name = question_data[i]['filename']

        answer = ProReason_example.run_ProReason(Question=question, pic=file_name)
        sample['model_prediction'] = answer

        answer_list.append(sample)
        
        with open('ProReason_HallusionBench.json', 'w', encoding='utf-8') as f:
            json.dump(answer_list, f, ensure_ascii=False, indent=4)
