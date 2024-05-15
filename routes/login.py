import logging
from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_pymongo import PyMongo
from functools import wraps
from pymongo import MongoClient
from bson.objectid import ObjectId
from wtforms import Form, StringField, PasswordField, validators

app = Flask(__name__)

# Configuration de la journalisation
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration de la clé secrète pour JWT
app.config['JWT_SECRET_KEY'] = 'Rassaye08@'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/mydatabase'  # Remplacez avec votre URI MongoDB
jwt = JWTManager(app)
mongo = PyMongo(app)

# Modèle utilisateur
class User:
    def __init__(self, username, password, role='user'):
        self.username = username
        self.password = password
        self.role = role

    @staticmethod
    def from_dict(user_dict):
        return User(user_dict['username'], user_dict['password'], user_dict.get('role', 'user'))

    def to_dict(self):
        return {'username': self.username, 'password': self.password, 'role': self.role}

    def save(self):
        users = mongo.db.users
        user_data = self.to_dict()
        result = users.insert_one(user_data)
        return result.inserted_id

    @staticmethod
    def find_by_username(username):
        users = mongo.db.users
        user_data = users.find_one({'username': username})
        if user_data:
            return User.from_dict(user_data)
        else:
            return None

    @staticmethod
    def find_by_id(user_id):
        users = mongo.db.users
        user_data = users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User.from_dict(user_data)
        else:
            return None

# Fonction de vérification des autorisations
def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            user = User.find_by_username(current_user)
            if not user or not user.role == required_role:
                abort(403)  # Interdit
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Formulaire de création d'utilisateur
class RegistrationForm(Form):
    username = StringField('Nom d\'utilisateur', [validators.Length(min=4, max=25)])
    password = PasswordField('Mot de passe', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Les mots de passe doivent correspondre'),
        validators.Length(min=8)
    ])
    confirm = PasswordField('Confirmer le mot de passe')

# Gestion des erreurs de validation
def handle_validation_error(err):
    messages = [message for field, message in err.errors.items()]
    return jsonify({"error": "Validation Error", "messages": messages}), 400

@app.errorhandler(422)
def handle_unprocessable_entity(err):
    messages = [message for message in err.data.get('messages').values()]
    return jsonify({"error": "Unprocessable Entity", "messages": messages}), 422

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not Found", "message": "La ressource demandée est introuvable"}), 404

@app.errorhandler(403)
def forbidden_error(error):
    return jsonify({"error": "Forbidden", "message": "Accès interdit"}), 403

@app.route('/admin', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_route():
    logging.info("Accès à la route admin.")
    return jsonify({'msg': 'Vous avez accès à la route admin.'}), 200

@app.route('/user', methods=['GET'])
@jwt_required()
@role_required('user')
def user_route():
    logging.info("Accès à la route utilisateur.")
    return jsonify({'msg': 'Vous avez accès à la route utilisateur.'}), 200

# Route pour l'enregistrement d'un utilisateur
@app.route('/register', methods=['POST'])
def register():
    form = RegistrationForm(request.json)
    if not form.validate():
        logging.error("Échec de validation lors de l'enregistrement d'un utilisateur.")
        return handle_validation_error(form)

    username = form.username.data
    password = form.password.data

    existing_user = User.find_by_username(username)
    if existing_user:
        logging.error("Nom d'utilisateur déjà utilisé lors de l'enregistrement d'un utilisateur.")
        return jsonify({"msg": "Nom d'utilisateur déjà utilisé"}), 400

    new_user = User(username, password)
    new_user.save()
    logging.info("Utilisateur enregistré avec succès.")
    return jsonify({"msg": "Utilisateur enregistré avec succès"}), 201

# Route pour l'authentification
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = User.find_by_username(username)
    if user and user.password == password:
        access_token = create_access_token(identity=username)
        logging.info("Connexion réussie.")
        return jsonify(access_token=access_token), 200
    else:
        logging.error("Échec de la connexion.")
        return jsonify({"msg": "Nom d'utilisateur ou mot de passe incorrect"}), 401

# Route protégée nécessitant un JWT valide
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Obtention de l'identité du JWT
    current_user = get_jwt_identity()
    logging.info("Accès à la route protégée.")
    return jsonify(logged_in_as=current_user), 200

if __name__ == '__main__':
    app.run(debug=True)
