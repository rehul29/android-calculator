import requests
import json
from os import environ
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
from glob import glob
import sys
import os
import github_utils

def parsefile(file):
    parser = make_parser()
    parser.setContentHandler(ContentHandler())
    parser.parse(file)

if __name__ == '__main__':
    token = "token " + os.environ["GITHUB_ACCESS_TOKEN"]
    try:
        pullreq = os.environ["CIRCLE_PULL_REQUEST"]
        pullid = pullreq[pullreq.rindex('/')+1:]
    except KeyError:
        pullid = os.environ["CIRCLE_PR_NUMBER"]
    headers={'Authorization': token}
    r=requests.get('https://api.github.com/repos/'+os.environ["CIRCLE_PROJECT_USERNAME"]+'/'+os.environ["CIRCLE_PROJECT_REPONAME"]+'/pulls/'+pullid+'/files',headers=headers)
    obj=json.loads(r.text); 
    path = os.getcwd()
    filenames=[os.path.join(path,item['filename']) for item in obj]
    print(filenames)
    flag=0
    msg_string=" "
    for file in filenames:
        if os.path.isfile(file):
            if file.endswith('.xml'): 
                try:
                    parsefile(file)
                    print("%s is well-formed" % file)
                except Exception, e:
                    msg_string= msg_string + "%s is NOT well-formed!" % file
                    flag=1
            elif file.endswith('.json') or (file.endswith('.config') and 'app/src/main/assets/bin/Data/' not in file): 
                try:
                    json_object = json.load(open(file))
                    print("%s is well-formed" % file)
                except Exception, e:
                    msg_string= msg_string + "%s is NOT well-formed!" % file
                    flag=1    

    if flag==1:  
        github_utils.comment_on_pr("XML/JSON Validation errors", "fail", "There are XML/JSON validation errors in this PR.<br/>"+msg_string, pullid)          
        sys.exit(-1)
    else:
        github_utils.comment_on_pr("XML/JSON Validation check passsed", "pass", "All XML/JSON are well formed in this PR.", pullid)
            
