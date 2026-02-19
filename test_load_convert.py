import tensorflow as tf
import os

print(f"TF Version: {tf.__version__}")
try:
    import keras
    print(f"Keras Version: {keras.__version__}")
except:
    pass

model_path = "backend/gold_diamond_estimation_model.h5"
ring_model_path = "backend/gold_diamond_estimator.h5"

try:
    print(f"Loading {model_path}...")
    model = tf.keras.models.load_model(model_path, compile=False)
    print("Success. Saving as .keras...")
    model.save("gold_diamond_estimation_model.keras")
    print("Saved .keras version.")
except Exception as e:
    print(f"Failed to load {model_path}: {e}")

try:
    print(f"Loading {ring_model_path}...")
    model2 = tf.keras.models.load_model(ring_model_path, compile=False)
    print("Success. Saving as .keras...")
    model2.save("gold_diamond_estimator.keras")
    print("Saved .keras version.")
except Exception as e:
    print(f"Failed to load {ring_model_path}: {e}")
