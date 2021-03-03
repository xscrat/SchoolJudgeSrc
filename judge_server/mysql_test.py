import MySQLdb

db = MySQLdb.connect(
    host='localhost',
    user='root',
    passwd='135246',
    db='school_judge'
)

cur = db.cursor()

db.commit()


def _get_sum_sql(is_top_5=True):
    return 'SELECT program_id, CAST(SUM(mark) AS SIGNED) FROM judge_summary GROUP BY program_id ORDER BY SUM(mark) DESC' + (
        ' LIMIT 5' if is_top_5 else '')


def _get_judge_register_sql(judge_id):
    return 'INSERT INTO judges(judge_id) VALUES (%i)' % judge_id


try:
    cur.execute(_get_judge_register_sql(4))
except:
    print 'already used'

db.commit()

# for row in cur.fetchall():
#     print row
