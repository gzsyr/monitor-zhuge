import time
import requests
from urllib.parse import urlencode


def read_txt():
    note = open('zg-' + time.strftime('%Y-%m-%d') + '.txt', encoding='utf-8', mode='r')
    return note.read()


def byte_size(s):
    return len(s.encode('gbk'))


if __name__ == '__main__':
    content = read_txt()
    content = content.replace(u'\u3000', u'').replace(' ', '')

    ary_line = content.splitlines()
    for i in range(len(ary_line)):
        line = ary_line[i]
        ary_data = line.split('|')

        ary_data[0] = ' ' + ary_data[0] + ''.ljust(40 - byte_size(ary_data[0]), ' ')
        ary_data[1] = ' ' + ary_data[1].rjust(10, ' ') + ' '
        ary_data[2] = ' ' + ary_data[2].rjust(10, ' ') + ' '
        ary_data[3] = ''.rjust(10 - byte_size(ary_data[3]), ' ') + ary_data[3] + ' '

        line = '    |' + '|'.join(ary_data) + '|'

        ary_line[i] = line

    content = '\n'.join(ary_line)

    content = '<pre>\n\n<b>    ' + time.strftime('%Y-%m-%d') + ' 监控结果如下：</b>\n\n'\
              + content + '\n\n</pre>'

    mail_param = {
        "k": "b8be9c6c70ed10e04b033847895970f6",
        "a": "sendmail",
        "toid": "wangxiaojie,zhuqiang,zhusuyun,zhangjing,zhaobaorong1",
        "fromid": "zhaobaorong1",
        "copy_uids": "",
        "subject": time.strftime('%Y-%m-%d') + " 诸葛数据监控结果",
        "content": content
    }

    url = "http://oa.house365.com/api/api_el.php?" + urlencode(mail_param, encoding='gbk')

    res = requests.get(url)
    print(res)
