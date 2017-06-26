from hashlib import md5
import re
from app import db
from app import app
from config import WHOOSH_ENABLED
from passlib.apps import custom_app_context as pwd_context
import datetime
from dateutil.parser import parse
#from datetime import datetime

#not sure how he imported sql alchemy at all so added this one
#from sqlalchemy.orm import relationship

import sys
if sys.version_info >= (3, 0):
    enable_search = False
else:
    enable_search = WHOOSH_ENABLED
    if enable_search:
        import flask_whooshalchemy


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True, nullable=False)
    manpower_admin = db.Column(db.Boolean, default=False)
    mobility_admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    #mobilitys = db.relationship('Mobility', backref='username', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)
    followed = db.relationship('User',
                               secondary=followers,
                               primaryjoin=(followers.c.follower_id == id),
                               secondaryjoin=(followers.c.followed_id == id),
                               backref=db.backref('followers', lazy='dynamic'),
                               lazy='dynamic')
    def hash_password(self, password):
        self.password_hash=pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def make_valid_username(username):
        return re.sub('[^a-zA-Z0-9_\.]', '', username)

    @staticmethod
    def make_unique_username(username):
        if User.query.filter_by(username=username).first() is None:
            return username
        version = 2
        while True:
            new_username = username + str(version)
            if User.query.filter_by(username=new_username).first() is None:
                break
            version += 1
        return new_username

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    #md5(self.username had md5(self.email
    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % \
            (md5(self.username.encode('utf-8')).hexdigest(), size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id).order_by(
                    Post.timestamp.desc())

    def __repr__(self):  # pragma: no cover
        return '<user> %r' % (self.username)


class Post(db.Model):
    __searchable__ = ['body']

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    language = db.Column(db.String(5))

    def __repr__(self):  # pragma: no cover
        return '<Post %r>' % (self.body)


class Mobility(db.Model):
    username=db.Column(db.String, primary_key=True)
    cc_letter=db.Column(db.String(45))
    drug_pref=db.Column(db.String(45))
    afsc=db.Column(db.String(5))
    qnft=db.Column(db.String(45))

    edi= db.Column(db.Integer)
    line_badge= db.Column(db.Integer)

    dog_tags= db.Column(db.Boolean)

    pt_excellence= db.Column(db.Integer)
    pt_score= db.Column(db.Numeric)
    pt_test= db.Column(db.DateTime)
    #Manual DateTimes
    cac_expiration= db.Column(db.DateTime)
    gtc_expiration= db.Column(db.DateTime)
    bus_license= db.Column(db.DateTime)
    mri_hri= db.Column(db.DateTime)
    vred= db.Column(db.DateTime)
    form_2760= db.Column(db.DateTime)
    small_arms= db.Column(db.DateTime)
    security_clearance= db.Column(db.DateTime)
    form_55= db.Column(db.DateTime)
    green_dot= db.Column(db.DateTime)
    #CBT's autopopulate
    sabc_hands_on_cbt= db.Column(db.DateTime)
    cbrn_cbt= db.Column(db.DateTime)
    sabc_cbt= db.Column(db.DateTime)
    dod_iaa_cyber_cbt= db.Column(db.DateTime)
    force_protection_cbt= db.Column(db.DateTime)
    human_relations_cbt= db.Column(db.DateTime)
    protecting_info_cbt= db.Column(db.DateTime)
    af_c_ied_video_cbt= db.Column(db.DateTime)
    af_c_ied_awrns_cbt= db.Column(db.DateTime)
    af2a_culture_cbt= db.Column(db.DateTime)
    biometrics_cbt= db.Column(db.DateTime)
    collect_and_report_cbt= db.Column(db.DateTime)
    east_cbt= db.Column(db.DateTime)
    eor_cbt= db.Column(db.DateTime)
    free_ex_of_religion_cbt= db.Column(db.DateTime)
    loac_cbt= db.Column(db.DateTime)
    mental_health_cbt= db.Column(db.DateTime)
    tbi_awareness_cbt= db.Column(db.DateTime)
    uscentcom_cult_cbt= db.Column(db.DateTime)
    unauthorized_disclosure_cbt= db.Column(db.DateTime)
    deriv_class_cbt= db.Column(db.DateTime)
    marking_class_info_cbt= db.Column(db.DateTime)
    sere_100_cst_cbt= db.Column(db.DateTime)

    def add_months(self, dt0, months):
        for i in range(months):
            dt1 = dt0.replace(day=1)
            dt2 = dt1 + datetime.timedelta(days=32)
            dt0 = dt2.replace(day=1)
        return dt0

    def is_expired(self, attr_name, date):
        a=Rules.query.filter_by(name=attr_name).first()
        if str(type(a)) == "<type \'NoneType\'>":
        	return True
        value=getattr(self, attr_name)
        if value != None:
            #Rule 1 checks 36 months into future
            if a.rule==1:
                date=parse(date)
                value=self.add_months(value, 36)
                if date>value:
                    return True
            #Rule 2 checks 12 months into the future
            elif a.rule==2:
                date=parse(date)
                value=self.add_months(value, 12)
                if date>value:
                    return True
            #Rule 3 checks 24 months into the future
            elif a.rule==3:
                date=parse(date)
                value=self.add_months(value,24)
                if date>value:
                    return True
            #Rule 4 checks 76 months into the future
            elif a.rule==4:
                date=parse(date)
                value=self.add_months(value,76)
                if date>value:
                    return True
            #Rule 5 checks current date
            elif a.rule==5:
                date=parse(date)
                if date>value:
                    return True
            #Rule 6 checks 12 months if pt_score>90 else 6 months
            elif a.rule==6:
                date=parse(date)
                if self.pt_score>=90:
                    value=self.add_months(value,12)
                else:
                    value=self.add_months(value,6)
                if date>value:
                    return True
            return False

    def __repr__(self):  # pragma: no cover
        return '<Mobility %r>' % (self.username)

class Rules(db.Model):
    name=db.Column(db.String, primary_key=True)
    rule=db.Column(db.Integer, default='0', unique=False)
    args=db.Column(db.String)
    
    def __repr__(self):  # pragma: no cover
        return '<Rules %r>' % (self.name)

class History(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    date=db.Column(db.DateTime)
    table=db.Column(db.String)
    column=db.Column(db.String)
    valueOld=db.Column(db.String)
    valueNew=db.Column(db.String)
    
    def __repr__(self):  # pragma: no cover
        return '<History %r>' % (self.name)
#if enable_search:
#    whooshalchemy.whoosh_index(app, Post)