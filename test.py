print("Python is working!")
print("Trying to import Flask...")
try:
    from flask import Flask
    print("Flask imported successfully!")
    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "Hello World! Flask is working!"
    
    if __name__ == '__main__':
        print("Starting Flask app on http://127.0.0.1:5000")
        app.run(host='127.0.0.1', port=5000, debug=True)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
