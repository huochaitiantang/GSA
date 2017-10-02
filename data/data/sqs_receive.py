import sys
import boto3
import json
sys.path.append('..')
import database.sql as sql

sqs = boto3.resource('sqs')
clear = False
if len(sys.argv) >=2 and sys.argv[1] == 'clear':
    clear = True
# Get the queue
queue = sqs.get_queue_by_name(QueueName='gsa_queue')
cnt = 1
while True:
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Author']):
        # Get the custom author message attribute if it was set
        print "## ",cnt
        cnt += 1
        if clear == False and (message.message_attributes is not None):
            author_name = message.message_attributes.get('Author').get('StringValue')
            if author_name and author_name == 'liuliang':
                # Print out the body and author (if set)
                res =  json.loads(message.body)
                print "Insert:",res
                if res['msg_type'] == 'single_rela':
                    tmp = {}
                    tmp[res['key_0']] = res['des_val'][res['key_0']]
                    for ii in res['des_val'][res['key_1']]:
                        tmp[res['key_1']] = ii
                        sql.insert(res['table_name'],tmp)
                else:
                    sql.insert(res['table_name'],res['des_val'])
        # Let the queue know that the message is processed
        message.delete()
    if clear == True:
        break
