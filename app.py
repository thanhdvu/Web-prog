import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "vendor"))

from flask import Flask, render_template, request, redirect, url_for, flash  # thêm request, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_cors import CORS
from auth import auth_bp
from werkzeug.utils import secure_filename

from models import db, LostItem 

app = Flask(__name__, static_folder='static')
app.secret_key = 'yonsei_uni_140'
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yonsei.db'  # hoặc đường dẫn database bạn dùng
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

UPLOAD_FOLDER = 'static/uploads'  
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('ko/index_ko.html')

# Chinese page
@app.route('/ch')
def index_ch():
    return render_template('ch/index_ch.html')

@app.route('/ch/find')
def find_ch():
    return render_template('ch/find_ch.html')

@app.route('/ch/register')
def register_ch():
    return render_template('ch/register_ch.html')

# English page
@app.route('/en')
def index_en():
    return render_template('en/index_en.html')

@app.route('/en/find')
def find_en():
    return render_template('en/find_en.html')

@app.route('/en/register')
def register_en():
    return render_template('en/register_en.html')

# Korean page
@app.route('/ko')
def index_ko():
    return render_template('ko/index_ko.html')

@app.route('/ko/find')
def find_ko():
    return render_template('ko/find_ko.html')

@app.route('/ko/register', methods=['GET', 'POST'])
@login_required
def register_item():
    if request.method == 'POST':
        category = request.form['PRDT_CL_NM']
        date_found = request.form['START_YMD']
        item_name = request.form['PRDT_NM']
        building = request.form['uBuilding']

        file = request.files['itemImage']
        filename = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_item = LostItem(
            user_id=current_user.id,
            category=category,
            date_found=date_found,
            item_name=item_name,
            building_found=building,
            image_filename=filename 
        )
        db.session.add(new_item)
        db.session.commit()

        flash('등록이 완료되었습니다!', 'success')
        return redirect(url_for('index_ko'))

    return render_template('register.html')

@app.route('/ko/login')
def login_ko():
    return render_template('ko/auth/login_ko.html')

@app.route('/ko/signup')
def signup_ko():
    return render_template('ko/auth/signup_ko.html')

@app.route('/ko/map')
def map_ko():
    return render_template('ko/map_ko.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

