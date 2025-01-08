from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F
import os
from tqdm import tqdm
import numpy as np

# Load the model and tokenizer
model_name = "openbmb/MiniCPM-Embedding"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
model = AutoModel.from_pretrained(model_name, trust_remote_code=True, attn_implementation="flash_attention_2", torch_dtype=torch.float16)

# Wrap the model with DataParallel if multiple GPUs are available
if torch.cuda.device_count() > 1:
    print(f"Using {torch.cuda.device_count()} GPUs")
    model = torch.nn.DataParallel(model)

model = model.to("cuda")

batch_size = 16  # Adjust this value based on your GPU memory

@torch.no_grad()
def get_embeddings(sentences, cache_file):
    if os.path.exists(cache_file):
        print(f"Loading embeddings from cache file: {cache_file}")
        return np.load(cache_file)

    embeddings = []
    for i in tqdm(range(0, len(sentences), batch_size), desc="Processing sentences"):
        batch_sentences = sentences[i:i + batch_size]
        batch_dict = tokenizer(batch_sentences, max_length=512, padding=True, truncation=True, return_tensors='pt', return_attention_mask=True).to("cuda")
        outputs = model(**batch_dict)
        batch_embeddings = F.normalize(outputs.last_hidden_state.mean(dim=1), p=2, dim=1).detach().cpu().numpy()
        embeddings.append(batch_embeddings)

    embeddings = np.vstack(embeddings)
    np.save(cache_file, embeddings)
    print(f"Embeddings saved to cache file: {cache_file}")
    return embeddings

import re

def extract_instances(file_path, tag):
    instances = []
    pattern = re.compile(f'<{tag}>(.*?)</{tag}>')
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in tqdm(file, desc=f"Extracting {tag} instances"):
            matches = pattern.findall(line)
            instances.extend(matches)
    return instances

def main():
    # File paths
    ch_file_path = '/path/to/chinese_corpus.txt'
    en_file_path = '/path/to/english_corpus.txt'
    cache_files = {
        'time': ('ch_time_embeddings.npy', 'en_time_embeddings.npy'),
        'place': ('ch_place_embeddings.npy', 'en_place_embeddings.npy'),
        'manner': ('ch_manner_embeddings.npy', 'en_manner_embeddings.npy'),
        'cause': ('ch_cause_embeddings.npy', 'en_cause_embeddings.npy'),
        'effect': ('ch_effect_embeddings.npy', 'en_effect_embeddings.npy'),
        'condition': ('ch_condition_embeddings.npy', 'en_condition_embeddings.npy'),
        'purpose': ('ch_purpose_embeddings.npy', 'en_purpose_embeddings.npy'),
        'concession': ('ch_concession_embeddings.npy', 'en_concession_embeddings.npy')
    }

    for block, (ch_cache_file, en_cache_file) in cache_files.items():
        # Extract instances
        instances_ch = extract_instances(ch_file_path, block)
        instances_en = extract_instances(en_file_path, block)

        # Get embeddings
        embeddings_ch = get_embeddings(instances_ch, ch_cache_file)
        embeddings_en = get_embeddings(instances_en, en_cache_file)

if __name__ == "__main__":
    main()