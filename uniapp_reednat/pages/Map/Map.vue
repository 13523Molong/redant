<template>
  <view class="flex-col page">
    <!-- 状态栏区域 -->
    <view class="status-bar">
      <text class="time">9:41</text>
      <view class="status-icons">
        <image class="icon" src="/static/signal.png" />
        <image class="icon wifi" src="/static/wifi.png" />
        <image class="icon battery" src="/static/battery.png" />
      </view>
    </view>

    <!-- 标题区域 -->
    <view class="title-section">
      <image class="decorative-icon" src="/static/left-icon.png" />
      <view class="title-container">
        <text class="main-title">农业智能助手</text>
        <image class="title-icon" src="/static/assistant-icon.png" />
      </view>
      <image class="decorative-icon" src="/static/right-icon.png" />
    </view>

    <!-- 主图区域 -->
    <view class="map-section">
      <map 
        id="mainMap"
	    @click="handleMapClick"
        :longitude="mapData.longitude"
        :latitude="mapData.latitude"
        :markers="markers"
        :show-location="true"
        style="width: 100%; height: 750rpx;"
        @regionchange="handleMapDrag"
        :enable-satellite="enableSatellite">
        
      </map>
    </view>

    <!-- 机器人选择 -->
    <view class="robot-selection">
      <view v-for="(robot, index) in robots" :key="index" class="robot-card" @click="selectRobot(index)">
        <text class="robot-label">机器人{{ index + 1 }}号</text>
      </view>
    </view>

    <!-- 坐标显示 -->
   <!-- <view class="coordinates-section">
      <text class="coordinates-text">
        {{ coordinateSource === 'click' ? '点击坐标' : '当前坐标' }}\n
        经度：{{ displayCoordinates.longitude.toFixed(6) }}\n
        纬度：{{ displayCoordinates.latitude.toFixed(6) }}
      </text>
    </view> -->
	<view class="coordinates-section">
	  <text class="coordinates-text">
	    {{ coordinateSource === 'click' ? '点击坐标' : '当前坐标' }}
	    经度：{{ displayCoordinates.longitude.toFixed(6) }}
	    纬度：{{ displayCoordinates.latitude.toFixed(6) }}
	  </text>
	</view>

    <!-- 操作按钮 -->
    <view class="action-button" @click="sendCoordinates">
      <text>前往指定坐标</text>
    </view>

    <!-- 功能导航 -->
    <view class="navigation-bar">
      <view class="nav-item">
        <image class="nav-icon" src="/static/frontier-icon.png" />
        <text>前沿</text>
      </view>
      <view class="nav-item">
        <image class="nav-icon" src="/static/operation-icon.png" />
        <text>操作</text>
      </view>
      <view class="nav-item">
        <image class="nav-icon" src="/static/management-icon.png" />
        <text>管理</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { reactive, ref, onMounted, watchEffect } from 'vue';

import config from '../../config';

// 地图基础数据
const mapData = reactive({
  longitude: 116.397428,
  latitude: 39.90923
});

//地图响应式坐标储存
const mapClickCoords = reactive({
  longitude: null,
  latitude: null
});



// 生成随机坐标函数
const generateRandomCoordinates = (baseLat, baseLng) => {
  const randomRobots = [];
  for (let i = 0; i < 3; i++) {
    randomRobots.push({
      id: i + 2,
      latitude: baseLat + (Math.random() - 0.5) * 0.01,
      longitude: baseLng + (Math.random() - 0.5) * 0.01,
      title: `机器人${i + 1}号`,
      iconPath: '/static/marker.png',
      width: 35,
      height: 35
    });
  }
  return randomRobots;
};

// 初始化标记
const markers = reactive([
  {
    id: 1,
    latitude: mapData.latitude,
    longitude: mapData.longitude,
    title: "当前位置",
    iconPath: '/static/marker.png',
    width: 35,
    height: 35
  },
  ...generateRandomCoordinates(mapData.latitude, mapData.longitude)
]);

// 机器人列表
const robots = reactive([...markers.slice(1)]);

// 坐标显示相关
const coordinateSource = ref('default');
const displayCoordinates = reactive({ ...mapData });

// 监听地图中心变化
watchEffect(() => {
  if (coordinateSource.value === 'default') {
    displayCoordinates.longitude = mapData.longitude;
    displayCoordinates.latitude = mapData.latitude;
  }
});

// 地图点击处理
// 修改后的点击处理函数
const handleMapClick = (e) => {
  try {
    // 参数安全校验
    if (!e.detail || typeof e.detail.latitude === 'undefined') {
      console.error('无效的点击参数结构', e);
      uni.showToast({ title: '获取坐标失败', icon: 'none' });
      return;
    }

    const { latitude: lat, longitude: lng } = e.detail;
    console.log('有效点击坐标：', lat, lng);

    // 清除旧标记
    const clickIndex = markers.findIndex(m => m.id === 999);
    if (clickIndex > -1) markers.splice(clickIndex, 1);

    // 添加新标记（确保响应式）
    const newMarker = {
      id: 999,
      latitude: lat,
      longitude: lng,
      iconPath: '/static/position.png',
      width: 40,
      height: 40
    };
    markers.push(newMarker);

    // 更新显示坐标
    coordinateSource.value = 'click';
    displayCoordinates.longitude = lng;
    displayCoordinates.latitude = lat;

  } catch (error) {
    console.error('坐标处理异常:', error);
    uni.showToast({ title: '坐标处理出错', icon: 'none' });
  }
   // 存储地图点击坐标
    mapClickCoords.longitude = lng;
    mapClickCoords.latitude = lat;
};



