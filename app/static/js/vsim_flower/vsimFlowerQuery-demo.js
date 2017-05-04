/**
 *
 * @type {Array}
 */

function GridColumnsSet() {
    this.dateFormat = 'yyyy-MM-dd HH:mm:ss';
    this.gridColumns = [];
}

GridColumnsSet.prototype.setColumns = function (grid_id, grid_src_adapter) {
    this.gridColumns = [
        {
            text: 'num', sortable: true, filterable: false, editable: false, groupable: false, draggable: false,
            resizable: false, datafield: '', width: 50, columntype: 'number',
            cellsrenderer: function (row, column, value) {
                return "<div style='margin:4px;'>" + (value + 1) + "</div>";
            }
        },
        {
            text: 'imsi', datafield: 'imsi', width: 150,
            filtertype: "custom",
            createfilterpanel: function (datafield, filterPanel) {
                buildFilterPanel(filterPanel, datafield, grid_id, grid_src_adapter);
            }
        },
        {text: 'time(GMT0)', datafield: 'time', cellsformat: this.dateFormat, width: 200,
            filtertype: 'date', hidden: true},
        {text: 'mcc', datafield: 'mcc', filtertype: "range", width: 100, hidden: true},
        {text: 'plmn', datafield: 'plmn', filtertype: "range", width: 100, hidden: true},
        {text: 'lac', datafield: 'lac', filtertype: "range", width: 100, hidden: true},
        {text: 'Flower/MB', datafield: 'Flower', width: 300}
    ];
    return this;
};
GridColumnsSet.prototype.dateFormatSet = function (format_date) {
    this.dateFormat = format_date;
};

function gridFieldsSet() {
    return [
            {name: 'imsi', type: 'string'},
            {name: 'time', type: 'date'},
            {name: 'mcc', type: 'string'},
            {name: 'plmn', type: 'string'},
            {name: 'lac', type: 'string'},
            {name: 'Flower', type: 'number'}
        ];
}
//-显示选择菜单设置
var jqxDropDownList = [
    {label: 'imsi', value: 'imsi', checked: true},
    {label: 'time', value: 'time', checked: false},
    {label: 'plmn', value: 'plmn', checked: false},
    {label: 'mcc', value: 'mcc', checked: false},
    {label: 'lac', value: 'lac', checked: false},
    {label: 'Flower', value: 'Flower', checked: true}
];
//初始化显示选择函数
function initjqxDropDownList() {
// Create a jqxDropDownList
    $("#jqxDropDownList").jqxDropDownList({
        checkboxes: true,
        source: jqxDropDownList,
        autoOpen: true,
        animationType: 'fade',
        filterable: true,
        dropDownHeight: 300,
        Width: 150
    });
}
//动作函数
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

//刷新数据button模块
$('#FlowerQueryFlash').click(function () {
    $('#FlowerQueryjqxGrid').jqxGrid('updatebounddata');

});

