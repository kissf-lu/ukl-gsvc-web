/**
 * Created by wang.ding on 2017/4/5.
 */



/**=====================================================
 *  -------FilterPanel set func-------
 *======================================================
 *JqxGrid columns FilterPanel setting;
 * @param filterPanel panel to init;
 * @param datafield : grid column datafield param;
 * @param filterGrid : jquery type of grid DOC ID;
 * @param SrcAdapter : grid SrcAdapter param ;
 *=============================================================*/
var buildFilterPanel = function (filterPanel, datafield,filterGrid,SrcAdapter) {
    var textInput = $("<input style='margin:5px;'/>");
    var applyinput = $("<div class='filter' style='height: 25px; margin-left: 20px; margin-top: 7px;'></div>");
    var filterbutton = $('<span tabindex="0" style="padding: 4px 12px; margin-left: 2px;">筛选</span>');
    applyinput.append(filterbutton);
    var filterclearbutton = $('<span tabindex="0" style="padding: 4px 12px; margin-left: 5px;">清除筛选</span>');
    applyinput.append(filterclearbutton);
    filterPanel.append(textInput);
    filterPanel.append(applyinput);
    filterbutton.jqxButton({ height: 20 });
    filterclearbutton.jqxButton({height: 20 });
    var dataSource ={
        localdata: SrcAdapter.records,
        datatype: "json",
        async: false
    };
    var dataadapter = new $.jqx.dataAdapter(dataSource,
        {
            autoBind: false,
            autoSort: true,
            autoSortField: datafield,
            async: false,
            uniqueDataFields: [datafield]
        });
    var column = filterGrid.jqxGrid('getcolumn', datafield);
    textInput.jqxInput({ placeHolder: "Enter " + column.text, popupZIndex: 9999999, displayMember: datafield, source: dataadapter, height: 23, width: 175 });
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
        filterGrid.jqxGrid('addfilter', datafield, filtergroup);
        //apply the filters.
        filterGrid.jqxGrid('applyfilters');
        filterGrid.jqxGrid('closemenu');
    });
    filterbutton.keydown(function (event) {
        if (event.keyCode === 13) {
            filterbutton.trigger('click');
        }
    });
    filterclearbutton.click(function () {
        filterGrid.jqxGrid('removefilter', datafield);
        // apply the filters.
        filterGrid.jqxGrid('applyfilters');
        filterGrid.jqxGrid('closemenu');
    });
    filterclearbutton.keydown(function (event) {
        if (event.keyCode === 13) {
            filterclearbutton.trigger('click');
        }
        textInput.val("");
    });
};

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
    var time_picker = true;
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
 * @param selector : 通知栏id属性
    * html页面的通知栏标签ID号,用于获取通知栏位置，为初始化参数
 * @param appendContainer : 通知栏的内容显示容器id
    *用于设置在指定位置容器中显示通知栏，为初始化参数
 * @param autoCloseDelay : 自动关闭标签延时阈值 单位：毫秒级. 默认3秒
    *
 * @param autoClose : 是否自动关闭，  数据类型bool ：true/false . 默认true
    *
 * @param content : 通知内容， 数据类型 string: 默认：''
    *
 * @constructor :
 *
 *==========================================================================================*/
