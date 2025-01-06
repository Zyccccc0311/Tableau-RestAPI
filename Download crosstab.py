import jwt,datetime,uuid,requests
import xml.etree.ElementTree as ET
import re

# Username in Tableau Server
user_name = 'tabadmin' 

# Three properties when created Connected Apps in Tableau Server

#Client ID
connectedAppClientId = 'ec81db70-1083-48a8-bcbd-2e1d0f0fd0cc'  
#Secret ID
connectedAppSecretId = '9df6485b-26c4-4361-8335-ff40e0ee907c'  
#Secret KEY
connectedAppSecretKey ='jL9XZf8AS+yBfeqqC7uXIjK2LCFL8h0N4OXcMAMOABg='


token = jwt.encode(
    {
        "iss": connectedAppClientId,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "jti": str(uuid.uuid4()),
        "aud": "tableau",
        "sub": user_name,
        "scp": ['tableau:workbooks:download', 'tableau:datasources:download','tableau:views:download','tableau:content:read'],
    },
    connectedAppSecretKey,
    algorithm="HS256",
    headers={
        'kid': connectedAppSecretId,
        'iss': connectedAppClientId
    }
)

print("--------------------------------token--------------------------------")
print(token)

server = 'http://www.kudu.tech:49801' 
api_version = '3.19'
#Null means Default Site, or you can fill in with your specific site name
site_name = ''

taburl = server+"/api/{0}/auth/signin".format(api_version)

# print("--------------------------------taburl--------------------------------")
# print(taburl)

#Create XML file for login 
xml_request = ET.Element('tsRequest')
credentials_element = ET.SubElement(xml_request, 'credentials', jwt=token)
ET.SubElement(credentials_element, 'site', contentUrl="")
xml_request = ET.tostring(xml_request)

# print("--------------------------------xml_request--------------------------------")
# print(xml_request)

response = requests.post(url=taburl,data=xml_request,headers={'Accept': 'application/json'})

# print(response.status_code)
if response.status_code == 200:
    print("\n**********登录成功**********\n")
else :
    print(response.status_code)

print("--------------------------------response.content--------------------------------")
print(response.text)

response_text = response.json()
credentials_token = response_text.get('credentials').get('token')
site_id = response_text.get('credentials').get('site').get('id')
user_id=response_text.get('credentials').get('user').get('id')
# print("--------------------------------credentials_token--------------------------------")
# print(credentials_token)
# print("--------------------------------site_id--------------------------------")
# print(site_id)
# print("--------------------------------user_id--------------------------------")
# print(user_id)

# Fill in with your specific workbook ID, your can get workbook ID in GetID.py
view_id="d41a7c4a-4fc9-4da1-b8f3-0268ab47df90"

# def download(server, auth_token, site_id):

print("\tQuering")

# url = server + "/api/3.19/sites/{0}/workbooks?filter=name:eq:Tableau_Email_Records".format(site_id)
# /api/api-version/sites/site-id/views/view-id/crosstab/excel
# /api/api-version/sites/site-id/views/view-id/data
url = server + "/api/{0}/sites/{1}/views/{2}/crosstab/excel".format(api_version,site_id,view_id)
url1 = server + "/api/{0}/sites/{1}/views/{2}/data".format(api_version,site_id,view_id)
headers={"X-Tableau-Auth": credentials_token}
response = requests.get(url, headers=headers)
# print (response.content)

if response.status_code == 200:
    # 将响应内容保存为 Excel 文件
    with open("crosstab.xlsx", "wb") as file:
        file.write(response.content)
    print("Excel文件已成功下载并保存")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")

response = requests.get(url1, headers=headers)
# print (response.content)

if response.status_code == 200:
    # 将响应内容保存为 Csv 文件
    with open("crosstab.csv", "wb") as file:
        file.write(response.content)
    print("Csv文件已成功下载并保存")
else:
    print(f"请求失败，状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
