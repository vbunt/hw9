from flask import Flask, request, render_template
from models import db, people, ans, qs, people_ans
import sqlite3


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/questions')
def questions():
    return render_template("questions.html")


@app.route('/results')
def results():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()

    name = request.values.get('person_name')
    from_vologda = request.values.get('from_vologda')
    record = people(name=name, from_vologda=from_vologda)
    db.session.add(record)
    db.session.commit()

    ln = cursor.execute('select * from people;')
    person_id = len(ln.fetchall())

    for arg in request.args:
        if arg != 'person_name' and arg != 'from_vologda':
            q = arg
            cursor.execute('''select id from qs
                                where question = (?) ''', (q,))
            q_id = cursor.fetchall()[0][0]

            for a in request.args.getlist(q):
                cursor.execute('''select id_a from ans
                                    where answer = (?) ''', (a,))
                a_id = cursor.fetchall()[0][0]
                cursor.execute('''select is_right from ans
                                    where answer = (?) ''', (a,))
                is_right = cursor.fetchall()[0][0]

                record = people_ans(person_id=person_id, q_id=q_id, a_id=a_id, is_right=is_right)
                db.session.add(record)
                db.session.commit()

    result = cursor.execute('''select sum(is_right) from people_ans
                                where id_person = (?)''', (person_id,)).fetchone()[0]

    vologda_percentage = cursor.execute('''select (count(from_vologda)*100 / (select count(id_person) from people)) from people
                                            where from_vologda == 'yes' ''').fetchone()[0]

    hardest_qs = cursor.execute('''select question_name, round(avg(is_right)*100, 1) as d
                                    from people_ans
                                    join qs on people_ans.q_id=qs.id
                                    group by q_id
                                    order by d
                                    limit 3 ''').fetchall()

    cursor.execute('''update people
                    set result = (?)
                    where id_person = (?)''', (result, person_id))
    conn.commit()

    return render_template("results.html", result=result, number_of_people=person_id+1, vologda_percentage=vologda_percentage, hardest_qs=hardest_qs)


if __name__ == '__main__':
    app.run()
