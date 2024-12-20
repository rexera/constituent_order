from transformers import AutoModel, AutoTokenizer
import torch
import torch.nn.functional as F
import os
from tqdm import tqdm
import numpy as np

# Load the new model and tokenizer
model_name = "openbmb/MiniCPM-Embedding"
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)  # Use the slow tokenizer
model = AutoModel.from_pretrained(model_name, trust_remote_code=True, attn_implementation="flash_attention_2",
                                  torch_dtype=torch.float16)

# Wrap the model with DataParallel
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
        batch_dict = tokenizer(batch_sentences, max_length=512, padding=True, truncation=True, return_tensors='pt',
                               return_attention_mask=True).to("cuda")
        outputs = model(**batch_dict)
        batch_embeddings = F.normalize(outputs.last_hidden_state.mean(dim=1), p=2, dim=1).detach().cpu().numpy()
        embeddings.append(batch_embeddings)

    embeddings = np.vstack(embeddings)
    np.save(cache_file, embeddings)
    print(f"Embeddings saved to cache file: {cache_file}")
    return embeddings


def get_sentences(file_path, mode='time', lines=None):
    sentences = []
    with open(file_path, 'r', encoding='utf-8') as file:
        if mode == 'time':
            if lines is None:
                raise ValueError("Lines must be provided when mode is 'time'")
            for i, line in enumerate(tqdm(file, desc="Reading sentences")):
                if i in lines:
                    sentence = ''.join([char for char in line if char not in '<>'])
                    sentences.append(sentence.strip())
        elif mode == 'all':
            for line in tqdm(file, desc="Reading sentences"):
                sentence = ''.join([char for char in line if char not in '<>'])
                sentences.append(sentence.strip())
        else:
            raise ValueError("Invalid mode. Use 'time' or 'all'.")
    return sentences


def main():
    # File paths
    ch_file_path = '/root/constituent_order/crude_anno/ch_annotated.txt'
    en_file_path = '/root/constituent_order/crude_anno/en_annotated.txt'
    ch_cache_file = 'ch_embeddings.npy'
    en_cache_file = 'en_embeddings.npy'
    ch_time_cache_file = 'ch_time_embeddings.npy'
    en_time_cache_file = 'en_time_embeddings.npy'

    # Line indices
    ch_lines = [205, 234, 328, 355, 651, 679, 861, 863, 865, 869, 871, 930, 1116, 1520, 1606, 1670, 1748]
    en_lines = [81, 172, 176, 184, 243, 266, 404, 406, 426, 440, 443, 457, 520, 529, 546, 659, 830, 871, 910, 918, 949,
                955, 972, 1011, 1028, 1043, 1094, 1111, 1153, 1165, 1184, 1191, 1209, 1249, 1250, 1285, 1342, 1377,
                1389, 1428, 1458, 1473, 1474, 1477, 1518, 1583, 1645, 1677, 1722, 1728, 1756, 1809, 1862, 1865, 1880,
                1905, 1909, 1983, 1987, 1997, 2000, 2060, 2168, 2321, 2381, 2390, 2417, 2510, 2604, 2623, 2649, 2663,
                2671, 2688, 2743, 2779, 2780, 2825, 2855, 2939, 2942]

    # Get sentences
    sentences_ch = get_sentences(ch_file_path, 'all', ch_lines)
    sentences_en = get_sentences(en_file_path, 'all', en_lines)

    # Get embeddings
    embeddings_ch = get_embeddings(sentences_ch, ch_cache_file)
    embeddings_en = get_embeddings(sentences_en, en_cache_file)

    # Get sentences
    sentences_ch_time = get_sentences(ch_file_path, 'time', ch_lines)
    sentences_en_time = get_sentences(en_file_path, 'time', en_lines)

    # Get embeddings
    embeddings_ch_time = get_embeddings(sentences_ch_time, ch_time_cache_file)
    embeddings_en_time = get_embeddings(sentences_en_time, en_time_cache_file)


if __name__ == "__main__":
    main()