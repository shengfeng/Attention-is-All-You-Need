from keras import backend as K 
from keras.engine.topology import Layer
import numpy as np
from keras.preprocessing import sequence
from keras.layers import *
from keras import Model
from keras.callbacks import TensorBoard
from itertools import chain
from transformer import Attension, Position_Embedding
from keras.datasets import imdb


max_features = 20000
maxlen = 80
batch_size = 32

print('Loading data...')
(x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
print(len(x_train), 'train sequences')
print(len(x_test), 'test sequences')


print('Pad sequences (sample x time)')
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)


K.clear_session()
callbacks = [TensorBoard("log/")]
S_inputs = Input(shape=(None,), dtype='int32')
embeddings = Embedding(max_features, 128)(S_inputs)
embeddings = Position_Embedding()(embeddings)
O_seq = Attension(8, 16)([embeddings, embeddings, embeddings])
O_seq = GlobalAveragePooling1D()(O_seq)
O_seq = Dropout(0.5)(O_seq)
outputs = Dense(1, activation='sigmoid')(O_seq)

model = Model(inputs=S_inputs, outputs=outputs)
model.summary


model.compile(loss='binary_crossentropy', optimizer='adam',metrics=['accuracy'])
model.fit(x_train, y_train, validation_data=(x_test, y_test), 
        epochs=50, batch_size=batch_size, callbacks=callbacks)