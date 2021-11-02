const localhost_ip = "http://10.8.34.218:8080";

function localIp(path) {
    return localhost_ip + path;
}

function selectOmsFun() {
    let selectFun = document.getElementById("select-fun")
    let functionElements = document.getElementsByName("functions")
    // 获取被选中的索引
    let funX = selectFun.selectedIndex;
    functionElements.forEach(function (value, index) {
        let selectedFun = document.getElementById("fun" + index)
        if (funX == index) {
            selectedFun.style["display"] = "inline"
        } else {
            selectedFun.style["display"] = "none"
        }
    })
}