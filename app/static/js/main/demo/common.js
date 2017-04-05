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