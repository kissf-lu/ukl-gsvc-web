/**
 * Created by lujian on 2017-04-25.
 */


//
function staticTable1View(panel_param, next_ajax_data, table_id, table_data) {
    var tbHTML = '';
    var tbButtonID = [];
    for (var i = 0; i < table_data.length; i++) {
        var td_i = '';
        td_i = (function (i) {
            this.td = '';
            this.TableMake = function () {
                if (i === 0) {
                    this.td = [
                        '<tr>',
                        '<td>', (i + 1), '</td>',
                        '<td>', this.PackageName, '</td>',
                        '<td>', this.NextUpdateTime, '</td>',
                        '<td>', this.all_num, '</td>',
                        '<td ', 'class="', (this.Percentage >= 60 ? 'text-navy' : 'text-warning'), '"',
                        '>', this.Percentage,
                        '</td>',
                        '<td>', '', '</td>',
                        '</tr>'
                    ].join('');
                } else {
                    var bt_id = ('bt' + i);
                    tbButtonID.push(bt_id);
                    this.td = [
                        '<tr>',
                        '<td>', (i + 1), '</td>',
                        '<td>', this.PackageName, '</td>',
                        '<td>', this.NextUpdateTime, '</td>',
                        '<td>', this.all_num, '</td>',
                        '<td ', 'class="',
                        (this.Percentage >= 60 ? 'text-navy' : 'text-warning'),
                        '"', '>', this.Percentage, '</td>',
                        '<td>', '<button type="button" ' +
                        'class="btn btn-sm btn-primary pull-right m-t-n-xs"',
                        'id="', bt_id, '"', '>', '点击查询流量',
                        '<span class="glyphicon glyphicon-search" aria-hidden="true"></span>', '</button>',
                        '</td>',
                        '</tr>'
                    ].join('');
                }
            };
            this.TableMake();
            return this.td
        }).call(table_data[i], i);
        tbHTML += td_i;
    }
    // remove old form html
    table_id.simPackage.children().remove();
    // append new form html
    table_id.simPackage.append(tbHTML);
    /**======================================
     * 后续添加button按钮对应的数据及动作函数
     *======================================*/
    addTableButtonAction(panel_param, next_ajax_data, table_data, tbButtonID);
}
/**==========================================================================
 * 动态添加批量button动作
 *
 * @param panel_param        设置面板参数
 * @param package_set_data   套餐查询设置条件
 * @param table_data         套餐表数据
 * @param bt_list_id         按钮列表
 */
function addTableButtonAction(panel_param, package_set_data, table_data, bt_list_id) {
    if (bt_list_id) {
        for (var i = 0; i < bt_list_id.length; i++) {
            var bt_num = Number((bt_list_id[i]).slice(2));
            // 实例button动作函数
            new ButtonAction($(["#", bt_list_id[i]].join('')), bt_num).BTClick(package_set_data, table_data[bt_num], panel_param);
        }
    }
}
/**====================================================
 *
 * 单一按钮实例化构造方法
 *
 * @param bt_id     button对应的id
 * @param bt_num    button对应行数
 * @constructor
 *====================================================*/
function ButtonAction(bt_id, bt_num) {
    this.btID = bt_id;
    this.btNum = bt_num;
}
/**
 *
 * @param first_set_param        首次ajax设置条件
 * @param get__row_package_data  归属button行的数据
 * @param panel_param            流量查询面板设置参数
 * @constructor
 */
ButtonAction.prototype.BTClick = function (first_set_param, get__row_package_data, panel_param) {
    this.btID.click(function () {
        var panelData = {
            LastUpdateTime: (
                get__row_package_data.LastUpdateTime === null ?
                    moment().set({'minute': 0, 'second': 0}) : get__row_package_data.LastUpdateTime),
            NextUpdateTime: (
                get__row_package_data.NextUpdateTime === null ?
                    moment().set({'minute': 0, 'second': 0}) : get__row_package_data.NextUpdateTime),
            PackageName: get__row_package_data.PackageName,
            SimNum: get__row_package_data.all_num

        };
        // 显示流量查询控制面板
        new SetPanelView(panel_param.modalID).SetPanelInit(panel_param, panelData);
    });
    return this;
};
/**===============================================================================
 *
 * 套餐统计ajax请求函数
 *
 * @param option_data
 * @param option_id
 * @param ajax_set
 * @param panel_set
 * @returns {boolean}
 */
