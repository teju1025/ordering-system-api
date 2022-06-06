from flask import jsonify, abort
from flask.helpers import make_response
from flask_restful import Resource, reqparse
import json

class Statistic(Resource) :
    def __init__(self):
        self.reqparse_args = reqparse.RequestParser()
        super().__init__()

    def get(self):
        with open('./database/food_ingredient_info.json', 'r', encoding='utf-8') as f:
            foods = json.load(f)

        with open('./database/ingredient_stock.json', 'r', encoding='utf-8') as f:
            ingredients = json.load(f)

        with open('./database/order_history.json', 'r', encoding='utf-8') as f:
            history = json.load(f)

        statistic = {}
        for food in foods:
            statistic[food] = {
                '銷售成本': 0,
                '銷售收入': 0
            }

        for order in history:
            for food in history[order]['訂購內容']:
                num = history[order]['訂購內容'][food]
                cost = 0
                income = 0
                for ingredient in foods[food]['食材']:
                    cost += ingredients[ingredient]['成本'] * foods[food]['食材'][ingredient]
                    
                income += foods[food]['價格']
                
                statistic[food]['銷售成本'] += cost * num
                statistic[food]['銷售收入'] += income * num
        
        return jsonify(statistic)
