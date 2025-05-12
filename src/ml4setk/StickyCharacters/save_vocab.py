from transformers import AutoTokenizer
import os
import argparse

def save_vocab_to_file(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    vocab = tokenizer.get_vocab()
    filename = model_name.replace('/', '_') + '_vocab.txt'
    sorted_vocab = sorted(vocab.items(), key=lambda x: x[1])
    with open(filename, 'w', encoding='utf-8') as f:
        for token, token_id in sorted_vocab:
            f.write(f"{token}\t{token_id}\n")
    
    print(f"Vocabulary has been saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Save model vocabulary to a text file')
    parser.add_argument('--model_name', type=str, default="bigcode/starcoder2-3b",
                      help='Name of the model to get vocabulary from (default: codellama/CodeLLaMA-7b-hf)')
    
    args = parser.parse_args()
    save_vocab_to_file(args.model_name) 