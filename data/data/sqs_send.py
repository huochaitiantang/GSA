import boto3
import json

sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName='gsa_queue')
print ("MY_QUEUE:",queue.url)

def send(table_name,des_val,msg_type,key_0,key_1):
    info = dict()
    info['msg_type'] = msg_type
    info['table_name'] = table_name
    info['des_val'] = des_val
    if msg_type == 'single_rela':
        info['key_0'] = key_0
        info['key_1'] = key_1
    msg = json.dumps(info)
    response = queue.send_message(
	MessageBody = msg,
	MessageAttributes = {
    	    'Author': {
                'StringValue': 'liuliang',
                'DataType': 'String'
            }
        }
    )
    print "Send <",msg,">",response.get('Failed')

