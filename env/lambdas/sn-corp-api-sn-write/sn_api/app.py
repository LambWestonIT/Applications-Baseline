import json
import requests
import boto3
import os

from base64 import b64decode

# expected incoming structure
#{
#  "Type": "Incident",
#  "AssignmentGroup": "SN Boomi Support",
#  "ShortDesc": "A Short Description",
#  "Desc": "A Description",
#  "urgency": "1",
#  "priority":"3"
# }

def lambda_handler(event, context):
    # TODO implement
    print(event)
    print(context)

    ticketType = event['Type']
    assignmentGroup = event['AssignmentGroup']
    shortDesc = event['ShortDesc']
    Desc = event['Description']
    impact = event['Impact']
    urgency = event['Urgency']
    instance = event['Instance']

    ## connect to SNOW and fire the API call here.
    # it should be a post to this URL:  lambweston.service-now.com/api/now/table/incident
    # i think...
    # lambwestontest.service-now.com/api/now/table/incident
    # {
    #   "impact": "3",
    #   "urgency": "2",
    #   "short_description": "a short description",
    #   "description": "a description",
    #   "assignment_group": "SN Boomi Support"
    # }

    # change URL based on stage...
    url = ""
    if instance == "TEST":
        url = "https://lambwestontest.service-now.com/api/now/table/incident"
    elif instance == "PROD":
       url = "https://lambweston.service-now.com/api/now/table/incident"
    

    ENCRYPTED = os.environ['APIKEY']
    # Decrypt code should run once and variables stored outside of the function
    # handler so that these are decrypted once per container
    passW = boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(ENCRYPTED),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    userName = "Power_Automate_User"
    
    api_header = {"Accept": "application/json",
                  "Content-Type": "application/json"
                  }

    bodydata = {}
    bodydata['impact'] = impact
    bodydata['urgency'] = urgency
    bodydata['short_description']=shortDesc
    bodydata['description'] = Desc
    bodydata['assignment_group']= assignmentGroup

    print("doing the post...")
    print("body data:", json.dumps(bodydata))
    print("headers:", json.dumps(api_header))
    # Send the POST request
    response = requests.post(url, headers=api_header, data=f"{bodydata}", 
        auth = (userName,passW))  # Output the response

    print("Status Code:", response.status_code)
    #print("Response Body:", json.dump(response.json()))



    ticketNumber = 'something'

    #response = {}
    #response['ticket'] = ticketNumber
    #response['success'] = 1
    #response['response'] = thereturn

    return {
        "statusCode": response.status_code,
        "body": response.text
    }

