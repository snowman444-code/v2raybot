from flask import Flask, request, redirect
import requests

app = Flask(__name__)

MERCHANT_ID = 'b7e177ee-406a-11ea-90aa-000c295eb8fc'
CALLBACK_BASE = 'https://your-heroku-app.herokuapp.com/verify'

@app.route('/pay')
def pay():
    amount = int(request.args.get('amount', 10000))
    plan = request.args.get('plan', 'default')

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "callback_url": f"{CALLBACK_BASE}?plan={plan}&amount={amount}",
        "description": f"خرید پلن {plan}"
    }
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    res = requests.post("https://api.zarinpal.com/pg/v4/payment/request.json", json=data, headers=headers)
    response = res.json()

    if response['data']['code'] == 100:
        authority = response['data']['authority']
        return redirect(f"https://www.zarinpal.com/pg/StartPay/{authority}")
    else:
        return f"خطا در پرداخت: {response}"

@app.route('/verify')
def verify():
    status = request.args.get('Status')
    authority = request.args.get('Authority')
    plan = request.args.get('plan')
    amount = int(request.args.get('amount'))

    if status != 'OK':
        return 'پرداخت لغو شد.'

    data = {
        "merchant_id": MERCHANT_ID,
        "amount": amount,
        "authority": authority,
    }
    headers = {'accept': 'application/json', 'content-type': 'application/json'}
    res = requests.post("https://api.zarinpal.com/pg/v4/payment/verify.json", json=data, headers=headers)
    response = res.json()

    if response['data']['code'] == 100:
        return f"پرداخت موفق بود! پلن شما: {plan} — مبلغ: {amount}"
    else:
        return f"پرداخت ناموفق بود. کد: {response['data']['code']}"

if __name__ == '__main__':
    app.run()
