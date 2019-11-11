from flask import Flask, render_template,request
from wtforms import Form, TextAreaField, validators,IntegerField,StringField,FormField
import sqlite3

# from vectorizer import predict

app = Flask(__name__)

from keras.models import load_model
model = load_model('my_model_weights.h5')

col_max = [3.0,10.0, 16.0, 8.0, 33.0, 8.0, 5.0, 5.0, 10.0, 2.0, 10.0, 6.0]

  

check = [(1.0,3.0),(0.0, 9.0),
 (1.0, 16.0),
 (0.0, 7.0),
 (0.0, 99.0),
 (0.0, 7.0),
 (0.0, 4.0),
 (0.0, 4.0),
 (0.0, 9.0),
 (1.0, 2.0),
 (0.0, 9.0),
 (1.0, 6.0)]



def en(d,col_max,check):
    first =1
    new = [0]*(int(sum(col_max)))
    index = 0
    i = 0
    while(index<=len(new) and i!=len(d)):
        if first == 1:
            new[int(index+int(d[i]))] = 1
            index = int(col_max[i])-1
            i +=1
            first = 0
        elif check[i][0] ==0:
            new[index+d[i]+1] = 1
            index = index + int(col_max[i])
            i+=1
        else:
            new[index+int(d[i])] = 1
            index = index + int(col_max[i])
            i+=1
    return new

import numpy as np
def predict(d):
    a = en(d,col_max,check)
    a.append(0)
    a.append(0)
    a.append(0)
    c = np.array(a)
    c = c.reshape(1,119)
    b =model.predict([c])
    binary =0
    if b>0.5:
        b= 'long live'
        binary =1
    else:
        b='short life'
    percent = model.predict([c])[0][0]*100
    if percent<50:
        percent = percent*2
    return b, round(percent,2),binary



    
def sqlite_entry(path, input, feedback,predict_percentage,mortality):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    c.execute('INSERT INTO review'\
            "(input,feedback,predict_percentage,mortality,date) VALUES "\
            "(?,?,?,?,DATETIME('now'))",(input,feedback,predict_percentage,mortality))
    conn.commit()
    conn.close()
class HelloForm(Form):
    sayhello = TextAreaField('',[validators.DataRequired()])




@app.route('/')
def index():
	form = HelloForm(request.form)
    
	return render_template('first_app.html', form=form)


@app.route('/hello', methods=['POST'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['sayhello']
        name = name.strip()
        nam = [int(i) for i in name.strip()]
        expectancy,percent,binary = predict(nam)

        return render_template('hello.html', expectancy=expectancy,percent = percent,inpu = name,binary=binary)
    return render_template('first_app.html', form=form)


@app.route('/thanks', methods=['POST'])
def feedback():
    feedback = request.form['feedback_button']
    review = request.form['review']
    prediction = request.form['prediction']
    y = request.form['y_object']

    inv_label = {'Incorrect': 0, 'Correct': 1}
    feedback = inv_label[feedback]

    # if feedback == 'Incorrect':
    #     y = int(not(y))
    # train(review, y)
    db= 'db.sqlite'
    sqlite_entry(db, review, feedback,prediction,y)
    return render_template('thanks.html',feedback=feedback,review=review,prediction=prediction,y=y)



if __name__ == '__main__':
	app.run(debug=True)


#d = [4,1,0,0,1,4,2,0,2,1,3]
    
    