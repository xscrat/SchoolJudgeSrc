# -- coding:utf8 --

import SimpleHTTPServer
import SocketServer
import json
import MySQLdb
import logging

log_format = '%(asctime)s %(message)s'
logging.basicConfig(filename='judge.log', level=logging.INFO, format=log_format)

programs_names = ['绣红旗', '我和我的祖国', '生命的河', '记得当年清水塘', '绒花',
                  '江山如此多娇', '致敬范文澜', '青春少年', '我的梦', '上善若水',
                  '透过历史的眼眸', '文澜人 文澜志', '寄明月', '澜学趣品', '我的祖国',
                  '变脸', '南泥湾', '精忠报国', '你笑起来真好看', '青春战歌',
                  '文澜之光']

teachers_programs_ids = [4, 11, 16]

judge_names = map(lambda x: str(x) + '号评委', list(range(1, 1 + 25)))
cur_mark = {}

db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='135246',
    db='school_judge'
)

cur = db.cursor()


class MyHttpRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    @staticmethod
    def _get_path_eles_from_path(path):
        return path.split('/')

    @staticmethod
    def _get_insert_sql(program_id, judge_id, mark):
        return 'INSERT INTO judge_summary(program_id, judge_id, mark) VALUES (%i, %i, %f) ON DUPLICATE KEY UPDATE mark=%f' % (
        program_id, judge_id, mark, mark)

    @staticmethod
    def _get_sum_sql(is_top_5=True):
        return 'SELECT program_id, CAST(SUM(mark) AS SIGNED) FROM judge_summary GROUP BY program_id ORDER BY SUM(mark) DESC' + (' LIMIT 5' if is_top_5 else '')

    @staticmethod
    def _get_judge_register_sql(judge_id):
        return 'INSERT INTO judges(judge_id) VALUES (%i)' % judge_id

    def do_GET(self):
        logging.info('get ' + self.path)
        path_eles = self._get_path_eles_from_path(self.path)
        content_json = {}
        if path_eles[1] == 'get_judge_names':
            content_json = {'judge_names': judge_names}
        elif path_eles[1] == 'get_programs':
            student_program_ids = []
            student_program_names = []
            for i in range(len(programs_names)):
                if i not in teachers_programs_ids:
                    student_program_ids.append(i)
                    student_program_names.append(programs_names[i])
            content_json = {'programs_names': student_program_names, 'programs_ids': student_program_ids}
        elif path_eles[1] == 'get_midway_results':
            cur.execute(self._get_sum_sql())
            for row in cur.fetchall():
                content_json[programs_names[row[0]]] = int(row[1])
        elif path_eles[1] == 'get_results':
            cur.execute(self._get_sum_sql(is_top_5=False))
            for i, program_name in enumerate(programs_names):
                if i not in teachers_programs_ids:
                    content_json[program_name] = 0
            for row in cur.fetchall():
                content_json[programs_names[row[0]]] = int(row[1])

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(json.dumps(content_json))
        return

    def do_POST(self):
        is_successful = True
        logging.info('post ' + self.path)
        path_eles = self._get_path_eles_from_path(self.path)
        if path_eles[1] == 'post_mark':
            judge_id = int(path_eles[2])
            program_id = int(path_eles[3])
            if program_id not in teachers_programs_ids:
                if judge_id < 16:
                    mark = int(path_eles[4]) * 0.2 / 16
                else:
                    mark = int(path_eles[4]) * 0.8 / 9
                cur.execute(self._get_insert_sql(program_id, judge_id, mark))
        elif path_eles[1] == 'post_judge_register':
            judge_id = int(path_eles[2])
            try:
                cur.execute(self._get_judge_register_sql(judge_id))
            except:
                is_successful = False
        elif path_eles[1] == 'delete_db':
            cur.execute('DELETE FROM judge_summary')
            cur.execute('DELETE FROM judges')
        db.commit()

        self.send_response(200 if is_successful else 401)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return


handler_object = MyHttpRequestHandler

PORT = 8000
my_server = SocketServer.TCPServer(('', PORT), handler_object)


my_server.serve_forever()
