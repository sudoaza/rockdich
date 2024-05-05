"""Code to augment the translated/untranslated passwords and create a dataset for the password translation task."""

import pandas as pd
import random

N_SAMPLES = 10000

def mutate_password_pair(pair):
    # 20% of the times we will capitalize the first letter
    if random.random() < 0.2:
        pair = (pair[0].capitalize(), pair[1].capitalize())
    # 20% of the times we will add a number at the end
    if random.random() < 0.2:
        number = random.randint(0, 9)
        pair = (pair[0] + str(number), pair[1] + str(number))
    # 20% of the times we will add a symbol at the end
    if random.random() < 0.2:
        symbol = random.choice(['!', '@', '#', '$', '%', '&', '*'])
        pair = (pair[0] + symbol, pair[1] + symbol)
    # 20% of the tims we will replace a letter with a number
    if random.random() < 0.2:
        if "e" in pair[0]:
            letter = "e"
            number = "3"
        elif "E" in pair[0]:
            letter = "E"
            number = "3"
        elif "i" in pair[0]:
            letter = "i"
            number = "1"
        elif "I" in pair[0]:
            letter = "I"
            number = "1"
        elif "o" in pair[0]:
            letter = "o"
            number = "0"
        elif "O" in pair[0]:
            letter = "O"
            number = "0"
        elif "a" in pair[0]:
            letter = "a"
            number = "4"
        elif "A" in pair[0]:
            letter = "A"
            number = "4"
        elif "t" in pair[0]:
            letter = "t"
            number = "7"
        elif "T" in pair[0]:
            letter = "T"
            number = "7"
        else:
            return pair
        
        # replace only first occurrence
        pair = (pair[0].replace(letter, number, 1), pair[1].replace(letter, number, 1))
    return pair

def create_dataframes():
    # Read the files
    with open('original_train.txt', 'r', encoding='latin1') as file:
        original = file.readlines()
    with open('translated_train.txt', 'r', encoding='utf-8') as file:
        translated = file.readlines()
    with open('untranslated.txt', 'r', encoding='latin1') as file:
        untranslated = file.readlines()

    # Create a dataframe from original and translated lists
    df_translated = pd.DataFrame({
        'original': [line.strip() for line in original],
        'translated': [line.strip() for line in translated]
    })

    # List for untranslated
    untranslated_list = [line.strip() for line in untranslated]

    # Create an empty dataframe for instructions
    df_instructions = pd.DataFrame(columns=['instruction', 'input', 'output'])

    # Generate 100 instruction rows (arbitrary choice to generate a substantial sample)
    for _ in range(N_SAMPLES):
        # Randomly pick 8 translated pairs
        sampled_translated = df_translated.sample(8)
        original_samples = sampled_translated['original'].tolist()
        translated_samples = sampled_translated['translated'].tolist()

        # Randomly pick 2 untranslated passwords
        untranslated_samples = random.sample(untranslated_list, 2)

        # Combine and shuffle maintaining pairing
        total_input = original_samples + untranslated_samples
        total_output = translated_samples + untranslated_samples

        combined_list = list(zip(total_input, total_output))
        random.shuffle(combined_list)
        combined_list = [mutate_password_pair(pair) for pair in combined_list]
        shuffled_input, shuffled_output = zip(*combined_list)

        new_rows = {
            'instruction': 'Translate this passwords while keeping the original format.',
            'input': "\n".join(list(shuffled_input)),
            'output': "\n".join(list(shuffled_output))
        }
        df_instructions = df_instructions._append(new_rows, ignore_index=True)

    return df_instructions

# Generate the dataframe
df_instructions = create_dataframes()

# Output to check
print(df_instructions.head())

# Saving the new DataFrame to a CSV (optional)
df_instructions.to_csv('password_translation_instructions.csv', index=False)
