// 告警通用文字
var queryAndReturnAlert = '<div class="alert alert-warning" role="alert">' +
    '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
    '<span aria-hidden="true">&times;</span>' +
    '</button>';
//-----------------------------------------------------------表格模块初始化------------------------------------------
//流量查询数据存储变量
var FlowerQueryGridArrayData = [];
//国流量查询表格数据初始化
var FlowerQuerySource = {
    localdata: FlowerQueryGridArrayData,
    datatype: "json",
    datafields: [
        {name: 'imsi', type: 'string'},
        {name: 'time', type: 'date'},
        {name: 'mcc', type: 'string'},
        {name: 'plmn', type: 'string'},
        {name: 'lac', type: 'string'},
        {name: 'Flower', type: 'number'}
    ],
};
//jqxgrid data adapter
var FlowerQueryAdapter = new $.jqx.dataAdapter(FlowerQuerySource);
//--------------------------------------------------py-------------
function FlowerQueryjqxGrid() {
    $("#FlowerQueryjqxGrid").jqxGrid({
        width: "99.8%",
        source: FlowerQueryAdapter,
        filterable: true,
        columnsresize: true,
        enablebrowserselection: true,
        selectionmode: 'multiplerows',
        altrows: true,
        sortable: true,
        pageable: true,
        pageSize: 1000,
        pagesizeoptions: ['1000', '5000', '10000'],
        localization: getLocalization('zh-CN'),
        ready: function () {
        },
        autoshowfiltericon: true,
        columnmenuopening: function (menu, datafield, height) {
            var column = $("#FlowerQueryjqxGrid").jqxGrid('getcolumn', datafield);
            if (column.filtertype == "custom") {
                menu.height(155);
                setTimeout(function () {
                    menu.find('input').focus();
                }, 25);
            }
            else menu.height(height);
        },
        columns: [
            {
                text: 'num',
                sortable: true,
                filterable: false,
                editable: false,
                groupable: false,
                draggable: false,
                resizable: false,
                datafield: '',
                width: 50,
                columntype: 'number',
                cellsrenderer: function (row, column, value) {
                    return "<div style='margin:4px;'>" + (value + 1) + "</div>";
                },
            },
            {
                text: 'imsi', datafield: 'imsi', width: 150,
                filtertype: "custom",
                createfilterpanel: function (datafield, filterPanel) {
                    ProbDicBuildFilterPanel(filterPanel, datafield);
                }
            },
            {
                text: 'time(GMT0)', datafield: 'time', cellsformat: 'yyyy-MM-dd HH:mm:ss', width: 200,
                filtertype: 'date', hidden: true
            },
            {text: 'mcc', datafield: 'mcc', filtertype: "range", width: 100, hidden: true},
            {text: 'plmn', datafield: 'plmn', filtertype: "range", width: 100, hidden: true},
            {text: 'lac', datafield: 'lac', filtertype: "range", width: 100, hidden: true},
            {text: 'Flower/MB', datafield: 'Flower', width: 300},
        ]
    });
}
//--------------------------------------------------------------END ----------------------------------------------------


//-------------------------------------------------------显示选择菜单设置----------------------------------------
var jqxDropDownList = [
    {label: 'imsi', value: 'imsi', checked: true},
    {label: 'time', value: 'time', checked: false},
    {label: 'plmn', value: 'plmn', checked: false},
    {label: 'mcc', value: 'mcc', checked: false},
    {label: 'lac', value: 'lac', checked: false},
    {label: 'Flower', value: 'Flower', checked: true}
];
//---------------------------------------------------初始化显示选择函数
function initjqxDropDownList() {
// Create a jqxDropDownList
    $("#jqxDropDownList").jqxDropDownList({
        checkboxes: true,
        source: jqxDropDownList,
        autoOpen: true,
        animationType: 'fade',
        filterable: true,
        dropDownHeight: 300,
        Width: 150,
    });

}
//-----------------------------------------------动作函数---------------
$("#jqxDropDownList").on('checkChange', function (event) {
    $("#FlowerQueryjqxGrid").jqxGrid('beginupdate');
    if (event.args.checked) {
        $("#FlowerQueryjqxGrid").jqxGrid('showcolumn', event.args.value);

    }
    else {
        $("#FlowerQueryjqxGrid").jqxGrid('hidecolumn', event.args.value);
    }
    $("#FlowerQueryjqxGrid").jqxGrid('endupdate');
});
//--------------------------------------------------------------显示选择菜单设置-END-------------------------------


