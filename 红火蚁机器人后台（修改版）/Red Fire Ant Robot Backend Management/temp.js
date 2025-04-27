/*
        License here,
        I dont think too  much about licence
        just feel free to do anything you want... :-)
*/
var PrettyJSON = {
    view: {},
    tpl: {}
};
PrettyJSON.util = {
    isObject: function (v) {
        return Object.prototype.toString.call(v) === '[object Object]';
    },
    pad: function (str, length) {
        str = String(str);
        while (str.length < length)
            str = '0' + str;
        return str;
    },
    dateFormat: function (date, f) {
        f = f.replace('YYYY', date.getFullYear());
        f = f.replace('YY', String(date.getFullYear()).slice(-2));
        f = f.replace('MM', PrettyJSON.util.pad(date.getMonth() + 1, 2));
        f = f.replace('DD', PrettyJSON.util.pad(date.getDate(), 2));
        f = f.replace('HH24', PrettyJSON.util.pad(date.getHours(), 2));
        f = f.replace('HH', PrettyJSON.util.pad((date.getHours() % 12), 2));
        f = f.replace('MI', PrettyJSON.util.pad(date.getMinutes(), 2));
        f = f.replace('SS', PrettyJSON.util.pad(date.getSeconds(), 2));
        return f;
    }
}
PrettyJSON.tpl.Node = '' + '<span class="node-container">' + '<span class="node-top node-bracket" />' + '<span class="node-content-wrapper">' + '<ul class="node-body" />' + '</span>' + '<span class="node-down node-bracket" />' + '</span>';
PrettyJSON.tpl.Leaf = '' + '<span class="leaf-container">' + '<span class="<%= type %>"> <%-data%></span><span><%= coma %></span>' + '</span>';
PrettyJSON.view.Node = Backbone.View.extend({
    tagName: 'span',
    data: null,
    level: 1,
    path: '',
    type: '',
    size: 0,
    isLast: true,
    rendered: false,
    events: {
        'click .node-bracket': 'collapse',
        'mouseover .node-container': 'mouseover',
        'mouseout .node-container': 'mouseout'
    },
    initialize: function (opt) {
        if (opt.data instanceof AMap.LngLat) {
            opt.data = {
                lng: opt.data.lng,
                lat: opt.data.lat
            }
        }
        this.options = opt;
        this.data = this.options.data;
        this.level = this.options.level || this.level;
        this.path = this.options.path;
        this.isLast = _.isUndefined(this.options.isLast) ? this.isLast : this.options.isLast;
        this.dateFormat = this.options.dateFormat;
        var m = this.getMeta();
        this.type = m.type;
        this.size = m.size;
        this.childs = [];
        this.render();
        if (this.level == 1)
            this.show();
    },
    getMeta: function () {
        var val = {
            size: _.size(this.data),
            type: _.isArray(this.data) ? 'array' : 'object',
        };
        return val;
    },
    elements: function () {
        this.els = {
            container: $(this.el).find('.node-container'),
            contentWrapper: $(this.el).find('.node-content-wrapper'),
            top: $(this.el).find('.node-top'),
            ul: $(this.el).find('.node-body'),
            down: $(this.el).find('.node-down')
        };
    },
    render: function () {
        this.tpl = _.template(PrettyJSON.tpl.Node);
        $(this.el).html(this.tpl);
        this.elements();
        var b = this.getBrackets();
        this.els.top.html(b.top);
        this.els.down.html(b.bottom);
        this.hide();
        return this;
    },
    renderChilds: function () {
        var count = 1;
        _.each(this.data, function (val, key) {
            var isLast = (count == this.size);
            count = count + 1;
            var path = (this.type == 'array') ? this.path + '[' + key + ']' : this.path + '.' + key;
            var opt = {
                key: key,
                data: val,
                parent: this,
                path: path,
                level: this.level + 1,
                dateFormat: this.dateFormat,
                isLast: isLast
            };
            var child = (PrettyJSON.util.isObject(val) || _.isArray(val)) ? new PrettyJSON.view.Node(opt) : new PrettyJSON.view.Leaf(opt);
            child.on('mouseover', function (e, path) {
                this.trigger("mouseover", e, path);
            }, this);
            child.on('mouseout', function (e) {
                this.trigger("mouseout", e);
            }, this);
            var li = $('<li/>');
            var colom = '&nbsp;:&nbsp;';
            var left = $('<span />');
            var right = $('<span />').append(child.el);
            (this.type == 'array') ? left.html('') : left.html(key + colom);
            left.append(right);
            li.append(left);
            this.els.ul.append(li);
            child.parent = this;
            this.childs.push(child);
        }, this);
    },
    isVisible: function () {
        return this.els.contentWrapper.is(":visible");
    },
    collapse: function (e) {
        e.stopPropagation();
        this.isVisible() ? this.hide() : this.show();
        this.trigger("collapse", e);
    },
    show: function () {
        if (!this.rendered) {
            this.renderChilds();
            this.rendered = true;
        }
        this.els.top.html(this.getBrackets().top);
        this.els.contentWrapper.show();
        this.els.down.show();
    },
    hide: function () {
        var b = this.getBrackets();
        this.els.top.html(b.close);
        this.els.contentWrapper.hide();
        this.els.down.hide();
    },
    getBrackets: function () {
        var v = {
            top: '{',
            bottom: '}',
            close: '{ ... }'
        };
        if (this.type == 'array') {
            v = {
                top: '[',
                bottom: ']',
                close: '[ ... ]'
            };
        }
        ; v.bottom = (this.isLast) ? v.bottom : v.bottom + ',';
        v.close = (this.isLast) ? v.close : v.close + ',';
        return v;
    },
    mouseover: function (e) {
        e.stopPropagation();
        this.trigger("mouseover", e, this.path);
    },
    mouseout: function (e) {
        e.stopPropagation();
        this.trigger("mouseout", e);
    },
    expandAll: function () {
        _.each(this.childs, function (child) {
            if (child instanceof PrettyJSON.view.Node) {
                child.show();
                child.expandAll();
            }
        }, this);
        this.show();
    },
    collapseAll: function () {
        _.each(this.childs, function (child) {
            if (child instanceof PrettyJSON.view.Node) {
                child.hide();
                child.collapseAll();
            }
        }, this);
        if (this.level != 1)
            this.hide();
    }
});
PrettyJSON.view.Leaf = Backbone.View.extend({
    tagName: 'span',
    data: null,
    level: 0,
    path: '',
    type: 'string',
    isLast: true,
    events: {
        "mouseover .leaf-container": "mouseover",
        "mouseout .leaf-container": "mouseout"
    },
    initialize: function (opt) {
        this.options = opt;
        this.data = this.options.data;
        this.level = this.options.level;
        this.path = this.options.path;
        this.type = this.getType();
        this.dateFormat = this.options.dateFormat;
        this.isLast = _.isUndefined(this.options.isLast) ? this.isLast : this.options.isLast;
        this.render();
    },
    getType: function () {
        var m = 'string';
        var d = this.data;
        if (_.isNumber(d))
            m = 'number';
        else if (_.isBoolean(d))
            m = 'boolean';
        else if (_.isDate(d))
            m = 'date';
        else if (_.isNull(d))
            m = 'null'
        return m;
    },
    getState: function () {
        var coma = this.isLast ? '' : ',';
        var state = {
            data: this.data,
            level: this.level,
            path: this.path,
            type: this.type,
            coma: coma
        };
        return state;
    },
    render: function () {
        var state = this.getState();
        if (state.type == 'date' && this.dateFormat) {
            state.data = PrettyJSON.util.dateFormat(this.data, this.dateFormat);
        }
        if (state.type == 'null') {
            state.data = 'null';
        }
        if (state.type == 'string') {
            state.data = (state.data == '') ? '""' : '"' + state.data + '"';
        }
        this.tpl = _.template(PrettyJSON.tpl.Leaf);
        $(this.el).html(this.tpl(state));
        return this;
    },
    mouseover: function (e) {
        e.stopPropagation();
        var path = this.path + '&nbsp;:&nbsp;<span class="' + this.type + '"><b>' + this.data + '</b></span>';
        this.trigger("mouseover", e, path);
    },
    mouseout: function (e) {
        e.stopPropagation();
        this.trigger("mouseout", e);
    }
});






