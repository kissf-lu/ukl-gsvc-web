/**
 * Created by wang.ding on 2017/4/5.
 */


/**=================================================
 *            Select2FuncBase
 * =================================================
 * @param select_class :
    * 为select 函数在html中的id标签
 *
 * @param select_data :
    * 为select设置数据源
 * @constructor :
 * .init()为初始化函数
 * .set()为设置参数目前包含placeholder, allowClear参数设置
 *==================================================*/
function Select2FuncBase(select_class, select_data){
    this.selectClass = select_class;
    this.selectData = select_data;
}
Select2FuncBase.prototype.init = function () {
    this.selectClass.select2({
        data: this.selectData
    });
};
Select2FuncBase.prototype.set = function (placeholder_str, if_allow_clear) {
    this.selectClass.select2({
        placeholder: placeholder_str||' ',
        allowClear: if_allow_clear||true
    });
};
/**=======================================================
 *                          appendAlertInfo api
 *=========================================================
 * @param alert_type :
    * 设置告警栏的class属性
 * @param info_str :
    * 设置告警栏的内容
 * @param alert_id :
    * 告警栏在html中的标签id
 *========================================================== */
function appendAlertInfo(alert_type, info_str, alert_id){
    var alertHTML = (
    '<div '+'class='+ ['"','alert alert-', alert_type, '"'].join('') + 'role="alert">' +
    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">'+
    '<span aria-hidden="true">&times;</span>'+
    '</button>'+
    '<strong>'+info_str+'</strong> '+
    '</div>');
    // remove old form html
    alert_id.children().remove();
    // append new form html
    alert_id.append(alertHTML);
}
//
/**=============================================
 *         Mydaterange API
 *         ：完成date range picker 插件的初始化设置
 * =============================================
 * @param number :
    * 与time参数配合使用，如：time_type='h', number=7 ,表示距今7小时
 * @param time_type  :
    * moment().subtract 函数调用time_type 用于设置起始时间距今距离类型: 'h':hour, 'd':day
 * @param timeSelector :
    * 为date range time 在html中的id
 * @constructor initTime() 初始化函数,
 *====================================================*/
function Mydaterange(number, time_type, timeSelector){
    this.begintime = moment().subtract(number, time_type);
    this.timeSelector = timeSelector;
}
/**
 *
 * @param set_time :
    * 设置日期，格式为{'date': 11,'hour': 16,'minute': 0, 'second': 0}
 *========================================================*/
Mydaterange.prototype.initTime = function (set_time, set_format, if_hour) {
    if((if_hour) || (if_hour ===undefined)){
        time_picker = true
    } else {
        time_picker = if_hour
    }
    this.timeSelector.daterangepicker({
        showDropdowns: true,
        timePicker: time_picker,
        timePicker24Hour: true,
        singleDatePicker: true,
        startDate: this.begintime.set(set_time||{'minute': 0, 'second': 0}),
        locale: {
        format: set_format||"YYYY-MM-DD HH:mm:ss",
        applyLabel: "确定",
        cancelLabel: "取消",
        daysOfWeek: ["周日","周一","周二","周三","周四","周五","周六"],
        monthNames: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
        firstDay: 1
    }
    });
};
/**=========================================================================================
 *
 * =========================================================================================
 * @param selector
 * @param appendContainer
 * @param autoCloseDelay
 * @param autoClose
 * @param content
 * @constructor
 *==========================================================================================*/
function Notificationbar(selector,appendContainer,autoCloseDelay,autoClose,content) {
    this.selector = selector;
    this.appendContainer = appendContainer;
    this.autoCloseDelay = autoCloseDelay;
    this.autoClose = autoClose;
    this.content = content;
}
Notificationbar.prototype.init = function () {
   //初始化通知
   this.selector.jqxNotification({
       width: "100%",
       position: "top-right",
       blink: true ,
       appendContainer: this.appendContainer,
       opacity: 0.9,
       autoOpen: false,
       animationOpenDelay: 800,
       autoClose: this.autoClose,   //控制显示与隐藏
       autoCloseDelay: this.autoCloseDelay,
       template: "info"
    });
   return this
};
Notificationbar.prototype.notificationContent = function (notifi_content) {
    //通知内容设置
    this.content.children().detach();
    this.content.append(notifi_content);
    return this
};
Notificationbar.prototype.notificationAction = function (action_flag) {
    //可视化操作
    this.selector.jqxNotification(action_flag);
};

function AjaxJsonFunc(ajax_param, ajax_id) {
    this.ajaxParam = ajax_param;
    this.id = ajax_id;
}
AjaxJsonFunc.prototype.core = function () {
    $.ajax({
        type: this.ajaxParam.type,
        //get方法url地址
        url: this.ajaxParam.url,
        //request set
        contentType: "application/json",
        //data参数
        data: JSON.stringify(this.ajaxParam.postData),
        //server back data type
        dataType: "json"
    })
        .done(function (data) {
            var getData = data;
            if (getData.data.length === 0) {
                if (getData.info.err) {
                    //delete old alter
                    appendAlertInfo(
                        'danger',
                        ['Error:', getData.info.errinfo].join(' '),
                        this.id.queryAlert);
                }
                else {
                    appendAlertInfo(
                        'warning',
                        '无查询结果!',
                        this.id.queryAlert);
                }
            }
            else {
                var GridArrayData = [];
                appendAlertInfo(
                    'success',
                    ['查询完成，', '结果如下：'].join(' '),
                    this.id.queryAlert);
                $.each(getData.data, function (i, item) {
                     GridArrayData.push({
                        country: item.country,
                        imsi: item.imsi,
                        iccid: item.iccid,
                        package_type_name: item.package_type_name,
                        next_update_time: item.next_update_time,
                        bam: item.bam,
                        imsi_con: item.imsi_con,
                        imei_con: item.imei_con,
                        Flower: item.Flower,
                        err: item.err
                    });
                });//each函数完成
                return GridArrayData;
            }
        })
        .fail(function (jqXHR, status) {
            appendAlertInfo(
                'warning',
                ['Servers False:', jqXHR, status].join(' '),
                this.id.queryAlert);
        })
        .always(function () {
            ProQueryjqxNotification.notificationAction('closeLast');
            this.id.queryBt.attr("disabled", false);
        });
};
AjaxJsonFunc.prototype.doneAjax = function (call_back_item) {

};