/**
 * Created by lujian on 2017-04-27.
 */


/**
 *
 * @type {string}
 */


/**     --------appendManulForm func-------
 *
 * @param modal_title_id: modal title name string value to make different title;
 * @param modal_body_id: id obtaining jquery type var inserted form data into modal body html;
 * @param modal_head_name: value to set modal head title;
 * @param temple_title: value to set modal html get_temple_button name.
 * @returns {boolean}
 */

function appendManulForm(modal_title_id, modal_body_id, modal_head_name, temple_title){
    /**
     *
     * @type {string}
     * @private
     */
    var idModalTitle = modal_title_id;
    var idModalbody = modal_body_id;
    idModalTitle.text(modal_head_name);

    //var manulForm = ();
    // remove old form html
    //idModalbody.children().remove();
    // append new form html
    //idModalbody.append(manulForm);
    return false;
}
function SetPanelView(modal_id){
    this.clickBtId = modal_id;

}
SetPanelView.prototype.SetPanelInit = function (panel_param, panel_data) {
    //$("#progressAjax").jqxLoader({ text: "提交更新数据中...", width: 100, height: 60 });
    var actionParam = panel_param;
    // 套餐流量设置
    var dateBegin = new Mydaterange(0, 'h', panel_param.beginTimeID).SetTime(panel_data.LastUpdateTime);
    dateBegin.initTime({'minute': 0, 'second': 0}, "YYYY-MM-DD HH");
    var dateEnd = new Mydaterange(0, 'h', panel_param.endTimeID).SetTime(panel_data.NextUpdateTime);
    dateEnd.initTime({'minute': 0, 'second': 0}, "YYYY-MM-DD HH");
    //append html of modal
    var appendHtlm = appendManulForm(actionParam.modalTitleID, actionParam.modalBodyID, actionParam.modalHeadTitle,
        actionParam.getTempleTitle);
    // show modal
    this.clickBtId.modal();
};
// 点击查询构造ajax
function PackageFlowerGetAjax(id_bt_get ) {
    //this.PostData =
}