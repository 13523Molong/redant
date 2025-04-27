<template>
<view class="flex-col page">
  <!-- 状态栏 -->
  <view class="status-bar">
    <text class="time">9:41</text>
    <view class="signal-group">
      <image class="signal-icon" src="/static/signal.png"/>
      <image class="wifi-icon ml-5" src="/static/wifi.png"/>
      <image class="battery-icon ml-5" src="/static/battery.png"/>
    </view>
  </view>

  <!-- 用户头像 -->
  <view class="avatar-container">
    <image class="avatar" src="/static/avatar.png"/>
    <text class="avatar-title">我的账号</text>
  </view>

  <!-- 登录表单 -->
  <view class="login-form">
    <view class="input-group">
      <input class="phone-input" placeholder="请输入手机号" />
      <view class="verification-group">
        <input class="code-input" placeholder="请输入验证码" />
        <text class="get-code">获取验证码</text>
      </view>
    </view>

    <text class="forgot-pwd">忘记密码？</text>
    
    <view class="register-tip">
      <text>没有账号，</text>
      <text class="register-link">去注册</text>
    </view>

    <button class="login-btn">登录</button>
  </view>

  <!-- 其他登录方式 -->
  <view class="other-login">
    <view class="divider-line">
      <view class="line"></view>
      <text class="divider-text">其他方式登录</text>
      <view class="line"></view>
    </view>
	
    <image class="password-login-icon" src="/static/wechat.png"/>
  </view>
</view>
</template>

<style scoped lang="scss">
.page {
  background: #f9f9f9;
  min-height: 100vh;
}

/* 状态栏 */
.status-bar {
  padding: 20rpx 32rpx;
  display: flex;
  justify-content: space-between;
  align-items: center;
  
  .time {
    font-size: 32rpx;
    font-weight: 700;
  }
  
  .signal-group {
    display: flex;
    align-items: center;
    
    image {
      width: 34rpx;
      height: 22rpx;
      &[class*="wifi"] { width: 30rpx; }
      &[class*="battery"] { width: 48rpx; }
    }
  }
}

/* 头像区域 */
.avatar-container {
  margin: 80rpx auto 0;
  text-align: center;
  
  .avatar {
    width: 100rpx;
    height: 100rpx;
    border-radius: 50%;
  }
  
  .avatar-title {
    margin-top: 28rpx;
    font-size: 44rpx;
    display: block;
  }
}

/* 登录表单 */
.login-form {
  margin: 80rpx 64rpx 0;
  
  .input-group {
    border-bottom: 1rpx solid #eee;
    padding-bottom: 40rpx;
    
    input {
      height: 100rpx;
      font-size: 32rpx;
      border-bottom: 1rpx solid #bdc4ce;
      padding: 20rpx 0;
      
      &:last-child {
        border: none;
      }
    }
    
    .verification-group {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .get-code {
        color: #2a82e4;
        font-size: 28rpx;
      }
    }
  }

  .forgot-pwd {
    color: #969696;
    font-size: 26rpx;
    text-align: right;
    margin-top: 30rpx;
    display: block;
  }

  .register-tip {
    text-align: center;
    margin-top: 40rpx;
    color: #969696;
    
    .register-link {
      color: #2a82e4;
    }
  }

  .login-btn {
    margin-top: 60rpx;
    background: #2a82e4;
    color: white;
    border-radius: 40rpx;
    height: 80rpx;
    line-height: 80rpx;
  }
}

/* 其他登录方式 */
.other-login {
  margin-top: 100rpx;
  
  .divider-line {
    display: flex;
    align-items: center;
    padding: 0 100rpx;
    
    .line {
      flex: 1;
      height: 1rpx;
      background: #ddd;
    }
    
    .divider-text {
      padding: 0 20rpx;
      color: #8c9198;
    }
  }

  .password-login-icon {
    width: 84rpx;
    height: 84rpx;
    display: block;
    margin: 40rpx auto 0;
  }
}
</style>