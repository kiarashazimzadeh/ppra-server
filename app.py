from flask import Flask, render_template, flash, redirect, url_for, session, logging, request, send_file
from flask_mysqldb import MySQL
from wtforms import Form, StringField, SelectField, FloatField, EmailField, PasswordField, SubmitField, validators
from passlib.hash import sha256_crypt
import pandas as pd
import numpy as np
import math
import locale
import jdatetime

app = Flask(__name__)

# Locale date
locale.setlocale(locale.LC_ALL, "fa_IR.utf8")
date = jdatetime.datetime.now().strftime("%Y/%d/%m")

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hGTrDAfF8zY'
app.config['MYSQL_DB'] = 'application'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# MySQL initialization
mysql = MySQL(app)

class LaboratoryData(Form):
    user_first_name = StringField('نام', [
        validators.Length(max=100),
        validators.Regexp('^[‌ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+$', message=('به فارسی بنویسید.')),
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    user_last_name = StringField('نام خانوادگی', [
        validators.Length(max=100),
        validators.Regexp('^[‌ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+$', message=('به فارسی بنویسید.')),
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    entry_date = StringField('تاریخ ثبت داده‌ها', render_kw={'readonly': True, 'placeholder': date})
    lab_name = StringField('نام آزمایشگاه', [
        validators.Length(max=100),
        validators.Regexp('^[‌ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+$', message=('به فارسی بنویسید.')),
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})    
    tech_first_name = StringField('نام کارشناس', [
        validators.Length(max=100),
        validators.Regexp('^[‌ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+$', message=('به فارسی بنویسید.')),
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    tech_last_name = StringField('نام خانوادگی کارشناس', [
        validators.Length(max=100),
        validators.Regexp('^[‌ آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی]+$', message=('به فارسی بنویسید.')),
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    station_id = SelectField('نام ایستگاه', [
        validators.InputRequired(message=('این مورد ضروری است.'))], choices=[('1', 'ایستگاه ۱'), ('2', 'ایستگاه ۲'), ('3', 'ایستگاه ۳')])
    measur_start_date = StringField('تاریخ شروع اندازه‌گیری', [
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    measur_end_date = StringField('تاریخ پایان اندازه‌گیری', [
        validators.InputRequired(message=('این مورد ضروری است.'))], render_kw={'required': False})
    fd = FloatField('میزان غبار ریزشی در ماه اندازه‌گیری', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    ag_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    ag_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    al_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    al_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    as_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    as_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    ba_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    ba_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    be_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    be_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    cd_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    cd_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    co_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    co_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    cr_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    cr_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    cu_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    cu_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    f_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    f_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    fe_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    fe_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    hg_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    hg_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    mo_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    mo_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    ni_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    ni_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    pb_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    pb_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    sb_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    sb_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    se_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    se_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    sn_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    sn_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    ti_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    ti_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    v_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    v_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    zn_ci = FloatField('Ci', [
        validators.InputRequired(message=('این مورد ضروری است.'))],
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False })
    zn_local_ci = FloatField('Local Ci', 
        render_kw = { 'step': '0.1', 'min': '0', 'type': 'number', 'required': False, 'value': '0' })
    submit = SubmitField('ثبت داده‌ها')

@app.route("/", methods=['GET', 'POST'])
def main():
    form = LaboratoryData(request.form)

    if request.method == 'POST' and form.validate():
        user_first_name = form.user_first_name.data
        user_last_name = form.user_last_name.data
        entry_date = form.entry_date.data
        lab_name = form.lab_name.data
        tech_first_name = form.tech_first_name.data
        tech_last_name = form.tech_last_name.data
        station_id = form.station_id.data
        measur_start_date = form.measur_start_date.data
        measur_end_date = form.measur_end_date.data
        ag_ci = form.ag_ci.data
        ag_local_ci = form.ag_local_ci.data
        al_ci = form.al_ci.data
        al_local_ci = form.al_local_ci.data
        as_ci = form.as_ci.data
        as_local_ci = form.as_local_ci.data
        ba_ci = form.ba_ci.data
        ba_local_ci = form.ba_local_ci.data
        be_ci = form.be_ci.data
        be_local_ci = form.be_local_ci.data
        cd_ci = form.cd_ci.data
        cd_local_ci = form.cd_local_ci.data
        co_ci = form.co_ci.data
        co_local_ci = form.co_local_ci.data
        cr_ci = form.cr_ci.data
        cr_local_ci = form.cr_local_ci.data
        cu_ci = form.cu_ci.data
        cu_local_ci = form.cu_local_ci.data
        f_ci = form.f_ci.data
        f_local_ci = form.f_local_ci.data
        fe_ci = form.fe_ci.data
        fe_local_ci = form.fe_local_ci.data
        hg_ci = form.hg_ci.data
        hg_local_ci = form.hg_local_ci.data
        mo_ci = form.mo_ci.data
        mo_local_ci = form.mo_local_ci.data
        ni_ci = form.ni_ci.data
        ni_local_ci = form.ni_local_ci.data
        pb_ci = form.pb_ci.data
        pb_local_ci = form.pb_local_ci.data
        sb_ci = form.sb_ci.data
        sb_local_ci = form.sb_local_ci.data
        se_ci = form.se_ci.data
        se_local_ci = form.se_local_ci.data
        sn_ci = form.sn_ci.data
        sn_local_ci = form.sn_local_ci.data
        ti_ci = form.ti_ci.data
        ti_local_ci = form.ti_local_ci.data
        v_ci = form.v_ci.data
        v_local_ci = form.v_local_ci.data
        zn_ci = form.zn_ci.data
        zn_local_ci = form.zn_local_ci.data

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO lab_data (user_first_name, user_last_name, lab_name, tech_first_name, tech_last_name, station_id, measur_start_date, measur_end_date, ag_ci, ag_local_ci, al_ci, al_local_ci, as_ci, as_local_ci, ba_ci, ba_local_ci, be_ci, be_local_ci, cd_ci, cd_local_ci, co_ci, co_local_ci, cr_ci, cr_local_ci, cu_ci, cu_local_ci, f_ci, f_local_ci, fe_ci, fe_local_ci, hg_ci, hg_local_ci, mo_ci, mo_local_ci, ni_ci, ni_local_ci, pb_ci, pb_local_ci, sb_ci, sb_local_ci, se_ci, se_local_ci, sn_ci, sn_local_ci, ti_ci, ti_local_ci, v_ci, v_local_ci, zn_ci, zn_local_ci) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (user_first_name, user_last_name, lab_name, tech_first_name, tech_last_name, station_id, measur_start_date, measur_end_date, ag_ci, ag_local_ci, al_ci, al_local_ci, as_ci, as_local_ci, ba_ci, ba_local_ci, be_ci, be_local_ci, cd_ci, cd_local_ci, co_ci, co_local_ci, cr_ci, cr_local_ci, cu_ci, cu_local_ci, f_ci, f_local_ci, fe_ci, fe_local_ci, hg_ci, hg_local_ci, mo_ci, mo_local_ci, ni_ci, ni_local_ci, pb_ci, pb_local_ci, sb_ci, sb_local_ci, se_ci, se_local_ci, sn_ci, sn_local_ci, ti_ci, ti_local_ci, v_ci, v_local_ci, zn_ci, zn_local_ci))
        mysql.connection.commit()
        
        cur.execute("SELECT ag_cn, ag_tr, al_cn, al_tr, as_cn, as_tr, ba_cn, ba_tr, be_cn, be_tr, cd_cn, cd_tr, co_cn, co_tr, cr_cn, cr_tr, cu_cn, cu_tr, f_cn, f_tr, fe_cn, fe_tr, hg_cn, hg_tr, mo_cn, mo_tr, ni_cn, ni_tr, pb_cn, pb_tr, sb_cn, sb_tr, se_cn, se_tr, sn_cn, sn_tr, ti_cn, ti_tr, v_cn, v_tr, zn_cn, zn_tr FROM er_ref_values")
        er_ref_values = cur.fetchone()

        ag_cn = er_ref_values["ag_cn"]
        ag_tr = er_ref_values["ag_tr"]
        al_cn = er_ref_values["al_cn"]
        al_tr = er_ref_values["al_tr"]
        as_cn = er_ref_values["as_cn"]
        as_tr = er_ref_values["as_tr"]
        ba_cn = er_ref_values["ba_cn"]
        ba_tr = er_ref_values["ba_tr"]
        be_cn = er_ref_values["be_cn"]
        be_tr = er_ref_values["be_tr"]
        cd_cn = er_ref_values["cd_cn"]
        cd_tr = er_ref_values["cd_tr"]
        co_cn = er_ref_values["co_cn"]
        co_tr = er_ref_values["co_tr"]
        cr_cn = er_ref_values["cr_cn"]
        cr_tr = er_ref_values["cr_tr"]
        cu_cn = er_ref_values["cu_cn"]
        cu_tr = er_ref_values["cu_tr"]
        f_cn = er_ref_values["f_cn"]
        f_tr = er_ref_values["f_tr"]
        fe_cn = er_ref_values["fe_cn"]
        fe_tr = er_ref_values["fe_tr"]
        hg_cn = er_ref_values["hg_cn"]
        hg_tr = er_ref_values["hg_tr"]
        mo_cn = er_ref_values["mo_cn"]
        mo_tr = er_ref_values["mo_tr"]
        ni_cn = er_ref_values["ni_cn"]
        ni_tr = er_ref_values["ni_tr"]
        pb_cn = er_ref_values["pb_cn"]
        pb_tr = er_ref_values["pb_tr"]
        sb_cn = er_ref_values["sb_cn"]
        sb_tr = er_ref_values["sb_tr"]
        se_cn = er_ref_values["se_cn"]
        se_tr = er_ref_values["se_tr"]
        sn_cn = er_ref_values["sn_cn"]
        sn_tr = er_ref_values["sn_tr"]
        ti_cn = er_ref_values["ti_cn"]
        ti_tr = er_ref_values["ti_tr"]
        v_cn = er_ref_values["v_cn"]
        v_tr = er_ref_values["v_tr"]
        zn_cn = er_ref_values["zn_cn"]
        zn_tr = er_ref_values["zn_tr"]
        f_cn = er_ref_values["f_cn"]
        f_tr = er_ref_values["f_tr"]
        fe_cn = er_ref_values["fe_cn"]
        fe_tr = er_ref_values["fe_tr"]
        hg_cn = er_ref_values["hg_cn"]
        hg_tr = er_ref_values["hg_tr"]
        mo_cn = er_ref_values["mo_cn"]
        mo_tr = er_ref_values["mo_tr"]
        ni_cn = er_ref_values["ni_cn"]
        ni_tr = er_ref_values["ni_tr"]
        pb_cn = er_ref_values["pb_cn"]
        pb_tr = er_ref_values["pb_tr"]
        sb_cn = er_ref_values["sb_cn"]
        sb_tr = er_ref_values["sb_tr"]
        se_cn = er_ref_values["se_cn"]
        se_tr = er_ref_values["se_tr"]
        sn_cn = er_ref_values["sn_cn"]
        sn_tr = er_ref_values["sn_tr"]
        ti_cn = er_ref_values["ti_cn"]
        ti_tr = er_ref_values["ti_tr"]
        v_cn = er_ref_values["v_cn"]
        v_tr = er_ref_values["v_tr"]
        zn_cn = er_ref_values["zn_cn"]
        zn_tr = er_ref_values["zn_tr"]
        test = 5

        cur.close()

        df_er = pd.DataFrame(data = [[ag_ci, ag_local_ci, ag_cn, ag_tr], [al_ci, al_local_ci, al_cn, al_tr], [as_ci, as_local_ci, as_cn, as_tr], [ba_ci, ba_local_ci, ba_cn, ba_tr], [be_ci, be_local_ci, be_cn, be_tr], [cd_ci, cd_local_ci, cd_cn, cd_tr], [co_ci, co_local_ci, co_cn, co_tr], [cr_ci, cr_local_ci, cr_cn, cr_tr], [cu_ci, cu_local_ci, cu_cn, cu_tr], [f_ci, f_local_ci, f_cn, f_tr], [fe_ci, fe_local_ci, fe_cn, fe_tr], [hg_ci, hg_local_ci, hg_cn, hg_tr], [mo_ci, mo_local_ci, mo_cn, mo_tr], [ni_ci, ni_local_ci, ni_cn, ni_tr], [pb_ci, pb_local_ci, pb_cn, pb_tr], [sb_ci, sb_local_ci, sb_cn, sb_tr], [se_ci, se_local_ci, se_cn, se_tr], [sn_ci, sn_local_ci, sn_cn, sn_tr], [ti_ci, ti_local_ci, ti_cn, ti_tr], [v_ci, v_local_ci, v_cn, v_tr], [zn_ci, zn_local_ci, zn_cn, zn_tr]], columns = ['Ci', 'Local Ci', 'Cn', 'TR'], index = ["Ag", "Al", "As", "Ba", "Be", "Cd", "Co", "Cr", "Cu", "F", "Fe", "Hg", "Mo", "Ni", "Pb", "Sb", "Se", "Sn", "Ti", "V", "Zn"])

        df_er = df_er.replace(0,np.nan)

        def EF(cn, ci):
            EF = (cn/82000) / (ci/82300)
            return EF
        df_er['EF'] = np.vectorize(EF)(df_er['Cn'], df_er['Ci']).round(2)
        def ef_labeler(ef):
            if ef < 2:
                return 'mild enrichment'
            elif ef >= 2 and ef < 5:
                return 'moderate enrichment'
            elif ef >= 5 and ef < 20:
                return 'high enrichment'
            elif ef >= 20 and ef < 40:
                return 'very high enrichment'
            elif ef >= 40:
                return 'extreme enrichment'
            else:
                return 'error'
        df_er['EF_Label'] = np.vectorize(ef_labeler)(df_er['EF'])
        df_er['Local EF'] = np.vectorize(EF)(df_er['Cn'], df_er['Local Ci']).round(2)
        df_er['Local EF_Label'] = np.vectorize(ef_labeler)(df_er['Local EF'])

        df_er['CF'] = (df_er['Ci']/df_er['Cn']).round(2)
        def cf_labeler(cf):
            if cf < 1:
                return "no contamination"
            elif cf > 1 and cf < 2:
                return 'no to moderate contamination'
            elif cf > 2 and cf < 3:
                return "moderate contamination"
            elif cf > 3 and cf < 4:
                return 'moderate to high contamination'
            elif cf > 4 and cf < 5:
                return 'high contamination'
            elif cf > 5 and cf < 6:
                return 'high to extreme contamination'
            elif cf > 6:
                return 'extreme contamination'
            else:
                return 'error'
        df_er['CF_Label'] = np.vectorize(cf_labeler)(df_er['CF'])
        df_er['Local CF'] = (df_er['Local Ci']/df_er['Cn']).round(2)
        df_er['Local CF_Label'] = np.vectorize(cf_labeler)(df_er['Local CF'])

        def igeo(ci, cn):
            l = ci / (cn * 1.5)
            m = math.log2(l)
            return m
        df_er['Igeo'] = np.vectorize(igeo)(df_er['Ci'], df_er['Cn']).round(2)
        def igeo_labeler(i):
            if i < 0:
                return 'class A, not contaminated'
            elif i >= 0 and i < 1:
                return 'class B, none to moderate contamination'
            elif i >= 1 and i < 2:
                return 'class C, moderate contamination'
            elif i >= 2 and i < 3:
                return 'Class D, moderate to high contamination'
            elif i >= 3 and i < 4:
                return 'Class E, high contamination'
            elif i >= 4 and i < 5:
                return 'Class F, very high contamination'
            elif i >= 5:
                return 'Class G, extreme contamination'
            else:
                return "error"
        df_er['Igeo_Label'] = np.vectorize(igeo_labeler)(df_er['Igeo'])
        df_er['Local Igeo'] = np.vectorize(igeo)(df_er['Local Ci'], df_er['Cn']).round(2)
        df_er['Local Igeo_Label'] = np.vectorize(igeo_labeler)(df_er['Local Igeo'])

        MEC = df_er['CF'].mean().round(2)
        df_er['MEC'] = MEC

        df_er['ERP'] = df_er['CF'] * df_er['TR']
        def erp_labeler(e):
            if e < 40:
                return 'low'
            elif e < 80:
                return 'moderate'
            elif e < 160:
                return 'considerable'
            elif e < 320:
                return 'high'
            elif e >= 320:
                return 'very high'
            else:
                return 'error'
        df_er['ERP_Label'] = np.vectorize(erp_labeler)(df_er['ERP'])

        RI = df_er['ERP'].sum()
        df_er['RI'] = RI
        def ri_labeler(r):
            if r < 150:
                return "low"
            elif r < 300:
                return 'moderate'
            elif r < 600:
                return 'high'
            elif r >= 600:
                return 'very high'
            else:
                return 'error'
        df_er['RI_Label'] = np.vectorize(ri_labeler)(df_er['RI'])

        prod = df_er['CF'].prod()
        n = len(df_er)
        PLI = np.power(prod, 1/n).round(2)
        df_er['PLI'] = PLI

        NIPI = np.sqrt(((df_er['CF'].max())**2 + df_er['CF'].mean()) / 2).round(2)
        df_er['NIPI'] = NIPI

        df_er = df_er.fillna(0)

        df_er_total = pd.DataFrame()
        df_er_total[['MEC', 'RI', 'RI_Label', 'PLI', 'NIPI']] = df_er[['MEC', 'RI', 'RI_Label', 'PLI', 'NIPI']]
        df_er_total = df_er_total.loc[['Ag'], :]
        df_er_total = df_er_total.rename(index={'Ag': 'Total'})

        df_er_html = df_er.to_dict('index')
        df_er_total_html = df_er_total.to_dict('records')

        return render_template('results.html', output = df_er_html, output_total = df_er_total_html)
        print(MEC_total)
    
    return render_template('main.html', form = form)
    

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.secret_key='733676397924423F4528482B4D6251655468576D5A7134743777217A25432A46'
    app.run(host='0.0.0.0', debug=True)