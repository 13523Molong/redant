"use strict";
const common_vendor = require("../../common/vendor.js");
const common_assets = require("../../common/assets.js");
const config = require("../../config.js");
const _sfc_main = {
  __name: "index",
  setup(__props) {
    const data = common_vendor.reactive({
      login_name: "",
      login_pwd: ""
    });
    const currentTime = common_vendor.ref(getCurrentTime());
    const showPassword = common_vendor.ref(false);
    function getCurrentTime() {
      const date = /* @__PURE__ */ new Date();
      return `${date.getHours()}:${date.getMinutes().toString().padStart(2, "0")}`;
    }
    function togglePasswordVisibility() {
      showPassword.value = !showPassword.value;
    }
    function login() {
      if (!data.login_name || !data.login_pwd) {
        common_vendor.index.showToast({ title: "请输入完整信息", icon: "none" });
        return;
      }
      common_vendor.index.showLoading({ title: "登录中..." });
      common_vendor.index.request({
        url: `${config.config.apiBaseUrl}/index/`,
        header: { "Content-Type": "application/json" },
        method: "POST",
        data: {
          login_name: data.login_name,
          login_pwd: data.login_pwd
        },
        // 登录方法修正部分
        success: (res) => {
          var _a;
          common_vendor.index.__f__("log", "at pages/index/index.vue:118", "登录响应数据:", res.data);
          common_vendor.index.hideLoading();
          if (res.statusCode === 200) {
            if ((_a = res.data) == null ? void 0 : _a.token) {
              const cookies = res.data.token || res.data["token"];
              common_vendor.index.setStorageSync("session_cookies", cookies);
              common_vendor.index.showToast({ title: "登录成功", icon: "success" });
              setTimeout(() => {
                common_vendor.index.navigateTo({
                  url: "/pages/Map/Map"
                });
              });
            } else {
              common_vendor.index.__f__("error", "at pages/index/index.vue:133", "接口返回缺少必要字段:", res.data);
              common_vendor.index.showToast({ title: "登录异常，请重试", icon: "none" });
            }
          } else if (res.statusCode === 400) {
            common_vendor.index.showToast({ title: "用户名或密码错误", icon: "none" });
          }
        },
        fail: (err) => {
          common_vendor.index.__f__("error", "at pages/index/index.vue:141", "登录请求失败:", err);
          common_vendor.index.hideLoading();
          common_vendor.index.showToast({ title: "网络异常，请检查连接", icon: "none" });
        }
      });
    }
    function navigateToRegister() {
      common_vendor.index.navigateTo({ url: "/pages/register/register" });
    }
    function navigateToForgotPwd() {
      common_vendor.index.navigateTo({ url: "/pages/forgot-pwd/forgot-pwd" });
    }
    common_vendor.onMounted(() => {
      setInterval(() => {
        currentTime.value = getCurrentTime();
      }, 1e3);
    });
    return (_ctx, _cache) => {
      return {
        a: common_vendor.t(currentTime.value),
        b: common_assets._imports_0,
        c: common_assets._imports_1,
        d: common_assets._imports_2,
        e: common_assets._imports_3,
        f: common_assets._imports_3$1,
        g: data.login_name,
        h: common_vendor.o(($event) => data.login_name = $event.detail.value),
        i: common_assets._imports_4,
        j: showPassword.value ? "text" : "password",
        k: data.login_pwd,
        l: common_vendor.o(($event) => data.login_pwd = $event.detail.value),
        m: showPassword.value ? "/static/eye-open.png" : "/static/eye-close.png",
        n: common_vendor.o(togglePasswordVisibility),
        o: common_vendor.o(navigateToForgotPwd),
        p: common_vendor.o(login),
        q: common_vendor.o(navigateToRegister),
        r: common_assets._imports_4$1,
        s: common_assets._imports_7
      };
    };
  }
};
wx.createPage(_sfc_main);
//# sourceMappingURL=../../../.sourcemap/mp-weixin/pages/index/index.js.map
