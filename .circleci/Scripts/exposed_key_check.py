import xml.etree.ElementTree as ET
import re
import os
import github_utils

try:
    pullreq = os.environ["CIRCLE_PULL_REQUEST"]
    pr_id = pullreq[pullreq.rindex('/')+1:]
except KeyError:
    pr_id = os.environ["CIRCLE_PR_NUMBER"]

path = os.getcwd()
print("path: "+str(path))
tree = ET.parse(os.path.join(path,"app/src/main/AndroidManifest.xml"))
#root = tree.getroot()
exposed_keys = []
exception = []
for item in tree.iter():
    if item.tag == "meta-data":
        name = item.attrib.get('{http://schemas.android.com/apk/res/android}name')
        value = item.attrib.get('{http://schemas.android.com/apk/res/android}value')
        if not value:
            value = ''
        if 'key' in name.lower() or 'key' in value.lower():
            if name.lower() not in exception:
                if(not value.startswith('@string')):
                    exposed_keys.append(name)
if(exposed_keys):
    github_utils.comment_on_pr("Exposed Key Check Failed", "fail", "There are exposed keys in AndroidManifest.xml: \n{}".format('\n'.join(exposed_keys)), pr_id)
    assert False, "There are exposed keys in AndroidManifest.xml: \n{}".format('\n'.join(exposed_keys))
else:
    github_utils.comment_on_pr("Exposed Key Check Passed", "pass", "There are no exposed keys in AndroidManifest.xml", pr_id)