//excel导出栏
$("#FlowerQueryExcelExport").click(function () {
    var rows = $('#FlowerQueryjqxGrid').jqxGrid('getdisplayrows');
    var alldatanum = rows.length;
    //alert(alldatanum);
    var view_data = [];
    var json_data = {'data': view_data};
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
                            time: new MomentTime(rows[i + j].time).getAddUTCTime(),    // UTC时间协调
                            mcc: rows[i + j].mcc,
                            plmn: rows[i + j].plmn,
                            lac: rows[i + j].lac,
                            Flower: rows[i + j].Flower
                        })
                    }
                }
            }
        }
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
        temp.action = $SCRIPT_ROOT + "/api/v1.0/export_Flower/";  //"/test_exportExcel";
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
//时间维度选择通知timeDim
function TimeDimChange(param) {
    var timeChange = {
        days:{
            columnsCellsFormat: 'yyyy-MM-dd',
            dateRangeBeginTOEndGap: 15,
            dateRangeBeginTOEndGapUnit: 'days',
            dateRangeTimeBeginID: param.TimeBegin,
            dateRangeBeginInitTime: {'hour':0,'minute': 0, 'second': 0},
            dateRangeBeginFormat: "YYYY-MM-DD HH",
            dateRangeBeginIfHourView: true,
            dateRangeEndTONowGap: 0,
            dateRangeEndTONowGapUnit: 'days',
            dateRangeTimeEndID: param.TimeEnd,
            dateRangeEndInitTime: {'hour':0,'minute': 0, 'second': 0},
            dateRangeEndFormat: "YYYY-MM-DD HH",
            dateRangeEndIfHourView: true
        },
        hours:{
            columnsCellsFormat: 'yyyy-MM-dd HH',
            dateRangeBeginTOEndGap: 6,
            dateRangeBeginTOEndGapUnit: 'h',
            dateRangeTimeBeginID: param.TimeBegin,
            dateRangeBeginInitTime: {'minute': 0, 'second': 0},
            dateRangeBeginFormat: "YYYY-MM-DD HH",
            dateRangeEndTONowGap: 0,
            dateRangeEndTONowGapUnit: 'h',
            dateRangeTimeEndID: param.TimeEnd,
            dateRangeEndInitTime: {'minute': 0, 'second': 0},
            dateRangeEndFormat: "YYYY-MM-DD HH"
        }
    };
    var NotificationTimeDim = new Notificationbar(
        param.Notification,
        param.NotificationContainer,
        2000,
        true,
        param.NotificationContent
    ).init();
    var TimeDimVar = param.TimeDim.val();
    var HtmlNotification = ['<strong>', '时间颗粒度设置为：', TimeDimVar, '</strong>'].join('');
    if (TimeDimVar) {
        NotificationTimeDim.notificationContent(HtmlNotification);
        NotificationTimeDim.notificationAction('open');
        param.Grid.jqxGrid('setcolumnproperty', 'time', 'cellsformat', timeChange[TimeDimVar].columnsCellsFormat);
        var daterange_day_begin = new Mydaterange(
            timeChange[TimeDimVar].dateRangeBeginTOEndGap,
            timeChange[TimeDimVar].dateRangeBeginTOEndGapUnit,
            timeChange[TimeDimVar].dateRangeTimeBeginID);
        daterange_day_begin.initTime(
            timeChange[TimeDimVar].dateRangeBeginInitTime,
            timeChange[TimeDimVar].dateRangeBeginFormat,
            timeChange[TimeDimVar].dateRangeBeginIfHourView
        );
        var daterange_day_end = new Mydaterange(
            timeChange[TimeDimVar].dateRangeEndTONowGap,
            timeChange[TimeDimVar].dateRangeEndTONowGapUnit,
            timeChange[TimeDimVar].dateRangeTimeEndID
        );
        daterange_day_end.initTime(
            timeChange[TimeDimVar].dateRangeEndInitTime,
            timeChange[TimeDimVar].dateRangeEndFormat,
            timeChange[TimeDimVar].dateRangeEndIfHourView
        );
    } else {
        HtmlNotification = ['<strong>', '请设置时间颗粒度！', '</strong>'].join('');
        NotificationTimeDim.notificationContent(HtmlNotification);
        NotificationTimeDim.notificationAction('open');
    }
}
function get_ajax_time_list(time_dim ,str_begin_time, str_end_time, time_gap) {
    var list_time = [];
    if (time_dim ==='hours'){
        list_time = new GetSplitTimeDay(str_begin_time, str_end_time, 0).towPartListDic();
    } else {
        list_time = (moment(str_begin_time, "YYYY-MM-DD HH:mm:ss").get('h') ===0 &&
                     moment(str_end_time, "YYYY-MM-DD HH:mm:ss").get('h') ===0) ?
            new GetSplitTimeDay(str_begin_time, str_end_time, 0).towPartListDic() :
            new GetSplitTimeDay(str_begin_time, str_end_time, time_gap).thirdPartListDic();
    }
    return list_time;
}

