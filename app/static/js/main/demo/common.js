/**
 * Created by wang.ding on 2017/4/5.
 */
//ajax
function myPostAction(data,target_url,callback,method,datatype,errfunc) {
    if(target_url == undefined){
        alert('no url specified');
        return ;
    }

    if(method == undefined){
        method = 'POST';
    }

    if(datatype == undefined){
        datatype = 'json';
    }

    $.ajax({
        type:method.toUpperCase(),
        url:target_url,
        dataType:datatype,
        data:data,
        processData:false,
        success:function (data) {
            if(callback != undefined){
                if(typeof callback === "function"){
                    callback(data);
                }
            }
        },
        error:function (XMLHttpRequest, textStatus, errorThrown) {
            if(errfunc != undefined){
                if(typeof errfunc === "function"){
                    errfunc(XMLHttpRequest, textStatus, errorThrown);
                }
            }
        }
    });
};




//-----------------------------------------------------------初始化小时颗粒度时间面板
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


//-----------起始时间/截止时间选择通知
function changeNotice(timeSelector,flowerNot,flowerContent,flag){
    timeSelector.change(function () {
        // Do something
        flowerContent.children().detach();
        var inputDateRangeStart = timeSelector.val();
        if (inputDateRangeStart != ''){
            //$("#country_lineChart_date").children().detach();
            if(flag == 1){
                flowerContent.append(
                '<strong>'+'起始时间设置为：'+ inputDateRangeStart +'</strong>');
            }else if(flag == 0){
                flowerContent.append(
                '<strong>'+'截止时间设置为：'+ inputDateRangeStart +'</strong>');
            }
            //
            var setNotificationOpen = new Notificationbar($("#FlowerQueryNotification"),"#container",2000,true,"open");
            setNotificationOpen.notificationBar();
            // SetNotification_init();
            // flowerNot.jqxNotification("open");
        }
        else{
            if(flag == 1){
                flowerContent.append('<strong>'+'请设置起始时间'+'</strong>');
            }else if(flag == 0){
                 flowerContent.append('<strong>'+'请设置截止时间'+'</strong>');
            }
            setNotificationOpen.notificationBar();
            // SetNotification_init();
            // flowerNot.jqxNotification("open");
        }
    });
}


//通知栏
// ---初始化选择/查询通知栏
function Notificationbar(selector,appendContainer,autoCloseDelay,autoClose,flag) {
    this.selector = selector;
    this.appendContainer = appendContainer;
    this.autoCloseDelay = autoCloseDelay;
    this.autoClose = autoClose;
    this.flag = flag;
}
Notificationbar.prototype.notificationBar = function () {
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
   this.selector.jqxNotification(this.flag);
};

