import urllib
from bs4 import BeautifulSoup
from urllib2 import urlopen
import os
from dateutil.parser import parse
from .models import User, Mobility, Rules
from app import db
from flask import flash

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

def cbt(fileloc):
    #read current file directory
    import codecs
    '''
    wk_dir = os.path.dirname(os.path.realpath('__file__'))
    filename = os.path.join(wk_dir, 'print_transcript_page.htm')
    '''
    filename=fileloc
    html=codecs.open(filename, 'r', 'windows-1252')

    #for reading url's
    #url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    #html = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(html, "html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    #split text on \n to break into items i can iterate over
    text=text.split('\n')

    cbt=[]
    date=[]
    for i in range(len(text)):
        if text[i]=='GoLearn' or text[i]=='AETC':
            if is_date(text[i+3])==True:
                cbt.append(text[i+1])
                if text[i+4] != 'PASS':
                    datestring=text[i+3]+text[i+4]
                else:
                    datestring=text[i+3]
                date.append(datestring)
            elif is_date(text[i+4])==True:
                cbtstring=text[i+1]+text[i+2]
                cbt.append(cbtstring)
                if text[i+5] != 'PASS':
                    datestring=text[i+4]+text[i+5]
                else:
                    datestring=text[i+4]
                date.append(datestring)
            elif is_date(text[i+5])==True:
                cbtstring=text[i+1]+text[i+2]+text[i+3]
                cbt.append(cbtstring)
                if text[i+6] != 'PASS':
                    datestring=text[i+5]+text[i+6]
                else:
                    datestring=text[i+5]
                date.append(datestring)

    email=text[2].replace(u'\xa0', '#').replace('Org', '#').split('#')[1]

    #parse dates to datetime
    for i in range(len(date)):
        date[i]=parse(date[i])

    user=User.query.filter_by(email=email).first()

    #build list of cbt's from columns
    m=Mobility.query.filter_by(username=user.username).first()
    cbt_entries=[]
    for head in m.__table__.columns:
        if 'cbt' in head.name:
            cbt_entries.append(head.name)
    #make index of cbt's with keywords in inside, but disclude ones with keywords from not_inside
    for head in cbt_entries:
        rules=Rules.query.filter_by(name=head).first()
        args=rules.args
        if args != None:
            args=rules.args.encode('utf-8')
            if '@' in args:
                args=args.split('@')
                inside=args[0].split(' ')
                not_inside=args[1].split(' ')
                del inside[len(inside)-1]
                del not_inside[0]
            else:
                inside=args.split(' ')
                not_inside=['']

        index=[]
        for i in range(len(cbt)):
            if not_inside ==['']:
                if all(x in cbt[i] for x in inside) == True:
                    index.append(i)
            else:
                if all(x in cbt[i] for x in inside) == True and any(x in cbt[i] for x in not_inside) == False:
                    index.append(i)
        if len(index)==0:
            print("Not found")
        elif len(index)>1:
            print("Found multiples")
            dates=[]
            cbts=[]
            for i in index:
                dates.append(date[i])
                cbts.append(cbt[i])
            biggest=parse('1969-06-09')
            for i in range(len(cbts)):
                if dates[i]>biggest:
                    biggest=dates[i]
                    index=i
            setattr(m,head,dates[index])
        else:
            print("Found 1")
            setattr(m,head,date[index[0]])

    db.session.commit()
    flash("Updated CBTs for " + user.username)

