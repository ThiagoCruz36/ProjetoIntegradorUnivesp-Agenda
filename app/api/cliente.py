"""Cliente"""
from flask import jsonify, request
from app import db
from app.api import bp
import uuid
from app.models import Cliente


@bp.route('/clientes', methods=['GET'])
def get_clientes():
    """
    @api {get} /clientes
    Retorna os dados de todos os clientes
    @apiName get_clientes
    @apiGroup Cliente

    @apiSuccessExample {json} Dados dos clientes
        HTTP/1.1 200 OK
        {
            "ddd": "16",
            "email": "thiagoaugustocruz@gmail.com",
            "id_cliente": "123",
            "nome": "Thiago",
            "observacao": "Teste",
            "telefone": "981865343"
        }

    @apiError 404 O id_cliente não foi encontrado
    """

    clientes = Cliente.query.order_by(Cliente.nome)

    return jsonify([cliente.to_dict() for cliente in clientes])


@bp.route('/cliente/<string:id_cliente>', methods=['GET'])
def get_cliente(id_cliente):
    """
    @api {get} /cliente/:id_cliente
    Retorna os dados de um cliente
    @apiName get_cliente
    @apiGroup Cliente

    @apiParam {String} id_cliente ID do cliente

    @apiSuccessExample {json} Dados do cliente
        HTTP/1.1 200 OK
        {
            "ddd": "16",
            "email": "thiagoaugustocruz@gmail.com",
            "id_cliente": "123",
            "nome": "Thiago",
            "observacao": "Teste",
            "telefone": "981865343"
        }

    @apiError 404 O id_cliente não foi encontrado
    """

    cliente = Cliente.query.filter(Cliente.id_cliente == id_cliente).first_or_404()

    return jsonify(cliente.to_dict())


@bp.route('/clientes', methods=['POST'])
def create_cliente():
    """
    @api {post} /clientes
    Cadastra um novo cliente
    @apiName create_cliente
    @apiGroup Cliente

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X POST http://localhost:5000/api/clientes \
         -d '{}'

    @apiSuccessExample {json} Cliente cadastrado
        HTTP/1.1 201 Created
        {}

    """

    data = request.get_json() or {}

    obrigatorios = ['nome', 'ddd', 'telefone']
    ausentes = [campo for campo in obrigatorios if campo not in data]
    if len(ausentes) > 0:
        return("Campos obrigatórios não informados")

    cliente = Cliente()
    cliente.from_dict(data)
    cliente.id_cliente = uuid.uuid4().hex

    db.session.add(cliente)
    db.session.commit()

    return jsonify({'Sucesso': cliente.to_dict()}), 201


@bp.route('/clientes/<string:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    """
    @api {put} /clientes/:id_cliente
    Atualiza dados de um cliente
    @apiName update_cliente
    @apiGroup Cliente

    @apiParam {String} id_cliente ID do cliente

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X PUT http://localhost:5000/api/clientes/:id_cliente \
         -d '{
                "observacao": "Realizada alteração de dados do cliente"
            }'

    @apiSuccessExample {json} Cliente atualizado
        HTTP/1.1 200 OK
        {
        }

    @apiError 404 O id_cliente não foi encontrado
    """

    data = request.get_json() or {}

    cliente = Cliente.query.get_or_404(id_cliente)

    cliente.from_dict(data)
    db.session.add(cliente)
    db.session.commit()

    return jsonify({'Sucesso': cliente.to_dict()}), 200


@bp.route('/clientes/<string:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    """
    @api {delete} /clientes/:id_cliente
    Apaga o registro de um cliente
    @apiName delete_cliente
    @apiGroup Cliente

    @apiParam {String} id_cliente ID do cliente

    @apiExample Exemplo de requisição:
        curl -X DELETE -i http://localhost:5000/clientes/:id_cliente
    @apiSuccessExample {Null} Cliente deletado
        HTTP/1.1 204 No Content

    @apiError 404 O id_cliente não foi encontrado
    """

    cliente = Cliente.query.get_or_404(id_cliente)

    db.session.delete(cliente)
    db.session.commit()
    return ('Cliente deletado com sucesso'), 201