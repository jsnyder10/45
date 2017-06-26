from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
mobility = Table('mobility', post_meta,
    Column('username', String, primary_key=True, nullable=False),
    Column('cc_letter', String(length=45)),
    Column('sabc_cbt', DateTime),
    Column('sabc_hands_on', DateTime),
    Column('cbrn_cbt', DateTime),
    Column('cbrn_hands_on', DateTime),
    Column('mri_hri', DateTime),
    Column('qnft', String(length=45)),
    Column('dog_tags', Boolean),
    Column('vred', DateTime),
    Column('form_2760', DateTime),
    Column('small_arms', DateTime),
    Column('pt_excellence', Integer),
    Column('pt_score', Numeric),
    Column('security_clearance', DateTime),
    Column('form_55', DateTime),
    Column('dod_iaa_cyber', DateTime),
    Column('force_protection', DateTime),
    Column('human_relations', DateTime),
    Column('protecting_info', DateTime),
    Column('green_dot', DateTime),
    Column('af_c_ied_video', DateTime),
    Column('af_c_ied_awrns', DateTime),
    Column('af2a_culture', DateTime),
    Column('biometrics', DateTime),
    Column('collect_and_report', DateTime),
    Column('east', DateTime),
    Column('eor', DateTime),
    Column('free_ex_of_religion', DateTime),
    Column('loac', DateTime),
    Column('mental_health', DateTime),
    Column('tbi_awareness', DateTime),
    Column('uscentcom_cult', DateTime),
    Column('unauthorized_disclosure', DateTime),
    Column('deriv_class', DateTime),
    Column('marking_class_info', DateTime),
    Column('sere_100_cst', DateTime),
    Column('cac_expiration', DateTime),
    Column('gtc_expiration', DateTime),
    Column('line_badge', Numeric),
    Column('bus_license', DateTime),
    Column('edi', Numeric),
    Column('drug_pref', String(length=45)),
    Column('afsc', String(length=5)),
    Column('pt_test', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mobility'].columns['af2a_culture'].create()
    post_meta.tables['mobility'].columns['af_c_ied_awrns'].create()
    post_meta.tables['mobility'].columns['af_c_ied_video'].create()
    post_meta.tables['mobility'].columns['afsc'].create()
    post_meta.tables['mobility'].columns['biometrics'].create()
    post_meta.tables['mobility'].columns['bus_license'].create()
    post_meta.tables['mobility'].columns['cac_expiration'].create()
    post_meta.tables['mobility'].columns['cbrn_cbt'].create()
    post_meta.tables['mobility'].columns['cbrn_hands_on'].create()
    post_meta.tables['mobility'].columns['collect_and_report'].create()
    post_meta.tables['mobility'].columns['deriv_class'].create()
    post_meta.tables['mobility'].columns['dod_iaa_cyber'].create()
    post_meta.tables['mobility'].columns['dog_tags'].create()
    post_meta.tables['mobility'].columns['drug_pref'].create()
    post_meta.tables['mobility'].columns['east'].create()
    post_meta.tables['mobility'].columns['edi'].create()
    post_meta.tables['mobility'].columns['eor'].create()
    post_meta.tables['mobility'].columns['force_protection'].create()
    post_meta.tables['mobility'].columns['form_2760'].create()
    post_meta.tables['mobility'].columns['form_55'].create()
    post_meta.tables['mobility'].columns['free_ex_of_religion'].create()
    post_meta.tables['mobility'].columns['green_dot'].create()
    post_meta.tables['mobility'].columns['gtc_expiration'].create()
    post_meta.tables['mobility'].columns['human_relations'].create()
    post_meta.tables['mobility'].columns['line_badge'].create()
    post_meta.tables['mobility'].columns['loac'].create()
    post_meta.tables['mobility'].columns['marking_class_info'].create()
    post_meta.tables['mobility'].columns['mental_health'].create()
    post_meta.tables['mobility'].columns['mri_hri'].create()
    post_meta.tables['mobility'].columns['protecting_info'].create()
    post_meta.tables['mobility'].columns['pt_excellence'].create()
    post_meta.tables['mobility'].columns['pt_score'].create()
    post_meta.tables['mobility'].columns['pt_test'].create()
    post_meta.tables['mobility'].columns['qnft'].create()
    post_meta.tables['mobility'].columns['sabc_hands_on'].create()
    post_meta.tables['mobility'].columns['security_clearance'].create()
    post_meta.tables['mobility'].columns['sere_100_cst'].create()
    post_meta.tables['mobility'].columns['small_arms'].create()
    post_meta.tables['mobility'].columns['tbi_awareness'].create()
    post_meta.tables['mobility'].columns['unauthorized_disclosure'].create()
    post_meta.tables['mobility'].columns['uscentcom_cult'].create()
    post_meta.tables['mobility'].columns['vred'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['mobility'].columns['af2a_culture'].drop()
    post_meta.tables['mobility'].columns['af_c_ied_awrns'].drop()
    post_meta.tables['mobility'].columns['af_c_ied_video'].drop()
    post_meta.tables['mobility'].columns['afsc'].drop()
    post_meta.tables['mobility'].columns['biometrics'].drop()
    post_meta.tables['mobility'].columns['bus_license'].drop()
    post_meta.tables['mobility'].columns['cac_expiration'].drop()
    post_meta.tables['mobility'].columns['cbrn_cbt'].drop()
    post_meta.tables['mobility'].columns['cbrn_hands_on'].drop()
    post_meta.tables['mobility'].columns['collect_and_report'].drop()
    post_meta.tables['mobility'].columns['deriv_class'].drop()
    post_meta.tables['mobility'].columns['dod_iaa_cyber'].drop()
    post_meta.tables['mobility'].columns['dog_tags'].drop()
    post_meta.tables['mobility'].columns['drug_pref'].drop()
    post_meta.tables['mobility'].columns['east'].drop()
    post_meta.tables['mobility'].columns['edi'].drop()
    post_meta.tables['mobility'].columns['eor'].drop()
    post_meta.tables['mobility'].columns['force_protection'].drop()
    post_meta.tables['mobility'].columns['form_2760'].drop()
    post_meta.tables['mobility'].columns['form_55'].drop()
    post_meta.tables['mobility'].columns['free_ex_of_religion'].drop()
    post_meta.tables['mobility'].columns['green_dot'].drop()
    post_meta.tables['mobility'].columns['gtc_expiration'].drop()
    post_meta.tables['mobility'].columns['human_relations'].drop()
    post_meta.tables['mobility'].columns['line_badge'].drop()
    post_meta.tables['mobility'].columns['loac'].drop()
    post_meta.tables['mobility'].columns['marking_class_info'].drop()
    post_meta.tables['mobility'].columns['mental_health'].drop()
    post_meta.tables['mobility'].columns['mri_hri'].drop()
    post_meta.tables['mobility'].columns['protecting_info'].drop()
    post_meta.tables['mobility'].columns['pt_excellence'].drop()
    post_meta.tables['mobility'].columns['pt_score'].drop()
    post_meta.tables['mobility'].columns['pt_test'].drop()
    post_meta.tables['mobility'].columns['qnft'].drop()
    post_meta.tables['mobility'].columns['sabc_hands_on'].drop()
    post_meta.tables['mobility'].columns['security_clearance'].drop()
    post_meta.tables['mobility'].columns['sere_100_cst'].drop()
    post_meta.tables['mobility'].columns['small_arms'].drop()
    post_meta.tables['mobility'].columns['tbi_awareness'].drop()
    post_meta.tables['mobility'].columns['unauthorized_disclosure'].drop()
    post_meta.tables['mobility'].columns['uscentcom_cult'].drop()
    post_meta.tables['mobility'].columns['vred'].drop()
