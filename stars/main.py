import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

def load_images():
    files = Path("./").glob("*.npy")  
    return [np.load(str(path)).astype(int) for path in files]

images = load_images()

def get_neighbors(y, x):
    return [(y, x - 1), (y - 1, x)]

def validate_neighbors(B, neighbors):
    valid_neighbors = []
    for ny, nx in neighbors:
        if 0 <= ny < B.shape[0] and 0 <= nx < B.shape[1] and B[ny, nx] != 0:
            valid_neighbors.append((ny, nx))
    return valid_neighbors

def find_root(label, linked):
    while linked[label] != 0:
        label = linked[label]
    return label

def merge_labels(label1, label2, linked):
    root1 = find_root(label1, linked)
    root2 = find_root(label2, linked)
    if root1 != root2:
        linked[root2] = root1

def connected_components(B):
    labels = np.zeros_like(B, dtype=int)
    linked = np.zeros(B.size // 2 + 1, dtype=int)
    current_label = 1

    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if B[y, x] != 0:
                neighbors = validate_neighbors(B, get_neighbors(y, x))
                if not neighbors:
                    labels[y, x] = current_label
                    current_label += 1
                else:
                    min_label = min(labels[ny, nx] for ny, nx in neighbors)
                    labels[y, x] = min_label
                    for ny, nx in neighbors:
                        merge_labels(min_label, labels[ny, nx], linked)

    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if B[y, x] != 0:
                labels[y, x] = find_root(labels[y, x], linked)

    unique_labels = np.unique(labels)
    mapping = {old: new for new, old in enumerate(unique_labels)}
    for old, new in mapping.items():
        labels[labels == old] = new

    return labels

star_kernel = np.array([
    [1, 0, 0, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1]
])

cross_kernel = np.array([
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0]
])

def filter_objects(B):
    result = np.zeros_like(B)
    for y in range(2, B.shape[0] - 2):
        for x in range(2, B.shape[1] - 2):
            submatrix = B[y-2:y+3, x-2:x+3]
            if np.array_equal(submatrix, star_kernel) or np.array_equal(submatrix, cross_kernel):
                result[y, x] = 1
    return result

for image_index, image in enumerate(images):
    filtered_image = filter_objects(image)
    labeled_image = connected_components(filtered_image)
    object_count = np.amax(labeled_image)
    print(f"Количество объектов на изображении {image_index + 1}: {object_count}")
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image, cmap='gray')

    plt.subplot(1, 2, 2)
    plt.imshow(labeled_image, cmap='nipy_spectral')

    plt.show()

