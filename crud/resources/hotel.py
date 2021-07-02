from flask_restful import Resource, reqparse
from model.hotel import HotelModel

hoteis = [
    {
        'hotel_id': 'hotel01',
        'nome': 'Hotel 01',
        'estrelas': 4.2,
        'diaria': 420.50,
        'cidade': 'Rio de Janeiro'
    },
    {
        'hotel_id': 'hotel02',
        'nome': 'Hotel 02',
        'estrelas': 4.5,
        'diaria': 520.50,
        'cidade': 'Amapá'
    },
    {
        'hotel_id': 'hotel03',
        'nome': 'Hotel 03',
        'estrelas': 3.9,
        'diaria': 350.50,
        'cidade': 'Curitiba'
    }
]

class Hoteis(Resource):
    def get(self):
        return {'hoteis': hoteis}

class Hotel(Resource):
    argumento = reqparse.RequestParser()
    argumento.add_argument('nome', type=str, required=True, help="The field 'nome' cannot be blank")
    argumento.add_argument('estrelas', type=float, required=True, help="The field 'entrelas' cannot be blank")
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')


    def get(self, hotel_id):
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]} # SELECT * FROM  hoteis

    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {'message': 'Hotel id "{}" already exists.'.format(hotel_id)},400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        # novo_hotel = hotel_objeto.json()
        # novo_hotel = { 'hotel_id': hotel_id, **dados}
        try:
            hotel.save_hotel()
        except:
            return {'message': 'An internal error ocurred'},500
        # hoteis.append(novo_hotel)
        # return novo_hotel, 200
        return hotel.json()

    def put(self, hotel_id):
        dados = Hotel.atributos.parse_args()

        hotel_encontrado = HotelModel.find_hotel()
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json, 200

        hotel = HotelModel(hotel_id, **dados)
        hotel.save_hotel()
        return hotel.json(), 201

    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            hotel.delete_hotel()
            return {'message': 'Hotel deleted.'}
        return {'message': 'Hotel not found.'}