function getFlowerAjax(option_data, option_id, ajax_set, grid_obj) {
    var momentBegin = moment(option_data.Begintime, "YYYY-MM-DD HH:mm:ss");
    var momentEnd = moment(option_data.Endtime, "YYYY-MM-DD HH:mm:ss");
    var HourGap = momentEnd.diff(momentBegin, 'hours');
    var DayGap = momentEnd.diff(momentBegin, 'days');
    var TimezoneOffset = moment().utcOffset();
    var QueryjqxNotification = new Notificationbar(
        option_id.id_JqxNotification,
        option_id.id_JqxNotificationContainer,
        3000,
        false,
        option_id.id_JqxNotificationContent
    );
    //
    var list_tiem = get_ajax_time_list(option_data.TimeDim, option_data.Begintime, option_data.Endtime, DayGap);
    QueryjqxNotification.init();
    //隐藏上次通知
    QueryjqxNotification.notificationAction('closeLast');
    //  隐藏上一次告警栏
    option_id.id_Alert.children().detach();
    //输入格式匹配
    var conformPlmn = checkplmnReg(option_data.Plmn);
    //mcc have the same reg rules
    var conformMcc = checkplmnReg(option_data.Mcc);
    var conformImsi = checkImsiReg(option_data.Imsi);
    var alert_str = '';
    var alertClass = 'warning';
    var queryPost = {
        querySort: option_data.TimeDim,
        timeList: list_tiem,
        mcc: option_data.Mcc,
        plmn: option_data.Plmn,
        imsi: option_data.Imsi,
        agg_group_key: option_data.AddKey,
        TimezoneOffset: TimezoneOffset
    };
    if (!(conformImsi)) {
        alert_str = ['imsi输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
    }
    else if (option_data.Begintime === "") {
        alert_str = ['请选择要查询的起始时间!', '完成输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
    }
    else if (option_data.Endtime === "") {
        alert_str = ['请选择要查询的截止时间!', '完成输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
    }
    else if ((option_data.Plmn !== "") && (!(conformPlmn))) {
        alert_str = ['plmn输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
    }
    else if ((option_data.Mcc !== "") && (!(conformMcc))) {
        alert_str = ['mcc输入格式不对!', '请按照正确格式输入！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
    }
    else {
        if (HourGap === 0) {
            alert_str = ['起始和截止时间相同!', '请按照正确格式输入！'].join(' ');
            appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
        }
        else {
            var notifi_content = '';
            if ((option_data.TimeDim === 'hours') && (HourGap > 48)) {

                alert_str = ['时常超过48小时，', '请重新设置时间!'].join(' ');
                appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
            } else if ((option_data.TimeDim === 'days') && (DayGap > 93)) {
                alert_str = ['天数超过93天，', '请重新设置时间!'].join(' ');
                appendAlertInfo(alertClass, alert_str, option_id.id_Alert);
            }
            else {
                var ajaxOption = {
                    ajaxParam: {
                        type: ajax_set.type,
                        url: ajax_set.url,
                        postData: queryPost
                    },
                    idTag: {
                        id_Alert: option_id.id_Alert,
                        id_GetDataBt: option_id.id_GetDataButtonAjax,
                        id_Grid: option_id.id_JqxGrid
                    },
                    objClass: {
                        objGrid: grid_obj.gridObj,
                        objNotification: QueryjqxNotification
                    }
                };
                var ajaxRT = new AjaxFunc(ajaxOption.ajaxParam);
                var checkIf = ajaxRT.ajaxParamCheck(['url']);
                if(!(checkIf)){
                    QueryjqxNotification.notificationAction('closeLast');
                } else {
                    if (option_data.TimeDim === 'hours'){
                        notifi_content = ['<strong>', '查询时差为：', HourGap, '  数据获取中......', '</strong>'].join('');
                    }else {
                        notifi_content = ['<strong>', '查询天数为：', DayGap, '  数据获取中......', '</strong>'].join('');
                    }
                    QueryjqxNotification.notificationContent(notifi_content);
                    QueryjqxNotification.notificationAction('open');
                    // 做表格数据清空操作
                    option_id.id_JqxGrid.jqxGrid("clear");
                    // 禁用查询按钮,防止多次点击，造成重复查询
                    option_id.id_GetDataButtonAjax.attr("disabled", true);
                    option_id.id_JqxGrid.jqxGrid("showloadelement");
                    ajaxRT.GridPostAjax({idTag:ajaxOption.idTag, objClass: ajaxOption.objClass});
                }
            }
        }
    }
    return false;
}
//main-初始化主程序
$(function () {
    //--------------------------初始化统计表单
    var GlobeIdSet = {
        flowerGrid: $("#FlowerQueryjqxGrid"),
        flowerDataGet: $("#FlowerQuery_dataGet"),
        timeDim: $('#timeDim'),
        timeStart:  $('#input-daterange-start'),
        timeEnd: $('#input-daterange-end'),
        notificationFirLayer: $("#FlowerNotification"),
        notificationFirLayerContent: $("#FlowerNotificationContent"),
        notificationFirLayerContainer: ("#NotificationContainerFirst"),
        notificationSecLayer: $("#QueryingQueryjqxNotification"),
        notificationSecLayerContent: $("#QueryingNotificationContent"),
        notificationSecLayerContainer: ("#QuerycontainerSecond"),
        chosenFlowerKey: $("#chosenFlowerQueryKey"),
        mcc: $('#FlowerQueryMCC'),
        plmn: $('#FlowerQueryPlmn'),
        imsi: $('#inputimsi'),
        alertSecLayer: $("#queryQlert"),
        dropDownList: $("#jqxDropDownList")
    };
    GlobeIdSet.chosenFlowerKey.on('change', function (evt, params) {
        var ChosenAction = new ChosenView(GlobeIdSet.flowerGrid);
        var ActionID = {
            DropDownListID: GlobeIdSet.dropDownList
        };
        ChosenAction.GridAction(ActionID, params);
    });
    var FlowerJqxGrid = new GridInit(GlobeIdSet.flowerGrid, gridFieldsSet());
    var GridColumnSet = new GridColumnsSet().setColumns(GlobeIdSet.flowerGrid, FlowerJqxGrid.GridAdapter);
    FlowerJqxGrid.set({columns: GridColumnSet.gridColumns});
    //初始化显示栏
    initjqxDropDownList();
    //初始化小时颗粒日期栏
    var daterange_hour_begin = new Mydaterange(6, 'h', GlobeIdSet.timeStart).UTCTime();
    daterange_hour_begin.initTime({'minute': 0, 'second': 0}, "YYYY-MM-DD HH");
    var daterange_hour_end = new Mydaterange(0, 'h', GlobeIdSet.timeEnd).UTCTime();
    daterange_hour_end.initTime({'minute': 0, 'second': 0}, "YYYY-MM-DD HH");
    // 初始化chosen
    GlobeIdSet.chosenFlowerKey.chosen({width: "100%"});
    GlobeIdSet.timeDim.change(function () {
        var Param = {
            Grid: GlobeIdSet.flowerGrid,
            Notification: GlobeIdSet.notificationFirLayer,
            NotificationContent: GlobeIdSet.notificationFirLayerContent,
            NotificationContainer: GlobeIdSet.notificationFirLayerContainer,
            TimeDim: GlobeIdSet.timeDim,
            TimeBegin: GlobeIdSet.timeStart,
            TimeEnd: GlobeIdSet.timeEnd
        };
        TimeDimChange(Param);
    });
    GlobeIdSet.flowerDataGet.click( function (){
        var option = {
            data:{
                TimeDim: GlobeIdSet.timeDim.val(),
                Mcc: GlobeIdSet.mcc.val(),
                Plmn : GlobeIdSet.plmn.val(),
                Begintime : GlobeIdSet.timeStart.val(),
                Endtime: GlobeIdSet.timeEnd.val(),
                Imsi : GlobeIdSet.imsi.val(),
                AddKey : GlobeIdSet.chosenFlowerKey.val()
            },
            id:{
                id_JqxNotification: GlobeIdSet.notificationSecLayer,
                id_JqxNotificationContent: GlobeIdSet.notificationSecLayerContent,
                id_JqxNotificationContainer: GlobeIdSet.notificationSecLayerContainer,
                id_Alert: GlobeIdSet.alertSecLayer,
                id_JqxGrid: GlobeIdSet.flowerGrid,
                id_GetDataButtonAjax: GlobeIdSet.flowerDataGet
            },
            ajaxSet:{
                type: 'POST',
                url: $SCRIPT_ROOT + "/api/v1.0/get_FlowerQuery/"
            },
            gridObj: {
                gridObj: FlowerJqxGrid,
                gridColObj: GridColumnSet
            }
        };
        getFlowerAjax(option.data, option.id, option.ajaxSet, option.gridObj);
    });
    // tooltip init
    $('[data-toggle="tooltip"]').tooltip();
});
//-----------------------------------------------------end main 函数-----------------------------------------------------
