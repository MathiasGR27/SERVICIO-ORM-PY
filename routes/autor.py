from flask import Blueprint, request, jsonify
from models.autor import Autor
from repository.repositorio_autor import RepositorioAutor

autor_bp = Blueprint('autor', __name__, url_prefix='/autores')
repositorio = RepositorioAutor()

@autor_bp.route('/', methods=['GET'])
def obtener_autores():
    autores = repositorio.obtener_todos()
    return jsonify([autor.get_diccionario() for autor in autores]), 200

@autor_bp.post("/")
def crear():
    datos = request.get_json()
    if not datos or not datos.get('nombre'):
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    nuevo_autor = Autor(nombre=datos['nombre'])
    repositorio.crear(nuevo_autor)
    
    return jsonify(nuevo_autor.get_diccionario()), 200