{
    // //     //地图区县高亮
    // //     var adCode = 230404;
    // //     var depth = 2;
    // //     var temp = [{'中文名': '广州市', 'adcode': 440100, 'citycode': 20}, {'中文名': '广州市市辖区', 'adcode': 440101, 'citycode': 20}, {'中文名': '荔湾区', 'adcode': 440103, 'citycode': 20}, {'中文名': '越秀区', 'adcode': 440104, 'citycode': 20}, {'中文名': '海珠区', 'adcode': 440105, 'citycode': 20}, {'中文名': '天河区', 'adcode': 440106, 'citycode': 20}, {'中文名': '白云区', 'adcode': 440111, 'citycode': 20}, {'中文名': '黄埔区', 'adcode': 440112, 'citycode': 20}, {'中文名': '番禺区', 'adcode': 440113, 'citycode': 20}, {'中文名': '花都区', 'adcode': 440114, 'citycode': 20}, {'中文名': '南沙区', 'adcode': 440115, 'citycode': 20}, {'中文名': '从化区', 'adcode': 440117, 'citycode': 20}, {'中文名': '增城区', 'adcode': 440118, 'citycode': 20}, {'中文名': '韶关市', 'adcode': 440200, 'citycode': 751}, {'中文名': '韶关市市辖区', 'adcode': 440201, 'citycode': 751}, {'中文名': '武江区', 'adcode': 440203, 'citycode': 751}, {'中文名': '浈江区', 'adcode': 440204, 'citycode': 751}, {'中文名': '曲江区', 'adcode': 440205, 'citycode': 751}, {'中文名': '始兴县', 'adcode': 440222, 'citycode': 751}, {'中文名': '仁化县', 'adcode': 440224, 'citycode': 751}, {'中文名': '翁源县', 'adcode': 440229, 'citycode': 751}, {'中文名': '乳源瑶族自治县', 'adcode': 440232, 'citycode': 751}, {'中文名': '新丰县', 'adcode': 440233, 'citycode': 751}, {'中文名': '乐昌市', 'adcode': 440281, 'citycode': 751}, {'中文名': '南雄市', 'adcode': 440282, 'citycode': 751}, {'中文名': '深圳市', 'adcode': 440300, 'citycode': 755}, {'中文名': '深圳市市辖区', 'adcode': 440301, 'citycode': 755}, {'中文名': '罗湖区', 'adcode': 440303, 'citycode': 755}, {'中文名': '福田区', 'adcode': 440304, 'citycode': 755}, {'中文名': '南山区', 'adcode': 440305, 'citycode': 755}, {'中文名': '宝安区', 'adcode': 440306, 'citycode': 755}, {'中文名': '龙岗区', 'adcode': 440307, 'citycode': 755}, {'中文名': '盐田区', 'adcode': 440308, 'citycode': 755}, {'中文名': '龙华区', 'adcode': 440309, 'citycode': 755}, {'中文名': '坪山区', 'adcode': 440310, 'citycode': 755}, {'中文名': '光明区', 'adcode': 440311, 'citycode': 755}, {'中文名': '珠海市', 'adcode': 440400, 'citycode': 756}, {'中文名': '珠海市市辖区', 'adcode': 440401, 'citycode': 756}, {'中文名': '香洲区', 'adcode': 440402, 'citycode': 756}, {'中文名': '斗门区', 'adcode': 440403, 'citycode': 756}, {'中文名': '金湾区', 'adcode': 440404, 'citycode': 756}, {'中文名': '汕头市', 'adcode': 440500, 'citycode': 754}, {'中文名': '汕头市市辖区', 'adcode': 440501, 'citycode': 754}, {'中文名': '龙湖区', 'adcode': 440507, 'citycode': 754}, {'中文名': '金平区', 'adcode': 440511, 'citycode': 754}, {'中文名': '濠江区', 'adcode': 440512, 'citycode': 754}, {'中文名': '潮阳区', 'adcode': 440513, 'citycode': 754}, {'中文名': '潮南区', 'adcode': 440514, 'citycode': 754}, {'中文名': '澄海区', 'adcode': 440515, 'citycode': 754}, {'中文名': '南澳县', 'adcode': 440523, 'citycode': 754}, {'中文名': '佛山市', 'adcode': 440600, 'citycode': 757}, {'中文名': '佛山市市辖区', 'adcode': 440601, 'citycode': 757}, {'中文名': '禅城区', 'adcode': 440604, 'citycode': 757}, {'中文名': '南海区', 'adcode': 440605, 'citycode': 757}, {'中文名': '顺德区', 'adcode': 440606, 'citycode': 757}, {'中文名': '三水区', 'adcode': 440607, 'citycode': 757}, {'中文名': '高明区', 'adcode': 440608, 'citycode': 757}, {'中文名': '江门市', 'adcode': 440700, 'citycode': 750}, {'中文名': '江门市市辖区', 'adcode': 440701, 'citycode': 750}, {'中文名': '蓬江区', 'adcode': 440703, 'citycode': 750}, {'中文名': '江海区', 'adcode': 440704, 'citycode': 750}, {'中文名': '新会区', 'adcode': 440705, 'citycode': 750}, {'中文名': '台山市', 'adcode': 440781, 'citycode': 750}, {'中文名': '开平市', 'adcode': 440783, 'citycode': 750}, {'中文名': '鹤山市', 'adcode': 440784, 'citycode': 750}, {'中文名': '恩平市', 'adcode': 440785, 'citycode': 750}, {'中文名': '湛江市', 'adcode': 440800, 'citycode': 759}, {'中文名': '湛江市市辖区', 'adcode': 440801, 'citycode': 759}, {'中文名': '赤坎区', 'adcode': 440802, 'citycode': 759}, {'中文名': '霞山区', 'adcode': 440803, 'citycode': 759}, {'中文名': '坡头区', 'adcode': 440804, 'citycode': 759}, {'中文名': '麻章区', 'adcode': 440811, 'citycode': 759}, {'中文名': '遂溪县', 'adcode': 440823, 'citycode': 759}, {'中文名': '徐闻县', 'adcode': 440825, 'citycode': 759}, {'中文名': '廉江市', 'adcode': 440881, 'citycode': 759}, {'中文名': '雷州市', 'adcode': 440882, 'citycode': 759}, {'中文名': '吴川市', 'adcode': 440883, 'citycode': 759}, {'中文名': '茂名市', 'adcode': 440900, 'citycode': 668}, {'中文名': '茂名市市辖区', 'adcode': 440901, 'citycode': 668}, {'中文名': '茂南区', 'adcode': 440902, 'citycode': 668}, {'中文名': '电白区', 'adcode': 440904, 'citycode': 668}, {'中文名': '高州市', 'adcode': 440981, 'citycode': 668}, {'中文名': '化州市', 'adcode': 440982, 'citycode': 668}, {'中文名': '信宜市', 'adcode': 440983, 'citycode': 668}, {'中文名': '肇庆市', 'adcode': 441200, 'citycode': 758}, {'中文名': '肇庆市市辖区', 'adcode': 441201, 'citycode': 758}, {'中文名': '端州区', 'adcode': 441202, 'citycode': 758}, {'中文名': '鼎湖区', 'adcode': 441203, 'citycode': 758}, {'中文名': '高要区', 'adcode': 441204, 'citycode': 758}, {'中文名': '广宁县', 'adcode': 441223, 'citycode': 758}, {'中文名': '怀集县', 'adcode': 441224, 'citycode': 758}, {'中文名': '封开县', 'adcode': 441225, 'citycode': 758}, {'中文名': '德庆县', 'adcode': 441226, 'citycode': 758}, {'中文名': '四会市', 'adcode': 441284, 'citycode': 758}, {'中文名': '惠州市', 'adcode': 441300, 'citycode': 752}, {'中文名': '惠州市市辖区', 'adcode': 441301, 'citycode': 752}, {'中文名': '惠城区', 'adcode': 441302, 'citycode': 752}, {'中文名': '惠阳区', 'adcode': 441303, 'citycode': 752}, {'中文名': '博罗县', 'adcode': 441322, 'citycode': 752}, {'中文名': '惠东县', 'adcode': 441323, 'citycode': 752}, {'中文名': '龙门县', 'adcode': 441324, 'citycode': 752}, {'中文名': '梅州市', 'adcode': 441400, 'citycode': 753}, {'中文名': '梅州市市辖区', 'adcode': 441401, 'citycode': 753}, {'中文名': '梅江区', 'adcode': 441402, 'citycode': 753}, {'中文名': '梅县区', 'adcode': 441403, 'citycode': 753}, {'中文名': '大埔县', 'adcode': 441422, 'citycode': 753}, {'中文名': '丰顺县', 'adcode': 441423, 'citycode': 753}, {'中文名': '五华县', 'adcode': 441424, 'citycode': 753}, {'中文名': '平远县', 'adcode': 441426, 'citycode': 753}, {'中文名': '蕉岭县', 'adcode': 441427, 'citycode': 753}, {'中文名': '兴宁市', 'adcode': 441481, 'citycode': 753}, {'中文名': '汕尾市', 'adcode': 441500, 'citycode': 660}, {'中文名': '汕尾市市辖区', 'adcode': 441501, 'citycode': 660}, {'中文名': '城区', 'adcode': 441502, 'citycode': 660}, {'中文名': '海丰县', 'adcode': 441521, 'citycode': 660}, {'中文名': '陆河县', 'adcode': 441523, 'citycode': 660}, {'中文名': '陆丰市', 'adcode': 441581, 'citycode': 660}, {'中文名': '河源市', 'adcode': 441600, 'citycode': 762}, {'中文名': '河源市市辖区', 'adcode': 441601, 'citycode': 762}, {'中文名': '源城区', 'adcode': 441602, 'citycode': 762}, {'中文名': '紫金县', 'adcode': 441621, 'citycode': 762}, {'中文名': '龙川县', 'adcode': 441622, 'citycode': 762}, {'中文名': '连平 县', 'adcode': 441623, 'citycode': 762}, {'中文名': '和平县', 'adcode': 441624, 'citycode': 762}, {'中文名': '东源县', 'adcode': 441625, 'citycode': 762}, {'中文名': '阳江 市', 'adcode': 441700, 'citycode': 662}, {'中文名': '阳江市市辖区', 'adcode': 441701, 'citycode': 662}, {'中文名': '江城区', 'adcode': 441702, 'citycode': 662}, {'中文名': '阳东区', 'adcode': 441704, 'citycode': 662}, {'中文名': '阳西县', 'adcode': 441721, 'citycode': 662}, {'中文名': '阳春市', 'adcode': 441781, 'citycode': 662}, {'中文名': '清远市', 'adcode': 441800, 'citycode': 763}, {'中文名': '清远市市辖区', 'adcode': 441801, 'citycode': 763}, {'中文名': '清城区', 'adcode': 441802, 'citycode': 763}, {'中文名': '清新区', 'adcode': 441803, 'citycode': 763}, {'中文名': '佛冈县', 'adcode': 441821, 'citycode': 763}, {'中文名': '阳山县', 'adcode': 441823, 'citycode': 763}, {'中文名': '连山壮族瑶族自治县', 'adcode': 441825, 'citycode': 763}, {'中文名': '连南瑶族自治县', 'adcode': 441826, 'citycode': 763}, {'中文名': '英德市', 'adcode': 441881, 'citycode': 763}, {'中文名': '连州市', 'adcode': 441882, 'citycode': 763}, {'中文名': '东莞市', 'adcode': 441900, 'citycode': 769}, {'中文名': '中山市', 'adcode': 442000, 'citycode': 760}, {'中文名': '潮州市', 'adcode': 445100, 'citycode': 768}, {'中文名': '潮州市市辖区', 'adcode': 445101, 'citycode': 768}, {'中文名': '湘桥区', 'adcode': 445102, 'citycode': 768}, {'中文名': '潮安区', 'adcode': 445103, 'citycode': 768}, {'中文名': '饶平县', 'adcode': 445122, 'citycode': 768}, {'中文名': '揭阳市', 'adcode': 445200, 'citycode': 663}, {'中文名': '揭阳市市辖区', 'adcode': 445201, 'citycode': 663}, {'中文名': '榕城区', 'adcode': 445202, 'citycode': 663}, {'中文名': '揭东区', 'adcode': 445203, 'citycode': 663}, {'中文名': '揭西县', 'adcode': 445222, 'citycode': 663}, {'中文名': '惠来县', 'adcode': 445224, 'citycode': 663}, {'中文名': '普宁市', 'adcode': 445281, 'citycode': 663}, {'中文名': '云浮市', 'adcode': 445300, 'citycode': 766}, {'中文名': '云浮市市辖区', 'adcode': 445301, 'citycode': 766}, {'中文名': '云城区', 'adcode': 445302, 'citycode': 766}, {'中文名': '云安区', 'adcode': 445303, 'citycode': 766}, {'中文名': '新兴县', 'adcode': 445321, 'citycode': 766}, {'中文名': '郁南县', 'adcode': 445322, 'citycode': 766}, {'中文名': '罗定市', 'adcode': 445381, 'citycode': 766}]
    // //     var adcodes_province = [{ "adcode": 100000, "name": "全国" }, { "adcode": 110000, "name": "北京市" }, { "adcode": 120000, "name": "天津市" }, { "adcode": 130000, "name": "河北省" }, { "adcode": 140000, "name": "山西省" }, { "adcode": 150000, "name": "内蒙古自治区" }, { "adcode": 210000, "name": "辽宁省" }, { "adcode": 220000, "name": "吉林省" }, { "adcode": 230000, "name": "黑龙江省" }, { "adcode": 310000, "name": "上海市" }, { "adcode": 320000, "name": "江苏省" }, { "adcode": 330000, "name": "浙江省" }, { "adcode": 340000, "name": "安徽省" }, { "adcode": 350000, "name": "福建省" }, { "adcode": 360000, "name": "江西省" }, { "adcode": 370000, "name": "山东省" }, { "adcode": 410000, "name": "河南省" }, { "adcode": 420000, "name": "湖北省" }, { "adcode": 430000, "name": "湖南省" }, { "adcode": 440000, "name": "广东省" }, { "adcode": 450000, "name": "广西壮族自治区" }, { "adcode": 460000, "name": "海南省" }, { "adcode": 500000, "name": "重庆市" }, { "adcode": 510000, "name": "四川省" }, { "adcode": 520000, "name": "贵州省" }, { "adcode": 530000, "name": "云南省" }, { "adcode": 540000, "name": "西藏自治区" }, { "adcode": 610000, "name": "陕西省" }, { "adcode": 620000, "name": "甘肃省" }, { "adcode": 630000, "name": "青海省" }, { "adcode": 640000, "name": "宁夏回族自治区" }, { "adcode": 650000, "name": "新疆维吾尔自治区" }, { "adcode": 710000, "name": "台湾省" }, { "adcode": 810000, "name": "香港特别行政区" }, { "adcode": 820000, "name": "澳门特别行政区" }]
    // //     var adcodes_city = []
    // //     var adcodes_district =[]
    // //     // 创建省份图层
    // //     var disProvince;
    // //     function initPro(code, dep) {
    // //         dep = typeof dep == 'undefined' ? 2 : dep;
    // //         adCode = code;
    // //         depth = dep;

    // //         disProvince && disProvince.setMap(null);

    // //         disProvince = new AMap.DistrictLayer.Province({
    // //             zIndex: 12,
    // //             adcode: [code],
    // //             depth: dep,
    // //             styles: {
    // //                 'fill': function (properties) {
    // //                     // properties为可用于做样式映射的字段，包含
    // //                     // NAME_CHN:中文名称
    // //                     // adcode_pro
    // //                     // adcode_cit
    // //                     // adcode
    // //                     var adcode = properties.adcode;
    // //                     return getColorByAdcode(adcode);
    // //                 },
    // //                 'province-stroke': 'cornflowerblue',
    // //                 'city-stroke': 'white', // 中国地级市边界
    // //                 'county-stroke': 'rgba(255,255,255,0.5)' // 中国区县边界
    // //             }
    // //         });

    // //         disProvince.setMap(map);
    // //     }
    // //     // 颜色辅助方法
    // //     var colors = {};
    // //     var getColorByAdcode = function (adcode) {
    // //         if (!colors[adcode]) {
    // //             var gb = Math.random() * 155 + 50;
    // //             colors[adcode] = 'rgb(' + gb + ',' + gb + ',255)';
    // //         }

    // //         return colors[adcode];
    // //     };

    // //     // 按钮事件
    // //     function changeAdcode(e) {
    // //         var code = e.target.value;
    // //         if (code != 100000) {
    // //             initPro(code, depth);
    // //         }
    // //     }

    // //     function changeDepth(e) {
    // //         var dep = e.target.value;
    // //         initPro(adCode, dep);
    // //     }

    // //     initPro(adCode, depth);

    // //     // 构造下拉框
    // //     var optArr = temp.map(function (item) {
    // //         if (item.adcode == 100000) {
    // //             item.name = '选择省份';
    // //         }

    // //         return '<option ' + (item.adcode == adCode ? 'selected' : '') + ' value="' + item.adcode + '">' + item.中文名 + '</option>';
    // //     });

    // //     document.getElementById('adcode-list').innerHTML = optArr.join('');

    // //     document.getElementById('adcode-list').addEventListener("change", changeAdcode);
    // //     document.getElementById('depth-list').addEventListener("change", changeDepth);
    // //     document.getElementById('city-list').addEventListener("change", function (e) {
    // //         var cityCode = e.target.value;
    // //         if (cityCode != -1) {
    // //             // 根据所选市代码设置地图视野
    // //             var bounds = cityBounds[cityCode]; // 假设cityBounds是一个包含各市边界的对象
    // //             map.setBounds(bounds);
    // //         }
    // //     });

    // //     document.getElementById('district-list').addEventListener("change", function (e) {
    // //         var districtCode = e.target.value;
    // //         if (districtCode != -1) {
    // //             // 根据所选区县代码设置地图视野
    // //             var bounds = districtBounds[districtCode]; // 假设districtBounds是一个包含各区县边界的对象
    // //             map.setBounds(bounds);
    // //         }
    // //     });
        
        
        
    // //    // 注册地图点击事件
    // //     map.on('click', function (e) {
    // //         // 获取点击位置的经纬度坐标
    // //         var lnglat = e.lnglat;

    // //         // 创建逆地理编码对象
    // //         var geocoder = new AMap.Geocoder();

    // //         // 逆地理编码，获取行政区划信息
    // //         geocoder.getAddress(lnglat, function (status, result) {
    // //         try {
    // //             var addressComponent = result.regeocode.addressComponent;
    // //             var adcode = addressComponent.adcode;
    // //             var district = addressComponent.district;
    // //             console.log("所在区县的adcode:", adcode);
    // //             console.log("所在区县名称:", district);
    // //         } catch (error) {
    // //             // 发生错误时执行的代码
    // //             console.error('发生错误：', error);
    // //             // 进行错误分析
    // //             if (error instanceof ReferenceError) {
    // //                 console.error('可能是由于引用错误导致的异常，请检查变量名、函数名等是否正确。');
    // //             } else if (error instanceof TypeError) {
    // //                 console.error('可能是由于类型错误导致的异常，请检查变量的类型是否正确。');
    // //             } else if (error instanceof SyntaxError) {
    // //                 console.error('可能是由于语法错误导致的异常，请检查代码的语法是否正确。');
    // //             } else {
    // //                 console.error('发生未知错误，请检查代码并尝试修复。');
    // //             }
    // //         }}
    // //         // geocoder.getAddress(lnglat, function (status, result) {
    // //         //     if (status === 'complete' && result.regeocode) {
    // //         //         var addressComponent = result.regeocode.addressComponent;
    // //         //         var adcode = addressComponent.adcode;
    // //         //         var district = addressComponent.district;
    // //         //         console.log("所在区县的adcode:", adcode);
    // //         //         console.log("所在区县名称:", district);
    // //         //     } else {
    // //         //         console.log(status);
    // //         //         console.log(result.regeocode);
    // //         //         console.error("逆地理编码失败");
    // //         //     }
    // //         // }
    // //     );
    // //     });
    }





    //     var map, district, polygons = [], citycode;
    //     var citySelect = document.getElementById('city');
    //     var districtSelect = document.getElementById('district');
    //     var areaSelect = document.getElementById('street');
    //     function search(obj) {
    //         //清除地图上所有覆盖物
    //         for (var i = 0, l = polygons.length; i < l; i++) {
    //             polygons[i].setMap(null);
    //         }
    //         var option = obj[obj.options.selectedIndex];
    //         var keyword = option.text; //关键字
    //         var adcode = option.adcode;
    //         district.setLevel(option.value); //行政区级别
    //         district.setExtensions('all');
    //         //行政区查询
    //         //按照adcode进行查询可以保证数据返回的唯一性
    //         district.search(adcode, function (status, result) {
    //             if (status === 'complete') {
    //                 getData(result.districtList[0], obj.id);
    //             }
    //         });
    //     }
    //     function setCenter(obj) {
    //         map.setCenter(obj[obj.options.selectedIndex].center)
    //     }   
    //      function getData(data, level) {
    //         var bounds = data.boundaries;
    //         if (bounds) {
    //             for (var i = 0, l = bounds.length; i < l; i++) {
    //                 var polygon = new AMap.Polygon({
    //                     map: map,
    //                     strokeWeight: 1,
    //                     strokeColor: '#0091ea',
    //                     fillColor: '#80d8ff',
    //                     fillOpacity: 0.2,
    //                     path: bounds[i]
    //                 });
    //                 polygons.push(polygon);
    //             }
    //             map.setFitView();//地图自适应
    //         }

    //         //清空下一级别的下拉列表
    //         if (level === 'province') {
    //             citySelect.innerHTML = '';
    //             districtSelect.innerHTML = '';
    //             areaSelect.innerHTML = '';
    //         } else if (level === 'city') {
    //             districtSelect.innerHTML = '';
    //             areaSelect.innerHTML = '';
    //         } else if (level === 'district') {
    //             areaSelect.innerHTML = '';
    //         }

    //         var subList = data.districtList;
    //         if (subList) {
    //             var contentSub = new Option('--请选择--');
    //             var curlevel = subList[0].level;
    //             var curList = document.querySelector('#' + curlevel);
    //             curList.add(contentSub);
    //             for (var i = 0, l = subList.length; i < l; i++) {
    //                 var name = subList[i].name;
    //                 var levelSub = subList[i].level;
    //                 var cityCode = subList[i].citycode;
    //                 contentSub = new Option(name);
    //                 contentSub.setAttribute("value", levelSub);
    //                 contentSub.center = subList[i].center;
    //                 contentSub.adcode = subList[i].adcode;
    //                 curList.add(contentSub);
    //             }
    //         }

    //     }
        

    // //行政区划查询
    
        
    //    async function loadMapPlugin() {
    //         return new Promise((resolve, reject) => {
    //             var script = document.createElement('script');
    //             script.type = 'text/javascript';
    //             script.src = '//webapi.amap.com/maps?v=2.0&key=6c889de4ee1c73ea291466419487e294&plugin=AMap.DistrictSearch';
    //             script.onload = resolve;
    //             script.onerror = reject;
    //             document.head.appendChild(script);
    //         });
    //     }

    //     async function initMap() {
    //         try {
    //             await loadMapPlugin();
//                 var map = new AMap.Map('container', {
//                     zoom: 7,
//                     center: [113.378688, 22.973147]
//                 });

    //             citySelect.onchange = search;
    //             districtSelect.onchange = search;
    //             areaSelect.onchange = search;
    //             var opts = {
    //                 subdistrict: 1,
    //                 showbiz: false
    //             };
    //             district = new AMap.DistrictSearch(opts);
    //             district.search('中国', function (status, result) {
    //                 if (status == 'complete') {
    //                     getData(result.districtList[0]);
    //                 }
    //             });
    //         } catch (error) {
    //             console.error('初始化地图出错：', error);
    //         }
    //     }



        
    //     initMap();