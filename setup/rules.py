#!flask/bin/python
from app import db, models
a=models.Rules.query.all()
a=models.Rules(name='form_55',rule='2')
db.session.add(a)

b=models.Rules(name='dod_iaa_cyber_cbt',rule='2')
db.session.add(b)

c=models.Rules(name='vred',rule='2')
db.session.add(c)

d=models.Rules(name='force_protection_cbt',rule='2')
db.session.add(d)

e=models.Rules(name='human_relations_cbt',rule='2')
db.session.add(e)

f=models.Rules(name='protecting_info_cbt',rule='2')
db.session.add(f)

g=models.Rules(name='green_dot',rule='2')
db.session.add(g)

h=models.Rules(name='unauthorized_disclosure_cbt',rule='2')
db.session.add(h)

i=models.Rules(name='sabc_cbt',rule='1')
db.session.add(i)

j=models.Rules(name='sabc_hands_on_cbt',rule='1')
db.session.add(j)

k=models.Rules(name='cbrn_cbt',rule='1')
db.session.add(k)

l=models.Rules(name='cbrn_hands_on',rule='1')
db.session.add(l)

m=models.Rules(name='mri_hri',rule='1')
db.session.add(m)

n=models.Rules(name='af_c_ied_video_cbt',rule='1')
db.session.add(n)

o=models.Rules(name='af_c_ied_awrns_cbt',rule='1')
db.session.add(o)

p=models.Rules(name='af2a_culture_cbt',rule='1')
db.session.add(p)

q=models.Rules(name='biometrics_cbt',rule='1')
db.session.add(q)

r=models.Rules(name='collect_and_report_cbt',rule='1')
db.session.add(r)

s=models.Rules(name='east_cbt',rule='1')
db.session.add(s)

t=models.Rules(name='eor_cbt',rule='1')
db.session.add(t)

u=models.Rules(name='free_ex_of_religion_cbt',rule='1')
db.session.add(u)

v=models.Rules(name='sere_100_cst_cbt',rule='1')
db.session.add(v)not_inside

w=models.Rules(name='loac_cbt',rule='1')
db.session.add(w)

x=models.Rules(name='mental_health_cbt',rule='1')
db.session.add(x)

y=models.Rules(name='tbi_awareness_cbt',rule='1')
db.session.add(y)

z=models.Rules(name='uscentcom_cult_cbt',rule='1')
db.session.add(z)

aa=models.Rules(name='small_arms',rule='3')
db.session.add(aa)

ab=models.Rules(name='deriv_class_cbt',rule='3')
db.session.add(ab)

ac=models.Rules(name='security_clearance',rule='4')
db.session.add(ac)

ad=models.Rules(name='marking_class_info_cbt',rule='5')
db.session.add(ad)

ae=models.Rules(name='form_2760',rule='5')
db.session.add(ae)

af=models.Rules(name='cac_expiration',rule='5')
db.session.add(af)

ag=models.Rules(name='gtc_expiration',rule='5')
db.session.add(ag)

ah=models.Rules(name='bus_license',rule='5')
db.session.add(ah)

ai=models.Rules(name='pt_test',rule='6')
db.session.add(ai)

db.session.commit()
'''
    def rules(rule):
        a=rule.split('@')
        #rule1 takes in days ahead and date then returns the days ahead + date
        if int(a[0])==1:
            # formate 1@days_forward@start_date
            date=a[2]
            date=datetime.datetime.strptime(date, '%Y-%m-%d')+datetime.timedelta(days=int(a[1]))
            return date
        #rule2 takes in months ahead and date then returns the months ahead + date
        elif int(a[0])==2:
            months=a[1]
            date=a[2]
            date=datetime.datetime.strptime(date, '%Y-%m-%d')
            for i in range(int(a[1])):
                date=add_one_month(date)
            #date=datetime.datetime.strptime(date, '%Y-%m-%d')+datetime.monthdelta(int(a[1]))
            return date
        #2months
        #3current date
        #4pt test rule score>90 12 months
        return False
'''