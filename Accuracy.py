import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator


IMG_SIZE = 224
BATCH_SIZE = 32
DATASET_PATH = "dataset-resized/"
MODEL_PATH = "garbage_classifier.h5"

model = tf.keras.models.load_model(MODEL_PATH)

datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

loss, accuracy = model.evaluate(val_data)

print(f"✅ Точность модели: {accuracy * 100:.2f}%")
print(f"❌ Средняя ошибка (loss): {loss:.4f}")
