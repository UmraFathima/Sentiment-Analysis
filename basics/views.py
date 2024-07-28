from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
def file(request):
    if(request.method=="POST"):
        data=request.POST
        
         #store all the val of txtboxs
        neo=data.get('neo')
        

        
        if('buttonflo' in request.POST):
            import os 
            import json
            import tensorflow
            from zipfile import ZipFile
            import pandas as pd
            from sklearn.model_selection import train_test_split
            from tensorflow.keras.models import Sequential
            from tensorflow.keras.layers import Dense, Embedding, LSTM
            from tensorflow.keras.preprocessing.text import Tokenizer
            from tensorflow.keras.preprocessing.sequence import pad_sequences
            data=pd.read_csv("C:\\Users\\umraf\\Downloads\\archive\\IMDB Dataset.csv")
            data.replace({"sentiment":{"positive": 1,"negative": 0}}, inplace=True)
            train_data, test_data =train_test_split(data, test_size=0.2,random_state=42)
            # print(train_data.shape)
            # print(test_data.shape)
            #tokenzing text data
            tokenizer = Tokenizer(num_words=5000)
            tokenizer.fit_on_texts(train_data["review"])
            X_train = pad_sequences(tokenizer.texts_to_sequences(train_data["review"]),maxlen=200)
            X_test = pad_sequences(tokenizer.texts_to_sequences(test_data["review"]),maxlen=200)
            Y_train=train_data["sentiment"]
            Y_test=test_data["sentiment"]
            # print(Y_train)
            # print(Y_test)
            model = Sequential()
            model.add(Embedding(input_dim=5000,output_dim=128,input_length=200))
            model.add(LSTM(128,dropout=0.2,recurrent_dropout=0.2))
            model.add(Dense(1,activation="sigmoid"))
            model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])
            model.fit(X_train,Y_train,epochs=5,batch_size=64,validation_split=0.2)
            loss,accuracy=model.evaluate(X_test,Y_test)
            print(f"Test Loss{loss}")
            print(f"Test accuracy{accuracy}")
            def predict_sentiment(review):
                sequence=tokenizer.texts_to_sequences([review])
                padded_sequence=pad_sequences(sequence,maxlen=200)
                prediction=model.predict(padded_sequence)
                sentiment="positive" if prediction[0][0]>0.5 else "negative"
                return sentiment
            # import numpy as np
            # newip=np.array([[neo]])
            # newip=sc.transform(newip)
            # res=model.predict(newip)
            res=predict_sentiment(neo)
            if res=="positive":
                result="Is positive Sentiment"
            else:
                result="Is negative Sentiment"

            # print(f"The sentiment of the review is {result}")
            return render(request,"file.html",context={'result':result})
    return render(request,'file.html')

# dt(res)
