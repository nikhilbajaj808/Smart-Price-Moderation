from flask import Flask, render_template, request, jsonify
from agents.price_agent import PriceAgent
from agents.moderation_agent import ModerationAgent

app = Flask(__name__, static_folder='static', template_folder='templates')
price_agent = PriceAgent()
mod_agent = ModerationAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/negotiate', methods=['POST'])
def negotiate():
    data = request.get_json() or request.form.to_dict()
    result = price_agent.suggest_price(data)
    result['input_asking_price'] = data.get('asking_price')
    return jsonify(result)

@app.route('/api/moderate', methods=['POST'])
def moderate():
    data = request.get_json() or request.form.to_dict()
    res = mod_agent.moderate(data)
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
