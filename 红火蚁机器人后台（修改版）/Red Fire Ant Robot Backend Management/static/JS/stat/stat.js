;

var myChart1 = echarts.init(document.getElementById('obj_val'),'dark');
// 指定图表的配置项和数据
var option1 = {
    title: {
        text: '最近一周下发的命令',
        left:'center',
        
    },
    dataZoom: [{
              type: 'slider',
              show: true, //flase直接隐藏图形
              xAxisIndex: [0],
              left: '5%', //滚动条靠左侧的百分比
              bottom: -1,
              start: 0,//滚动条的起始位置
              end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
          }],
    grid:{
       containLabel:true

    },
    tooltip:{//配置提示弹窗
            trigger:'item',
            formatter:'{b}<br/>下发{c}个命令',

        },
    xAxis: {
        name:"星期",
        nameTextStyle: { // x轴name的样式调整
            color: 'white', 
            fontSize: 14,
          },
          nameGap: 25,  // x轴name与横坐标轴线的间距
          nameLocation: "middle", // x轴name处于x轴的什么位置
          type: 'category',
        data:['周日','周一','周二','周三','周四','周五','周六']
    },
    yAxis: {
        name:"下发的命令个数",
        type: 'value',
        nameTextStyle: { // x轴name的样式调整
            color: 'white', 
            fontSize: 14,
        },
        axisLabel : {
        formatter: '{value} 个'}
    },
 
    series: [
            {
                type: 'bar',	//line折线图。bar柱形图
                data:[1,3,6,1,2,4,1],
               
                // itemStyle:{normal: {color:"#31b0d5"}}
                itemStyle:{normal: {color:"#2ec7c9"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#06FFFD'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }
                },
              
                
            }
    ],
    color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [{
            offset: 0, color: 'rgb(118, 214, 243)' // 0% 处的颜色
        }, {
            offset: 1, color: 'aqua' // 100% 处的颜色
        }],
        globalCoord: false // 缺省为 false
    }
    };
myChart1.setOption(option1);


var myChart2 = echarts.init(document.getElementById('room_val'),'dark');
var option2 = {
    title: {
        text: '正运行的环境终端土壤温度',
        left:'center',

    },

    grid:{
       containLabel:true

    },

    dataset:{
        // 提供一份数据
        source:[
            ['product','1号集群','2号集群','6号集群'],
            ['10h前',20,21,25],
            ['9h前',19,19,25],
            ['8h前',18,23,25],
            ['7h前',18,24,26],
            ['6h前',19,23,28],
            ['5h前',19,25,27],
            ['4h前',18,25,28],
            ['3h前',20,25,28],
            ['2h前',20,25,27],
            ['1h前',21,26,28],
            ['现在',21,26,28],

        ]
    },
    // 图例位置
    legend: {
        orient:'vertical',
        x:'right',
        y:'top',
        padding:[10.10,0,0]
    },
    tooltip: {},
    dataZoom: [{
              type: 'slider',
              show: true, //flase直接隐藏图形
              xAxisIndex: [0],
              left: '18%', //滚动条靠左侧的百分比
              bottom: -1,
              start: 0,//滚动条的起始位置
              end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
          }],
    xAxis: {
        name:"过去10小时",
        // nameLocation:"middle",
        nameTextStyle: { // x轴name的样式调整
            color: 'white',
            fontSize: 14,
          },
          nameGap: 25,  // x轴name与横坐标轴线的间距
          nameLocation: "middle", // x轴name处于x轴的什么位置
          type: 'category',
        // data:['S408','S407','S405' ]
    },
    yAxis: {
        name:"土壤温度",
        type: 'value',
        nameTextStyle: { // x轴name的样式调整
            color: 'white',
            fontSize: 14,
        },
        axisLabel : {
        formatter: '{value} 度'}
    },
    series: [
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#2ec7c9"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#06FFFD'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }
                },
                lineStyle:{
                    width:4
                }


            },
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#b6a2de"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#9a7fd1'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }

                },
                lineStyle:{
                    width:4
                }

                // stack: 'x'

            },
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#3fb1e3"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#3fb1e3'
                    //   color: '#0066FF'
                    },

                },
                lineStyle:{
                    width:4
                }

                // stack: 'x'
            }
        ]
    };
myChart2.setOption(option2);

