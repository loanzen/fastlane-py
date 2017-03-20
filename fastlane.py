Class FastlaneClient(object):
	def __init__(self,env,username,password):
		self.env = env
		self.username = username
		self.password = password
	def getVehicleDetails():
		import requests

		url = "https://web.fastlaneindia.com/sandbox/api/v1.2/vehicle"

		querystring = {"regn_no":"DL10CB3330"}

		headers = {
		    'accept': "application/json",
		    'authorization': "Basic TjAxMVRFU1QxOm4xMWxuekA3MyQ=",
		    'cache-control': "no-cache",
		    'postman-token': "bc450ac9-6773-e49b-e831-ad62878a75f9"
		    }

		response = requests.request("GET", url, headers=headers, params=querystring)

		print(response.text)