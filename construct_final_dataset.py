import copy
import random
from constants import data_file, num_options_per_mcq, cocoa_dataset_file
from utils.ioutils import read_from_json, write_to_json


def camel_case_split(str):
    new_string = ""
    for i in str:
        if not i.islower():
            new_string += "*" + i
        else:
            new_string += i
    x = new_string.split("*")
    x.remove('')
    return " ".join(x)


def split_by_entropy(sorted_flight_options, sorted_labels):
    num_pos = sorted_labels.count('1')
    num_neg = sorted_labels.count('0')
    num_neg_options = num_options_per_mcq - 1

    if num_neg < num_neg_options:
        return None

    spacing = (num_neg - (num_neg_options - 1)) / num_pos

    pos_options, neg_options = [], []
    for option, label in zip(sorted_flight_options, sorted_labels):
        if label == '0':
            neg_options.append(option)
        elif label == '1':
            pos_options.append(option)
        else:
            print('Invalid label')

    starting_points = [0]
    for index in range(1, num_pos):
        next_index = int(spacing * index)
        starting_points.append(next_index)

    neg_buckets = []
    for starting_pt in starting_points:
        one_bucket = []
        for offset in range(num_neg_options):
            neg_option = neg_options[starting_pt + offset]
            one_bucket.append(neg_option)
        neg_buckets.append(one_bucket)

    choice_sets = []
    for pos, neg_bucket in zip(pos_options, neg_buckets):
        one_set = [pos]
        one_set.extend(neg_bucket)
        choice_sets.append(one_set)

    return choice_sets


def num2char(num):
    return chr(((num - 1) % 26) + ord('A'))


def shuffle_and_simplify(test_sample, choice_sets, id):
    new_samples = []
    for choice_set in choice_sets:
        ans = choice_set[0]
        random.shuffle(choice_set)
        ans_index = choice_set.index(ans)
        option_letters = []
        for index in range(len(choice_set)):
            option_letters.append(num2char(index + 1))
        ans_letter = num2char(ans_index + 1)
        one_sample = {}
        one_sample['id'] = str(id + 1)
        id = id + 1
        one_sample['query'] = test_sample['final_question']
        one_sample['query_fol'] = test_sample['pos_condition']
        one_sample['max_dependency'] = test_sample['max_dependency']
        one_sample['average_dependency'] = test_sample['average_dependency']
        one_sample['largest_connected_component'] = test_sample['largest_connected_component']
        one_sample['width'] = test_sample['reasoning_width']
        one_sample['slots'] = test_sample['slots']
        one_sample['minterms'] = test_sample['minterms']
        one_sample['is_natural'] = test_sample['is_natural']
        one_sample['entropy_avg'] = [x['entropy_avg'] for x in choice_set]
        one_sample['entropy_overall'] = [x['entropy_overall'] for x in choice_set]
        one_sample['condition_templates'] = test_sample['condition_templates']

        for index, one_choice in enumerate(choice_set):
            one_choice_copy = copy.deepcopy(one_choice)
            del one_choice_copy['entropy_overall']
            del one_choice_copy['entropy_avg']
            del one_choice_copy['entropy_max']
            del one_choice_copy['LayoverLocations']
            del one_choice_copy['LayoverTimes']
            new_choice = {}
            for key, value in one_choice_copy.items():
                new_key = camel_case_split(key)
                if key == 'CarbonEmissionAvgDiff(%)':
                    if value is None or value == 'None':
                        new_choice[new_key] = '+0'
                        continue
                    if int(value) >= 0:
                        new_choice[new_key] = '+' + str(value)
                    else:
                        new_choice[new_key] = str(value)
                else:
                    new_choice[new_key] = str(value)

            one_sample['Option ' + num2char(index + 1)] = new_choice

        one_sample['Answer'] = ans_letter
        new_samples.append(one_sample)

    return new_samples


compositional_dataset = read_from_json(data_file)

cocoa_dataset = []
for test_sample in compositional_dataset:
    labels = test_sample['labels']
    flight_options = test_sample['flight_options']
    srt = sorted(zip(flight_options, labels), key=lambda k: k[0]['entropy_overall'], reverse=True)

    sorted_flight_options, sorted_labels = [x[0] for x in srt], [x[1] for x in srt]
    choice_sets = split_by_entropy(sorted_flight_options, sorted_labels)
    if choice_sets is None:
        continue
    samples = shuffle_and_simplify(test_sample, choice_sets, len(cocoa_dataset))
    cocoa_dataset.extend(samples)

random.shuffle(cocoa_dataset)
write_to_json(cocoa_dataset, cocoa_dataset_file)
