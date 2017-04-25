/**
 * Created by lujian on 2017-04-25.
 */


function getPackageInfoAjax(option_data, option_id, ajax_set) {

    var country = option_data.Country;
    var packageTypeName = option_data.PackageTypeName;
    alert('进入套餐查询'+country+packageTypeName);


}
//main-初始化主程序
$(function () {
    var globParam = {
        class: {
            selectCountryCL: $(".select-country"),
            selectOrgCL: $(".select-org"),
            selectSimTypeCL: $(".form-sim-type")
        },
        id: {
            getSimPackageID: $("#id-get-sim-package-info"),
            countrySelectID: $("#id-select-country"),
            orgSelectID: $("#id-select-org"),
            simTypeSelectID: $("#id-select-sim-type"),
            packageTypeNameInputID: $("#id-package-type-name"),
            warnFirLayerID: $("#fir-layer-warn"),
            notificationFirID: $("#id-notification-fir"),
            notificationContentFirID: $("#id-notification-content-fir"),
            notificationContainerFirID: $("#id-notification-container-fir")
        }
    };
    //select 下拉列表筛选数据-国家：
    var country_data = [{text: 'AD'}, {text: 'AE'}, {text: 'AF'}, {text: 'AG'}, {text: 'AI'}, {text: 'AL'}, {text: 'AM'}, {text: 'AO'}, {text: 'AQ'}, {text: 'AR'}, {text: 'AS'}, {text: 'AT'}, {text: 'AU'}, {text: 'AW'}, {text: 'AX'}, {text: 'AZ'}, {text: 'BA'}, {text: 'BB'}, {text: 'BD'}, {text: 'BE'}, {text: 'BF'}, {text: 'BG'}, {text: 'BH'}, {text: 'BI'}, {text: 'BJ'}, {text: 'BL'}, {text: 'BM'}, {text: 'BN'}, {text: 'BO'}, {text: 'BQ'}, {text: 'BR'}, {text: 'BS'}, {text: 'BT'}, {text: 'BV'}, {text: 'BW'}, {text: 'BY'}, {text: 'BZ'}, {text: 'CA'}, {text: 'CC'}, {text: 'CD'}, {text: 'CF'}, {text: 'CG'}, {text: 'CH'}, {text: 'CI'}, {text: 'CK'}, {text: 'CL'}, {text: 'CM'}, {text: 'CN'}, {text: 'CO'}, {text: 'CR'}, {text: 'CU'}, {text: 'CV'}, {text: 'CW'}, {text: 'CX'}, {text: 'CY'}, {text: 'CZ'}, {text: 'DE'}, {text: 'DJ'}, {text: 'DK'}, {text: 'DM'}, {text: 'DO'}, {text: 'DZ'}, {text: 'EC'}, {text: 'EE'}, {text: 'EG'}, {text: 'EH'}, {text: 'ER'}, {text: 'ES'}, {text: 'ET'}, {text: 'FI'}, {text: 'FJ'}, {text: 'FK'}, {text: 'FM'}, {text: 'FO'}, {text: 'FR'}, {text: 'GA'}, {text: 'GB'}, {text: 'GD'}, {text: 'GE'}, {text: 'GF'}, {text: 'GG'}, {text: 'GH'}, {text: 'GI'}, {text: 'GL'}, {text: 'GM'}, {text: 'GN'}, {text: 'GP'}, {text: 'GQ'}, {text: 'GR'}, {text: 'GS'}, {text: 'GT'}, {text: 'GU'}, {text: 'GW'}, {text: 'GY'}, {text: 'HK'}, {text: 'HM'}, {text: 'HN'}, {text: 'HR'}, {text: 'HT'}, {text: 'HU'}, {text: 'ID'}, {text: 'IE'}, {text: 'IL'}, {text: 'IM'}, {text: 'IN'}, {text: 'IO'}, {text: 'IQ'}, {text: 'IR'}, {text: 'IS'}, {text: 'IT'}, {text: 'JE'}, {text: 'JM'}, {text: 'JO'}, {text: 'JP'}, {text: 'KE'}, {text: 'KG'}, {text: 'KH'}, {text: 'KI'}, {text: 'KM'}, {text: 'KN'}, {text: 'KP'}, {text: 'KR'}, {text: 'KW'}, {text: 'KY'}, {text: 'KZ'}, {text: 'LA'}, {text: 'LB'}, {text: 'LC'}, {text: 'LI'}, {text: 'LK'}, {text: 'LR'}, {text: 'LS'}, {text: 'LT'}, {text: 'LU'}, {text: 'LV'}, {text: 'LY'}, {text: 'MA'}, {text: 'MC'}, {text: 'MD'}, {text: 'ME'}, {text: 'MF'}, {text: 'MG'}, {text: 'MH'}, {text: 'MK'}, {text: 'ML'}, {text: 'MM'}, {text: 'MN'}, {text: 'MO'}, {text: 'MP'}, {text: 'MQ'}, {text: 'MR'}, {text: 'MS'}, {text: 'MT'}, {text: 'MU'}, {text: 'MV'}, {text: 'MW'}, {text: 'MX'}, {text: 'MY'}, {text: 'MZ'}, {text: 'NA'}, {text: 'NC'}, {text: 'NE'}, {text: 'NF'}, {text: 'NG'}, {text: 'NI'}, {text: 'NL'}, {text: 'NO'}, {text: 'NP'}, {text: 'NR'}, {text: 'NU'}, {text: 'NZ'}, {text: 'OM'}, {text: 'PA'}, {text: 'PC'}, {text: 'PE'}, {text: 'PF'}, {text: 'PG'}, {text: 'PH'}, {text: 'PK'}, {text: 'PL'}, {text: 'PM'}, {text: 'PN'}, {text: 'PR'}, {text: 'PS'}, {text: 'PT'}, {text: 'PW'}, {text: 'PY'}, {text: 'QA'}, {text: 'RE'}, {text: 'RO'}, {text: 'RS'}, {text: 'RU'}, {text: 'RW'}, {text: 'SA'}, {text: 'SB'}, {text: 'SC'}, {text: 'SD'}, {text: 'SE'}, {text: 'SG'}, {text: 'SH'}, {text: 'SI'}, {text: 'SJ'}, {text: 'SK'}, {text: 'SL'}, {text: 'SM'}, {text: 'SN'}, {text: 'SO'}, {text: 'SR'}, {text: 'ST'}, {text: 'SV'}, {text: 'SX'}, {text: 'SY'}, {text: 'SZ'}, {text: 'TC'}, {text: 'TD'}, {text: 'TF'}, {text: 'TG'}, {text: 'TH'}, {text: 'TJ'}, {text: 'TK'}, {text: 'TL'}, {text: 'TM'}, {text: 'TN'}, {text: 'TO'}, {text: 'TR'}, {text: 'TT'}, {text: 'TV'}, {text: 'TW'}, {text: 'TZ'}, {text: 'UA'}, {text: 'UG'}, {text: 'UM'}, {text: 'US'}, {text: 'UY'}, {text: 'UZ'}, {text: 'VA'}, {text: 'VC'}, {text: 'VE'}, {text: 'VG'}, {text: 'VI'}, {text: 'VN'}, {text: 'VU'}, {text: 'WF'}, {text: 'WS'}, {text: 'YE'}, {text: 'YT'}, {text: 'ZA'}, {text: 'ZM'}, {text: 'ZW'}]
    // country init
    var select2Country = new Select2FuncBase(globParam.class.selectCountryCL, country_data);
    select2Country.init();
    select2Country.set('', true);
    //select 下拉列表筛选数据-org：
    var org_name = [{text:'35ORG'}, {text:'a2network'}, {text:'CelloMobile'}, {text:'GFC_simbank'}, {text:'GLOBALWIFI'},
        {text:'北京信威'}, {text:'GWIFI'}, {text:'JETFI桔豐科技'}, {text:'LianLian'}, {text:'POCWIFI'}, {text:'TestMvno'},
        {text:'VisonData-ORG'}, {text:'YROAM'}, {text:'all'}];
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
    globParam.id.getSimPackageID.click( function (){
        //alert(moment(GlobeIdSet.timeStart.val()).add(moment().utcOffset(),'m').unix());
        var option = {
            data:{
                Country: globParam.id.countrySelectID.val(),
                Org: globParam.id.orgSelectID.val(),
                SimType : globParam.id.simTypeSelectID.val(),
                PackageTypeName : globParam.id.packageTypeNameInputID.val()
            },
            id:{
                Notification: globParam.id.notificationFirID,
                NotificationContent: globParam.id.notificationContentFirID,
                NotificationContainer: globParam.id.notificationContainerFirID,
                Warn: globParam.id.warnFirLayerID,
                DataGetButtonAjax: globParam.id.getSimPackageID
            },
            ajaxSet:{
                type: 'GET',
                url: $SCRIPT_ROOT + "/api/v1.0/get_package_flower/",
                data: this.data
            }
        };
        getPackageInfoAjax(option.data, option.id, option.ajaxSet);
    });
});