/**
 * Created by wang.ding on 2017/4/5.
 */


/**=======================================================
 *                          appendAlertInfo api
 *=========================================================
 * @param alert_class 设置告警栏的class属性
 * @param info_str 设置告警栏的内容
 * @param alert_id 告警栏在html中的标签id
 *===================================================================================*/
function appendAlertInfo(alert_class, info_str, alert_id){

    var alertHTML = (
    alert_class +
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
//初始化小时颗粒度时间面板
function Mydaterange(number,time,timeSelector){
    this.begintime = moment().subtract(number, time);
    this.timeSelector = timeSelector;
}
Mydaterange.prototype.initTime = function () {
    this.timeSelector.daterangepicker({
        showDropdowns: true,
        timePicker: true,
        timePicker24Hour: true,
        singleDatePicker: true,
        startDate: this.begintime,
        locale: {
        format: "YYYY-MM-DD HH:mm:ss",
        applyLabel: "确定",
        cancelLabel: "取消",
        daysOfWeek: ["周日","周一","周二","周三","周四","周五","周六"],
        monthNames: ["1月","2月","3月","4月","5月","6月","7月","8月","9月","10月","11月","12月"],
        firstDay: 1
    }
    });
};
// ---初始化选择/查询通知栏
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
};
Notificationbar.prototype.notificationContent = function (notifi_content) {
    //通知内容设置
    this.content.children().detach();
    this.content.append(notifi_content);
};
Notificationbar.prototype.notificationAction = function (action_flag) {
    //可视化操作
    this.selector.jqxNotification(action_flag);
};