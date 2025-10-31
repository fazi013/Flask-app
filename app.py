from flask import Flask ,request ,jsonify
from config import URI,SQLALCHEMY_TRACK_MODIFICATIONS
from model import db, Product



app = Flask(__name__)

# db connection 
app.config['SQLALCHEMY_DATABASE_URI'] = URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# db initialize
db.init_app(app)

@app.route('/')
def home ():
    return('this is the environment setting ')

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

if __name__ == '__main__':
    app.run()
