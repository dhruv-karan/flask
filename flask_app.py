from flask import Flask, render_template,request
from wtforms import Form, TextAreaField, validators,IntegerField,StringField,FormField
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
    if b>0.5:
        b= 'long live'
    else:
        b='short life'
    return b,model.predict([c])[0][0]*100

    




    
class HelloForm(Form):
    sayhello = TextAreaField('',[validators.DataRequired()])
    #country_code = IntegerField('Country Code', [validators.required()])
    #area_code    = IntegerField('Area Code/Exchange', [validators.required()])
    #number       = StringField('Number')
    #first_name   = StringField()
    #last_name    = StringField()
    #mobile_phone = FormField(TelephoneForm)
    #office_phone = FormField(TelephoneForm)
    



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
        name = [int(i) for i in name.strip()]
        if len(name)!=12:
        	name = 'Invalid Input'
        	return render_template('hello.html', name=name)
        else:
	        name,percent = predict(name)
	        return render_template('hello.html', name=name,percent = percent)
    return render_template('first_app.html', form=form)


if __name__ == '__main__':
	app.run(debug=True)


#d = [4,1,0,0,1,4,2,0,2,1,3]
    
    