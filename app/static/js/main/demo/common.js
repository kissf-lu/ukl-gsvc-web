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
            SetNotification_init();
            flowerNot.jqxNotification("open");
        }
        else{
            if(flag == 1){
                flowerContent.append('<strong>'+'请设置起始时间'+'</strong>');
            }else if(flag == 0){
                 flowerContent.append('<strong>'+'请设置截止时间'+'</strong>');
            }
            SetNotification_init();
            flowerNot.jqxNotification("open");
        }
    });
}