// 新增响应式对象存储坐标
const selectedRobotCoords = reactive({
  longitude: null,
  latitude: null
});


// 选择机器人
const selectRobot = (index) => {
  robots.forEach(robot => {
    robot.iconPath = '/static/marker.png';
    robot.width = 35;
    robot.height = 35;
  });

  const selected = robots[index];
  selected.iconPath = '/static/position.png';
  selected.width = 40;
  selected.height = 40;

  // 更新坐标显示
  coordinateSource.value = 'robot';
  Object.assign(displayCoordinates, {
    longitude: selected.longitude,
    latitude: selected.latitude
  });

  // 移动地图中心
  Object.assign(mapData, {
    longitude: selected.longitude,
    latitude: selected.latitude
  });
  
  uni.createMapContext('mainMap').moveToLocation({
    longitude: selected.longitude,
    latitude: selected.latitude
  });
  
  selectedRobotCoords.longitude = selected.longitude,
  selectedRobotCoords.latitude = selected.latitude
};

// 发送坐标
const sendCoordinates = async () => {
  try {
    if (!selectedRobotCoords.longitude || !mapClickCoords.longitude) {
		uni.showToast({ title: '请先选择机器人并点击地图位置', icon: 'none' });
		return;
	  }
    const { data: res } = await uni.request({
      url: `${config.apiBaseUrl}/navigation/`,
      method: 'POST',
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
    
    uni.showToast({
      title: res.code === 200 ? '发送成功' : '发送失败',
      icon: 'none'
    });
  } catch (err) {
    uni.showToast({ title: '网络异常', icon: 'none' });
  }
};

// 初始化定位
// 修改onMounted中的定位初始化逻辑
onMounted(() => {
  // 环境判断（H5等平台不支持）
  if (!uni.getLocation) {
    console.log('当前环境不支持定位功能');
    return;
  }

  // 获取定位权限的正确方式
  uni.getSetting({
    success(res) {
      if (!res.authSetting['scope.userLocation']) {
        uni.request({
          url: '',
          method: 'POST',
          data: {
            longitude: displayCoordinates.longitude,
            latitude: displayCoordinates.latitude
          }
        });
      }
      uni.getLocation({
        type: 'gcj02',
        success: (res) => {
          Object.assign(mapData, {
            longitude: res.longitude,
            latitude: res.latitude
          });
          markers[0].latitude = res.latitude;
          markers[0].longitude = res.longitude;
        },
        fail: (err) => {
          console.error('获取定位失败', err);
          uni.showToast({
            title: '需要位置权限才能使用地图功能',
            icon: 'none'
          });
        }
      });
    },
    fail: (err) => {
      console.error('获取设置失败', err);
    }
  });
});
</script>

<style scoped lang="scss">
.page {
  background: #f5f5f5;
  min-height: 100vh;
  padding: 36rpx 0;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 30rpx;

.time {
    font-size: 32rpx;
    font-weight: 700;
    color: #333;
  }

.status-icons {
    display: flex;
    gap: 20rpx;

  .icon {
      width: 40rpx;
      height: 26rpx;

      &.wifi { width: 36rpx }
      &.battery { width: 56rpx }
    }
  }
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 24rpx 42rpx 0 34rpx;

.decorative-icon {
    width: 70rpx;
    height: 70rpx;
  }

.title-container {
    background: #e5f5c9;
    border: 3rpx solid #89b32d;
    border-radius: 10rpx;
    padding: 8rpx 12rpx;
    display: flex;
    align-items: center;

  .main-title {
      color: #2a8952;
      font-size: 36rpx;
      margin: 0 50rpx;
    }

  .title-icon {
      width: 56rpx;
      height: 56rpx;
    }
  }
}

.map-section {
  margin: 40rpx 0;
  border-radius: 16rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 12rpx rgba(0,0,0,0.1);
  height: 750rpx; /* 确保有明确的高度 */
}

.robot-selection {
  display: flex;
  gap: 20rpx;
  padding: 0 28rpx;
  margin-top: 16rpx;

.robot-card {
    flex: 1;
    background: white;
    border: 3rpx solid #b3b3b3;
    border-radius: 20rpx;
    padding: 16rpx 0;

  .robot-label {
      font-size: 44rpx;
      color: #000;
    }
  }
}


.action-button {
  background: #8cb9ed;
  border-radius: 30rpx;
  width: 408rpx;
  margin: 94rpx auto 0;
  padding: 24rpx;
  text-align: center;
}

.navigation-bar {
  background: white;
  border-top: 2rpx solid #999;
  margin-top: 18rpx;
  padding: 24rpx;
  display: flex;
  justify-content: space-around;

.nav-item {
    display: flex;
    flex-direction: column;
    align-items: center;

  .nav-icon {
      width: 90rpx;
      height: 90rpx;
      margin-bottom: 10rpx;
    }
  }
}



.coord-tip {
  position: absolute;
  bottom: 20rpx;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.7);
  color: white;
  padding: 10rpx 20rpx;
  border-radius: 8rpx;
  font-size: 28rpx;
}

// 删除重复的.coordinates-section定义
.coordinates-section {
  background: #fff;
  padding: 20rpx;
  margin: 20rpx;
  border-radius: 12rpx;
  box-shadow: 0 2rpx 6rpx rgba(0,0,0,0.1);
  
  .coordinates-text {
    font-size: 32rpx;
    color: #333;
    line-height: 1.6;
    white-space: pre-line;
    display: block;
  }
}
</style>