import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Çevresel değişkeni kullanarak bot tokenini al
BOT_TOKEN = os.getenv('BOT_TOKEN')

@app.route('/api/check_invite', methods=['POST'])
def check_invite_availability():
    try:
        data = request.get_json()
        keyword = data.get('keyword')
        
        if not keyword:
            return jsonify({'result': 'Geçersiz anahtar kelime.'}), 400

        url = f"https://discord.com/api/v10/invites/{keyword}"
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 404:
            return jsonify({'result': f"https://discord.gg/{keyword} kullanılabilir!"})
        elif response.status_code == 200:
            return jsonify({'result': f"https://discord.gg/{keyword} zaten başka bir sunucu tarafından kullanılıyor."})
        else:
            return jsonify({'result': f"Bir hata oluştu: {response.status_code} - {response.text}"})
    except Exception as e:
        return jsonify({'result': f"Bir hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
