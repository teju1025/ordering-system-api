from flask import jsonify, abort
from flask.helpers import make_response
from flask_restful import Resource, reqparse
import json

class EditIngredientStock(Resource):

    def __init__(self):
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('is_delete', type=bool, required=False)
        self.reqparse_args.add_argument('ingredient', type=str, required=False)
        self.reqparse_args.add_argument('stock', type=int, required=False)
        self.reqparse_args.add_argument('cost', type=int, required=False)
        super().__init__()
    
    def _is_ingredient_required_in_food_ingredient_info(self, ingredient):
        with open('./database/food_ingredient_info.json', 'r', encoding='utf-8') as f:
            foods = json.load(f)

        for food in foods:
            if ingredient in foods[food]['食材']:
                return True
        return False

    def post(self):
        args = self.reqparse_args.parse_args()
        ingredient = args['ingredient']
        stock = args['stock']
        cost = args['cost']

        with open('./database/ingredient_stock.json', 'r', encoding='utf-8') as f:
            ingredients = json.load(f)

        return jsonify({'message': '修改成功'})