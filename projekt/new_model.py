import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
 
# Function to add noise to audio
def add_noise(audio, noise_factor=0.005):
    noise = np.random.randn(*audio.shape)  # Generate noise with the same shape as the audio
    augmented_audio = audio + noise_factor * noise
    return augmented_audio
 
# Augment the dataset by adding noise
def augment_audio_data(X):
    X_augmented = []
    for sample in X:
        augmented_sample = add_noise(sample)  # Add noise
        X_augmented.append(augmented_sample)
    return np.array(X_augmented)
 
# Load your data
X = np.load('X_mfcc_features.npy')
y = np.load('y_labels.npy')
 
# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)
 
# Standardize the MFCC features (mean=0, std=1)
X = X.reshape(-1, X.shape[2])  # Flatten for standardization
scaler = StandardScaler()
X = scaler.fit_transform(X)
X = X.reshape(-1, 100, 13)  # Reshape back after scaling
 
# Augment the audio data by adding noise
X_augmented = augment_audio_data(X)
 
# Combine original and augmented data
X_combined = np.concatenate((X, X_augmented), axis=0)
y_combined = np.concatenate((y_encoded, y_encoded), axis=0)  # Duplicate labels for augmented data
 
# Split the data into training, validation, and test sets
X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
 
# Build a 1D CNN model with L2 regularization
model = Sequential()
 
# Define the input shape using Input layer
model.add(Input(shape=(X_train.shape[1], X_train.shape[2])))
 
# First Conv1D layer with L2 regularization
model.add(Conv1D(64, kernel_size=3, activation='relu', kernel_regularizer=l2(0.001)))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(0.5))
 
# Second Conv1D layer with L2 regularization
model.add(Conv1D(128, kernel_size=3, activation='relu', kernel_regularizer=l2(0.001)))
model.add(MaxPooling1D(pool_size=2))
model.add(Flatten())
 
# Dense layer with L2 regularization
model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.001)))
model.add(Dropout(0.5))
 
# Output layer
model.add(Dense(len(np.unique(y_encoded)), activation='softmax'))
 
# Compile the model with a higher learning rate
model.compile(optimizer=Adam(learning_rate=0.0001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
 
# Add EarlyStopping callback with more patience
early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
 
# Train the model using the training and validation sets
history = model.fit(X_train, y_train, epochs=100, batch_size=64, validation_data=(X_val, y_val), callbacks=[early_stopping])
 
# Evaluate the model on the test set
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {test_accuracy:.4f}")

model.save(filepath="final_model.keras")