;
// 温度湿度折线图
var chartDom1 = document.getElementById('1');
var myChart1 = echarts.init(chartDom1);
var option1;
var now = new Date();
var month = now.getMonth()+1
var date=now.getDate()
var one_day=24*60*60*1000
var tomorrow=new Date(now.getTime()+one_day)
var tomorrow2=new Date(now.getTime()+one_day*2)
var tomorrow3=new Date(now.getTime()+one_day*3)
var date1=tomorrow.getDate()
var date2=tomorrow2.getDate()
var date3=tomorrow3.getDate()
var jsonStr
var select=document.getElementById('city');
var xh2=new XMLHttpRequest()
select.addEventListener('change',function () {
    getweather(this.value)
})
function getweather(c){
    var url =`https://restapi.amap.com/v3/weather/weatherInfo?city=${c}市&key=5ddbeb883cc30e150b9a51e9c5e4e0c8&extensions=all`
    console.log(url)
    xh2.open('GET',url,true);
    xh2.send()
    xh2.onreadystatechange=function(){
        if (xh2.readyState == 4 && xh2.status == 200){
            var a = JSON.stringify(xh2.responseText)
                console.log(a,typeof(a));
                jsonStr = a;

            // 正则表达式只匹配"temperature"字段后的温度值
            let regex = /"daytemp\\":\\"(\d+)\\"/g;
            let matches;
            let dayTemps = [];

            while ((matches = regex.exec(jsonStr)) !== null) {
                // matches[1] 包含数字部分
                dayTemps.push(parseInt(matches[1])); // 转换为整数
            }

            console.log(dayTemps); // 输出: [36, 36, 34, 34]

            option1.series[0].data=dayTemps
            console.log(option1)
            myChart1.setOption(option1)




    }}
    }

option1 = {
    title: {
        text: '温度'
    },
    dataZoom: [{
        type: 'slider',
        show: true, //flase直接隐藏图形
        xAxisIndex: [0],
        left: '10%', //滚动条靠左侧的百分比
        bottom: -1,
        start: 0,//滚动条的起始位置
        end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
    }],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true }
        }
    },
    legend: {
        data: ['温度']
    },
    xAxis: [
        {
            type: 'category',
            data: [`${month}-${date}`, `${month}-${date1}`, `${month}-${date2}`, `${month}-${date3}`],
            axisPointer: {
                type: 'shadow'
            }
        }
    ],
    yAxis: [
         {
            type: 'value',
            name: '温度',
            min: 20,
            max: 40,
            interval: 2,
            axisLabel: {
                formatter: '{value} °C'
            }
        },
        {
            type: 'value',
            name: '',
            min: 20,
            max: 40,
            interval: 2,
            axisLabel: {
                formatter: ' '
            }
        }

    ],
    series: [
        {
            name: '温度',
            type: 'bar',
            yAxisIndex: 1,
            tooltip: {
                valueFormatter: function (value) {
                    return value + ' °C';
                }
            },
            data: [28, 28, 27, 28]
        },
        {
            name: '温度',
            type: '',
            tooltip: {
                valueFormatter: function (value) {
                    return value + ' %';
                }
            },
            data:
             [28, 28, 27, 28]
        },

    ]
};

myChart1.setOption(option1);

//光照强度and光谱频段
var chartDom2 = document.getElementById('2');
var myChart2 = echarts.init(chartDom2);
var option2 = {
    title: {
        text: '近年来全球与广东治理投入规模'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['广东治理投入规模', '全国治理投入规模', ],
        right:'15px',
        top:'1px'
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['2013', '2016', '2019', '2022', '2025E', '2028E']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name: '广东治理投入规模',
            type: 'line',
           
            data: [2397.81, 3119.94, 3140.64, 3083.93, 4925.18, 5643.39]
        },
        {
            name: '全国治理投入规模',
            type: 'line',
            
            data: [3268.5, 4183.51, 10912.05,12378.57,15340.54,18451.51]
        },
        
    ]
};

