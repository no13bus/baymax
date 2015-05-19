$(function() {
        Highcharts.setOptions({
            global: {
                useUTC: false
            }
        });
        var steps_chart = new Highcharts.Chart({
            chart: {
                type: 'spline',
                renderTo: 'steps_chart'
            },
            title: {
                text: '步数'
            },

            xAxis: {
                type: 'datetime',
                title: {
                    text: '日期'
                }
            },
            yAxis: {
                title: {
                    text: '步数'
                }
            },
            loading: {
                hideDuration: 1000,
                showDuration: 1000
            },
            tooltip: {
                headerFormat: '<b>{series.name}</b><br>',
                pointFormat: 'time: {point.x:%Y-%m-%e} <br> 步数: {point.y}'
            },
            series: [{
                name: 'Steps'
            }]
        });
        var coding_chart = new Highcharts.Chart({
                chart: {
                    type: 'column',
                    renderTo: 'coding_chart'
                },
                title: {
                    text: 'GitHub代码提交次数'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: '日期'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Commit次数'
                    }
                },
                loading: {
                    hideDuration: 1000,
                    showDuration: 1000
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'time: {point.x:%Y-%m-%e} <br> Commit 数量: {point.y}'
                },
                series: [{
                    name: 'Coding'
                }]
            });
        var calories_out_chart = new Highcharts.Chart({
                chart: {
                    type: 'spline',
                    renderTo: 'calories_out_chart'
                },
                title: {
                    text: '消耗卡路里'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: '日期'
                    }
                },
                yAxis: {
                    title: {
                        text: '卡路里(卡)'
                    }
                },
            loading: {
                hideDuration: 1000,
                showDuration: 1000
            },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'time: {point.x:%Y-%m-%e} <br> 卡路里: {point.y}'
                },
                series: [{
                    name: 'calories_out'
                }]
            });
        var distance_chart = new Highcharts.Chart({
                chart: {
                    type: 'spline',
                    renderTo: 'distance_chart'
                },
                title: {
                    text: '步行距离'
                },                
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: '日期'
                    }
                },
                yAxis: {
                    title: {
                        text: '距离(km)'
                    }
                },
            loading: {
                hideDuration: 1000,
                showDuration: 1000
            },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'time: {point.x:%Y-%m-%e} <br> 卡路里: {point.y}'
                },
                series: [{
                    name: 'distance'
                }]
            });
        var times_chart = new Highcharts.Chart({
                chart: {
                    type: 'spline',
                    renderTo: 'times_chart'
                },
                title: {
                    text: '网络时间分布'
                },
                xAxis: {
                    type: 'datetime',
                    title: {
                        text: '日期'
                    }
                },
                yAxis: {
                    title: {
                        text: '花费的时间(小时)'
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: 'time: {point.x:%Y-%m-%e} <br> 小时数: {point.y}'
                },

                loading: {
                    hideDuration: 1000,
                    showDuration: 1000
                },
                series: [{
                    name: '开发'
                },
                {
                    name: '沟通&计划'
                },
                {
                    name: '信息&新闻'
                },
                {
                    name: '娱乐'
                }
                ]
            });

        var steps_data = [];
        var coding_data = [];
        var calories_out_data = [];
        var distance_data = [];
        var communication_and_scheduling_data = [];
        var entertainment_data = [];
        var news_data = [];
        var software_development_data = [];

        function getForm() {
            var url = "/api/user/" + username + "/steps";
            $.ajax({
                url: "/api/user/"+username+"/steps",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0){
                        for (var i=0; i<obj['result'].length; i++){
                            steps_data.push({x:Date.parse(obj['result'][i][0]),y:parseFloat(obj['result'][i][1])});
                        }
                        steps_chart.series[0].setData(steps_data);
                        steps_chart.hideLoading();
                    }else{
                        $('#steps_chart').hide();
                    }

                },
                error: function() {
                    alert('Show steps error!')
                }
            });
            $.ajax({
                url: "/api/user/"+username+"/coding",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            coding_data.push({x: Date.parse(obj['result'][i][0]), y: parseFloat(obj['result'][i][1])});
                        }
                        coding_chart.series[0].setData(coding_data);
                        coding_chart.hideLoading();
                    }else{
                        $('#coding_chart').hide();
                    }
                },
                error: function() {
                    alert('Show coding error!')
                }
            });

            $.ajax({
                url: "/api/user/"+username+"/calories_out",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            calories_out_data.push({
                                x: Date.parse(obj['result'][i][0]),
                                y: parseFloat(obj['result'][i][1])
                            });
                        }
                        calories_out_chart.series[0].setData(calories_out_data);
                        calories_out_chart.hideLoading();
                    }else{
                        $('#calories_out_chart').hide();
                    }
                },
                error: function() {
                    alert('Show calories_out error!')
                }
            });

            $.ajax({
                url: "/api/user/"+username+"/distance",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            distance_data.push({
                                x: Date.parse(obj['result'][i][0]),
                                y: parseFloat(obj['result'][i][1])
                            });
                        }
                        distance_chart.series[0].setData(distance_data);
                        distance_chart.hideLoading();
                    }else{
                        $('#distance_chart').hide();
                    }

                },
                error: function() {
                    alert('Show distance error!')
                }
            });

            $.ajax({
                url: "/api/user/"+username+"/communication_and_scheduling",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            communication_and_scheduling_data.push({
                                x: Date.parse(obj['result'][i][0]),
                                y: parseFloat(obj['result'][i][1])
                            });
                        }
                        times_chart.series[0].setData(communication_and_scheduling_data);
                    }

                },
                error: function() {
                    alert('Show communication_and_scheduling error!')
                }
            });
            $.ajax({
                url: "/api/user/"+username+"/news",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            news_data.push({x: Date.parse(obj['result'][i][0]), y: parseFloat(obj['result'][i][1])});
                        }
                        times_chart.series[1].setData(news_data);
                    }

                },
                error: function() {
                    alert('Show news error!')
                }
            });
            $.ajax({
                url: "/api/user/"+username+"/software_development",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            software_development_data.push({
                                x: Date.parse(obj['result'][i][0]),
                                y: parseFloat(obj['result'][i][1])
                            });
                        }
                        times_chart.series[2].setData(software_development_data);
                    }else{
                        $('#times_chart').hide();
                    }

                },
                error: function() {
                    alert('Show software_development_data error!')
                }
            });
            $.ajax({
                url: "/api/user/"+username+"/entertainment",
                dataType: "json",
                async: true,
                success: function(point) {
                    var obj = eval(point);
                    if (obj['result'].length > 0) {
                        for (var i = 0; i < obj['result'].length; i++) {
                            entertainment_data.push({
                                x: Date.parse(obj['result'][i][0]),
                                y: parseFloat(obj['result'][i][1])
                            });
                        }
                        times_chart.series[3].setData(entertainment_data);
                    }
                },
                error: function() {
                    alert('Show entertainment error!')
                }
            });
            steps_chart.showLoading();
            coding_chart.showLoading();
            calories_out_chart.showLoading();
            distance_chart.showLoading();

        }
        getForm();
    });