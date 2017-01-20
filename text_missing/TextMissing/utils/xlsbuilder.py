import random
import string

import xlsxwriter

#TODO: construct actual valid referat de necesitate here
class XlsBuilder:
    def __init__(self):
        self.file_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(20))
        self.workbook = xlsxwriter.Workbook(self.file_name)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.write(0, 0, 'User: ')

    def set_content(self, content):
        self.worksheet.write(0, 1, content['UserName'])

    def save(self):
        self.workbook.close()