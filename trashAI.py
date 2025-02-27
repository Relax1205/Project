import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os

# Параметры модели
IMG_SIZE = 224  # Размер входного изображения
BATCH_SIZE = 32
EPOCHS = 10
DATASET_PATH = "dataset-resized/"  # Путь к датасету

# Генератор данных (увеличивает обучающую выборку)
datagen = ImageDataGenerator(
    rescale=1./255,  # Нормализация
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    validation_split=0.2  # 20% данных отдадим под валидацию
)

# Загрузка данных
train_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATASET_PATH,
    target_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# Используем предобученную MobileNetV2
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))

# Замораживаем веса предобученной модели
base_model.trainable = False

# Создаем новую голову для классификации мусора
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    Dense(128, activation="relu"),
    Dropout(0.5),
    Dense(train_data.num_classes, activation="softmax")  # Количество классов
])

# Компиляция модели
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])

# Обучение модели
model.fit(train_data, validation_data=val_data, epochs=EPOCHS)

# Сохраняем модель
model.save("garbage_classifier_mobilenetv2.h5")

print("Модель успешно обучена и сохранена!")