//--------------------------------------------------------过滤菜单栏-----------------------------------------
var ProbDicBuildFilterPanel = function (filterPanel, datafield) {
    var textInput = $("<input style='margin:5px;'/>");
    var applyinput = $("<div class='filter' style='height: 25px; margin-left: 20px; margin-top: 7px;'></div>");
    var filterbutton = $('<span tabindex="0" style="padding: 4px 12px; margin-left: 2px;">Filter</span>');
    applyinput.append(filterbutton);
    var filterclearbutton = $('<span tabindex="0" style="padding: 4px 12px; margin-left: 5px;">Clear</span>');
    applyinput.append(filterclearbutton);
    filterPanel.append(textInput);
    filterPanel.append(applyinput);
    filterbutton.jqxButton({height: 20});
    filterclearbutton.jqxButton({height: 20});

    var dataSource =
        {
            localdata: FlowerQueryAdapter.records,
            datatype: "json",
            async: false
        }
    var dataadapter = new $.jqx.dataAdapter(dataSource,
        {
            autoBind: false,
            autoSort: true,
            autoSortField: datafield,
            async: false,
            uniqueDataFields: [datafield]
        });

    var column = $("#FlowerQueryjqxGrid").jqxGrid('getcolumn', datafield);
    textInput.jqxInput({
        placeHolder: "Enter " + column.text,
        popupZIndex: 9999999,
        displayMember: datafield,
        source: dataadapter,
        height: 23,
        width: 175
    });
    textInput.keyup(function (event) {
        if (event.keyCode === 13) {
            filterbutton.trigger('click');
        }
    });

    filterbutton.click(function () {
        var filtergroup = new $.jqx.filter();
        var filter_or_operator = 1;
        var filtervalue = textInput.val();
        var filtercondition = 'contains';
        var filter1 = filtergroup.createfilter('stringfilter', filtervalue, filtercondition);
        filtergroup.addfilter(filter_or_operator, filter1);
        // add the filters.
        $("#FlowerQueryjqxGrid").jqxGrid('addfilter', datafield, filtergroup);
        // apply the filters.
        $("#FlowerQueryjqxGrid").jqxGrid('applyfilters');
        $("#FlowerQueryjqxGrid").jqxGrid('closemenu');
    });

    filterbutton.keydown(function (event) {
        if (event.keyCode === 13) {
            filterbutton.trigger('click');
        }
    });
    filterclearbutton.click(function () {
        $("#FlowerQueryjqxGrid").jqxGrid('removefilter', datafield);
        // apply the filters.
        $("#FlowerQueryjqxGrid").jqxGrid('applyfilters');
        $("#FlowerQueryjqxGrid").jqxGrid('closemenu');
    });

    filterclearbutton.keydown(function (event) {
        if (event.keyCode === 13) {
            filterclearbutton.trigger('click');
        }
        textInput.val("");
    });
};

//------------------------------------------------------------刷新数据button模块--------------------------
$('#FlowerQueryFlash').click(function () {
    $('#FlowerQueryjqxGrid').jqxGrid('updatebounddata');

});

//----------------------------------------------------------excel导出栏----------------------------
$("#FlowerQueryExcelExport").click(function () {
    var rows = $('#FlowerQueryjqxGrid').jqxGrid('getdisplayrows');
    var alldatanum = rows.length;
    var view_data = [];
    var json_data = {'data': view_data}
    var paginginformation =
        $('#FlowerQueryjqxGrid').jqxGrid('getpaginginformation');
    // The page's number.
    var pagenum = paginginformation.pagenum;
    // The page's size.
    var pagesize = paginginformation.pagesize;
    // The number of all pages.
    var pagescount = paginginformation.pagescount;
    if (alldatanum == 0) {
        //delete old alter
        $("#queryQlert").children().detach();
        $("#queryQlert").append((queryAndReturnAlert + '<p>无输出数据！</p></div>'));
    }

    else {
        for (var i = 0; i < rows.length; i++) {
            if (i == pagenum * pagesize) {
                for (var j = 0; j < pagesize; j++) {
                    if (i + j < alldatanum) {
                        view_data.push({
                            imsi: rows[i + j].imsi,
                            time: rows[i + j].time,
                            mcc: rows[i + j].mcc,
                            plmn: rows[i + j].plmn,
                            lac: rows[i + j].lac,
                            Flower: rows[i + j].Flower
                        })
                    }

                }
            }
        }
        //$("#FlowerQueryjqxGrid").jqxGrid('exportdata', 'xls', 'FlowerQueryExcelExport', true, view_data);
        excelExport(json_data);
    }
    return false;

});

