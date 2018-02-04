from pydub import AudioSegment
from io import BytesIO
from pydub.silence import split_on_silence
import base64
import os
import sys
import boto3
import json

def lambda_handler(event, context):

    print('OK function start')
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key'] 
        download_path = '/tmp/{}{}'.format('file', key)
        print(download_path)
        s3_client.download_file(bucket, key, download_path)
       
        with open(download_path, "rb") as wav_file:

            sound = AudioSegment.from_file(wav_file, format="wav")

            chunks = split_on_silence(
                sound,

                # split on silences longer than 1000ms (1 sec)
                min_silence_len=100,

                # anything under -50 dBFS is considered silence
                silence_thresh=-50, 

                # keep 200 ms of leading/trailing silence
                keep_silence=200
            )

            # now recombine the chunks so that the parts are at least 2 minutes
            target_length = 120 * 1000
            output_chunks = [chunks[0]]
            for chunk in chunks[1:]:
                if len(output_chunks[-1]) < target_length:
                    output_chunks[-1] += chunk
                else:
                    # if the last output chunk is longer than the target length,
                    # we can start a new one
                    output_chunks.append(chunk)


            for index in range(len(output_chunks)):
                if index < 14:
                    print('part' + str(index + 1))
                    upload_path = '/tmp/{}{}.wav'.format('file', index)
                    output_chunks[index].export(upload_path, format="wav")
                    s3_client.upload_file(upload_path, '{}chunked'.format(bucket), '{}-{}-fromfnProject'.format(key,index))
    return 'Files Processed'

sys.stderr.write("Starting Function\n")

#print(os.environ["AWS_ACCESS_KEY_ID"])
#print(os.environ["AWS_SECRET_ACCESS_KEY"])
obj = json.loads(sys.stdin.read())

# Do not hard code credentials
s3_client = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id='AKIAJAT63M4N322SBXIQ',
    aws_secret_access_key='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'
)

lambda_handler(obj,obj)