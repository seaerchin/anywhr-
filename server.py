from flask import Flask, request, Response, jsonify
from werkzeug.exceptions import BadRequest
from flask_api import status
import hexagon as h 

app = Flask(__name__)

@app.route('/create', methods = ["POST"])
def create():
    """
    creates a hexagon with the specified name and registers it. any extra arguments are passed as keyword arguments to the constructor as its neighbours
    @param: json: {"name": str, "neighbours": list[list[int, str]]}
    @return: 200 with the name of the hexagon if successful; 500 otherwise. we do not want to cast the parameter to string because wrong types should cause an error in this case.
    """
    d = request.get_json()
    hexa = h.hexagon(**d)
    h.hexagons[d["name"]] = hexa
    return str(hexa), status.HTTP_200_OK

@app.route('/query', methods = ['GET'])
def query():
    """
    returns the neighbours of the specified hexagon 
    @param: url parameter of the name 
    @return: 200, list[tuple(int, str)]
    """
    name = request.args.get('name') 
    return str(h.hexagons[name].query()), status.HTTP_200_OK

# name of hexagon 
# neighbours as tuples
@app.route('/add', methods = ['POST'])
def insert():
    """
    adds the list of neighbours to the specified hexagon 
    @param: json: {"name": str, "neighbours": list[list[int, str]]}
    @return: 200, list[tuple(int, str)] representing the hexagon's neighbours
    """
    payload = request.get_json()
    hexa = h.hexagons[payload["name"]]
    for i in payload["neighbours"]:
        hexa.add_neighbour(i[0], h.hexagons[i[1]])
    return str(hexa.query()), status.HTTP_200_OK

@app.route('/remove', methods = ['GET'])
def remove():
    """
    removes the specified hexagon 
    @param: url parameter with the name of the specified hexagon 
    @return: 200, list[str] representing the rest of the hexagons if successful; 400 otherwise (also if the hexagon cannot be removed)
    """
    name = request.args.get('name')
    if h.remove(name):
        return jsonify(list(h.hexagons.keys())), status.HTTP_200_OK
    else:
        return status.HTTP_400_BAD_REQUEST

@app.route('/state', methods = ['GET'])
def state():
    """
    returns a list of all the existing nodes
    @return list[str] representing the list of hexagons.
    """ 
    return jsonify(list(h.hexagons.keys())), status.HTTP_200_OK
    
if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
