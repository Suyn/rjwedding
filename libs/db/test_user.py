from sqlalchemy import func

from connect import session
from models.acount_user_modules.user_modules import User, Retuser


#增
def add_user():
    # person = Retuser(u_id=1)
    # session.add(person)
    session.add_all([Retuser(u_id=1), Retuser(u_id=4), Retuser(u_id=5), Retuser(u_id=6), Retuser(u_id=10)])
    session.commit()

#删
def delete_user():
    row = session.query(User).filter_by(username='der')[0]
    print(row)
    session.delete(row)
    session.commit()

#改
def update_user():
    session.query(User).filter_by(id=3).update({User.password:'abcdefg'})
    session.commit()

#查
def query_user():
    # row = session.query(User).filter_by(username='suyn').all()
    # row = session.query(User).filter(User.username=='suyn').all()
    # row = session.query(func.count('*')).filter(User.id > 7).all()
    # row = session.query(User).filter_by(password='123456').order_by(-User.id).all()
    row = session.query(User.username, func.count(User.id)).group_by(User.username).having(func.count(User.id)==1).all()
    print(row)
    session.commit()

if __name__=='__main__':
    # add_user()
    # delete_user()
    # update_user()
    query_user()
    # print(User.locked)