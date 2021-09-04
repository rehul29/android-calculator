from os import environ
import github_utils
if __name__ == "__main__":
    changed_files = list()
    hidden_files = list()
    page_num = 1
    try:
        pullreq = environ["CIRCLE_PULL_REQUEST"]
        pr_id = pullreq[pullreq.rindex('/')+1:]
    except KeyError:
        pr_id = environ["CIRCLE_PR_NUMBER"]
    print(pr_id)
    all_changed_files = github_utils.get_all_changed_files(pr_id)
    changed_files = [x for x in all_changed_files if x.startswith("app/")]
    zipfiles = []
    hidden_files = []
    for i in range(0, len(changed_files)):
        if '/.' in changed_files[i]:
            hidden_files.append(changed_files[i])
        if changed_files[i].endswith(".zip"):
            zipfiles.append(changed_files[i])
    if len(zipfiles) > 0:
        open('changed_zip_files', 'w').write('\n'.join(zipfiles) + '\n')
    if len(hidden_files) > 0:
        print("[ERROR] : PR contains following hidden file(s): \n\t" + '\n\t'.join(hidden_files))
        github_utils.comment_on_pr("Hidden Files Check Failed", "fail", "PR contains following hidden file(s): <br/>" + '<br/>'.join(hidden_files), pr_id)
        exit(1)
    else:
        github_utils.comment_on_pr("Hidden Files Check Passed", "pass", "There are no hidden files in PR.", pr_id)
