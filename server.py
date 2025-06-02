from flask import Flask, render_template, request
import csv

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        data = request.form.to_dict()
        write_to_file(data)  # Save to database.csv
        return render_template('index.html', thank_you=True)
    return render_template('index.html', thank_you=False)

@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/components')
def components():
    return render_template('components.html')

def write_to_file(data):
    try:
        with open('database.csv', mode='a', newline='') as database:
            writer = csv.writer(database)
            writer.writerow([
                data.get("email", "N/A"),
                data.get("subject", "N/A"),
                data.get("message", "N/A")
            ])
    except Exception as e:
        print(f"Error writing to file: {e}")

if __name__ == '__main__':
    app.run(debug=True)
