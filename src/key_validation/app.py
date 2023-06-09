import json
import os
from datetime import datetime, timezone, timedelta

max_key_days = os.getenv('MAX_KEY_AGE')


def lambda_handler(event, context):
    time_limit = datetime.now(timezone.utc) - timedelta(days=int(max_key_days))
    older_access_keys = []

    for item in event:
        access_keys = item['AccessKeys']
        for access_key in access_keys:
            if access_key['Status'] == 'Active' and datetime.strptime(access_key['CreateDate'],
                                                                      '%Y-%m-%dT%H:%M:%SZ').replace(
                    tzinfo=timezone.utc) < time_limit:
                older_access_keys.append({'UserName': access_key['UserName'], 'AccessKey': access_key['AccessKeyId']})

    return {
        'accessKeys': older_access_keys,
        'count': len(older_access_keys)
    }
