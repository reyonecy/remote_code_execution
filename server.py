from flask import Flask, request, jsonify
import subprocess, tempfile, os

app = Flask(__name__)
SECRET = "mysecretkey123"

@app.route('/execute', methods=['POST'])
def execute():
    if request.headers.get('X-API-Key') != SECRET:
        return jsonify({'error': 'Unauthorized'}), 401

    code = request.json.get('code', '')
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False) as f:
        f.write(code)
        tmpfile = f.name

    result = subprocess.run(
        ['python3', tmpfile],
        capture_output=True, text=True, timeout=15
    )
    os.unlink(tmpfile)
    return jsonify({
        'stdout': result.stdout,
        'stderr': result.stderr,
        'returncode': result.returncode
    })

@app.route('/')
def health():
    return "Remote Python server is running! Testng for remote code execution by Reyone"

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
