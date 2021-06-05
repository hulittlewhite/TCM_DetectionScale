export function upDate() {
    setKey.value = $.datainteraction.upDate(setKey.value);
    setValue.value = setKey.value;
}

export function getdata() {
    try {
        let url = "http://192.168.43.178:5000/";
        $.getJSON({
            url: url,
            data: {},
            success: postSuccess,
            fail: postFailure
        });
    } catch (e) {
        alert(e);
    }
}

export function postSuccess(res) {
    console.log(res);
    var t1 = document.getElementById("category_count_id");
    var t2 = document.getElementById("total_amount_id");
    var t3 = document.getElementById("total_id");
    t1.innerHTML = res["category_count"];
    t2.innerHTML = res["total_amount"];
    t3.innerHTML = res["total"];
}

export function postFailure() {
    console.log("请求失败");
}

export function getproducts() {
    try {
        let url = "http://192.168.43.178:5000/getproducts";
        $.getJSON({
            url: url,
            data: {},
            success: updata_table,
            fail: function () {
                alert("请求失败！");
            }
        });
    } catch (e) {
        alert(e);
    }
}

export function updata_table(data) {
    // alert(data);
    var products_table = document.getElementById("products_table");
    var product_total_table = document.getElementById("product_total_table");
    var product_table_html;
    var product_total_html;
    product_table_html = "<tr>" +
        "<th>中药名称</th>" +
        "<th>中药重量</th>" +
        "<th>中药单价</th>" +
        "<th>小计</th>" +
        "</tr>";
    product_total_html = "<tr>" +
        "<th>中药种类</th>" +
        "<th>中药总重</th>" +
        "<th>总价</th>" +
        "</tr>";
    var products_count = 0;
    var total_price = 0;
    for (var i = 0; i < data.length; i++) {
        var subtotal = data[i]["unit_price"] * data[i]["products_count"];
        products_count += data[i]["products_count"];
        total_price += subtotal;
        var tr1 = "<tr>" +
            `<th>${data[i]["name"]}</th>` +
            `<th>${data[i]["products_count"]}g</th>` +
            `<th>¥${data[i]["unit_price"]}/g</th>` +
            `<th>¥${parseFloat(subtotal).toFixed(2)}</th>` +
            "</tr>";
        product_table_html += tr1;
    }

    products_table.innerHTML = product_table_html;

    product_total_html += "<tr>" +
        `<th>${data.length}</th>` +
        `<th>${parseFloat(products_count).toFixed(2)}g</th>` +
        `<th>¥${parseFloat(total_price).toFixed(2)}</th>` +
        "</tr>";
    product_total_table.innerHTML = product_total_html;
}

//重复执行某个方法
var t1 = window.setInterval(getdata, 1000);
var t2 = window.setInterval(getproducts, 1000);
//去掉定时器的方法
//window.clearInterval(t1);
