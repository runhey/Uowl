.pragma library

// GET
function get(url, success, failure)
{
    var xhr = new XMLHttpRequest;
    xhr.open("GET", url);
    xhr.onreadystatechange = function() {
        handleResponse(xhr, success, failure);
    }
    xhr.send();
}

// POST
function post(url, arg, success, failure)
{
    var xhr = new XMLHttpRequest;
    xhr.open("POST", url);
    xhr.setRequestHeader("Content-Length", arg.length);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded;");  //用POST的时候一定要有这句
    xhr.onreadystatechange = function() {
        handleResponse(xhr, success, failure);
    }
    xhr.send(arg);
}

// 处理返回值
function handleResponse(xhr, success, failure){
    if (xhr.readyState === XMLHttpRequest.DONE) {
        if (xhr.status ===  200){
            if (success !== null && success !== undefined)
            {
                var result = xhr.responseText;
                try{
                    success(result, JSON.parse(result));
                }catch(e){
                    success(result, {});
                }
            }
        }
        else{
            if (failure !== null && failure !== undefined)
                failure(xhr.responseText, xhr.status);
        }
    }
}