function getPackageInfoAjax(option_data, option_id, ajax_set, panel_set) {
    var country = option_data.Country;
    var packageTypeName = option_data.PackageTypeName;
    var alertClass = 'warning';

    if (!country) {
        alert_str = ['查询国家未设置，', '请选择需要查询的国家！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.Warn);
    } else if (!packageTypeName) {
        alert_str = ['查询套餐未设置，', '请选输入要查询的套餐名！'].join(' ');
        appendAlertInfo(alertClass, alert_str, option_id.Warn);
    } else {
        var Notification = new Notificationbar(
            option_id.Notification,
            option_id.NotificationContainer,
            3000,
            false,
            option_id.NotificationContent
        );
        option_id.Warn.children().remove();
        //
        Notification.init();
        // 隐藏上次通知
        Notification.notificationAction('closeLast');
        // 清空历史表单
        option_id.TableSimPackage.simPackage.children().remove();
        var ajaxOption = {
            ajaxParam: {
                type: ajax_set.type,
                url: ajax_set.url,
                postData: ajax_set.data
            },
            idTag: {
                id_Alert: option_id.Warn,
                id_GetDataBt: option_id.DataGetButtonAjax,
                idTableSimPackage: option_id.TableSimPackage
            },
            objClass: {
                objNotification: Notification
            }
        };
        var packageInfoAjax = new AjaxFunc(ajaxOption.ajaxParam);
        var notifi_content = ['<strong>', '查询信息：', country, '。  数据获取中......', '</strong>'].join('');
        Notification.notificationContent(notifi_content);
        Notification.notificationAction('open');
        option_id.DataGetButtonAjax.attr("disabled", true);
        var packageInfoData = packageInfoAjax.GetAjax({
            idTag: ajaxOption.idTag,
            objClass: ajaxOption.objClass,
            panelSet: panel_set
        });
    }
    return false;
}
/**
 *
 * @param ajax_param
 * @param ajax_option
 * @returns {boolean}
 * @constructor
 */
function AjaxPackageFlowerGet(ajax_param, ajax_option) {
    var day_gap = moment(ajax_param.data.FlowerEndTime).diff(moment(ajax_param.data.FlowerBeginTime), 'days');
    var time_list =[];
    var query_type = 'day';
    var alertClass = 'warning';
    if (day_gap > 3){
        time_list = new GetSplitTimeDay(
            ajax_param.data.FlowerBeginTime,
            ajax_param.data.FlowerEndTime,
            day_gap).thirdPartListDic();
    }
    if (0<day_gap <= 3){
        query_type = 'hour';
        time_list.push({
            begin: new UnixTime(ajax_param.data.FlowerBeginTime).getUCTUnix(),
            end: new UnixTime(ajax_param.data.FlowerEndTime).getUCTUnix()
        })
    }
    var ajaxParam = {
        type: ajax_param.type,
        url: ajax_param.url,
        postData: {
        Country: ajax_param.data.Country,
            Org: ajax_param.data.Org,
        SimType: ajax_param.data.SimType,
        PackageTypeName: ajax_param.data.PackageTypeName,
        NextUpdateTime: ajax_param.data.NextUpdateTime,
        AvaStatus: ajax_param.data.AvaStatus,
        BusinessStatus: ajax_param.data.BusinessStatus,
        PackageStatus: ajax_param.data.PackageStatus,
        SlotStatus: ajax_param.data.SlotStatus,
        BamStatus: ajax_param.data.BamStatus,
        queryType: query_type,
        ListTime: time_list,
        addGroupKey: ajax_param.data.addGroupKey
    }
    };
    var ajaxOption = {
        idTag: {
            id_Alert: ajax_option.id.warn_sec_id,
            id_GetDataBt: ajax_option.id.bt_ajax_get_id,
            id_Grid: ajax_option.id.grid_sec_id,
            id_Modal: ajax_option.id.modal_id,
            id_ModalProgress: ajax_option.id.modalProgressID
        },
        objClass: {
            objGrid: ajax_option.obj.gri_obj
        }
    };
    var GetPackageFlowerNextAjax = new AjaxFunc(ajaxParam);
    var ifUrl = GetPackageFlowerNextAjax.ajaxParamCheck(['url']);

    if (!ifUrl) {
        alert_str = ['url设置有误，', '请重新设置！'].join(' ');
        appendAlertInfo(alertClass, alert_str, ajax_option.id.warn_sec_id);
        ajax_option.id.modal_id.modal('hide');

    } else if (day_gap<0){
        alert_str = ['查询时间设置有误，', '请重新设置！'].join(' ');
        appendAlertInfo(alertClass, alert_str, ajax_option.id.warn_sec_id);
        ajax_option.id.modal_id.modal('hide');
    }
    else {
        // 做表格数据清空操作
        ajax_option.id.grid_sec_id.jqxGrid("clear");
        // 禁用查询按钮,防止多次点击，造成重复查询
        ajax_option.id.bt_ajax_get_id.attr("disabled", true);
        ajax_option.id.modalProgressID.modal('show');
        ajax_option.id.modalProgressBarCl.animate({width: "100%"});
        var flower_package = GetPackageFlowerNextAjax.GridPostModalAjax(ajaxOption);
    }
    return false;
}
function GridColumnsSet() {
    this.dateFormat = 'yyyy-MM-dd HH:mm:ss';
    this.gridColumns = [];
}
/**===================================================
 *     ----------------套餐列设置初始化-----
 * @param grid_id
 * @param grid_src_adapter
 * @returns {GridColumnsSet}
 *====================================================*/
GridColumnsSet.prototype.setColumns = function (grid_id, grid_src_adapter) {
    this.gridColumns = [
        {
            text: 'num', sortable: true, filterable: false, editable: false, groupable: false, draggable: false,
            resizable: false, datafield: '', width: 50, columntype: 'number',
            cellsrenderer: function (row, column, value) {
                return "<div style='margin:4px;'>" + (value + 1) + "</div>";
            }
        },
        {text: '国家', datafield: 'country', filtertype: "range", width: 100, hidden: false},
        {
            text: 'imsi', datafield: 'imsi', width: 150,
            filtertype: "custom",
            createfilterpanel: function (datafield, filterPanel) {
                buildFilterPanel(filterPanel, datafield, grid_id, grid_src_adapter);
            }
        },
        {text: '套餐名称', datafield: 'package_name', filtertype: "range", width: 200, hidden: false},
        {text: 'iccid', datafield: 'iccid', filtertype: "range", width: 200, hidden: false},
        {
            text: '下次套餐更新时间', datafield: 'next_update_time', cellsformat: this.dateFormat, width: 300,
            filtertype: 'date', hidden: false
        },
        {
            text: 'time(GMT0)', datafield: 'time', cellsformat: this.dateFormat, width: 300,
            filtertype: 'date', hidden: true
        },
        {text: '累计流量/MB', datafield: 'flower', width: 200 , hidden: false }
    ];
    return this;
};
/**
 *
 * @param format_date
 */
GridColumnsSet.prototype.dateFormatSet = function (format_date) {
    this.dateFormat = format_date;
};
/**
 *
 * @returns {[*,*,*,*,*,*]}
 */
function gridFieldsSet() {
    return [
        {name: 'country', type: 'string'},
        {name: 'imsi', type: 'string'},
        {name: 'package_name', type: 'string'},
        {name: 'iccid', type: 'string'},
        {name: 'next_update_time', type: 'string'},
        {name: 'time', type: 'string'},
        {name: 'flower', type: 'number'}
    ];
}
//-显示选择菜单设置
var jqxDropDownList = [
    {label: '国家', value: 'country', checked: true},
    {label: 'imsi', value: 'imsi', checked: true},
    {label: '套餐名称', value: 'package_name', checked: true},
    {label: 'iccid', value: 'iccid', checked: true},
    {label: '下次套餐更新时间(GMT0)', value: 'time', checked: true},
    {label: 'time(GMT0)', value: 'time', checked: false},
    {label: '累计流量/MB', value: 'flower', checked: true}
];
//main-初始化主程序
$(function () {
    var globParam = {
        class: {
            selectCountryCL: $(".select-country"),
            selectOrgCL: $(".select-org"),
            selectSimTypeCL: $(".form-sim-type"),
            modalProgressBarCl: $(".progress-bar")
        },
        id: {
            getSimPackageID: $("#id-get-sim-package-info"),
            countrySelectID: $("#id-select-country"),
            orgSelectID: $("#id-select-org"),
            simTypeSelectID: $("#id-select-sim-type"),
            packageTypeNameInputID: $("#id-package-type-name"),
            warnFirLayerID: $("#id-warn-fir-layer"),
            notificationFirID: $("#id-notification-fir"),
            notificationContentFirID: $("#id-notification-content-fir"),
            notificationContainerFirID: $("#id-notification-container-fir"),
            tableSimPackageID: $("#id-package-table"),
            avaStatusID: $("#id-ava-status"),
            businessStatusID: $("#id-business-status"),
            packageStatusID: $("#id-package-status"),
            slotStatusID: $("#id-slot-status"),
            bamStatusID: $("#id-bam-status"),
            modalID: $("#id-package-flower-modal"),
            modalTitleID: $("#id-modal-title"),
            modalBodyID: $("#id-modal-body"),
            packageNameReadOnlyID: $("#id-package-type-name-readonly"),
            packageSimNumReadOnlyID: $("#id-package-sim-num-readonly"),
            packageUpdateTimeReadOnlyID: $("#id-package-next-update-readonly"),
            beginTimeID: $("#input-daterange-start"),
            endTimeID: $("#input-daterange-end"),
            chosenID: $("#id-chosen-panel"),
            queryFlowerID: $("#id-package-flower-bt"),
            modalProgressID: $("#id-progress-modal"),
            gridID: $("#id-package-flower-grid"),
            dropDownListID: $("#jqxDropDownList"),
            warnSecID: $("#id-warn-sec-layer"),
            notificationSecID: $("#id-notification-sec"),
            notificationContentSecID: $("#id-notification-content-sec"),
            notificationContainerSecID: $("#id-notification-container-sec")
        }
    };
    //select 下拉列表筛选数据-国家：
    var country_data = [{text: 'AD'}, {text: 'AE'}, {text: 'AF'}, {text: 'AG'}, {text: 'AI'}, {text: 'AL'}, {text: 'AM'}, {text: 'AO'}, {text: 'AQ'}, {text: 'AR'}, {text: 'AS'}, {text: 'AT'}, {text: 'AU'}, {text: 'AW'}, {text: 'AX'}, {text: 'AZ'}, {text: 'BA'}, {text: 'BB'}, {text: 'BD'}, {text: 'BE'}, {text: 'BF'}, {text: 'BG'}, {text: 'BH'}, {text: 'BI'}, {text: 'BJ'}, {text: 'BL'}, {text: 'BM'}, {text: 'BN'}, {text: 'BO'}, {text: 'BQ'}, {text: 'BR'}, {text: 'BS'}, {text: 'BT'}, {text: 'BV'}, {text: 'BW'}, {text: 'BY'}, {text: 'BZ'}, {text: 'CA'}, {text: 'CC'}, {text: 'CD'}, {text: 'CF'}, {text: 'CG'}, {text: 'CH'}, {text: 'CI'}, {text: 'CK'}, {text: 'CL'}, {text: 'CM'}, {text: 'CN'}, {text: 'CO'}, {text: 'CR'}, {text: 'CU'}, {text: 'CV'}, {text: 'CW'}, {text: 'CX'}, {text: 'CY'}, {text: 'CZ'}, {text: 'DE'}, {text: 'DJ'}, {text: 'DK'}, {text: 'DM'}, {text: 'DO'}, {text: 'DZ'}, {text: 'EC'}, {text: 'EE'}, {text: 'EG'}, {text: 'EH'}, {text: 'ER'}, {text: 'ES'}, {text: 'ET'}, {text: 'FI'}, {text: 'FJ'}, {text: 'FK'}, {text: 'FM'}, {text: 'FO'}, {text: 'FR'}, {text: 'GA'}, {text: 'GB'}, {text: 'GD'}, {text: 'GE'}, {text: 'GF'}, {text: 'GG'}, {text: 'GH'}, {text: 'GI'}, {text: 'GL'}, {text: 'GM'}, {text: 'GN'}, {text: 'GP'}, {text: 'GQ'}, {text: 'GR'}, {text: 'GS'}, {text: 'GT'}, {text: 'GU'}, {text: 'GW'}, {text: 'GY'}, {text: 'HK'}, {text: 'HM'}, {text: 'HN'}, {text: 'HR'}, {text: 'HT'}, {text: 'HU'}, {text: 'ID'}, {text: 'IE'}, {text: 'IL'}, {text: 'IM'}, {text: 'IN'}, {text: 'IO'}, {text: 'IQ'}, {text: 'IR'}, {text: 'IS'}, {text: 'IT'}, {text: 'JE'}, {text: 'JM'}, {text: 'JO'}, {text: 'JP'}, {text: 'KE'}, {text: 'KG'}, {text: 'KH'}, {text: 'KI'}, {text: 'KM'}, {text: 'KN'}, {text: 'KP'}, {text: 'KR'}, {text: 'KW'}, {text: 'KY'}, {text: 'KZ'}, {text: 'LA'}, {text: 'LB'}, {text: 'LC'}, {text: 'LI'}, {text: 'LK'}, {text: 'LR'}, {text: 'LS'}, {text: 'LT'}, {text: 'LU'}, {text: 'LV'}, {text: 'LY'}, {text: 'MA'}, {text: 'MC'}, {text: 'MD'}, {text: 'ME'}, {text: 'MF'}, {text: 'MG'}, {text: 'MH'}, {text: 'MK'}, {text: 'ML'}, {text: 'MM'}, {text: 'MN'}, {text: 'MO'}, {text: 'MP'}, {text: 'MQ'}, {text: 'MR'}, {text: 'MS'}, {text: 'MT'}, {text: 'MU'}, {text: 'MV'}, {text: 'MW'}, {text: 'MX'}, {text: 'MY'}, {text: 'MZ'}, {text: 'NA'}, {text: 'NC'}, {text: 'NE'}, {text: 'NF'}, {text: 'NG'}, {text: 'NI'}, {text: 'NL'}, {text: 'NO'}, {text: 'NP'}, {text: 'NR'}, {text: 'NU'}, {text: 'NZ'}, {text: 'OM'}, {text: 'PA'}, {text: 'PC'}, {text: 'PE'}, {text: 'PF'}, {text: 'PG'}, {text: 'PH'}, {text: 'PK'}, {text: 'PL'}, {text: 'PM'}, {text: 'PN'}, {text: 'PR'}, {text: 'PS'}, {text: 'PT'}, {text: 'PW'}, {text: 'PY'}, {text: 'QA'}, {text: 'RE'}, {text: 'RO'}, {text: 'RS'}, {text: 'RU'}, {text: 'RW'}, {text: 'SA'}, {text: 'SB'}, {text: 'SC'}, {text: 'SD'}, {text: 'SE'}, {text: 'SG'}, {text: 'SH'}, {text: 'SI'}, {text: 'SJ'}, {text: 'SK'}, {text: 'SL'}, {text: 'SM'}, {text: 'SN'}, {text: 'SO'}, {text: 'SR'}, {text: 'ST'}, {text: 'SV'}, {text: 'SX'}, {text: 'SY'}, {text: 'SZ'}, {text: 'TC'}, {text: 'TD'}, {text: 'TF'}, {text: 'TG'}, {text: 'TH'}, {text: 'TJ'}, {text: 'TK'}, {text: 'TL'}, {text: 'TM'}, {text: 'TN'}, {text: 'TO'}, {text: 'TR'}, {text: 'TT'}, {text: 'TV'}, {text: 'TW'}, {text: 'TZ'}, {text: 'UA'}, {text: 'UG'}, {text: 'UM'}, {text: 'US'}, {text: 'UY'}, {text: 'UZ'}, {text: 'VA'}, {text: 'VC'}, {text: 'VE'}, {text: 'VG'}, {text: 'VI'}, {text: 'VN'}, {text: 'VU'}, {text: 'WF'}, {text: 'WS'}, {text: 'YE'}, {text: 'YT'}, {text: 'ZA'}, {text: 'ZM'}, {text: 'ZW'}]
    // country init
    var select2Country = new Select2FuncBase(globParam.class.selectCountryCL, country_data);
    select2Country.init();
    select2Country.set('', true);
    //select 下拉列表筛选数据-org：
    var org_name = [{text: '35ORG'}, {text: 'a2network'}, {text: 'CelloMobile'}, {text: 'GFC_simbank'}, {text: 'GLOBALWIFI'},
        {text: '北京信威'}, {text: 'GWIFI'}, {text: 'JETFI桔豐科技'}, {text: 'LianLian'}, {text: 'POCWIFI'}, {text: 'TestMvno'},
        {text: 'VisonData-ORG'}, {text: 'YROAM'}, {text: 'all'}];
    // org init and set
    var select2Org = new Select2FuncBase(globParam.class.selectOrgCL, org_name);
    select2Org.init();
    select2Org.set('GTBU', false);
    // sim type ini and set
    var sim_type_data = [{text: '本国卡'}, {text: '多国卡'}];
    var select2SimType = new Select2FuncBase(globParam.class.selectSimTypeCL, sim_type_data);
    select2SimType.init();
    select2SimType.set('多国/本国', true);
    // tooltip init
    $('[data-toggle="tooltip"]').tooltip();
    // 初始grid
    var FlowerJqxGrid = new GridInit(globParam.id.gridID, gridFieldsSet());
    var GridColumnSet = new GridColumnsSet().setColumns(globParam.id.gridID, FlowerJqxGrid.GridAdapter);
    FlowerJqxGrid.set({columns: GridColumnSet.gridColumns});
    // 初始化drop down list 模块
    var DropDownList1 = new DropDownList(globParam.id.dropDownListID).Init({sourceList: jqxDropDownList});
    DropDownList1.OnClick(globParam.id.gridID);
    // 初始化chosen 模块
    globParam.id.chosenID.chosen({width: "100%"});
    globParam.id.chosenID.on('change', function (evt, params) {
        var ChosenAction = new ChosenView(globParam.id.gridID);
        var ActionID = {
            DropDownListID: globParam.id.dropDownListID
        };
        ChosenAction.GridAction(ActionID, params);
    });
    var NotificationSec = new Notificationbar(
        globParam.id.notificationSecID,
        globParam.id.notificationContainerSecID,
        3000,
        false,
        globParam.id.notificationContentSecID
    ).init();
    // 套餐统计ajax
    globParam.id.getSimPackageID.click(function () {
        //alert(moment(GlobeIdSet.timeStart.val()).add(moment().utcOffset(),'m').unix());
        var option = {
            data: {
                Country: globParam.id.countrySelectID.val(),
                PackageTypeName: globParam.id.packageTypeNameInputID.val()
            },
            id: {
                Notification: globParam.id.notificationFirID,
                NotificationContent: globParam.id.notificationContentFirID,
                NotificationContainer: globParam.id.notificationContainerFirID,
                Warn: globParam.id.warnFirLayerID,
                DataGetButtonAjax: globParam.id.getSimPackageID,
                TableSimPackage: {
                    simPackage: globParam.id.tableSimPackageID
                }
            },
            ajaxSet: {
                type: 'GET',
                url: $SCRIPT_ROOT + "/api/v1.0/get_package_flower/",
                data: {
                    Country: globParam.id.countrySelectID.val(),
                    Org: globParam.id.orgSelectID.val(),
                    SimType: globParam.id.simTypeSelectID.val() ?
                        ((globParam.id.simTypeSelectID.val() === '本国卡') ? '0' : '1') : '',
                    PackageTypeName: globParam.id.packageTypeNameInputID.val(),
                    AvaStatus: globParam.id.avaStatusID.val(),
                    BusinessStatus: globParam.id.businessStatusID.val(),
                    PackageStatus: globParam.id.packageStatusID.val(),
                    SlotStatus: globParam.id.slotStatusID.val(),
                    BamStatus: globParam.id.bamStatusID.val()
                }
            },
            panelSet: {
                modalID: globParam.id.modalID,
                modalTitleID: globParam.id.modalTitleID,
                modalBodyID: globParam.id.modalBodyID,
                packageNameReadOnlyID: globParam.id.packageNameReadOnlyID,
                packageSimNumReadOnlyID: globParam.id.packageSimNumReadOnlyID,
                packageUpdateTimeReadOnlyID: globParam.id.packageUpdateTimeReadOnlyID,
                chosenID: globParam.id.chosenID,
                beginTimeID: globParam.id.beginTimeID,
                endTimeID: globParam.id.endTimeID,
                queryFlowerID: globParam.id.queryFlowerID,
                modalHeadTitle: '流量查询设置窗口'
            }
        };
        getPackageInfoAjax(option.data, option.id, option.ajaxSet, option.panelSet);
    });
    globParam.id.queryFlowerID.click(function () {
        var option_sec = {
            ajax_param: {
                type: 'POST',
                url: $SCRIPT_ROOT + "/api/v1.0/get_package_flower_next/",
                data: {
                    Country: globParam.id.countrySelectID.val(),
                    Org: globParam.id.orgSelectID.val(),
                    SimType: globParam.id.simTypeSelectID.val() ?
                        ((globParam.id.simTypeSelectID.val() === '本国卡') ? '0' : '1') : '',
                    PackageTypeName: globParam.id.packageNameReadOnlyID.val(),
                    NextUpdateTime: globParam.id.packageUpdateTimeReadOnlyID.val(),
                    AvaStatus: globParam.id.avaStatusID.val(),
                    BusinessStatus: globParam.id.businessStatusID.val(),
                    PackageStatus: globParam.id.packageStatusID.val(),
                    SlotStatus: globParam.id.slotStatusID.val(),
                    BamStatus: globParam.id.bamStatusID.val(),
                    FlowerBeginTime: globParam.id.beginTimeID.val(),
                    FlowerEndTime: globParam.id.endTimeID.val(),
                    addGroupKey: globParam.id.chosenID.val()
                }
            },
            ajax_option: {
                id: {
                    notification_sec_id: globParam.id.notificationSecID,
                    notification_content_sec_id: globParam.id.notificationContentSecID,
                    notification_container_sec_id: globParam.id.notificationContainerSecID,
                    modal_id: globParam.id.modalID,
                    modalProgressID: globParam.id.modalProgressID,
                    modalProgressBarCl: globParam.class.modalProgressBarCl,
                    grid_sec_id: globParam.id.gridID,
                    warn_sec_id: globParam.id.warnSecID,
                    bt_ajax_get_id: globParam.id.queryFlowerID
                },
                obj: {
                    gri_obj: FlowerJqxGrid
                }
            }
        };
        AjaxPackageFlowerGet(option_sec.ajax_param, option_sec.ajax_option);
    });
});