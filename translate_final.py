"""Translate a password dictionary using a finetuned model."""

from unsloth import FastLanguageModel
import torch
import argparse
import tqdm

max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = torch.float16 # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = True # Use 4bit quantization to reduce memory usage. Can be False.

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "unsloth/llama-3-8b-bnb-4bit",
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)

model = FastLanguageModel.get_peft_model(
    model,
    r = 16, # Choose any number > 0 ! Suggested 8, 16, 32, 64, 128
    target_modules = ["q_proj", "k_proj", "v_proj", "o_proj",
                      "gate_proj", "up_proj", "down_proj",],
    lora_alpha = 16,
    lora_dropout = 0, # Supports any, but = 0 is optimized
    bias = "none",    # Supports any, but = "none" is optimized
    # [NEW] "unsloth" uses 30% less VRAM, fits 2x larger batch sizes!
    use_gradient_checkpointing = "unsloth", # True or "unsloth" for very long context
    random_state = 3407,
    use_rslora = False,  # We support rank stabilized LoRA
    loftq_config = None, # And LoftQ
)

import re
def extract_response(text):
    # Define a regular expression to find the content after "### Response:"
    # Using non-greedy matching to stop at the first potential end-of-text token or excessive newlines
    match = re.search(r"### Response:\n(.*?)$", text, re.DOTALL)
    if match:
        response = match.group(1)
        response = response.replace("<|end_of_text|>", "")
        if response[-1] != "\n":
            response = response + "\n"
        return response
    else:
        raise "No response found in the text."

from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "lora_model", # YOUR MODEL YOU USED FOR TRAINING
    max_seq_length = max_seq_length,
    dtype = dtype,
    load_in_4bit = load_in_4bit,
)
FastLanguageModel.for_inference(model) # Enable native 2x faster inference
tokenizer.padding_side = "left"
alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:
{}

### Response:
{}"""

def process_batch(batch):
    inputs = []
    chunk_size = 10  # You can adjust the chunk size based on your needs
    for i in range(0, len(batch), chunk_size):
        chunk = ''.join(batch[i:i+chunk_size])
        inputs.append(alpaca_prompt.format(
                    "Translate this passwords while keeping the original format.", # instruction
                    chunk, # input
                    "", # output - leave this blank for generation!
                ))
    
    input_tokens = tokenizer(inputs, return_tensors = "pt", padding=True).to("cuda")
    outputs = model.generate(**input_tokens, max_new_tokens = 64, use_cache = True)
    return tokenizer.batch_decode(outputs).map(extract_response)

BATCH_SIZE = 1000

def process_file(infile, outfile):
    try:
        with open(infile, 'r', encoding='latin1') as file:
            lines = file.readlines()

        translated_lines = []
        
        # use tqdm for progress bar
        for i in tqdm(range(0, len(lines), BATCH_SIZE)):
            translated_batch = process_batch(lines[i:i+BATCH_SIZE])
            translated_lines.extend(translated_batch)

        # Write the translated text to another file
        with open(outfile, 'w', encoding='utf-8') as file:
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
