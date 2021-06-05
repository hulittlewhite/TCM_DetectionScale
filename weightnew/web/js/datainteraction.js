$.datainteraction = {
    getname: function () {
        try {
            var data = {name: "miao", age: 20}
            // var data = {name: "hh", age: "info"}
            var url = "http://127.0.0.1:5000/";
            $.get({
                method: "GET",
                url: url,
                data: {name: "hh", age: "info"},
                success: function (data) {
                    alert("请求成功：" + data);
                },
                failure: function () {
                    alert("请求失败");
                }
            });
        } catch (e) {
            alert(e);
        }
    },
    dataAdd: function (data) {
        data = parseInt(data) + 1;
        return data;
    },
    upDate: function (data) {
        data = $.datainteraction.dataAdd(data);
        return data;
    },
}
