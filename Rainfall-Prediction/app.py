import bz2
import pickle
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from sklearn.preprocessing import LabelEncoder
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(60), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

with app.app_context():
    db.create_all()

@app.route('/')
def newhome():
    return render_template('newhome.html')

@app.route('/register_rain', methods=['GET', 'POST'])
def register_rain():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', register_type='rain', error='Email already registered')
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_rain'))
    return render_template('register.html', register_type='rain')

@app.route('/register_crop', methods=['GET', 'POST'])
def register_crop():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            return render_template('register.html', register_type='crop', error='Email already registered')
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login_crop'))
    return render_template('register.html', register_type='crop')

@app.route('/login_rain', methods=['GET', 'POST'])
def login_rain():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/home')
        return render_template('login.html', login_type='rain', error='Invalid User')
    return render_template('login.html', login_type='rain')

@app.route('/login_crop', methods=['GET', 'POST'])
def login_crop():
    if request.method == 'POST':  # Corrected: Changed `]` to `)`
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/crop_index')
        return render_template('login.html', login_type='crop', error='Invalid User')
    return render_template('login.html', login_type='crop')

@app.route('/logout_rain')
def logout_rain():
    session.pop('email', None)
    return redirect(url_for('login_rain'))

@app.route('/logout_crop', methods=['POST'])
def logout_crop():
    session.pop('email', None)
    return redirect(url_for('login_crop'))

@app.before_request
def require_login():
    if request.endpoint == 'static':
        return

    allowed_routes = ['login_rain', 'login_crop', 'register_rain', 'register_crop', 'newhome', 'ground0', 'crop_home']
    login_route = 'login_rain'

    if request.endpoint and request.endpoint.startswith(('login_crop', 'crop_')):
        login_route = 'login_crop'

    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect(url_for(login_route))

@app.route('/rain_home')
def ground0():
    return render_template('ground0.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/konkan')
def konkan():
    return render_template('konkan.html')

@app.route('/konkan_prediction', methods=['POST'])
def konkan_prediction():
    model_path = "models/model1.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months'])
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)
    return 'Invalid request'

@app.route('/vidarbha')
def vidarbha():
    return render_template('vidarbha.html')

@app.route('/vidarbha_prediction', methods=['POST'])
def vidarbha_prediction():
    model_path = "models/model4.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months'])
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)
    return 'Invalid request'

@app.route('/marathwada')
def marathwada():
    return render_template('marathwada.html')

@app.route('/marathwada_prediction', methods=['POST'])
def marathwada_prediction():
    model_path = "models/model3.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months'])
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)
    return 'Invalid request'

@app.route('/madhya_maharashtra')
def madhya_maharashtra():
    return render_template('madhya_maharashtra.html')

@app.route('/madhya_maharashtra_prediction', methods=['POST'])
def madhya_maharashtra_prediction():
    model_path = "models/model2.pbz2"
    with bz2.BZ2File(model_path, 'rb') as f:
        model = pickle.load(f)
    if request.method == 'POST':
        num_periods = int(request.form['months'])
        start_date = datetime(datetime.now().year + 1, 1, 1)
        dates = [(start_date + relativedelta(months=i)).strftime('%B %Y') for i in range(num_periods)]
        predictions = model.predict(n_periods=num_periods)
        prediction_results = [{'Date': date, 'Rainfall': f"{prediction:.2f}"} for date, prediction in zip(dates, predictions)]
        return render_template('result.html', prediction_results=prediction_results)
    return 'Invalid request'

def decompress_pickle(file):
    with bz2.BZ2File(file, 'rb') as data:
        return pickle.load(data)

@app.route('/crop_home')
def crop_home():
    return render_template('crop_home.html')

@app.route('/crop_index')
def crop_index():
    return render_template('crop_index.html')

@app.route('/crop_parameters', methods=['POST'])
def crop_parameters():
    try:
        # Decompress and load the model
        model = decompress_pickle('models/XB.pbz2')
        
        # Retrieve form data
        N = float(request.form['N'])
        P = float(request.form['P'])
        K = float(request.form['K'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])
        
        # Load dataset and fit label encoder
        df = pd.read_csv("Dataset/Crop_recommendation.csv", encoding='utf-8')
        label_encoder = LabelEncoder()
        label_encoder.fit(df['label'])
        
        # Make prediction
        predicted_crop = model.predict([[N, P, K, temperature, humidity, ph, rainfall]])
        
        # Decode the prediction
        decoded_labels = label_encoder.inverse_transform(predicted_crop)
        predicted_crop=decoded_labels
        # Render the result template with prediction results
        return render_template('crop_result.html',crop= predicted_crop[0])
    
    except Exception as e:
        # Log and print any errors
        print(f"Error: {e}")
        return render_template('crop_result.html', crop="Error occurred during prediction")

    return 'Invalid request'

if __name__ == '__main__':
    app.run(debug=True)
