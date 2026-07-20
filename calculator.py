from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# ===== OOPS CLASS =====
class SmartCalculator:
    def __init__(self):
        self.history = []
    
    def evaluate(self, expression):
        try:
            allowed_chars = "0123456789.+-*/() "
            if not all(c in allowed_chars for c in expression):
                return "Error: Invalid Character"
            
            result = eval(expression)
            result = int(result) if result == int(result) else round(result, 8)
            self.history.append(f"{expression} = {result}")
            return result
            
        except ZeroDivisionError:
            return "Error: Division by Zero"
        except Exception:
            return "Error: Invalid Expression"
    
    def show_history(self):
        if not self.history:
            return ["No history yet"]
        return self.history[-5:]

calc = SmartCalculator()

# ===== HTML + CSS + JS =====
HTML_PAGE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Mobile Calculator</title>
    <style>
        body { font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; background: #222; }
        .calculator { background: #333; padding: 20px; border-radius: 20px; width: 320px; }
        #display { width: 100%; height: 60px; font-size: 32px; text-align: right; background: #000; color: #0f0; border: none; border-radius: 10px; padding: 10px; box-sizing: border-box; }
        .buttons { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-top: 10px; }
        button { height: 60px; font-size: 20px; border: none; border-radius: 10px; cursor: pointer; background: #555; color: white; }
        button:hover { background: #666; }
        .operator { background: #ff9500; }
        .equal { background: #ff9500; grid-column: span 2; }
        .clear { background: #a5a5a5; color: black; }
        #history { margin-top: 15px; color: #aaa; font-size: 12px; }
    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" value="0" readonly>
        <div class="buttons">
            <button class="clear" onclick="clearAll()">AC</button>
            <button class="clear" onclick="clearEntry()">C</button>
            <button class="operator" onclick="append('%')">%</button>
            <button class="operator" onclick="append('/')">/</button>
            <button onclick="append('7')">7</button><button onclick="append('8')">8</button><button onclick="append('9')">9</button><button class="operator" onclick="append('*')">*</button>
            <button onclick="append('4')">4</button><button onclick="append('5')">5</button><button onclick="append('6')">6</button><button class="operator" onclick="append('-')">-</button>
            <button onclick="append('1')">1</button><button onclick="append('2')">2</button><button onclick="append('3')">3</button><button class="operator" onclick="append('+')">+</button>
            <button onclick="append('0')">0</button><button onclick="append('.')">.</button><button class="equal" onclick="calculate()">=</button>
        </div>
        <div id="history"><b>History:</b><br></div>
    </div>
<script>
    let display = document.getElementById('display');
    function append(val) { if(display.value == "0" || display.value == "Error") display.value = ""; display.value += val; }
    function clearAll() { display.value = "0"; }
    function clearEntry() { display.value = display.value.slice(0, -1); if(display.value == "") display.value = "0"; }
    async function calculate() {
        let exp = display.value;
        let res = await fetch('/calculate', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({expression: exp}) });
        let data = await res.json(); display.value = data.result; updateHistory();
    }
    async function updateHistory() {
        let res = await fetch('/history'); let data = await res.json();
        document.getElementById('history').innerHTML = "<b>History:</b><br>" + data.history.join('<br>');
    }
    updateHistory();
</script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    result = calc.evaluate(data['expression'])
    return jsonify({'result': result})

@app.route('/history')
def history():
    return jsonify({'history': calc.show_history()})

if __name__ == '__main__':
    app.run(debug=True)