myChart2.setOption(option2);

//含水量与PH值
var chartDom3 = document.getElementById('3');
var myChart3 = echarts.init(chartDom3);
var option3;

option3 = {
    title: {
        text: '       运行详情图'
    },
    dataZoom: [{
        type: 'slider',
        show: true, //flase直接隐藏图形
        xAxisIndex: [0],
        left: '10%', //滚动条靠左侧的百分比
        bottom: -1,
        start: 0,//滚动条的起始位置
        end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
    }],
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'cross',
            crossStyle: {
                color: '#999'
            }
        }
    },
    toolbox: {
        feature: {
            dataView: { show: true, readOnly: false },
            magicType: { show: true, type: ['line', 'bar'] },
            restore: { show: true },
            saveAsImage: { show: true }
        }
    },
    legend: {
        data: ['执行中的机器人数量']
    },
    xAxis: [
        {
            type: 'category',
            data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月','8月','9月','10月','11月','12月'],
            axisPointer: {
                type: 'shadow'
            }
        }
    ],
    yAxis: [
        {
            type: 'value',
            name: '执行中的机器人数量/台',
            min: 0,
            max: 30,
            interval: 5,
            axisLabel: {
                formatter: '{value}'
            }
        },
        // {
        //     type: 'value',
        //     name: '发现蚁巢的数量/窝',
        //     min: 0,
        //     max: 30,
        //     interval: 5,
        //     axisLabel: {
        //         formatter: '{value}'
        //     }
        // }
    ],
    series: [
        {
            name: '执行中的机器人数量',
            type: 'bar',
            tooltip: {
                valueFormatter: function (value) {
                    return value + ' 台';
                }
            },
            data: [
                6, 4, 8, 16, 13, 19, 20, 11, 14, 8, 4, 3
            ]
        },
        // {
        //     name: '发现蚁巢的数量',
        //     type: 'line',
        //     yAxisIndex: 1,
        //     tooltip: {
        //         valueFormatter: function (value) {
        //             return value + ' 窝';
        //         }
        //     },
        //     data: [20,30,14,34,27,42,46,20,18,34,14,10]
        // }
    ]
};
myChart3.setOption(option3);

//各种土壤元素含量折线图
var chartDom4 = document.getElementById('4');
var myChart4 = echarts.init(chartDom4);
var option4 = {
    title: {
        text: '蚁巢数量图'
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data: ['蚁巢的数量']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1月', '2月', '3月', '4月', '5月', '6月', '7月','8月','9月','10月','11月','12月']
    },
    yAxis: {
        type: 'value',
        name: '窝数',
        min: 0,
        max: 50,
        interval: 5,
    },
    series: [
          {
            name: '蚁巢的数量',
            type: 'line',
            // yAxisIndex: 1,
            tooltip: {
                valueFormatter: function (value) {
                    return value + ' 窝';
                }
            },
            data: [20,30,14,34,27,42,46,20,18,34,14,10]
        }
        // {
        //     name: 'N',
        //     type: 'line',

        //     data: [120, 132, 101, 134, 90, 230, 210]
        // },
        // {
        //     name: 'P',
        //     type: 'line',

        //     data: [220, 182, 191, 234, 290, 330, 310]
        // },
        // {
        //     name: 'S',
        //     type: 'line',

        //     data: [200, 142, 196, 234, 296, 260, 310]
        // },
        // {
        //     name: 'K',
        //     type: 'line',

        //     data: [210, 189, 156, 252, 268, 300, 284]
        // },
        // {
        //     name: 'Ca',
        //     type: 'line',

        //     data: [160, 189, 220, 259, 258, 150, 320]
        // }
    ]
};

myChart4.setOption(option4);


$(".wrap>.head").click(
    // $(".wrap>.item").toggle()
    $(".wrap")
)