﻿import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd  # For creating a result table

def read_data(filepath):
    data = np.loadtxt(filepath)
    return data

def plot_and_save_data(data, title, save_path):
    plt.figure(figsize=(10, 4))
    plt.plot(data[:, 0], label='X-axis')
    plt.plot(data[:, 1], label='Y-axis')
    plt.plot(data[:, 2], label='Z-axis')
    plt.title(title)
    plt.legend()
    plt.savefig(save_path)
    plt.close()

def calculate_rms(data):
    return np.sqrt(np.mean(data**2, axis=0))

def plot_and_save_3d_features(features, labels, save_folder):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    colors = ['b', 'g', 'r']
    for i, action_features in enumerate(features):
        xs = [f[0] for f in action_features]
        ys = [f[1] for f in action_features]
        zs = [f[2] for f in action_features]
        ax.scatter(xs, ys, zs, c=colors[i % len(colors)], label=labels[i])
    ax.set_xlabel('RMS Feature of X-axis')
    ax.set_ylabel('RMS Feature of Y-axis')
    ax.set_zlabel('RMS Feature of Z-axis')
    ax.legend()
    plt.title('3D Feature Plot')
    plt.savefig(os.path.join(save_folder, '3D_Features.png'))
    plt.close()

def classify_actions(train_features, train_labels, test_features):
    classifier = KNeighborsClassifier(n_neighbors=3)
    classifier.fit(train_features, train_labels)
    predictions = classifier.predict(test_features)
    return predictions

def create_result_table(test_files, predictions, action_names):
    # Assuming the order of test_files is the same as the order of test_features
    results = pd.DataFrame({
        'Sample #': [os.path.splitext(file)[0] for file in test_files],  # Extract the number part from the filename
        'Class': [f'Act0{label+1}: {action_names[label]}' for label in predictions]  # Modify label format to match provided table
    })
    results.sort_values(by='Sample #', inplace=True)  # Sort the results by sample number
    print(results)
    results.to_csv("classification_results.csv", index=False)

def main():
    base_path = 'C:/Users/HuiShan/Documents/HAPP/Assignment0'
    actions = ['act01', 'act02', 'act03']
    action_names = ['Walking', 'Sitting', 'Jogging']
    all_features = []

    for action_folder, action_name in zip(actions, action_names):
        action_path = os.path.join(base_path, action_folder)
        file_names = os.listdir(action_path)
        save_folder = os.path.join(base_path, action_folder + '_plots')
        os.makedirs(save_folder, exist_ok=True)

        action_features = []
        for file_name in file_names:
            file_path = os.path.join(action_path, file_name)
            data = read_data(file_path)
            rms = calculate_rms(data)
            action_features.append(rms)

            plot_title = f'{action_name} Sample {file_name.split(".")[0]}'
            save_path = os.path.join(save_folder, f'{file_name}.png')
            plot_and_save_data(data, plot_title, save_path)

        all_features.append(action_features)

    train_features = np.concatenate(all_features[:-1])
    train_labels = np.concatenate([[i] * len(features) for i, features in enumerate(all_features[:-1])])

    test_folder = os.path.join(base_path, 'test')
    test_files = os.listdir(test_folder)
    test_features = []

    for test_file in test_files:
        test_file_path = os.path.join(test_folder, test_file)
        test_data = read_data(test_file_path)
        test_rms = calculate_rms(test_data)
        test_features.append(test_rms)

    test_features = np.array(test_features)
    predictions = classify_actions(train_features, train_labels, test_features)

    # Generate a table of results
    create_result_table(test_files, predictions, action_names)

    # Plot and save the 3D features for all actions
    plot_and_save_3d_features(all_features, action_names, base_path)

if __name__ == '__main__':
    main()
