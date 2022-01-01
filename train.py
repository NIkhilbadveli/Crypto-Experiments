from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
import numpy as np
from tensorflow import keras

df = pd.read_csv('input_data.csv')

x_arr = np.array(
    [np.fromstring(df['x'][i].replace('[', '').replace(']', ''), sep=' ', dtype=np.float32) for i in
     range(len(df['x']))])

y_arr = np.array(
    [np.fromstring(df['y'][i].replace('[', '').replace(']', ''), sep=' ', dtype=np.float32) for i in
     range(len(df['y']))])

spl = 0.8
N = len(x_arr)
sample = int(spl * N)

x_train, x_test, y_train, y_test = x_arr[:sample, :], x_arr[sample:, :], y_arr[:sample, ], y_arr[sample:, ]

model = Sequential()
model.add(Dense(1000, input_dim=152 * 4, activation='relu'))
model.add(Dense(2000, activation='relu'))
model.add(Dense(32, activation='softmax'))

model.summary()

# Loss function (crossentropy) and Optimizer (Adadelta)
model.compile(loss=keras.losses.BinaryCrossentropy(from_logits=True),
              optimizer=keras.optimizers.SGD(learning_rate=0.5),
              metrics=['accuracy', keras.metrics.BinaryAccuracy(threshold=.03)])

model.fit(x_train, y_train, epochs=10, batch_size=100)


# print('\nEvaluating model now...')
# scores = model.evaluate(x_test, y_test)
# print(scores)

def save_model():
    # serialize model to JSON
    model_json = model.to_json()
    with open("model.json", "w") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights("model.h5")
    print("Saved model to disk")


save_model()

# print('\n')
# column_names = ['y_raw', 'y_pred', 'y_actual', 'num']
# out_df = pd.DataFrame(columns=column_names)
# # print(x_test[10].reshape(1, 608).shape)
# threshold = 0.03  # can I dynamically set threshold?
# count = 0
# for i in range(int(len(x_test) / 10)):
#     print('Testing... ' + str(i))
#     y_raw = model.predict(x_test[i].reshape(1, 608))
#     y_pred = np.where(y_raw > threshold, 1, 0)
#     y_actual = y_test[i].astype(np.int32)
#     y_pred = y_pred[0]
#     num = (y_pred == y_actual).sum()
#     out_df = out_df.append(pd.Series([y_raw, y_pred, y_actual, num], index=column_names),
#                            ignore_index=True)
#     if np.array_equal(y_pred, y_actual):
#         count += 1
#
# print('total number of tests:- ' + str(len(x_test)))
# print(count)

# out_df.to_csv('results.csv')
