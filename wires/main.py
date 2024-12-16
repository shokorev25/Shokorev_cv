import numpy as np
from pathlib import Path

def load_images():
    files = Path("./").glob("*.npy")  
    return [np.load(str(path)).astype(int) for path in files]


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

def link_labels(label1, label2, linked):
    root1, root2 = find_root(label1, linked), find_root(label2, linked)
    if root1 != root2:
        linked[root2] = root1

def label_connected_components(B):
    labels = np.zeros_like(B, dtype=int)
    linked = np.zeros(B.size // 2 + 1, dtype=int)
    current_label = 1

    for y in range(B.shape[0]):
        for x in range(B.shape[1]):
            if B[y, x] != 0:
                neighbors = get_neighbors(y, x)
                valid_neighbors = validate_neighbors(B, neighbors)
                if not valid_neighbors:
                    label = current_label
                    current_label += 1
                else:
                    neighbor_labels = [labels[ny, nx] for ny, nx in valid_neighbors]
                    label = min(neighbor_labels)
                    for nl in neighbor_labels:
                        if nl != label:
                            link_labels(label, nl, linked)
                labels[y, x] = label

    for y in range(labels.shape[0]):
        for x in range(labels.shape[1]):
            if labels[y, x] != 0:
                labels[y, x] = find_root(labels[y, x], linked)

    unique_labels = np.unique(labels)[1:]
    for i, lbl in enumerate(unique_labels):
        labels[labels == lbl] = i + 1

    return labels

def thin_component(B, value):
    kernel = np.array([[value], [value], [value]])
    result = np.zeros_like(B, dtype=int)

    for y in range(1, B.shape[0] - 1):
        for x in range(B.shape[1]):
            if B[y, x] == value and np.all(B[y-1:y+2, x:x+1] == kernel):
                result[y, x] = value

    return result

def process_images(images):
    for image in images:
        connected_components = label_connected_components(image)
        cable_count = np.max(connected_components)

        for i in range(1, cable_count + 1):
            print(f"Кабель {i}:")
            thinned = thin_component(connected_components, i)
            parts_count = np.max(label_connected_components(thinned))

            if parts_count == 1:
                print("Кабель цел")
            elif parts_count == 0:
                print("Кабель разорван")
            else:
                print(f"Разорван на {parts_count} части(ей)")

        print("-" * 30)

images = load_images()
process_images(images)
