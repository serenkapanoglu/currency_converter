from flask import Flask, render_template, request, jsonify,redirect,flash
import requests

app = Flask(__name__)

@app.route('/')
def home():
    
    return render_template('home.html')

@app.route('/convert', methods=['POST'])
def convert():
    from_currency = request.form['from_currency']
    to_currency = request.form['to_currency']
    amount = request.form['amount']
    message1 = ''
    message2 = ''
    message3 = ''
    
    try:
        float(amount)
    except ValueError:
        message3 = "Not a valid amount."
    valid_currencies_response = requests.get('https://api.exchangerate.host/symbols')
    valid_currencies = valid_currencies_response.json()['symbols']
    
    if from_currency not in valid_currencies:
        message1 = f"Not a valid code:{from_currency}"
        
    if to_currency not in valid_currencies:
        message2 = f"Not a valid code:{to_currency}"
        
    if message1 or message2 or message3:
        return render_template("home.html", message1=message1, message2=message2, message3=message3)
    
    
    response = requests.get(f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}')
    data = response.json()
    if to_currency=="EUR":
        result = f"The result is €{str(round(data['result'],2))}."
    else:
        result= f"The result is {str(round(data['result'],2))} {to_currency}."
    return render_template("result.html", result=result)
        
    
if __name__ == '__main__':
    app.run(debug=True)

       

   

        
