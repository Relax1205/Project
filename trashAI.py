import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import os

# Параметры модели
IMG_SIZE = 224  
BATCH_SIZE = 32
EPOCHS = 20  # Увеличено количество эпох
DATASET_PATH = "dataset-resized/"

# Улучшенная аугментация данных
datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    fill_mode="nearest",
    validation_split=0.2  # 20% данных на валидацию
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

# Проверяем количество классов
num_classes = train_data.num_classes
print(f"Обнаружено {num_classes} классов мусора.")

# Загружаем MobileNetV2 и размораживаем верхние 30 слоев
base_model = MobileNetV2(weights="imagenet", include_top=False, input_shape=(IMG_SIZE, IMG_SIZE, 3))
for layer in base_model.layers[:-30]:  # Замораживаем все, кроме верхних 30 слоев
    layer.trainable = False

# Создаем модель
model = Sequential([
    base_model,
    GlobalAveragePooling2D(),
    BatchNormalization(),  # Улучшает стабильность обучения
    Dense(256, activation="relu"),
    Dropout(0.4),  # Увеличен dropout для борьбы с переобучением
    Dense(num_classes, activation="softmax")
])

# Компиляция модели с AdamW и меньшим LR
model.compile(optimizer=keras.optimizers.AdamW(learning_rate=0.0003),
              loss="categorical_crossentropy",
              metrics=["accuracy"])

# Callbacks: динамическое уменьшение LR и остановка при отсутствии улучшений
callbacks = [
    ReduceLROnPlateau(monitor="val_loss", factor=0.5, patience=3, verbose=1, min_lr=1e-6),
    EarlyStopping(monitor="val_loss", patience=5, verbose=1, restore_best_weights=True)
]

# Обучение модели
model.fit(train_data, validation_data=val_data, epochs=EPOCHS, callbacks=callbacks)

# Сохранение модели
model.save("garbage_classifier.h5")
print("✅ Модель успешно обучена и сохранена!")
