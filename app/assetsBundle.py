# -*- coding: utf-8 -*-

from flask_assets import Bundle


login_css = Bundle(
    'css/auth/styles.css',
    filters='cssmin',
    output='css/gsvc_login.css'
)
main_css = Bundle(
    'css/main/style.css',
    filters='cssmin',
    output='css/gsvc_main.css'
)
main_js = Bundle(
    'js/main/inspinia.js',
    filters='jsmin',
    output='js/gsvc_main.js'
)
home_js = Bundle(
    # ("-- customer js --")
    'js/home/home-demo.js',
    filters='jsmin',
    output='js/home/gsvc_home.js'
)
vsimFlowerQuery_js = Bundle(
    # ("-- customer js --")
    'js/main/demo/vsimFlowerQuery-demo.js',

    filters='jsmin',
    output='js/gsvc_vsimFlowerQuery.js'
)
probVsimFirstDict_js = Bundle(
    'js/main/demo/probVsimFirstDict-demo.js',
    filters='jsmin',
    output='js/gsvc_probVsimFirstDict.js'
)
vsimmanual_js = Bundle(
    # ("--vsimmanul-demo js--")
    'js/main/demo/vsimmanul02_demo.js',
    'js/main/demo/ManualDataBaseUpdate-demo.js',
    filters='jsmin',
    output='js/gsvc_vsimmanual.js'
)
muticountry140_js = Bundle(
    # (<!--定制脚本-->)
    'js/main/demo/140countryFlowerStatic-demo.js',
    filters='jsmin',
    output='js/gsvc_muticountry140.js'
)
uploadfiles_js = Bundle(
    # <!--定制脚本-->
    'js/main/demo/test_upfiles.js',
    filters='cssmin',
    output='js/gsvc_uploadfiles.js'
)
new_vsim_test_info_js = Bundle(
    # ("--vsimmanul-demo js--")
    'js/main/demo/newVsimInfoTable-demo.js',
    'js/main/demo/newVsimTestTableUpdate-demo.js',
    filters='jsmin',
    output='js/gsvc_new_vsim_test_info.js'
)
jqwidgets_globle_css = Bundle(
    # ("-- jqx css --")
    'css/jqxGrid/jqx.base.css',
    filters='cssmin',
    output='css/jqwidgets/gsvc_jqwidgets.min.css'
)
jqwidgets_globle_js = Bundle(
    # ("--jqwidgets js--")
    'js/jqwidgets/jqxcore.js',
    'js/jqwidgets/jqxgrid.js',
    'js/jqwidgets/jqxdata.js',
    'js/jqwidgets/jqxgrid.gsvc.js',
    'js/jqwidgets/localization.zh-CN.js',
    filters='jsmin',
    output='js/jqwidgets/gsvc_jqwidgets.min.js'
)
