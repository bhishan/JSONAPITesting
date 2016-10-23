import requests
import json 

key_passed_count = 0
key_failed_count = 0

def check_key_val(key, value, corresponding_dict):
    global key_passed_count
    global key_failed_count
    if not(key in corresponding_dict):
        print '{0:35}  {1}'.format(key, "failed")
        key_failed_count += 1
        return
    if corresponding_dict[key] == value:
        #print key, "\t\t\t\t", "passed"
        print '{0:35}  {1}'.format(key, "passed")
        key_passed_count += 1
        return
    #print key, "\t\t\t\t", "failed"
    print '{0:35}  {1}'.format(key, "failed")
    key_failed_count += 1

def iterate_keys(qa_dict, api_dict):
    for each_key in qa_dict:
        if type(qa_dict[each_key]) == dict:
            iterate_keys(qa_dict[each_key], api_dict[each_key])
        elif type(qa_dict[each_key]) in [int, bool, str, unicode]:
            value = qa_dict[each_key]
            check_key_val(each_key, value, api_dict)
        elif type(qa_dict[each_key]) == list:
            for each_qa_content, each_api_content in zip(qa_dict[each_key], api_dict[each_key]):
                iterate_keys(each_qa_content, each_api_content)

def main(api_endpoint):
    with open('expected_dict.json', 'rb') as f:
        json_obj = f.read()
    qa_dict = json.loads(json_obj)
    resp = requests.get('http://pastebin.com/raw/G1GmzbaK')
    json_data = resp.json()
    req_data = json_data['results']
    iterate_keys(qa_dict, req_data[0])
    print key_passed_count, " number of keys passed"
    print key_failed_count, " number of keys failed"

if __name__ == '__main__':
    api_endpoint = 'http://pastebin.com/raw/G1GmzbaK'
    main(api_endpoint)
