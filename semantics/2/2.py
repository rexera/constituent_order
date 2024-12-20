import os
import torch
from sklearn.manifold import TSNE
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt
import numpy as np

def load_embeddings(file_path):
    if os.path.exists(file_path):
        print(f"Loading embeddings from file: {file_path}")
        return np.load(file_path)
    else:
        raise FileNotFoundError(f"File not found: {file_path}")

def plot_embeddings(embeddings_ch, embeddings_en, title):
    tsne = TSNE(n_components=2, random_state=42)
    embeddings = np.vstack((embeddings_ch, embeddings_en))
    embeddings_2d = tsne.fit_transform(embeddings)

    plt.figure(figsize=(10, 10))
    plt.scatter(embeddings_2d[:len(embeddings_ch), 0], embeddings_2d[:len(embeddings_ch), 1], label='Chinese', alpha=0.5)
    plt.scatter(embeddings_2d[len(embeddings_ch):, 0], embeddings_2d[len(embeddings_ch):, 1], label='English', alpha=0.5)
    plt.legend()
    plt.title(f't-SNE of Sentence Embeddings - {title}')
    plt.show()

def calculate_distances(embeddings_ch, embeddings_en):
    center_ch = torch.tensor(np.mean(embeddings_ch, axis=0))
    center_en = torch.tensor(np.mean(embeddings_en, axis=0))

    euclidean_distance = torch.norm(center_ch - center_en).item()
    cosine_distance = cosine(center_ch.numpy(), center_en.numpy())

    return euclidean_distance, cosine_distance

def main():
    base_path = '/Users/mayiran/PycharmProjects/linguistics/semantics/2'
    categories = {
    'time': ('ch_time_embeddings.npy', 'en_time_embeddings.npy'),
    'place': ('ch_place_embeddings.npy', 'en_place_embeddings.npy'),
    'manner': ('ch_manner_embeddings.npy', 'en_manner_embeddings.npy'),
    'cause': ('ch_cause_embeddings.npy', 'en_cause_embeddings.npy'),
    'effect': ('ch_effect_embeddings.npy', 'en_effect_embeddings.npy'),
    'condition': ('ch_condition_embeddings.npy', 'en_condition_embeddings.npy'),
    'purpose': ('ch_purpose_embeddings.npy', 'en_purpose_embeddings.npy'),
    'concession': ('ch_concession_embeddings.npy', 'en_concession_embeddings.npy')
}

    for category, (ch_file_name, en_file_name) in categories.items():
        ch_file = os.path.join(base_path, ch_file_name)
        en_file = os.path.join(base_path, en_file_name)

        embeddings_ch = load_embeddings(ch_file)
        embeddings_en = load_embeddings(en_file)

        euclidean_distance, cosine_distance = calculate_distances(embeddings_ch, embeddings_en)
        print(f"Category: {category}")
        print(f"Euclidean Distance: {euclidean_distance}")
        print(f"Cosine Distance: {cosine_distance}")

        plot_embeddings(embeddings_ch, embeddings_en, category)

if __name__ == "__main__":
    main()