'''
(u'*DoD IAA CyberAwarenessChallenge V3.0 (ZZ133098)', u'1/26/2017 1:32:16PM')
(u'*Force Protection(ZZ133079)', u'1/27/2017 12:58:46PM')
(u'*Human Relations (ZZ133080) - NOLONGER AVAILABLE', u'1/27/2017 1:10:33PM')
(u'*Protecting SensitiveInformation (Formerly Security Administration) (ZZ133078)- NOLONGER AVAILABLE', u'1/27/2017 1:14:07PM')
(u'*Religious Freedom Training(ZZ133109)', u'6/29/2016 8:43:39AM')
(u'*Suicide Prevention (forBargaining Civilians Only) (ZZ133113) - NO LONGERAVAILABLE', u'1/3/2017 12:03:20PM')
(u'AEF Pre-Deployment SexualAssault Prevention and Response Training Course(Deactivated12/09/2015)', u'11/30/2015 12:51:05PM')
(u'AETC - Protection of thePresident (#ZZ133005)', u'8/16/2011 12:03:02PM')
(u'AF Counter IED Advanced - Fusion- Breaking the Cycle Video', u'8/25/2015 3:10:33PM')
(u'AF Counter-Improvised ExplosiveDevice (C-IED) Awareness (DEACTIVATED 30 Apr 16)', u'8/24/2015 12:35:34PM')
(u'Air Force Culture General Course(ZZ133104)', u'3/6/2015 2:50:04PM')
(u'Air Force Risk ManagementFundamentals Course', u'9/3/2013 10:35:33AM')
(u'Biometrics Awareness', u'6/17/2015 2:21:03PM')
(u'CBRN Defense Awareness - July2013 (DEACTIVATED 30 Apr 16)', u'11/7/2014 1:33:19PM')
(u'CBRN Defense Awareness v2.0 -PRETEST ONLY - April 2016', u'6/9/2016 3:51:33PM')
(u'CBRN Defense Survival SkillsCompletion (Hands-On)', u'6/28/2016 9:10:04AM')
(u'Collect and ReportInformation', u'3/6/2015 10:38:37AM')
(u'Communication EngagementTraining for Deploying Warfighters', u'1/3/2017 11:11:52AM')
(u'Counterinsurgency (COIN) - Part1', u'11/25/2013 2:25:53PM')
(u"Don't Ask, Don't Tell RepealTraining -- Tier 3", u'3/4/2013 8:17:03AM')
(u'Environmental Management System- General Awareness Training', u'9/3/2013 1:31:19PM')
(u'Equal Opportunity and Preventionof Sexual Harassment Deployment Briefing', u'1/3/2017 11:12:25AM')
(u'Expeditionary Active ShooterTraining (Hands On)', u'11/12/2015 9:42:46AM')
(u'Explosive Ordnance', u'2016')
(u'Explosive OrdnanceReconnaissance (EOR) v2.0 (DEACTIVATED 1 Dec 2016)', u'3/6/2015 10:16:50AM')
(u'Free Exercise of Religion -Supervisor Trng (ZZ133110)', u'3/4/2013 8:23:05AM')
(u'Intelligence Oversight **Courseis now Offline Training**', u'12/8/2016 11:49:00AM')
(u'L6 - AF Physical Training Leader- Advanced Certification', u'5/7/2015 7:38:48AM')
(u'L6 - Use of Force V2.0**NowAvailable on GoLearn**', u'6/18/2015 10:02:00AM')
(u'Law of Armed Conflict (LOAC) -2014', u'3/6/2015 10:28:24AM')
(u'Mental Health Pre-DeploymentTraining - Leadership (E5 and above)', u'4/1/2015 8:56:29AM')
(u'Operation OPSEC Awareness **NoLonger Available**', u'9/6/2016 1:32:47PM')
(u'Professional and UnprofessionalRelationships', u'1/3/2017 11:10:45AM')
(u'RT \u2013 LSN Balance YourThinking', u'2/27/2015 10:51:11AM')
(u'RT \u2013 LSN Interpersonal ProblemSolving', u'2/27/2015 11:00:00AM')
(u'SAPR Annual Training2014', u'6/4/2014 1:44:34PM')
(u'SAPR Annual Training2015', u'4/3/2015 11:50:35AM')
(u'SAPR Annual Training2016', u'6/2/2016 1:22:26PM')
(u'SERE 100, Level B - Code ofConduct', u'9/29/2011 1:29:49PM')
(u'SERE 100.2 (JKO course#J3TA-US1329)', u'11/18/2015 10:50:48AM')
(u'Self-Aid and Buddy Care(SABC)', u'6/1/2015 10:50:04AM')
(u'Self-aid Buddy Care(Hands-On)', u'6/30/2015 2:42:06PM')
(u'Suicide Prevention(Face-to-Face) Training (ZZ133113)', u'1/20/2016 12:45:07PM')
(u'Supervisor Safety Course(ZZ13212)', u'2/13/2017 11:30:32AM')
(u'Traumatic Brain Injury (TBI)Awareness For Deploying Leaders and Commanders', u'6/18/2015 10:04:51AM')
(u'USCENTCOM AF CultureSpecific-Afghanistan', u'3/6/2015 10:51:18AM')
(u'USCENTCOM AF CultureSpecific-Iraq', u'3/6/2015 11:10:16AM')
(u'*Airfield Driving', u'5/12/2015 2:09:30PM')
(u'*DoD IAA CyberAwarenessChallenge (ZZ133098)', u'4/29/2013 11:59:55AM')
(u'*DoD IAA CyberAwarenessChallenge V2.0 (ZZ133098)', u'6/18/2015 9:19:33AM')
(u'*DoD IAA CyberAwarenessChallenge V3.0 (ZZ133098)', u'6/27/2016 3:05:41PM')
(u'*DoD Information AssuranceAwareness (ZZ133098) v10', u'6/16/2011 3:12:15PM')
(u'*Force Protection(ZZ133079)', u'6/27/2016 12:18:22PM')
(u'*Human Relations(ZZ133080)', u'6/27/2016 3:19:07PM')
(u'*Information Protection(ZZ133078)', u'9/12/2013 9:36:34AM')
(u'*Protecting SensitiveInformation (Formerly Security Administration)(ZZ133078)', u'6/29/2016 9:29:04AM')
(u'*Religious Freedom Training(ZZ133109)', u'10/28/2014 9:53:33AM')
(u'*Security Administration(Formerly Information Protection) (ZZ133078)', u'3/25/2015 3:15:18PM')
(u'*Suicide Awareness(ZZ133113)', u'8/16/2011 2:08:08PM')
(u'*Suicide Prevention(ZZ133113)', u'9/12/2013 10:29:37AM')
(u'*Suicide Prevention (forBargaining Civilians Only) (ZZ133113)', u'11/30/2015 1:26:16PM')
(u'*Suicide Prevention (in 2015 forBargaining Civilians Only) (ZZ133113)', u'3/25/2015 3:39:38PM')
(u'AEF Pre-Deployment SexualAssault Prevention and Response Training Course', u'3/6/2015 11:32:49AM')
(u'AETC - Use of Force', u'10/28/2014 3:19:19PM')
(u'AF Counter IED Advanced - Fusion- Breaking the Cycle Video', u'12/5/2013 2:42:29PM')
(u'AF Counter-Improvised ExplosiveDevice (C-IED) Awareness (ZZ133095) \u2013 Jun 09', u'12/4/2013 1:31:57PM')
(u'Air Force CultureGeneral', u'5/9/2013 1:24:05PM')
(u'Biometrics Awareness Course(ZZ133117)', u'10/2/2013 2:46:25PM')
(u'CBRN Defense Awareness Course(ZZ133039) July 2013', u'4/29/2013 2:22:01PM')
(u'CBRN Defense Survival SkillsCompletion (Hands-On)', u'11/28/2014 2:59:51PM')
(u'Collect and Report Information(20091007) (ZZ133102)', u'4/30/2013 12:19:22PM')
(u'Communication EngagementTraining for Deploying Warfighters', u'3/6/2015 10:39:49AM')
(u'Communication EngagementTraining for Deploying Warfighters (20091007)(ZZ133099)', u'6/3/2013 9:12:47AM')
(u"Don't Ask, Don't Tell RepealTraining -- Tier 3", u'5/23/2011 3:32:38PM')
(u'Environmental Management System- General Awareness Training (ZZ133070)', u'5/11/2012 10:43:19AM')
(u'Equal Opportunity and Preventionof Sexual Harassment Deployment Briefing', u'3/6/2015 10:40:20AM')
(u'Equal Opportunity and Preventionof Sexual Harassment Deployment Briefing (20091007)(ZZ133101)', u'6/3/2013 8:24:51AM')
(u'Explosive Ordnance', u'2016')
(u'Explosive OrdnanceReconnaissance (EOR) Course v2.0 (ZZ133107), Dec 09', u'5/9/2013 1:41:53PM')
(u'Intelligence OversightCourse', u'12/8/2016 11:47:06AM')
(u'Law of Armed Conflict (LOAC) \u20132014', u'4/29/2013 2:37:36PM')
(u'Operation OPSECAwareness', u'12/1/2015 7:02:31AM')
(u'Professional and UnprofessionalRelationships', u'3/6/2015 10:33:25AM')
(u'Professional and UnprofessionalRelationships (October 2014)', u'4/30/2013 12:16:08PM')
(u'SAPR Annual Training2016', u'6/2/2016 9:12:41AM')
(u'SERE 100.1 (JKO Course #:A-US022)', u'2/8/2013 9:45:38PM')
(u'Self-Aid and Buddy Care(ZZ131008)', u'9/24/2013 2:36:22PM')
(u'Sexual Assault Prevention andResponse Training (Stand Down Day I)', u'12/4/2013 1:32:28PM')
(u'Suicide Prevention(Face-to-Face) Training (ZZ133113)', u'1/15/2016 8:40:45AM')
(u'Traumatic Brain Injury (TBI)Awareness For Deploying Leaders and Commanders (ZZ133128)', u'6/18/2015 9:38:31AM')
(u'USCENTCOM AF CultureSpecific-Afghanistan (ZZ133105)', u'6/3/2013 9:24:53AM')
(u'USCENTCOM AF CultureSpecific-Iraq (ZZ133106)', u'6/3/2013 9:32:17AM')
jonathan.snyder.9@us.af.mil
'''