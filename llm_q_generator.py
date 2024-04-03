# Author: Harsh Kohli
# Date Created: 23-12-2023

import os
from utils.ioutils import read_from_json, write_to_json
from openai import OpenAI
from constants import prompt1, prompt2, conditions_file, data_file

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

temp = 0.0
conditions_data = read_from_json(conditions_file)

for sample in conditions_data:
    templates = sample['condition_templates']
    paraphrased_conditions = []
    user_conditions = ''
    for template in templates:
        one_print = ''
        if len(template) > 1:
            one_print = 'Either '
        for index, y in enumerate(template):
            one_print = one_print + y
            if index != (len(template) - 1):
                one_print = one_print + ', or '

        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt1 + one_print,
                }
            ],
            temperature=temp,
            # model="gpt-4",
            model="gpt-4-1106-preview",
        )

        paraphrased_condition = completion.choices[0].message.content
        paraphrased_conditions.append(paraphrased_condition)

        user_conditions = user_conditions + paraphrased_condition + ' '

    completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt2 + user_conditions,
            }
        ],
        temperature=temp,
        # model="gpt-4",
        model="gpt-4-1106-preview",
    )

    final_requirement = completion.choices[0].message.content
    sample['final_question'] = final_requirement

write_to_json(conditions_data, data_file)
