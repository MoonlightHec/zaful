# _*_ coding: utf-8 _*_
"""
# @Time : 2021/4/8 15:20 
# @Author : mhec 
# @File : cod_before_risk.py
# @desc : cod事前风控
"""
from com.util.http_utils import HttpRequest

url = 'http://10.40.2.62:2087/gateway/'
headers = {"Content-Type": "application/json"}
data = {
    "header": {
        "service": "com.globalegrow.spi.pay.inter.PayRiskService",
        "method": "payBeforRiskHandle",
        "domain": "",
        "version": "1.0.0",
        "tokenId": "487d842de4e1c9b9c99ac868c7af15a4"
    },
    "body": {
        "appVersion": "7.2.2",
        "categoryIds": [
            "315"
        ],
        "goodsInfoList": [
            {
                "catName": "Bikini Bottoms",
                "catalogue": "Swimwear > Bikinis > Bikini Bottoms",
                "categoryId": 315,
                "categoryName": "Swimwear",
                "goodsSn": "465210111",
                "price": 11.49,
                "qty": 1,
                "title": "ZAFUL Striped High Cut Ruched Bikini Bottom"
            }
        ],
        "orderInfo": {
            "currencyCode": None,
            "currencyRate": None,
            "hasUseCoupon": 0,
            "insuranceFee": None,
            "logisticsLevel": None,
            "logisticsMethod": None,
            "payAmount": 11.49,
            "payCurrencyAmount": None,
            "pipelineCode": "ZF",
            "platform": 3,
            "shippingFee": None,
            "shippingIp": "10.35.100.41",
            "siteCode": "ZF",
            "skuCount": 1,
            "telephone": "7894561234"
        },
        "requestIp": "10.35.100.41",
        "shippingAddressInfo": {
            "address": "1111-1115 Massachusetts Avenue1111-1115 Massachusetts Avenue",
            "addressLine1": "1111-1115 Massachusetts Avenue",
            "addressLine2": "1111-1115 Massachusetts Avenue",
            "area": None,
            "city": "Duntocher",
            "country": "GB",
            "email": "zhongliping-buyer@globalegrow.com",
            "firstName": "United Kingdom",
            "fullName": "United KingdomUnited Kingdom",
            "lastName": "United Kingdom",
            "postalCode": "AB10 1AA",
            "state": "West Dunbartonshire"
        },
        "skuList": [
            "465210111"
        ],
        "sourceId": "6c1543277d81b0d63fc9238d4faa1539",
        "userInfo": {
            "accountAge": 0,
            "couponCode": None,
            "email": "lijun7@globalegrow.com",
            "hasCodOrder": None,
            "hasShippedRecords": 1,
            "orderCount": None,
            "unfinishedOrderCount": None,
            "userId": 188265,
            "userSex": 2
        }
    }
}
response = HttpRequest.post(url=url, headers=headers, body=data)
print(response.get('preview'))
