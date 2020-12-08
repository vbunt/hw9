from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ans(db.Model):
    __tablename__ = 'ans'

    id_a = db.Column('id_a', db.Integer, primary_key=True)
    id_q = db.Column('id_q', db.Integer)
    answer = db.Column('answer', db.Text)
    is_right = db.Column('is_right', db.Integer)


class qs(db.Model):
    __tablename__ = 'qs'

    id = db.Column('id', db.Integer, primary_key=True)
    question = db.Column('id_a', db.Text)
    question_name = db.Column('question_name', db.Text)


class people_ans(db.Model):
    __tablename__ = 'people_ans'

    person_id = db.Column('id_person', db.Integer, primary_key=True)
    q_id = db.Column('q_id', db.Integer)
    a_id = db.Column('a_id', db.Integer, primary_key=True)
    is_right = db.Column('is_right', db.Integer)


class people(db.Model):
    __tablename__ = 'people'

    person_id = db.Column('person_id', db.Integer, primary_key=True)
    name = db.Column('name', db.Text)
    from_vologda = db.Column('from_vologda', db.Integer)
    result = db.Column('result', db.Integer)