function excelExport(data) {
    var exportdata = data;

    if (exportdata.data == []) {
        //delete old alter
        $("#app-growl").children().detach();
        $("#app-growl").append((alertStr + '<p>无输出数据！</p></div>'));
    }
    else {
        var temp = document.createElement("form");
        temp.action = $SCRIPT_ROOT + "/api/v1.0/export_Flower/"//"/test_exportExcel";
        temp.method = "post";
        temp.style.display = "none";
        var opt = document.createElement("textarea");
        opt.name = "data";
        opt.value = JSON.stringify(exportdata.data);
        temp.appendChild(opt);
        document.body.appendChild(temp);
        temp.submit();
    }

    return false;

}

//------------------------------------------------------------excel导出栏--end--------------------------


//------------------------------------------chosen selected deselected Functions---
$("#chosenFlowerQueryKey").on('change', function (evt, params) {
    $("#FlowerQueryjqxGrid").jqxGrid('beginupdate');
    if (params.selected) {
        $("#FlowerQueryjqxGrid").jqxGrid('showcolumn', params.selected);//当选择后显示相关输出信息
        $("#jqxDropDownList").jqxDropDownList('checkItem', params.selected);
    }
    else if (params.deselected) {
        $("#FlowerQueryjqxGrid").jqxGrid('hidecolumn', params.deselected);//取消输出栏显示
        $("#jqxDropDownList").jqxDropDownList('uncheckItem', params.deselected);
    }
    else {
        var con = '';
    }
    $("#FlowerQueryjqxGrid").jqxGrid('endupdate');
});

//-----------时间维度选择通知--timeDim
$('#timeDim').change(function () {
    // Do something
    var NotificationTimeDim = new Notificationbar(
        $("#FlowerQueryNotification"),
        "#container",
        2000,
        true,
        $("#FlowerQueryNotificationContent")
    );
    NotificationTimeDim.init();
    var timeDimVar = $('#timeDim').val();
    if (timeDimVar != '') {
        var html_notif = '<strong>' + '时间颗粒度设置为：' + timeDimVar + '</strong>';
        //选择通知栏
        NotificationTimeDim.notificationContent(html_notif);
        NotificationTimeDim.notificationAction('open');
        if (timeDimVar == 'days') {
            var daterange_day_begin = new Mydaterange(15, 'days', $('#input-daterange-start'));
            daterange_day_begin.initTime({'hour':0,'minute': 0, 'second': 0},"YYYY-MM-DD", false);
            var daterange_day_end = new Mydaterange(0, 'days', $('#input-daterange-end'));
            daterange_day_end.initTime({'hour':0,'minute': 0, 'second': 0},"YYYY-MM-DD", false);
        }
        else {
            var daterange_hour_begin = new Mydaterange(6, 'h', $('#input-daterange-start'));
            daterange_hour_begin.initTime();
            var daterange_hour_end = new Mydaterange(0, 'h', $('#input-daterange-end'));
            daterange_hour_end.initTime();
        }
    }
    else {
        var html_notif = '<strong>' + '请设置时间颗粒度！' + '</strong>';
        NotificationTimeDim.notificationContent(html_notif);
        NotificationTimeDim.notificationAction('open');
    }
});

