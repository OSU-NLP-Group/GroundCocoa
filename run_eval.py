# Author: Harsh Kohli
# Date Created: 23-12-2023

import os
import time
from openai import OpenAI
from datasets import load_dataset
from utils.gen_utils import mark_correctness
from constants import question_prompt, cocoa_dataset_file, file_dir
from utils.ioutils import read_from_json, write_to_json

# change to "cot_full" for full CoT prompting, or "regular" for prompting without CoT
prompting_strategy = "regular"

# set to True if you wish to download and load the dataset from HuggingFace hub
load_from_huggingface = False

# Only required when evaluating an OpenAI model
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


# For GPT-4 Turbo, change to any other model call as desired
def get_model_response(final_prompt):
    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": final_prompt,
            }
        ],
        temperature=0.0,
        model="gpt-4-1106-preview",
    )
    model_response = completion.choices[0].message.content
    return model_response


if load_from_huggingface:
    all_samples = load_dataset("harsh147/GroundCocoa", split="test", trust_remote_code=True, streaming=True)
    cocoa_dataset = [sample for sample in all_samples]
else:
    cocoa_dataset = read_from_json(cocoa_dataset_file)['test_set']

cot_prompt = ''

if prompting_strategy != "regular":
    if prompting_strategy == "cot_partial":
        f = open(os.path.join(file_dir, 'cot_prompt.txt'), 'r', encoding='utf8')
    else:
        f = open(os.path.join(file_dir, 'cot_prompt_full.txt'), 'r', encoding='utf8')
    for line in f.readlines():
        cot_prompt = cot_prompt + line
    f.close()

start = time.time()
model_responses = []
for index, test_sample in enumerate(cocoa_dataset):
    try:
        question = test_sample['query']
        question = question + '\n\n Option A: ' + str(test_sample['Option A']) + '\n'
        question = question + '\n Option B: ' + str(test_sample['Option B']) + '\n'
        question = question + '\n Option C: ' + str(test_sample['Option C']) + '\n'
        question = question + '\n Option D: ' + str(test_sample['Option D']) + '\n'
        question = question + '\n Option E: ' + str(test_sample['Option E']) + '\n'

        if prompting_strategy != "regular":
            final_prompt = cot_prompt + question
        else:
            final_prompt = question_prompt + '"' + question + '"'

        model_response = get_model_response(final_prompt)
        test_sample['model_response'] = model_response
        model_responses.append(test_sample)
        if index % 100 == 0:
            print('Done with ' + str(index) + ' iterations')
            end = time.time()
            time_taken = str(end - start)
            print('Time taken ' + time_taken + ' seconds')
    except Exception as e:
        print('Aborting due to error')
        print(e)
        break

write_to_json(model_responses, os.path.join(file_dir, 'results.json'))
response_info = mark_correctness(model_responses)
print('Model Accuracy: ' + str(response_info.acc))
