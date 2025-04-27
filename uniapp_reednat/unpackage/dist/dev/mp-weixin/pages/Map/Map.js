"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const config = require("../../config.js");
const _sfc_main = {
  __name: "Map",
  setup(__props) {
    const mapData = common_vendor.reactive({
      longitude: 116.397428,
      latitude: 39.90923
    });
    const mapClickCoords = common_vendor.reactive({
      longitude: null,
      latitude: null
    });
    const generateRandomCoordinates = (baseLat, baseLng) => {
      const randomRobots = [];
      for (let i = 0; i < 3; i++) {
        randomRobots.push({
          id: i + 2,
          latitude: baseLat + (Math.random() - 0.5) * 0.01,
          longitude: baseLng + (Math.random() - 0.5) * 0.01,
          title: `机器人${i + 1}号`,
          iconPath: "/static/marker.png",
          width: 35,
          height: 35
        });
      }
      return randomRobots;
    };
    const markers = common_vendor.reactive([
      {
        id: 1,
        latitude: mapData.latitude,
        longitude: mapData.longitude,
        title: "当前位置",
        iconPath: "/static/marker.png",
        width: 35,
        height: 35
      },
      ...generateRandomCoordinates(mapData.latitude, mapData.longitude)
    ]);
    const robots = common_vendor.reactive([...markers.slice(1)]);
    const coordinateSource = common_vendor.ref("default");
    const displayCoordinates = common_vendor.reactive({ ...mapData });
    common_vendor.watchEffect(() => {
      if (coordinateSource.value === "default") {
        displayCoordinates.longitude = mapData.longitude;
        displayCoordinates.latitude = mapData.latitude;
      }
    });
    const handleMapClick = (e) => {
      try {
        if (!e.detail || typeof e.detail.latitude === "undefined") {
          common_vendor.index.__f__("error", "at pages/Map/Map.vue:156", "无效的点击参数结构", e);
          common_vendor.index.showToast({ title: "获取坐标失败", icon: "none" });
          return;
        }
        const { latitude: lat2, longitude: lng2 } = e.detail;
        common_vendor.index.__f__("log", "at pages/Map/Map.vue:162", "有效点击坐标：", lat2, lng2);
        const clickIndex = markers.findIndex((m) => m.id === 999);
        if (clickIndex > -1)
          markers.splice(clickIndex, 1);
        const newMarker = {
          id: 999,
          latitude: lat2,
          longitude: lng2,
          iconPath: "/static/position.png",
          width: 40,
          height: 40
        };
        markers.push(newMarker);
        coordinateSource.value = "click";
        displayCoordinates.longitude = lng2;
        displayCoordinates.latitude = lat2;
      } catch (error) {
        common_vendor.index.__f__("error", "at pages/Map/Map.vue:185", "坐标处理异常:", error);
        common_vendor.index.showToast({ title: "坐标处理出错", icon: "none" });
      }
      mapClickCoords.longitude = lng;
      mapClickCoords.latitude = lat;
    };
    const selectedRobotCoords = common_vendor.reactive({
      longitude: null,
      latitude: null
    });
    const selectRobot = (index) => {
      robots.forEach((robot) => {
        robot.iconPath = "/static/marker.png";
        robot.width = 35;
        robot.height = 35;
      });
      const selected = robots[index];
      selected.iconPath = "/static/position.png";
      selected.width = 40;
      selected.height = 40;
      coordinateSource.value = "robot";
      Object.assign(displayCoordinates, {
        longitude: selected.longitude,
        latitude: selected.latitude
      });
      Object.assign(mapData, {
        longitude: selected.longitude,
        latitude: selected.latitude
      });
      common_vendor.index.createMapContext("mainMap").moveToLocation({
        longitude: selected.longitude,
        latitude: selected.latitude
      });
      selectedRobotCoords.longitude = selected.longitude, selectedRobotCoords.latitude = selected.latitude;
    };
    const sendCoordinates = async () => {
      try {
        if (!selectedRobotCoords.longitude || !mapClickCoords.longitude) {
          common_vendor.index.showToast({ title: "请先选择机器人并点击地图位置", icon: "none" });
          return;
        }
        const { data: res } = await common_vendor.index.request({
          url: `${config.config.apiBaseUrl}/navigation/`,
          method: "POST",
          data: {
            robot_position: {
              longitude: selectedRobotCoords.longitude,
              latitude: selectedRobotCoords.latitude
            },
            ttarget_position: {
              longitude: mapClickCoords.longitude,
              latitude: mapClickCoords.latitude
            }
          }
        });
        common_vendor.index.showToast({
          title: res.code === 200 ? "发送成功" : "发送失败",
          icon: "none"
        });
      } catch (err) {
        common_vendor.index.showToast({ title: "网络异常", icon: "none" });
      }
    };
    common_vendor.onMounted(() => {
      if (!common_vendor.index.getLocation) {
        common_vendor.index.__f__("log", "at pages/Map/Map.vue:273", "当前环境不支持定位功能");
        return;
      }
      common_vendor.index.getSetting({
        success(res) {
          if (!res.authSetting["scope.userLocation"]) {
            common_vendor.index.request({
              url: "",
              method: "POST",
              data: {
                longitude: displayCoordinates.longitude,
                latitude: displayCoordinates.latitude
              }
            });
          }
          common_vendor.index.getLocation({
            type: "gcj02",
            success: (res2) => {
              Object.assign(mapData, {
                longitude: res2.longitude,
                latitude: res2.latitude
              });
              markers[0].latitude = res2.latitude;
              markers[0].longitude = res2.longitude;
            },
            fail: (err) => {
              common_vendor.index.__f__("error", "at pages/Map/Map.vue:301", "获取定位失败", err);
              common_vendor.index.showToast({
                title: "需要位置权限才能使用地图功能",
                icon: "none"
              });
            }
          });
        },
        fail: (err) => {
          common_vendor.index.__f__("error", "at pages/Map/Map.vue:310", "获取设置失败", err);
        }
      });
    });
    return (_ctx, _cache) => {
      return {
        a: common_assets._imports_0,
        b: common_assets._imports_1,
        c: common_assets._imports_2,
        d: common_assets._imports_3$2,
        e: common_assets._imports_4$2,
        f: common_assets._imports_5$1,
        g: common_vendor.o(handleMapClick),
        h: mapData.longitude,
        i: mapData.latitude,
        j: markers,
        k: common_vendor.o((...args) => _ctx.handleMapDrag && _ctx.handleMapDrag(...args)),
        l: _ctx.enableSatellite,
        m: common_vendor.f(robots, (robot, index, i0) => {
          return {
            a: common_vendor.t(index + 1),
            b: index,
            c: common_vendor.o(($event) => selectRobot(index), index)
          };
        }),
        n: common_vendor.t(coordinateSource.value === "click" ? "点击坐标" : "当前坐标"),
        o: common_vendor.t(displayCoordinates.longitude.toFixed(6)),
        p: common_vendor.t(displayCoordinates.latitude.toFixed(6)),
        q: common_vendor.o(sendCoordinates),
        r: common_assets._imports_6,
        s: common_assets._imports_7$1,
        t: common_assets._imports_8
      };
    };
  }
};
const MiniProgramPage = /* @__PURE__ */ common_vendor._export_sfc(_sfc_main, [["__scopeId", "data-v-3e2e0653"]]);
wx.createPage(MiniProgramPage);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/Map/Map.js.map
