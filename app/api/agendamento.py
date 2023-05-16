"""Agendamento"""
from flask import jsonify, request
from app import db
from app.api import bp
import uuid
from app.models import Agendamento


@bp.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    """
    @api {get} /agendamentos
    Retorna os dados de todos os agendamentos
    @apiName get_agendamentos
    @apiGroup Agendamento

    @apiParam {DateTime} [horario_inicio] Caso informado, filtra os agendamentos a partir da data informada
    @apiParam {DateTime} [horario_fim] Caso informado, filtra os agendamentos até da data informada

    @apiSuccessExample {json} Dados dos agendamentos
        HTTP/1.1 200 OK
        [
            {
                "cliente": {
                    "ddd": "11",
                    "email": "thiagoaugustocruz@gmail.com",
                    "id_cliente": "9fc609c312284d43904cc074519508d0",
                    "nome": "Thiago Cruz",
                    "observacao": "Realizada alteração de dados do cliente",
                    "telefone": "999999999"
                },
                "horario_fim": "Sun, 23 Apr 2023 11:00:00 GMT",
                "horario_inicio": "Sun, 23 Apr 2023 10:00:00 GMT",
                "id_agendamento": 2,
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "observacao": "Alteração"
            },
            {
                "cliente": {
                    "ddd": "11",
                    "email": "thiagoaugustocruz@gmail.com",
                    "id_cliente": "9fc609c312284d43904cc074519508d0",
                    "nome": "Thiago Cruz",
                    "observacao": "Realizada alteração de dados do cliente",
                    "telefone": "999999999"
                },
                "horario_fim": "Sun, 23 Apr 2023 13:00:00 GMT",
                "horario_inicio": "Sun, 23 Apr 2023 12:00:00 GMT",
                "id_agendamento": 1,
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "observacao": null
            }
        ]

    """

    parametros = []

    if 'horario_inicio' in request.args:
        parametros.append(Agendamento.horario_inicio >= request.args.get('horario_inicio'))

    if 'horario_fim' in request.args:
        parametros.append(Agendamento.horario_fim <= request.args.get('horario_fim'))

    if parametros:
        agendamentos = Agendamento.query.filter(*parametros).order_by(Agendamento.horario_inicio)
    else:
        agendamentos = Agendamento.query.order_by(Agendamento.horario_inicio)

    return jsonify([agendamento.to_dict() for agendamento in agendamentos])


@bp.route('/agendamentos/<int:id_agendamento>', methods=['GET'])
def get_agendamento(id_agendamento):
    """
    @api {get} /agendamento/:id_agendamento
    Retorna os dados de um agendamento
    @apiName get_agendamento
    @apiGroup Agendamento

    @apiParam {String} id_agendamento ID do agendamento

    @apiSuccessExample {json} Dados do agendamento
        HTTP/1.1 200 OK
        {
            "cliente": {
                "ddd": "11",
                "email": "thiagoaugustocruz@gmail.com",
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "nome": "Thiago Cruz",
                "observacao": "Realizada alteração de dados do cliente",
                "telefone": "999999999"
            },
            "horario_fim": "Sun, 23 Apr 2023 11:00:00 GMT",
            "horario_inicio": "Sun, 23 Apr 2023 10:00:00 GMT",
            "id_agendamento": 2,
            "id_cliente": "9fc609c312284d43904cc074519508d0",
            "observacao": "Alteração"
        }

    @apiError 404 O id_agendamento não foi encontrado
    """

    agendamento = Agendamento.query.filter(Agendamento.id_agendamento == id_agendamento).first_or_404()

    return jsonify(agendamento.to_dict())


