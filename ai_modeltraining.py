import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from kerastuner.tuners import RandomSearch

# Load the pre-trained VGG16 model without the top layer
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Freeze the base model
base_model.trainable = False

# Add custom top layers
x = Flatten()(base_model.output)
x = Dense(512, activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)  # Assuming binary classification

# Create the model
model = Model(inputs=base_model.input, outputs=x)

# Compile the model
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Data augmentation
train_datagen = ImageDataGenerator(
rescale=1./255,
rotation_range=40,
width_shift_range=0.2,
height_shift_range=0.2,
shear_range=0.2,
zoom_range=0.2,
horizontal_flip=True,
fill_mode='nearest'
)

train_generator = train_datagen.flow_from_directory(
'path/to/train/data',
target_size=(224, 224),
batch_size=32,
class_mode='binary'
)

# Hyperparameter tuning with Keras Tuner
def build_model(hp):
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
base_model.trainable = False
x = Flatten()(base_model.output)
x = Dense(hp.Int('units', min_value=128, max_value=512, step=32), activation='relu')(x)
x = Dense(1, activation='sigmoid')(x)
model = Model(inputs=base_model.input, outputs=x)
model.compile(optimizer=Adam(learning_rate=hp.Choice('learning_rate', values=[1e-2, 1e-3, 1e-4])),
loss='binary_crossentropy',
metrics=['accuracy'])
return model

tuner = RandomSearch(
build_model,
objective='val_accuracy',
max_trials=5,
executions_per_trial=3,
directory='my_dir',
project_name='kubu_hai_tuning'
)

tuner.search(train_generator, epochs=10, validation_data=validation_generator)

# Get the best model
best_model = tuner.get_best_models(num_models=1)[0]

# Unfreeze some layers of the base model for fine-tuning
for layer in base_model.layers[-4:]:
layer.trainable = True

# Recompile the model with a lower learning rate
best_model.compile(optimizer=Adam(learning_rate=1e-5), loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = best_model.fit(train_generator, epochs=10, validation_data=validation_generator)

# Save the model
best_model.save('kubu_hai_model.h5')
