# -*- coding: utf-8 -*-

from flask_assets import Bundle


login_css = Bundle(
    'css/auth/login_auth.css',
    filters='cssmin',
    output='css/auth/gsvc_login.css'
)
main_css = Bundle(
    'css/main/style.css',
    filters='cssmin',
    output='css/main/gsvc_main.css'
)
main_js = Bundle(
    'js/main/inspinia.js',
    filters='jsmin',
    output='js/main/gsvc_main.js'
)
home_js = Bundle(
    # ("-- customer js --")
    'js/home/home-demo.js',
    filters='jsmin',
    output='js/home/gsvc_home.js'
)
vsimFlowerQuery_js = Bundle(
    # ("-- customer js --")
    'js/main/demo/common.js',
    'js/vsim_flower/vsimFlowerQuery-demo.js',
    filters='jsmin',
    output='js/vsim_flower/gsvc_vsimFlowerQuery.js'
)
probVsimFirstDict_js = Bundle(
    'js/prob_vsim_dic/probVsimFirstDict-demo.js',
    filters='jsmin',
    output='js/prob_vsim_dic/gsvc_probVsimFirstDict.js'
)
vsimmanual_js = Bundle(
    # ("--vsimmanul-demo js--")
    'js/vsim_manual_model/vsimmanul02_demo.js',
    'js/vsim_manual_model/UpdateModel-demo.js',
    filters='jsmin',
    output='js/vsim_manual_model/gsvc_vsimmanual.js'
)
muticountry140_js = Bundle(
    # (<!--定制脚本-->)
    'js/mutl_country/140countryFlowerStatic-demo.js',
    filters='jsmin',
    output='js/mutl_country/gsvc_muticountry140.js'
)
uploadfiles_js = Bundle(
    # <!--定制脚本-->
    'js/test_js/test_upfiles.js',
    filters='cssmin',
    output='js/test_js/gsvc_uploadfiles.js'
)
new_vsim_test_info_js = Bundle(
    # ("--vsimmanul-demo js--")
    'js/new_vsim_test_model/newVsimInfoTable-demo.js',
    'js/new_vsim_test_model/newVsimTestTableUpdate-demo.js',
    filters='jsmin',
    output='js/new_vsim_test_model/gsvc_new_vsim_test_info.js'
)
jqwidgets_globle_css = Bundle(
    # ("-- jqx css --")
    'css/jqxGrid/jqx.base.css',
    filters='cssmin',
    output='css/jqxGrid/gsvc_jqwidgets.css'
)
jqwidgets_globle_js = Bundle(
    # ("--jqwidgets js--")
    'js/jqwidgets/jqxcore.js',
    'js/jqwidgets/jqxgrid.js',
    'js/jqwidgets/jqxdata.js',
    'js/jqwidgets/jqxgrid.gsvc.js',
    'js/jqwidgets/localization.zh-CN.js',
    filters='jsmin',
    output='js/jqwidgets/gsvc_jqwidgets.js'
)