var myChart3 = echarts.init(document.getElementById('warning_val'),'dark');
var option3 = {
    title: {
        text: '正运行的环境终端土壤湿度',
        left:'center',

    },
     grid:{
       containLabel:true
    },
    dataset:{
        // 提供一份数据
         source:[
            ['product','1号集群','2号集群','6号集群'],
            ['10h前',29,21,35],
            ['9h前',28,19,34],
            ['8h前',25,59,33],
            ['7h前',23,55,30],
            ['6h前',18,53,28],
            ['5h前',69,50,24],
            ['4h前',58,45,20],
            ['3h前',57,44,65],
            ['2h前',55,42,55],
            ['1h前',53,40,54],
            ['现在',50,39,50],

        ]
    },
    // 图例位置
    legend: {
        orient:'vertical',
        x:'right',
        y:'top',
        padding:[10.10,0,0]
    },
    tooltip: {},
     dataZoom: [{
              type: 'slider',
              show: true, //flase直接隐藏图形
              xAxisIndex: [0],
              left: '18%', //滚动条靠左侧的百分比
              bottom: -1,
              start: 0,//滚动条的起始位置
              end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
          }],
    xAxis: {
        name:"过去10小时",
        // nameLocation:"middle",
        nameTextStyle: { // x轴name的样式调整
            color: 'white', 
            fontSize: 14,
          },
          nameGap: 25,  // x轴name与横坐标轴线的间距
          nameLocation: "middle", // x轴name处于x轴的什么位置
          type: 'category',

    },
    yAxis: {
        name:"土壤湿度",
        type: 'value',
        nameTextStyle: { // x轴name的样式调整
            color: 'white', 
            fontSize: 14,
        },
        axisLabel : {
        formatter: '{value} %'}
    },
    series: [
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#2ec7c9"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#06FFFD'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }
                },
                lineStyle:{
                    width:4
                }
                
                
            },
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#b6a2de"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#9a7fd1'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }
                    
                },
                lineStyle:{
                    width:4
                }
                
                // stack: 'x'
                
            },
            {
                type: 'line',	//line折线图。bar柱形图
                // data:[25,5,39],
                itemStyle:{normal: {color:"#3fb1e3"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#3fb1e3'
                    //   color: '#0066FF'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: '致信楼S408'
                    }
                },
                lineStyle:{
                    width:4
                }
                
                // stack: 'x'
            }
        ]
    };
myChart3.setOption(option3);

var myChart4 = echarts.init(document.getElementById('mem_val'),'dark');
var option4 = {
      title: {
        text: '最近一个月设置的环境终端集群',
        left:'center',

    },
    dataZoom: [{
              type: 'slider',
              show: true, //flase直接隐藏图形
              xAxisIndex: [0],
              left: '15%', //滚动条靠左侧的百分比
              bottom: -1,
              start: 0,//滚动条的起始位置
              end: 100 //滚动条的截止位置（按比例分割你的柱状图x轴长度）
          }],
    grid:{
       containLabel:true

    },
    tooltip:{//配置提示弹窗
            trigger:'item',
            formatter:'{b}<br/>新建{c}个箱体',

        },
    xAxis: {
        name:"周",
        nameTextStyle: { // x轴name的样式调整
            color: 'white',
            fontSize: 14,
          },
          nameGap: 15,  // x轴name与横坐标轴线的间距
          nameLocation: "middle", // x轴name处于x轴的什么位置
          type: 'category',
        data:['第一周','第二周','第三周','第四周']
    },
    yAxis: {
        name:"新建环境终端集群数",
        type: 'value',
        nameTextStyle: { // x轴name的样式调整
            color: 'white',
            fontSize: 14,
        },
        axisLabel : {
        formatter: '{value} 个'}
    },

    series: [
            {
                type: 'bar',	//line折线图。bar柱形图
                data:[1,3,6,1],
                // itemStyle:{normal: {color:"#31b0d5"}}
                itemStyle:{normal: {color:"#2ec7c9"}},
                emphasis: {
                    itemStyle: {
                      // 高亮时点的颜色。
                      color: '#06FFFD'
                    },
                    label: {
                      show: true,
                      // 高亮时标签的文字。
                      formatter: ''
                    }
                },


            }
    ],
    color: {
        type: 'linear',
        x: 0,
        y: 0,
        x2: 0,
        y2: 1,
        colorStops: [{
            offset: 0, color: 'rgb(118, 214, 243)' // 0% 处的颜色
        }, {
            offset: 1, color: 'aqua' // 100% 处的颜色
        }],
        globalCoord: false // 缺省为 false
    }
    };
myChart4.setOption(option4);

var myChart5 = echarts.init(document.getElementById('map'),'dark');
$.get('../static/JS/stat/data.json',function(geoJson){
    echarts.registerMap('SZUN',geoJson,{});
    var option5 = {
        title: {
        text: '环境终端集群校园分布',
        left:'center',

    },
        tooltip:{//配置提示弹窗
            trigger:'item',
            formatter:'{b}<br/>{c}(环境终端集群/个)',
            
        },
        visualMap:{
            min:0,
            max:10,
            text:['High','Low'],
            left:'right',
            realtime:false,
            calculable:true,
            inRange:{

                color:['#957ef2','#66FFCC','#32fdfa','#08e0df','#3366ff','#feff77','#ffa83e','#ff7544','#f83435']
//                color:['#ffffff','#c9e8fa','#9fecff','#40cff3']
            }
        },
        series:[{

            name: 'SZUN',
            type: 'map',
            mapType: 'SZUN', // 自定义扩展图表类型，必须和registerMap的第一个参数相同
            roam: true, //可以拖拽和缩放
            aspectScale:1.5,
            label: {
                show: true,
                color: 'white',
                fontWeight:'bolder'
              },
            data: [
                { name: '校区', value: 20 },
                { name: '学院1', value:9 },
                { name: '学院2', value: 7},
                { name: '学院3', value: 3 },
                { name: '学院4', value: 0 },
                { name: '学院5', value: 0},
                { name: '学院6', value: 1 },
                { name: '教学楼1', value: 0 },
                { name: '教学楼2', value: 0 },
                { name: '教学楼3', value: 0 },
                { name: '学院7', value: 0 },
                { name: '宿舍1', value: 0 },
                { name: '食堂', value: 0 },
                { name: '学院8', value: 0 },
                { name: '宿舍2', value: 0 },


            ]
        }]
       

    };
    myChart5.setOption(option5);
})
