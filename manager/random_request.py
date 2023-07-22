from django.conf import settings
import requests
import random

from .models import RandomOrgRequest


class RandomorgRequest:
    API_KEY = settings.RANDOMORG_API
    API_URL = "https://api.random.org/json-rpc/4/invoke"

    '''
        API result request
        {
            "jsonrpc": "2.0",
            "result": {
                "random": {
                    "data": [
                        4, 5
                    ],
                    "completionTime": "2023-07-11 21:37:31Z"
                },
                "bitsUsed": 16,
                "bitsLeft": 249984,
                "requestsLeft": 999,
                "advisoryDelay": 2700
            },
            "id": 42
        }

        Created in 07.2023 year
    '''
    def generateIntegers(self, n: int, min: int, max: int, replacement: bool = False) -> dict:
        if n == 0:
            raise ValueError('The parameter "n" must be greater than zero')

        if n >= 1000:
            nDiv = int(n / 1000) if n % 1000 == 0 else (int(n / 1000) + 1)
        else:
            nDiv = 1

        for i in range(nDiv):
            nVal = 1000

            if (i == (nDiv - 1)) and ((nDiv * 1000) > n):
                nVal = n % 1000

            rBody = {
                "jsonrpc": "2.0",
                "method": "generateIntegers",
                "params": {
                    "apiKey": f"{self.API_KEY}",
                    "n": nVal,
                    "min": min,
                    "max": max,
                    "replacement": replacement
                },
                "id": int(RandomOrgRequest.objects.latest('id').pk if RandomOrgRequest.objects.all().__len__() > 0 else 0) + 1
            }

            r = requests.post(self.API_URL, json=rBody)

            RandomOrgRequest.objects.create(
                requestUrl=self.API_URL,
                requestBody=rBody.__str__(),
                responseBody=r.text,
                statusCode=r.status_code,
                headers=r.headers,
                functionName="generateIntegers"
            ).save()

            rj = r.json()
            if 'error' in rj:
                return {
                    'error': {
                        'code': rj['error']['code'],
                        'message': rj['error']['message']
                    },
                    'data': None
                }
            else:
                return {
                    'data': rj['result']['random']['data']
                }



    '''
        API result request

        {
            "jsonrpc": "2.0",
            "result": {
                "status": "running",
                "creationTime": "2023-07-09 19:07:38Z",
                "bitsLeft": 250000,
                "requestsLeft": 1000,
                "totalBits": 16,
                "totalRequests": 1
            },
            "id": 15998
        }

        Created in 07.2023 year
    '''
    def getUsage(self):
        rBody = {
            "jsonrpc": "2.0",
            "method": "getUsage",
            "params": {
                "apiKey": f"{self.API_KEY}"
            },
            "id": int(RandomOrgRequest.objects.latest('id').pk if RandomOrgRequest.objects.all().__len__() > 0 else 0) + 1
        }

        r = requests.post(self.API_URL, json=rBody)

        RandomOrgRequest.objects.create(
            requestUrl=self.API_URL,
            requestBody=rBody.__str__(),
            responseBody=r.text,
            statusCode=r.status_code,
            headers=r.headers,
            functionName="generateIntegers"
        ).save()

        if "error" in r.json():
            return {
                'status': False,
                'code': r.json()['error']['code'],
                'message': r.json()['error']['message'],
                'result': None,
            }

        return {
            'status': True,
            'code': 200,
            'message': "API Key is valid",
            'result': r.json()['result'],
        }




class DrawNumbers:

    def __init__(self) -> None:
        self.random_request = RandomorgRequest()

    def __generateNumber(self, n: int, min: int, max: int, replacement: bool = False) -> list:
        """
            The numbers generated using this function are not random but pseudo random.
            Because they have been generated using mathematical formulas
        """

        numbers = list(range(min, max + 1))
        random.shuffle(numbers)
        return numbers[:n]

    def getRandomNumber(self, n: int, min: int, max: int, replacement: bool = False) -> dict:
        data = {
            "error": {
                "status": False,
                "code": None,
                "message": None
            },
            "data": []
        }

        rData = self.random_request.generateIntegers(n, min, max, replacement)
        if 'error' not in rData:
            data['data'] = rData['data']
            return data
        else:
            data = {
                "error": {
                    "status": True,
                    "code": rData['error']['code'],
                    "message": rData['error']['message']
                }
            }

        data['data'] = self.__generateNumber(n, min, max, replacement)

        return data


class RandomAssign:
    def __init__(self) -> None:
        self.draw_num = DrawNumbers()

    def autoAssign(self, groups: list, teams: list) -> dict:

        groups_len = len(groups)
        teams_len = len(teams)

        if groups_len == 0 or teams_len == 0:
            return {}
        elif groups_len > teams_len:
            groups_len = teams_len
        elif groups_len == 1:
            return { f"{groups[0]}": teams }

        amount_teams_to_group = int(teams_len / groups_len)

        data = { i: amount_teams_to_group for i in range(groups_len) }

        if not (teams_len % groups_len) == 0:
            req = self.draw_num.getRandomNumber((teams_len % groups_len), 0, groups_len - 1)

            if req['error']['status']:
                print("Error:", req['error']['message'], req['error']['code'])

            for i in req['data']:
                data[i] += 1

        teams_list = teams
        dataRet = {}
        for key,value in data.items():

            teams_list_length = len(teams_list)
            if teams_list_length == value:
                dataRet[f'{groups[key]}'] = teams_list
                break

            get_random_num = self.draw_num.getRandomNumber(value, 0, teams_list_length - 1)

            if get_random_num['error']['status']:
                print("Error:", get_random_num['error']['message'], req['error']['code'])

            t = []
            for i, v in enumerate(get_random_num['data']):
                t.append(teams_list[i])
                teams_list.pop(i)

            dataRet[f'{groups[key]}'] = t

        return dataRet