from flask import Flask, render_template,request
from wtforms import Form, TextAreaField, validators,IntegerField,StringField,FormField
from vectorizer import predict

app = Flask(__name__)


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
        name = type(name)
        #name = predict(d)
        return render_template('hello.html', name=name)
    return render_template('first_app.html', form=form)


if __name__ == '__main__':
	app.run(debug=True)


#d = [4,1,0,0,1,4,2,0,2,1,3]
    
    