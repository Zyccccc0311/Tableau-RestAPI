import jwt,datetime,uuid,requests
import xml.etree.ElementTree as ET
import re

# Username in Tableau Server
user_name = 'admin' 

# Three properties when created Connected Apps in Tableau Server

#Client ID
connectedAppClientId = '1453bced-6de8-4ea9-9d08-9e4e0ef9f2d7'  
#Secret ID
connectedAppSecretId = 'e1181cbf-ebf6-4ea5-94c2-0de9c8e7659d'  
#Secret KEY
connectedAppSecretKey ='XtfB7wk7tit5RRycdag2FHxtflh+bzn4jNzJ2T0eo5I='


token = jwt.encode(
    {
        "iss": connectedAppClientId,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "jti": str(uuid.uuid4()),
        "aud": "tableau",
        "sub": user_name,
        "scp": ['tableau:workbooks:download', 'tableau:datasources:download']#],
    },
    connectedAppSecretKey,
    algorithm="HS256",
    headers={
        'kid': connectedAppSecretId,
        'iss': connectedAppClientId
    }
)

# print("--------------------------------token--------------------------------")
# print(token)

server = 'http://win-nc0gjlgvtt5' 
api_version = '3.19'
#Null means Default Site, or you can fill in with your specific site name
site_name = ''

taburl = server+"/api/{0}/auth/signin".format(api_version)

# print("--------------------------------taburl--------------------------------")
# print(taburl)

#Create XML file for login 
xml_request = ET.Element('tsRequest')
credentials_element = ET.SubElement(xml_request, 'credentials', name="admin", password="admin")
ET.SubElement(credentials_element, 'site', contentUrl="")
xml_request = ET.tostring(xml_request)

# print("--------------------------------xml_request--------------------------------")
# print(xml_request)

response = requests.post(url=taburl,data=xml_request,headers={'Accept': 'application/json'})


if response.status_code == 200:
    print("\n**********登录成功**********\n")

# print("--------------------------------response.content--------------------------------")
# print(response.text)

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
workbook_id="b8417879-2b63-427e-80d5-94e841554265"

def download(server, auth_token, site_id, workbook_id):

    print("\tDownloading workbook to a temp file")
    url = server + "/api/3.19/sites/{0}/workbooks/{1}/content".format(site_id, workbook_id)
    server_response = requests.get(url, headers={'x-tableau-auth': auth_token})
    
    filename = re.findall(r'filename="(.*)"', server_response.headers['Content-Disposition'])[0]
    with open(filename, 'wb') as f:
        f.write(server_response.content)
    return filename

download(server, credentials_token, site_id, workbook_id)
