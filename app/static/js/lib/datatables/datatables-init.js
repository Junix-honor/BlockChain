$(document).ready(function () {
    $('#myTable').DataTable(
        {
            "bPaginate": true, //翻页功能
            "bLengthChange": true, //改变每页显示数据数量
            "bFilter": true, //过滤功能
            "bSort": false, //排序功能
            "bInfo": true,//页脚信息
            "bAutoWidth": true,//自动宽度
            "aaSorting": [[1, "desc"]],//默认第几个排序
            "bStateSave": true,//状态保存
            "pading": false,
            // "pagingType": "full_numbers",
            "searching": true,//搜索框是否显示
            "lengthChange": true,//左上角每页显示条数是否显示
            "oLanguage": {//插件的汉化
                "sLengthMenu": "每页显示 _MENU_ 条记录",
                "sZeroRecords": "抱歉， 没有找到",
                "sInfo": "从 _START_ 到 _END_ /共 _TOTAL_ 条数据",
                "sInfoEmpty": "没有数据",
                "sInfoFiltered": "(从 _MAX_ 条数据中检索)",
                "oPaginate": {
                    "sFirst": "首页",
                    "sPrevious": "前一页",
                    "sNext": "后一页",
                    "sLast": "尾页"
                },
                "sZeroRecords": "没有检索到数据",
                "sProcessing": "<img src='' />",
                "sSearch": "Search"
            },
            dom: '<B><lfrtip>',
            buttons: [
                {
                    text: 'Add',
                    action: function (e, dt, node, config) {
                        alert('Activated!');
                        this.disable(); // disable button
                    }
                },
                {
                    extend: 'excel',
                    text: 'Export'
                },
            ]
        }
    )
});
