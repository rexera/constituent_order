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

def plot_embeddings(embeddings_ch, embeddings_en):
    tsne = TSNE(n_components=2, random_state=42)
    embeddings = np.vstack((embeddings_ch, embeddings_en))
    embeddings_2d = tsne.fit_transform(embeddings)

    plt.figure(figsize=(10, 10))
    plt.scatter(embeddings_2d[:len(embeddings_ch), 0], embeddings_2d[:len(embeddings_ch), 1], label='Chinese', alpha=0.5)
    plt.scatter(embeddings_2d[len(embeddings_ch):, 0], embeddings_2d[len(embeddings_ch):, 1], label='English', alpha=0.5)
    plt.legend()
    plt.title('t-SNE of Sentence Embeddings')
    plt.show()

def main():
    # File paths
    ch_cache_file = '/Users/mayiran/PycharmProjects/linguistics/semantics/1/ch_embeddings.npy'
    en_cache_file = '/Users/mayiran/PycharmProjects/linguistics/semantics/1/en_embeddings.npy'
    ch_time_cache_file = '/Users/mayiran/PycharmProjects/linguistics/semantics/1/ch_time_embeddings.npy'
    en_time_cache_file = '/Users/mayiran/PycharmProjects/linguistics/semantics/1/en_time_embeddings.npy'

    # Load embeddings
    embeddings_ch = load_embeddings(ch_cache_file)
    embeddings_en = load_embeddings(en_cache_file)

    # Calculate center vectors
    center_ch = torch.tensor(np.mean(embeddings_ch, axis=0))
    center_en = torch.tensor(np.mean(embeddings_en, axis=0))

    # Calculate Euclidean distance between center vectors
    center_distance = torch.norm(center_ch - center_en)
    print("Euclidean Distance (Entirety):")
    print(center_distance.item())

    # Calculate cosine distance between center vectors
    cosine_distance = cosine(center_ch.numpy(), center_en.numpy())
    print("Cosine Distance (Entirety):")
    print(cosine_distance)

    # Load time-specific embeddings
    embeddings_ch_time = load_embeddings(ch_time_cache_file)
    embeddings_en_time = load_embeddings(en_time_cache_file)

    # Calculate center vectors
    center_ch_time = torch.tensor(np.mean(embeddings_ch_time, axis=0))
    center_en_time = torch.tensor(np.mean(embeddings_en_time, axis=0))

    # Calculate Euclidean distance between center vectors
    center_distance_time = torch.norm(center_ch_time - center_en_time)
    print("Euclidean Distance (<time>):")
    print(center_distance_time.item())

    # Calculate cosine distance between center vectors
    cosine_distance_time = cosine(center_ch_time.numpy(), center_en_time.numpy())
    print("Cosine Distance (<time>):")
    print(cosine_distance_time)

    # Plot embeddings
    plot_embeddings(embeddings_ch, embeddings_en)
    plot_embeddings(embeddings_ch_time, embeddings_en_time)

if __name__ == "__main__":
    main()