@bp.route('/agendamentos', methods=['POST'])
def create_agendamento():
    """
    @api {post} /agendamentos
    Cadastra um novo agendamento
    @apiName create_agendamento
    @apiGroup Agendamento

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X POST http://localhost:5000/api/agendamentos \
         -d '{
                "horario_inicio": "2023-04-23 14:00:00",
                "horario_fim": "2023-04-23 15:00:00",
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "observacao": "Teste do agendamento de cliente"
            }'

    @apiSuccessExample {json} Agendamento cadastrado
        HTTP/1.1 201 Created
        {
            "Sucesso": {
                "cliente": {
                    "ddd": "11",
                    "email": "thiagoaugustocruz@gmail.com",
                    "id_cliente": "9fc609c312284d43904cc074519508d0",
                    "nome": "Thiago Cruz",
                    "observacao": "Realizada alteração de dados do cliente",
                    "telefone": "999999999"
                },
                "horario_fim": "Sun, 23 Apr 2023 15:00:00 GMT",
                "horario_inicio": "Sun, 23 Apr 2023 14:00:00 GMT",
                "id_agendamento": 2,
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "observacao": "Teste do agendamento de cliente"
            }
        }

    """

    data = request.get_json() or {}

    obrigatorios = ['horario_inicio', 'horario_fim', 'id_cliente']
    ausentes = [campo for campo in obrigatorios if campo not in data]
    if len(ausentes) > 0:
        return("Campos obrigatórios não informados")

    agendamento = Agendamento()
    agendamento.from_dict(data)

    db.session.add(agendamento)
    db.session.commit()

    return jsonify({'Sucesso': agendamento.to_dict()}), 201


@bp.route('/agendamentos/<string:id_agendamento>', methods=['PUT'])
def update_agendamento(id_agendamento):
    """
    @api {put} /agendamentos/:id_agendamento
    Atualiza dados de um agendamento
    @apiName update_agendamento
    @apiGroup Agendamento

    @apiParam {String} id_agendamento ID do agendamento

    @apiExample Exemplo de requisição:
        curl -H "Content-Type: application/json" \
         -X PUT http://localhost:5000/api/agendamentos/:id_agendamento \
         -d '{
                "horario_inicio": "2023-04-23 10:00:00",
                "horario_fim": "2023-04-23 11:00:00",
                "observacao": "Alteração"
            }'

    @apiSuccessExample {json} Agendamento atualizado
        HTTP/1.1 200 OK
        {
            "Sucesso": {
                "cliente": {
                    "ddd": "11",
                    "email": "thiagoaugustocruz@gmail.com",
                    "id_cliente": "9fc609c312284d43904cc074519508d0",
                    "nome": "Thiago Cruz",
                    "observacao": "Realizada alteração de dados do cliente",
                    "telefone": "999999999"
                },
                "horario_fim": "Sun, 23 Apr 2023 11:00:00 GMT",
                "horario_inicio": "Sun, 23 Apr 2023 10:00:00 GMT",
                "id_agendamento": 2,
                "id_cliente": "9fc609c312284d43904cc074519508d0",
                "observacao": "Alteração"
            }
        }

    @apiError 404 O id_agendamento não foi encontrado
    """

    data = request.get_json() or {}

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    alteraveis = ['horario_inicio', 'id_cliente', 'horario_fim', 'observacao']
    invalidos = [campo for campo in data if campo not in alteraveis]
    if len(invalidos) > 0:
        return("Campo inválido no corpo da requisição")

    agendamento.from_dict(data)
    db.session.add(agendamento)
    db.session.commit()

    return jsonify({'Sucesso': agendamento.to_dict()}), 200


@bp.route('/agendamentos/<string:id_agendamento>', methods=['DELETE'])
def delete_agendamento(id_agendamento):
    """
    @api {delete} /agendamentos/:id_agendamento
    Apaga o registro de um agendamento
    @apiName delete_agendamento
    @apiGroup Agendamento

    @apiParam {String} id_agendamento ID do agendamento

    @apiExample Exemplo de requisição:
        curl -X DELETE -i http://localhost:5000/agendamentos/:id_agendamento
    @apiSuccessExample {Null} Agendamento deletado
        HTTP/1.1 204 No Content

    @apiError 404 O id_agendamento não foi encontrado
    """

    agendamento = Agendamento.query.get_or_404(id_agendamento)

    db.session.delete(agendamento)
    db.session.commit()
    return ('Agendamento deletado com sucesso'), 201