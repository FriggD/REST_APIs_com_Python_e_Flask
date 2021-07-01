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
    argumento.add_argument('nome')
    argumento.add_argument('estrelas')
    argumento.add_argument('diaria')
    argumento.add_argument('cidade')

    def find_hotel(hotel_id):
        for hotel in hoteis:
            if hotel['hotel_id'] == hotel_id:
                return hotel
        return None

    def get(self, hotel_id):
        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            return hotel
        return {'message': 'Hotel not found.'}, 404

    def post(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        # novo_hotel = { 'hotel_id': hotel_id, **dados}

        hoteis.append(novo_hotel)
        return novo_hotel, 200

    def put(self, hotel_id):
        dados = Hotel.argumentos.parse_args()
        hotel_objeto = HotelModel(hotel_id, **dados)
        novo_hotel = hotel_objeto.json()
        # novo_hotel = { 'hotel_id': hotel_id, **dados}

        hotel = Hotel.find_hotel(hotel_id)
        if hotel:
            hotel.update(novo_hotel)
            return novo_hotel, 200

        hoteis.append(novo_hotel)
        return novo_hotel, 201

    def delete(self, hotel_id):
        global hoteis
        hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
        return {'message': 'Hotel deleted.'}
