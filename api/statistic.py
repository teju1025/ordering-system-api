from flask import jsonify, abort
from flask.helpers import make_response
from flask_restful import Resource, reqparse
import json
import datetime

class Statistic(Resource) :
    def __init__(self):
        self.reqparse_args = reqparse.RequestParser()
        self.reqparse_args.add_argument('dateBegin', type=str, required=False)
        self.reqparse_args.add_argument('dateEnd', type=str, required=False)
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

        dateBegin = self.reqparse_args.parse_args()['dateBegin']
        dateEnd = self.reqparse_args.parse_args()['dateEnd']
        
        if dateBegin and dateEnd:
            dateBegin = datetime.datetime.strptime(dateBegin, '%Y%m%d')
            dateEnd = datetime.datetime.strptime(dateEnd, '%Y%m%d')
            if dateBegin > dateEnd:
                abort(400, "起始日期不能大於結束日期")

            for order in history:
                if dateBegin <= datetime.datetime.strptime(history[order]['訂購時間'], '%Y-%m-%d %H:%M:%S') <= dateEnd:
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
        
        if dateBegin:
            dateBegin = datetime.datetime.strptime(dateBegin, '%Y%m%d')
            for order in history:
                if dateBegin <= datetime.datetime.strptime(history[order]['訂購時間'], '%Y-%m-%d %H:%M:%S'):
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
        
        if dateEnd:
            dateEnd = datetime.datetime.strptime(dateEnd, '%Y%m%d')
            for order in history:
                if datetime.datetime.strptime(history[order]['訂購時間'], '%Y-%m-%d %H:%M:%S') <= dateEnd:
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

        for order in history:
            if dateBegin <= datetime.datetime.strptime(history[order]['訂購時間'], '%Y-%m-%d %H:%M:%S') <= dateEnd:
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
