import os
import requests
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

def generate_similar_keywords(keyword):
    # List of base keywords to choose from
    base_keywords = [
        "hub", "center", "tutorial", "zone", "world", "community", "space", "group", "network",
        "info", "guide", "help", "base", "portal", "room", "center", "base", "place", "network",
        "club", "team", "crew", "guild", "society", "association", "forum", "link", "event", "meetup",
        "studio", "lab", "project", "service", "support", "chat", "connect", "resource", "info", "node",
        "line", "station", "showcase", "exchange", "market", "zone", "site", "land", "area", "region",
        "domain", "field", "hub", "square", "spot", "corner", "base", "nation", "country", "city"
    ]
    
    # Select a random base keyword
    random_base = random.choice(base_keywords)
    
    # Generate similar keywords by appending the random base keyword to the original keyword
    similar_keywords = [f"{keyword}{random_base}"]
    return similar_keywords


def find_available_invite(keywords):
    for keyword in keywords:
        url = f"https://discord.com/api/v10/invites/{keyword}"
        headers = {
            "Authorization": f"Bot {BOT_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            return f"https://discord.gg/{keyword}"
    return None

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
            result = f'<span style="color: green;">https://discord.gg/{keyword} kullanılabilir.</span>'
            return render_template_string(result)
        elif response.status_code == 200:
            similar_keywords = generate_similar_keywords(keyword)
            available_invite = find_available_invite(similar_keywords)
            if available_invite:
                result = f'<span style="color: red;">https://discord.gg/{keyword} zaten başka bir sunucu tarafından kullanılıyor.</span> Alternatif: {available_invite}'
            else:
                result = f'<span style="color: red;">https://discord.gg/{keyword} zaten başka bir sunucu tarafından kullanılıyor, ancak uygun bir alternatif bulunamadı.</span>'
            return render_template_string(result)
        else:
            result = f'<span style="color: red;">Bir hata oluştu: {response.status_code} - {response.text}</span>'
            return render_template_string(result)
    except Exception as e:
        result = f'<span style="color: red;">Bir hata oluştu: {str(e)}</span>'
        return render_template_string(result), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
