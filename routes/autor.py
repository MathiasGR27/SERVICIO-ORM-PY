from flask import Blueprint, request, jsonify
from models.autor import Autor
from repository.repositorio_autor import RepositorioAutor

autor_bp = Blueprint('autor', __name__, url_prefix='/autores')
repositorio = RepositorioAutor()

@autor_bp.route('/', methods=['GET'])
def obtener_autores():
    autores = repositorio.obtener_todos()
    return jsonify([autor.get_diccionario() for autor in autores]), 200

@autor_bp.route('/<int:id>', methods=['GET'])
def obtener_autor(id):
    autor = repositorio.obtener_por_id(id)

    if not autor:
        return jsonify({"error": "Autor no encontrado"}), 404

    return jsonify(autor.get_diccionario()), 200

@autor_bp.post("/")
def crear():
    datos = request.get_json()

    if not datos or not datos.get('nombre'):
        return jsonify({"error": "No se proporcionaron datos"}), 400
    
    nuevo_autor = Autor(
        nombre=datos['nombre'],
        pais=datos.get('pais')
    )

    repositorio.crear(nuevo_autor)
    
    return jsonify(nuevo_autor.get_diccionario()), 201

@autor_bp.route('/<int:id>', methods=['PUT'])
def actualizar(id):
    datos = request.get_json()

    if not datos:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    autor = repositorio.obtener_por_id(id)

    if not autor:
        return jsonify({"error": "Autor no encontrado"}), 404

    autor.nombre = datos.get('nombre', autor.nombre)
    autor.pais = datos.get('pais', autor.pais)

    repositorio.actualizar()

    return jsonify(autor.get_diccionario()), 200

@autor_bp.route('/<int:id>', methods=['DELETE'])
def eliminar(id):
    autor = repositorio.obtener_por_id(id)

    if not autor:
        return jsonify({"error": "Autor no encontrado"}), 404

    repositorio.eliminar(autor)

    return jsonify({"mensaje": "Autor eliminado correctamente"}), 200