function getFlowerAjax(option_data, option_id, ajax_set) {
    var TimeDim =option_data.TimeDim;
    var Mcc = option_data.Mcc;
    var Plmn = option_data.Plmn;
    var Begintime = option_data.Begintime;
    var Endtime = option_data.Endtime;
    var Imsi = option_data.Imsi;
    var addkey = option_data.AddKey;
    //
    var momentBegin = moment(Begintime, "YYYY-MM-DD HH:mm:ss");
    var momentEnd = moment(Endtime, "YYYY-MM-DD HH:mm:ss");
    var HourGap = momentEnd.diff(momentBegin, 'hours');
    var DayGap = momentEnd.diff(momentBegin, 'days');
    var TimezoneOffset = moment().utcOffset();
    //
    var id_item = option_id;
    //
    var QueryjqxNotification = new Notificationbar(
        id_item.id_JqxNotification,
        "#Querycontainer",
        3000,
        false,
        id_item.id_JqxNotificationContent
    );
    //
    QueryjqxNotification.init();
    //隐藏上次通知
    QueryjqxNotification.notificationAction('closeLast');
    //  隐藏上一次告警栏
    id_item.id_Alert.children().detach();
    //输入格式匹配
    var conformPlmn = checkplmnReg(Plmn);
    //mcc have the same reg rules
    var conformMcc = checkplmnReg(Mcc);
    var conformImsi = checkImsiReg(Imsi);
    var alert_str = '';
    var alertClass = 'warning';
    var queryPost = {
        querySort: TimeDim,
        begintime: Begintime,
        endtime: Endtime,
        mcc: Mcc,
        plmn: Plmn,
        imsi: Imsi,
        agg_group_key: addkey,
        TimezoneOffset: TimezoneOffset
    };

    if (!(conformImsi)) {
        alert_str = ['imsi输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
    }
    else if (Begintime === "") {
        alert_str = ['请选择要查询的起始时间!', '完成输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);

    }
    else if (Endtime === "") {
        alert_str = ['请选择要查询的截止时间!', '完成输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
    }
    else if ((Plmn !== "") && (!(conformPlmn))) {
        alert_str = ['plmn输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
    }
    else if ((Mcc !== "") && (!(conformMcc))) {
        alert_str = ['mcc输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
    }
    else {
        if (HourGap === 0) {
            alert_str = ['起始和截止时间相同!', '请按照正确格式输入！'].join(' ');
            appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
        }
        else {
            var notifi_content = '';
            if ((TimeDim === 'hours') && (HourGap > 48)) {
                alert_str = ['时常超过48小时，', '请重新设置时间!'].join(' ');
                appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
            } else if ((TimeDim === 'days') && (DayGap > 93)) {
                alert_str = ['天数超过93天，', '请重新设置时间!'].join(' ');
                appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
            }
            else {
                if (TimeDim === 'hours'){
                    notifi_content = ['<strong>', '查询时差为：', HourGap, '  数据获取中......', '</strong>'].join('');
                }else {
                    notifi_content = ['<strong>', '查询天数为：', DayGap, '  数据获取中......', '</strong>'].join('');
                }
                QueryjqxNotification.notificationContent(notifi_content);
                QueryjqxNotification.notificationAction('open');
                //重置表格历史数据
                FlowerQueryGridArrayData = [];
                //做表格数据清空操作
                id_item.id_JqxGrid.jqxGrid("clear");
                //禁用查询按钮,防止多次点击，造成重复查询
                id_item.id_GetDataButtonAjax.attr("disabled", true);
                $.ajax({
                    type: ajax_set.type,
                    //get方法url地址
                    url: ajax_set.url,
                    //request set
                    contentType: "application/json",
                    //data参数
                    data: JSON.stringify(queryPost),
                    //server back data type
                    dataType: "json"
                })
                    .done(function (data) {
                        //数据返回后关闭通知button
                        QueryjqxNotification.notificationAction('closeLast');
                        var getData = data;
                        var alert_str = "";
                        if (getData.data.length === 0) {
                            if (getData.info.err) {
                                alert_str = ['Error', ':', getData.info.errinfo].join(' ');
                                alertClass = 'danger';
                                appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
                            }
                            else {
                                alert_str = ['查询结束', ',', '无查询结果!'].join(' ');
                                appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
                            }
                        }
                        else {
                            alert_str = ['查询完成，', '结果如下：'].join(' ');
                            alertClass = 'success';
                            appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
                            $.each(getData.data, function (i, item) {
                                FlowerQueryGridArrayData.push({
                                    imsi: item.imsi,
                                    time: item.time,
                                    mcc: item.mcc,
                                    plmn: item.plmn,
                                    lac: item.lac,
                                    Flower: item.Flower
                                });
                            });//each函数完成
                            // set the new data
                            FlowerQuerySource.localdata = FlowerQueryGridArrayData;
                            id_item.id_JqxGrid.jqxGrid('updatebounddata');
                        }
                    })
                    .fail(function (jqXHR, status) {
                        //数据返回失败后关闭通知button
                        QueryjqxNotification.notificationAction('closeLast');
                        id_item.id_JqxGrid.jqxGrid("clear");
                        alert_str = ['Servers False', ':', jqXHR, status].join(' ');
                        alertClass = 'danger';
                        appendAlertInfo(alertClass, alert_str, id_item.id_Alert);
                    })
                    .always(function () {
                        //ajax结束后恢复查询按钮
                        $("#FlowerQuery_dataGet").attr("disabled", false);
                    });
            }
        }
    }
    return false;
}
//------------------------------------------------------------验证imsi格式
function checkImsiReg(str) {
    var stringTest = str;
    var RegExp1 = /^([0-9]+)$/;
    var RegExp2 = /^([0-9]+[,])*([0-9]+)$/;
    //plmn非空时监测输入格式是否合法
    if ((RegExp1.exec(stringTest) || (RegExp2.exec(stringTest)) ) && (str !== '')) {
        return ((RegExp1.exec(stringTest) || (RegExp2.exec(stringTest)) ) && (str !== ''));
    }
    else {
        return ((RegExp1.exec(stringTest) || (RegExp2.exec(stringTest)) ) && (str !== ''));
    }
}

//------------------------------------------------------------验证plmn格式
function checkplmnReg(str) {
    var RegExp1 = /^([0-9]+)$/;  //plmn非空时监测输入格式是否合法-规则为以数组开头结尾
    if ((RegExp1.exec(str) ) && (str !== '')) {
        return true;
    } else if (str === '') {
        return (str === '');
    }
    else {
        return false;
    }
}


//--------------------------------------------------------main-初始化主程序-----------------------------------------
$(function () {
    //--------------------------初始化统计表单
    FlowerQueryjqxGrid();
    //初始化显示栏
    initjqxDropDownList();
    //截止时间/起始V时间选择通知
    var selector = {
        "timeSelectorStart": $('#input-daterange-start'),
        "timeSelectorEnd": $('#input-daterange-end'),
        "flowerNot": $("#FlowerQueryNotification"),
        "flowerContent": $("#FlowerQueryNotificationContent"),
        "flowerQueryDataGet": $("#FlowerQuery_dataGet")
    };
    //初始化小时颗粒日期栏
    var daterange_hour_begin = new Mydaterange(6, 'h', selector.timeSelectorStart);
    daterange_hour_begin.initTime();
    var daterange_hour_end = new Mydaterange(0, 'h', selector.timeSelectorEnd);
    daterange_hour_end.initTime();
    //初始化chosen
    $("#chosenFlowerQueryKey").chosen({width: "100%"});

    selector.flowerQueryDataGet.click( function (){
        var option = {
            data:{
                TimeDim: $('#timeDim').val(),
                Mcc: $('#FlowerQueryMCC').val(),
                Plmn : $('#FlowerQueryPlmn').val(),
                Begintime : $('#input-daterange-start').val(),
                Endtime: $('#input-daterange-end').val(),
                Imsi : $('#inputimsi').val(),
                AddKey : $('#chosenFlowerQueryKey').val()
            },
            id:{
                id_JqxNotification: $("#QueryingQueryjqxNotification"),
                id_JqxNotificationContent: $("#QueryingNotificationContent"),
                id_Alert: $("#queryQlert"),
                id_JqxGrid: $("#FlowerQueryjqxGrid"),
                id_GetDataButtonAjax: $("#FlowerQuery_dataGet")
            },
            ajaxSet:{
                type: 'POST',
                url: $SCRIPT_ROOT + "/api/v1.0/get_FlowerQuery/"
            }
        };
        getFlowerAjax(option.data, option.id, option.ajaxSet);
    });


});
//-----------------------------------------------------end main 函数-----------------------------------------------------
