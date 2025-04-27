<template>
  <view class="container">
    <!-- 状态栏 -->
    <view class="status-bar">
      <text class="time">9:41</text>
      <view class="icons">
        <image class="icon" src="/static/signal.png" />
        <image class="icon" src="/static/wifi.png" />
        <image class="icon" src="/static/battery.png" />
      </view>
    </view>

    <!-- 标题 -->
    <view class="header">
      <text class="title">注册账号</text>
    </view>

    <!-- 表单 -->
    <view class="form">
      <!-- 用户名 -->
      <view class="input-group">
        <image class="icon" src="/static/user-icon.png" />
        <input class="input" placeholder="用户名" placeholder-class="placeholder" />
      </view>

      <!-- 密码 -->
      <view class="input-group">
        <image class="icon" src="/static/pwd-icon.png" />
        <input class="input" password placeholder="密码" placeholder-class="placeholder" />
        <image class="icon-eye" src="/static/eye-close.png" />
      </view>

      <!-- 手机号 -->
      <view class="input-group">
        <input class="input" type="number" placeholder="请输入手机号" placeholder-class="placeholder" />
      </view>

      <!-- 验证码 -->
      <view class="input-group code-group">
        <input class="input" type="number" placeholder="请输入验证码" placeholder-class="placeholder" />
        <text class="code-text">获取验证码</text>
      </view>

      <!-- 协议 -->
      <view class="agreement">
        <view class="checkbox"></view>
        <text class="agreement-text">我已同意用户隐私协议</text>
      </view>

      <!-- 注册按钮 -->
      <button class="register-btn">注册</button>

      <!-- 第三方登录 -->
      <view class="social-login">
        <text class="social-text">其他登录方式</text>
        <view class="social-icons">
          <image class="social-icon" src="/static/wechat.png" />
          <image class="social-icon" src="/static/qq.png" />
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {};
  },
};
</script>

<style lang="scss" scoped>
.container {
  background-color: #f9f9f9;
  min-height: 100vh;
  padding: 30rpx;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30rpx;

  .time {
    font-size: 32rpx;
    font-weight: bold;
  }

  .icons {
    display: flex;
    align-items: center;
    gap: 20rpx;

    .icon {
      width: 40rpx;
      height: 40rpx;
    }
  }
}

.header {
  text-align: center;
  margin-top: 80rpx;

  .logo {
    width: 100rpx;
    height: 100rpx;
    margin-bottom: 20rpx;
  }

  .title {
    font-size: 48rpx;
    color: #383838;
  }
}

.form {
  background-color: #ffffff;
  border-radius: 16rpx;
  padding: 60rpx 40rpx;
  margin-top: 80rpx;

  .input-group {
    display: flex;
    align-items: center;
    border-bottom: 1rpx solid #eee;
    padding: 40rpx 0;

    .icon {
      width: 40rpx;
      height: 40rpx;
      margin-right: 20rpx;
    }

    .input {
      flex: 1;
      font-size: 32rpx;
    }

    .icon-eye {
      width: 40rpx;
      height: 40rpx;
    }

    &.code-group {
      justify-content: space-between;

      .code-text {
        color: #06121e;
        font-size: 28rpx;
      }
    }
  }

  .agreement {
    display: flex;
    align-items: center;
    margin: 60rpx 0;

    .checkbox {
      width: 40rpx;
      height: 40rpx;
      border: 2rpx solid #ccc;
      border-radius: 50%;
      margin-right: 20rpx;
    }

    .agreement-text {
      font-size: 28rpx;
      color: #333;
    }
  }

  .register-btn {
    background-color: #a2c8f2;
    color: #000;
    border-radius: 40rpx;
    font-size: 36rpx;
    height: 80rpx;
    line-height: 80rpx;
  }

  .social-login {
    text-align: center;
    margin-top: 40rpx;

    .social-text {
      font-size: 28rpx;
      color: #666;
    }

    .social-icons {
      display: flex;
      justify-content: center;
      gap: 40rpx;
      margin-top: 20rpx;

      .social-icon {
        width: 60rpx;
        height: 60rpx;
      }
    }
  }
}

.placeholder {
  color: #bdc4ce;
}
</style>