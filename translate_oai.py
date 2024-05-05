"""Script to use the OpenAI API to translate passwords from English to German. Used to build a starting dataset for the password translation task."""
from openai import OpenAI

client = OpenAI()

import argparse

SYSTEM_PROMPT = """Translate the following password list to German. RESPECT the original casing even when it is grammatically incorrect. Don't add spaces or separators between words if they are not in the original. Respond only with the translated words one per line, nothing else.
Words:
password
iloveyou
princess
rockyou
abc123
nicole
loveyou

Translations:
passwort
ichliebedich
prinzessin
rockdich
abc123
nicole
liebedich
"""

TRANSLATE_PROMPT = """Words:
<<INPUT>>

Translations:
"""

def translate_to_german(text):
    """Translate English text to German using the OpenAI API."""
    chat_response = client.chat.completions.create(model="gpt-4",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": TRANSLATE_PROMPT.replace("<<INPUT>>", text)}
    ])
    response = chat_response.choices[0].message.content
    if response[-1] != "\n":
        response += "\n"
    return response


def process_file(input_file_path, output_file_path):
    """Process the file in chunks and translate each chunk."""
    try:
        with open(input_file_path, 'r', encoding='latin1') as file:
            lines = file.readlines()

        translated_lines = []
        chunk_size = 10  # You can adjust the chunk size based on your needs

        # Process the file in chunks
        for i in range(0, len(lines), chunk_size):
            chunk = ''.join(lines[i:i+chunk_size])
            print("SENT", chunk)  # Debug print to trace what is sent for translation
            translated_chunk = translate_to_german(chunk)
            print("GOT", translated_chunk)  # Debug print to see the translation
            translated_lines.append(translated_chunk)

        # Write the translated text to another file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.writelines(translated_lines)

    except FileNotFoundError:
        print("The input file was not found.")


def main():
    parser = argparse.ArgumentParser(description="Translate text file content to German.")
    parser.add_argument("-i", "--input_file", required=True, help="Path to the input text file")
    parser.add_argument("-o", "--output_file", required=True, help="Path to the output text file where translated text will be saved")

    args = parser.parse_args()

    process_file(args.input_file, args.output_file)

if __name__ == "__main__":
    main()
