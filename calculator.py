import os
from flask import Flask, render_template_string, request, jsonify
app = Flask(__name__)

class SmartCalculator:
    def __init__(self): self.history = []
    def evaluate(self, expression):
        try:
            result = eval(expression)
            result = int(result) if result == int(result) else round(result, 8)
            self.history.append(f"{expression} = {result}")
            return result
        except: return "Error"

calc = SmartCalculator()

HTML_PAGE = '''...tera wala HTML...''' # chota kar diya

@app.route('/')
def home(): return render_template_string(HTML_PAGE)
@app.route('/calculate', methods=['POST'])
def calculate(): 
    result = calc.evaluate(request.get_json()['expression'])
    return jsonify({'result': result})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)