from flask import Flask, render_template, request, jsonify,redirect
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
    
    valid_currencies_response = requests.get('https://api.exchangerate.host/symbols')
    valid_currencies = valid_currencies_response.json()['symbols']
    if from_currency not in valid_currencies and to_currency not in  valid_currencies:
        return render_template("home.html" ,message1 = f"Not a valid code:{from_currency}",message2 = f"Not a valid code:{to_currency}")
    
    
    try:
        float(amount)
    except ValueError:
        return render_template("home.html", message3="Not a valid amount.")
    
    
    response = requests.get(f'https://api.exchangerate.host/convert?from={from_currency}&to={to_currency}&amount={amount}')
    data = response.json()
    if to_currency=="EUR":
        result = f"The result is €{data['result']}."
    else:
        result= f"The result is {data['result']} {to_currency}."
    return render_template("result.html", result=result)
        
    
if __name__ == '__main__':
    app.run(debug=True)

       

   

        
