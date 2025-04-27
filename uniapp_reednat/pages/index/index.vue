<template>
  <view class="container">
    <!-- 顶部状态栏 -->
    <view class="status-bar">
      <text class="time">{{ currentTime }}</text>
      <view class="status-icons">
        <image class="icon" src="/static/signal.png" />
        <image class="icon" src="/static/wifi.png" />
        <image class="icon battery" src="/static/battery.png" />
      </view>
    </view>

    <!-- 用户头像区域 -->
    <view class="avatar-section">
      <image class="avatar" src="/static/avatar.png" />
      <text class="username">我的账号</text>
    </view>

    <!-- 登录表单 -->
    <view class="login-form">
      <view class="form-item">
        <image class="icon" src="/static/user-icon.png" />
        <input 
          v-model="data.login_name"
          placeholder="请输入用户名"
          placeholder-class="placeholder"
          class="input"
        />
      </view>
      
      <view class="form-item">
        <image class="icon" src="/static/pwd-icon.png" />
        <input 
          v-model="data.login_pwd"
          :type="showPassword ? 'text' : 'password'"
          placeholder="请输入密码"
          placeholder-class="placeholder"
          class="input"
        />
        <image 
          class="eye-icon" 
          :src="showPassword ? '/static/eye-open.png' : '/static/eye-close.png'" 
          @click="togglePasswordVisibility"
        />
      </view>

      <text class="forgot-pwd" @click="navigateToForgotPwd">忘记密码?</text>

      <view class="login-btn" @click="login">
        <text class="btn-text">登录</text>
      </view>

      <view class="register-section">
        <text>没有账号？</text>
        <text class="register-text" @click="navigateToRegister">立即注册</text>
      </view>
    </view>

    <!-- 其他登录方式 -->
    <view class="other-login">
      <view class="divider">
        <view class="line"></view>
        <text class="divider-text">其他方式登录</text>
        <view class="line"></view>
      </view>
      <view class="login-methods">
        <image class="method-icon" src="/static/wechat.png" />
        <image class="method-icon" src="/static/qq.png" />
      </view>
    </view>
  </view>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';
import config from '../../config.js';

// 响应式数据
const data = reactive({
  login_name: '',
  login_pwd: ''
});

const currentTime = ref(getCurrentTime());
const showPassword = ref(false);

// 获取当前时间
function getCurrentTime() {
  const date = new Date();
  return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
}

// 切换密码可见性
function togglePasswordVisibility() {
  showPassword.value = !showPassword.value;
}

// 登录方法
function login() {
  if (!data.login_name || !data.login_pwd) {
    uni.showToast({ title: '请输入完整信息', icon: 'none' });
    return;
  }

  uni.showLoading({ title: '登录中...' });

  // 发起登录请求
  uni.request({
    url: `${config.apiBaseUrl}/index/`,
	header: { 'Content-Type': 'application/json' },
    method: 'POST',
    data: {
      login_name: data.login_name,
      login_pwd: data.login_pwd
    },
  // 登录方法修正部分
  success: (res) => {
    console.log('登录响应数据:', res.data); // 调试日志
    uni.hideLoading();
    
    if (res.statusCode === 200) {
      // 检查必要字段是否存在
      if (res.data?.token) {
		const cookies = res.data.token || res.data['token']
        uni.setStorageSync('session_cookies',cookies);
        uni.showToast({ title: '登录成功', icon: 'success' });
        setTimeout(()=>{
			uni.navigateTo({
				url:'/pages/Map/Map'
			});
		1000})
      } else {
        console.error('接口返回缺少必要字段:', res.data);
        uni.showToast({ title: '登录异常，请重试', icon: 'none' });
      }
    } else if (res.statusCode === 400) {
      uni.showToast({ title: '用户名或密码错误', icon: 'none' });
    }
  },
  fail: (err) => {
    console.error('登录请求失败:', err);
    uni.hideLoading();
    uni.showToast({ title: '网络异常，请检查连接', icon: 'none' });
  }
  });
}

// 跳转到注册页面
function navigateToRegister() {
  uni.navigateTo({ url: '/pages/register/register' });
}

// 跳转到忘记密码页面
function navigateToForgotPwd() {
  uni.navigateTo({ url: '/pages/forgot-pwd/forgot-pwd' });
}

// 每秒更新时间
onMounted(() => {
  setInterval(() => {
    currentTime.value = getCurrentTime();
  }, 1000);
});
</script>

<style>
/* 通用样式 */
.container {
  padding: 40rpx;
  background-color: #f9f9f9;
  height: 100vh;
}

/* 状态栏样式 */
.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30rpx;
  margin-bottom: 80rpx;
}
.time {
  font-size: 32rpx;
  font-family: HarmonyOSSansSC;
  color: #000;
}
.status-icons {
  display: flex;
  align-items: center;
  gap: 20rpx;
}
.icon {
  width: 40rpx;
  height: 40rpx;
}
.battery {
  width: 50rpx;
}

/* 用户头像区域 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 80rpx;
}
.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 50%;
}
.username {
  font-size: 40rpx;
  margin-top: 20rpx;
  color: #383838;
}

/* 登录表单 */
.login-form {
  background: #fff;
  border-radius: 24rpx;
  padding: 60rpx 40rpx;
}
.form-item {
  display: flex;
  align-items: center;
  padding: 30rpx 0;
  border-bottom: 1rpx solid #eee;
}
.input {
  flex: 1;
  font-size: 32rpx;
  margin-left: 30rpx;
}
.placeholder {
  color: #c2c2c2;
}
.eye-icon {
  width: 40rpx;
  height: 40rpx;
  margin-left: 20rpx;
}

/* 登录按钮 */
.login-btn {
  background: linear-gradient(90deg, #2a82e4, #67b7f6);
  height: 100rpx;
  border-radius: 50rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 60rpx 0 40rpx;
}
.btn-text {
  color: #fff;
  font-size: 36rpx;
  font-weight: 500;
}

/* 其他样式 */
.forgot-pwd {
  color: #969696;
  font-size: 28rpx;
  text-align: right;
  margin-top: 30rpx;
}
.register-section {
  display: flex;
  justify-content: center;
  gap: 20rpx;
  color: #969696;
}
.register-text {
  color: #2a82e4;
}

/* 其他登录方式 */
.other-login {
  margin-top: 100rpx;
}
.divider {
  display: flex;
  align-items: center;
  gap: 30rpx;
  margin-bottom: 50rpx;
}
.line {
  flex: 1;
  height: 2rpx;
  background: #ddd;
}
.divider-text {
  color: #8c9198;
}
.login-methods {
  display: flex;
  justify-content: center;
  gap: 80rpx;
}
.method-icon {
  width: 80rpx;
  height: 80rpx;
}
</style>