
import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input, Concatenate, Dropout
from tensorflow.keras.models import Model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

# --- Configuration ---
DATASET_DIR = "dataset_ring"
CSV_FILE = os.path.join(DATASET_DIR, "data_with_images.csv")
MODEL_SAVE_PATH = "gold_diamond_estimator.h5"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 15  # Adjust as needed

def clean_weight(val):
    if isinstance(val, str):
        val = val.lower().replace(" g", "").replace(" ct", "").replace("carat", "").strip()
        try:
            return float(val)
        except ValueError:
            return None
    return val

def load_data():
    print(f"Loading data from {CSV_FILE}...")
    try:
        df = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        print("CSV file not found. Please run prepare_csv.py first.")
        return None, None, None

    # Filter rows with local images
    if 'LocalImage' not in df.columns:
        print("LocalImage column missing. Run prepare_csv.py.")
        return None, None, None
        
    df = df.dropna(subset=['LocalImage', 'Gold Weight', 'Diamond Weight'])
    
    # Process weights
    df['GoldWeight'] = df['Gold Weight'].apply(clean_weight)
    df['DiamondWeight'] = df['Diamond Weight'].apply(clean_weight)
    
    df = df.dropna(subset=['GoldWeight', 'DiamondWeight'])
    
    print(f"Training on {len(df)} samples.")
    return df

def preprocess_images(df):
    images = []
    valid_indices = []
    
    print("Loading images...")
    for idx, row in df.iterrows():
        img_path = os.path.join(DATASET_DIR, row['LocalImage'])
        if os.path.exists(img_path):
            try:
                img = load_img(img_path, target_size=IMG_SIZE)
                img_array = img_to_array(img)
                img_array = img_array / 255.0
                images.append(img_array)
                valid_indices.append(idx)
            except Exception as e:
                pass
        else:
            pass # Should verify in prepare_csv but good to be safe
            
    return np.array(images), df.loc[valid_indices].reset_index(drop=True)

def build_model(num_purity_features):
    # Image Branch
    input_img = Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3), name="image_input")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_tensor=input_img)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(128, activation='relu')(x)
    
    # Purity Branch
    input_purity = Input(shape=(num_purity_features,), name="purity_input")
    y = Dense(32, activation='relu')(input_purity)
    
    # Fusion
    combined = Concatenate()([x, y])
    z = Dense(64, activation='relu')(combined)
    z = Dropout(0.2)(z)
    
    # Output: 2 regression values (Gold Weight, Diamond Weight)
    # Using 'linear' activation for regression. 
    # Can use 'relu' if we are sure outputs are always positive, 
    # but linear is safer for general regression to avoid dying relu at 0 if normalization is off.
    output = Dense(2, activation='linear', name="output")(z)
    
    model = Model(inputs=[input_img, input_purity], outputs=output)
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def main():
    df = load_data()
    if df is None: return

    # Preprocess Images
    X_images, df_clean = preprocess_images(df)
    
    if len(df_clean) == 0:
        print("No valid images found.")
        return

    # Preprocess Tabular (Purity)
    # Extract just the K value e.g. "14K", "18K", "9K" if possible, or use raw string
    # Current Purity column seems to have values like "18 KT / Rose Gold / 10" or just "14K"
    # A simple approach is to use the 'Purity' column if it exists and clean it
    
    # Let's check 'Purity' column. If 'Purity' doesn't exist, try to parse 'Variant Title' or 'Body HTML'
    # Based on csv inspection, there is a 'Purity' column
    
    purity_encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    X_purity = purity_encoder.fit_transform(df_clean[['Purity']].astype(str))
    
    # Targets
    y = df_clean[['GoldWeight', 'DiamondWeight']].values
    
    # Split
    X_img_train, X_img_val, X_tab_train, X_tab_val, y_train, y_val = train_test_split(
        X_images, X_purity, y, test_size=0.2, random_state=42
    )
    
    print(f"Train shapes: Img {X_img_train.shape}, Tab {X_tab_train.shape}, Y {y_train.shape}")
    print(f"Val shapes: Img {X_img_val.shape}, Tab {X_tab_val.shape}, Y {y_val.shape}")
    
    # Build Model
    model = build_model(num_purity_features=X_tab_train.shape[1])
    
    # Train
    print("Starting training...")
    history = model.fit(
        [X_img_train, X_tab_train], y_train,
        validation_data=([X_img_val, X_tab_val], y_val),
        epochs=EPOCHS,
        batch_size=BATCH_SIZE
    )
    
    # Save
    model.save(MODEL_SAVE_PATH)
    print(f"Model saved to {MODEL_SAVE_PATH}")
    
    # Evaluate
    loss, mae = model.evaluate([X_img_val, X_tab_val], y_val)
    print(f"Validation MAE: {mae}")

if __name__ == "__main__":
    main()
