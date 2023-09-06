"""Flask app for Cupcakes"""

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///desserts'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

@app.route('/')
def index_page():
    cupcakes=Cupcake.query.all()
    return render_template('index.html',cupcakes=cupcakes)

@app.route('/api/cupcakes')
#We need to serialize each cupcake in the all_cupcakes list
#To achieve this we can use a list comprehension
def list_cupcakes():
    all_cupcakes=[cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

#we will coerce the id to be an int
@app.route('/api/cupcakes/<int:id>')
def get_cupcake(id):
    cupcake=Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())


##ask mentor how I could test for image=none in insomnia
@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():  
    data = request.json

    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()

    # POST requests should return HTTP status of 201 CREATED
    return (jsonify(cupcake=cupcake.serialize()), 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    data = request.json

    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor=data['flavor'],
    cupcake.rating=data['rating'],
    cupcake.size=data['size'],
    cupcake.image=data['image'] 

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.serialize()), 200)

@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    cupcake=Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")





#Had issues with this route
# @app.route('/api/cupcakes/', methods=["POST"])
# def create_cupcake():
#     try:
#         # Validate input JSON
#         required_fields = ["flavor", "size", "rating", "image"]
#         if not all(field in request.json for field in required_fields):
#             return jsonify({"error": "Missing required fields"}), 400

#         new_cupcake = Cupcake(
#             flavor=request.json["flavor"],
#             size=request.json["size"],
#             rating=request.json["rating"],
#             image=request.json["image"] or None
#         )

#         db.session.add(new_cupcake)
#         db.session.commit()

#         response_data = {
#             "message": "Cupcake created successfully",
#             "cupcake": new_cupcake.serialize()
#         }

    #     return jsonify(response_data), 201
    # except Exception as e:
    #     db.session.rollback()  # Rollback changes in case of an exception
    #     return jsonify({"error": str(e)}), 500

# @app.route('/api/todos/<int:id>', methods=["PATCH"])
# def update_todo(id):
#     todo=Todo.query.get_or_404(id)
#     todo.title = request.json.get('title', todo.title)
#     todo.title = request.json.get('done', todo.done)
#     db.session.commit()
#     return jsonify(todo=todo.serialize())

# @app.route('/api/todos/<int:id>', methods=["DELETE"])
# def delete_todo(id):
#     todo=Todo.query.get_or_404(id)
#     db.session.delete(todo)
#     db.session.commit()
#     return jsonify(message="deleted")




