__author__ = 'scottpecnik'
import cloudant
from base64 import *


def main():
    account_name = 'cloudant_account'
    username = 'cloudant_username'
    password = 'cloudant_password'
    account = cloudant.Account(account_name)
    account.login(username, password)
    database = account.database('timelapse')
    design = database.design('picsInDateRange1')
    pics = design.index('_view/picDateCreated?include_docs=true')
    # newFile = urllib.URLopener()
    i = 000
    for pic in pics:
        i = i+1
        file_name = '/Users/scottpecnik/Desktop/pictures/'+ format(i, '03d') +'.png'
        print(file_name)
        pic_URL = 'https://'+str(account_name)+'.'+'cloudant.com/timelapse/'+str(pic['doc']['_id'])+'/picture'
        r = design.attachment(pic_URL).get()
        with open(file_name, 'wb') as f:
            f.write(r.content)


if __name__ == "__main__":
    main()