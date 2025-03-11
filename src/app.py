"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object

initial_members = [
    
    {
        "id": 1,
        "first_name": "John",
        "age": 33,
        "lucky_numbers": [7, 13, 22]
    },
    {
        "id": 2,
        "first_name": "Jane",
        "age": 35,
        "lucky_numbers": [10, 14, 3]
    },
    {
        "id": 3,
        "first_name": "Jimmy",
        "age": 5,
        "lucky_numbers": [1, 14, 78]
    }
]


for member in initial_members:
    jackson_family.add_member(member)


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


def sitemap():
    return generate_sitemap(app)


@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()

    if not members:
        return jsonify({"message": "we can't find the members"}), 404

    return jsonify(members), 200


@app.route('/member/<int:id>', methods=['GET'])
def get_member(id):
    member = jackson_family.get_member(id)

    if not member:
        return jsonify({"message": "we can't find the member"}), 404

    return jsonify(member), 200


@app.route('/member', methods=['POST'])
def new_member():

    the_new_member = request.json

    jackson_family.add_member(the_new_member)

    return jsonify({"message": "Member added successfully"}), 200


@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):

    success = jackson_family.delete_member(id)

    if not success:
        return jsonify({
            "message": "Member not found",
            "done": False
            }), 404

    return jsonify({
        "message": "Member deleted successfully",
        "done": True
        }), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