function Notificationbar(selector,appendContainer,autoCloseDelay,autoClose,content) {
    this.selector = selector;
    this.appendContainer = appendContainer;
    this.autoCloseDelay = autoCloseDelay||3000;
    this.autoClose = autoClose||false;
    this.content = content||'';
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
/**=======================================================
 *             notificationContent API
 *             用于设置通知内容的接口
 * =======================================================
 * @param notifi_content : 用于设置通知内容， 数据类型 string
 * @returns {Notificationbar}
 *========================================================*/
Notificationbar.prototype.notificationContent = function (notifi_content) {
    //通知内容设置
    this.content.children().detach();
    this.content.append(notifi_content);
    return this
};
/**=================================================
 *                notificationAction API
 *                用于jqxNotification设置方法接口
 * =================================================
 *
 * @param action_flag : jqxNotification 方法接口: 'closeLast':清除最近通知，'open'：打开通知
 */
Notificationbar.prototype.notificationAction = function (action_flag) {
    //可视化操作
    this.selector.jqxNotification(action_flag);
};

function dic_list(data, list_key) {
    var key_item = list_key||[];
    var rt_dic = {};
    key_item.forEach(function (item) {
        rt_dic[item] = data[item] === undefined ? '' : data[item];
    });
    return rt_dic
}

/**
 *
 * @param ajax_param
 * @constructor
 */
function AjaxJsonFunc(ajax_param) {
    this.ajaxParam = ajax_param;
}
AjaxJsonFunc.prototype.core = function (key_item, alert_id, get_bt_id, notification_obj, grid_obj, gird_id) {

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
                        alert_id);
                }
                else {
                    appendAlertInfo(
                        'warning',
                        '无查询结果!',
                        alert_id);
                }
            }
            else {
                grid_obj.ClearGridData();
                var tableData = [];
                appendAlertInfo(
                    'success',
                    ['查询完成，', '结果如下：'].join(' '),
                    alert_id);
                getData.data.forEach(function (item) {
                    var each_data = dic_list(item, key_item);
                    tableData.push(each_data);
                });//each函数完成
                grid_obj.ResetGridData(tableData);
                gird_id.jqxGrid('updatebounddata');
                return grid_obj;
            }
        })
        .fail(function (jqXHR, status) {
            appendAlertInfo(
                'warning',
                ['Servers False:', jqXHR, status].join(' '),
                alert_id);
        })
        .always(function () {
            get_bt_id.attr("disabled", false);
            notification_obj.notificationAction('closeLast');
        });
};

AjaxJsonFunc.prototype.gridDataGet = function (grid_id) {
    
};

/**
 *
 * @param id
 * @param datafields
 * @constructor
 */
function GgridInit(id, datafields){
    this.girid_id = id;
    this.GridArrayData = [];
    this.GridSource = {
        localdata: this.GridArrayData,
        datatype: "json",
        datafields: datafields||[]
    };
    this.GridAdapter = new $.jqx.dataAdapter(this.GridSource);
}
GgridInit.prototype.set = function (set_param) {
    var gridSetParam = {
        width: (set_param.width !== undefined) ? set_param.width : '99.8%',
        height: (set_param.height !== undefined) ? set_param.height : 500,
        filterable: set_param.filterable ? set_param.filterable : true,
        pageSize: (set_param.pageSize !== undefined) ? set_param.pageSize : 1000,
        pagesizeoptions: (
            (set_param.pagesizeoptions !== undefined) ? set_param.pagesizeoptions : ['1000', '5000', '10000']
        ),
        columns:(set_param.columns !== undefined) ? set_param.columns : []
    };
    var idGrid = this.girid_id;
    idGrid.jqxGrid({
        width: gridSetParam.width,
        height: gridSetParam.height,
        source: this.GridAdapter,
        filterable: true,
        columnsresize: true,
        enablebrowserselection: true,
        selectionmode: 'multiplerows',
        altrows: true,
        sortable: true,
        pageable: true,
        pageSize: gridSetParam.pageSize,
        pagesizeoptions: gridSetParam.pagesizeoptions,
        localization: getLocalization('zh-CN'),
        ready: function () {
        },
        autoshowfiltericon: true,
        columnmenuopening: function (menu, datafield, height) {
            var column = idGrid.jqxGrid('getcolumn', datafield);
            if (column.filtertype === "custom") {
                menu.height(155);
                setTimeout(function () {
                    menu.find('input').focus();
                }, 25);
            }
            else menu.height(height);
        },
        columns: gridSetParam.columns
    });
    return this;
};
GgridInit.prototype.ClearGridData = function () {
    this.GridSource.localdata = [];
};
GgridInit.prototype.ResetGridData = function (array_data) {
    this.GridSource.localdata = array_data;
};