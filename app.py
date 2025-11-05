from flask import Flask, flash, redirect, render_template ,request ,jsonify,session
from config import URI
from model import db, User,DashboardData,AIResponse
from werkzeug.security import generate_password_hash, check_password_hash
import cohere



app = Flask(__name__)
app.secret_key = 'faisal_ki_secret_key'
# db connection 
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db initialize
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/sinup',methods=['GET','POST'])
def sinup():
    if request.method == 'POST':
        Username = request.form['username']
        Email = request.form['email']
        Password = request.form['password']
        hashed_password = generate_password_hash(Password)

        check_user= User.query.filter((User.username==Username)| (User.email==Email)).first()
        if check_user:
            flash('username or email already exist.')
            return redirect('/sinup')
        new_user= User(username=Username,password=hashed_password,email=Email)
        db.session.add(new_user)
        db.session.commit()
        flash('user regester succesfuly')
        return redirect('/login')
    return render_template('/sinup.html')
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST':
        Username=request.form['username']
        Password = request.form['password']

        check_user= User.query.filter(User.username==Username).first()
        if check_user and check_password_hash(check_user.password,Password) :
            session['user_id']=check_user.id
            session['username']=check_user.username
            return redirect('/dashboard')
        else:
            flash('Invalid username or password.')
            return redirect('/login')

    return render_template('login.html')

@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')
    user_id=session['user_id']
    if request.method=='POST':
        lan=request.form.get('language')
        dur=request.form.get('duration')
        defi = request.form.get('difficulty')
        existing = DashboardData.query.filter_by(user_id=user_id).first()

        if existing:
            flash('Your data already exists.')

            '''
            existing.language = lan
            existing.duration = dur
            existing.difficulty = defi
            '''
        else:
            new_entry = DashboardData(
                user_id=user_id,
                language=lan,
                duration=dur,
                difficulty=defi
            )
            db.session.add(new_entry)

        db.session.commit()
    return render_template('dashboard.html', username=session['username'])

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.')
    return redirect('/login')

@app.route('/showdata')
def showdata():
    if 'user_id' not in session:
        flash('Please login first.')
        return redirect('/login')
    user = db.session.get(User, session['user_id'])

    dashboard=user.dashboard
    ai_response=user.ai_response
    if not dashboard:
        flash('Please Enter data before reponse')
        return redirect('/dashboard')

    if dashboard and not ai_response:
        prompt = f"User wants to learn {dashboard.language} for {dashboard.duration} at {dashboard.difficulty} level. Suggest a learning path."
        
        co = cohere.Client('HegsLkYqWKHkZR6PzPdwpotqYrXAA187FvjO9xDN')
       
        response = co.chat(
            message=prompt,
            temperature=0.7,
            max_tokens=300
        )
        reply = response.text.strip()

        

        new_reply = AIResponse(user_id=user.id, response_text=reply)
        db.session.add(new_reply)
        db.session.commit()
        ai_response = new_reply


   
    return render_template('showdata.html', dashboard=dashboard, reply=ai_response.response_text)


    

if __name__ == '__main__':
    app.run()







'''
@app.route('/add',methods =['POST'])
def add_function():
    data = request.get_json()
    Name = data.get('name')
    Description = data.get ('description')
    Price = data.get('price')
    Quantity = data.get('quantity')

    new_product = Product(name=Name,description=Description,price=Price,quantity=Quantity)
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully'}), 201

@app.route("/get",methods=['GET'])
def get():
    get_products=Product.query.all()
    list_products=[]
    for p in get_products:
        list_products.append({'id':p.id,'description':p.description,'price':p.price,'quantity':p.quantity})
    return jsonify(list_products)

@app.route("/update/<int:id>",methods=['PUT'])
def update(id):
    data = request.get_json()
    get_id = Product.query.get(id)
    if not get_id:
        return jsonify({"message":"not record found"})


    get_id.description = data.get('description', get_id.description)
    get_id.name = data.get('name', get_id.name)
    get_id.price = data.get('price', get_id.price)
    get_id.quantity = data.get('quantity', get_id.quantity)
    db.session.add(get_id)
    db.session.commit()
    return jsonify({'message': 'Product update successfully'}), 201


@app.route("/delete/<int:id>",methods=['DELETE'])
def delete(id):

    get_id = Product.query.get(id)
    if not get_id:
        return jsonify({"message": "not record found"})
    db.session.delete(get_id)
    db.session.commit()
    return jsonify({"message":"product delete "})

   ''' 


