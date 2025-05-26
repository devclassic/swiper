<template>
  <div v-show="state.showLeft" class="left">
    <div class="item" @click="fullscreen">切换全屏</div>
    <div class="item" @click="showSettings">轮播设置</div>
  </div>

  <el-dialog
    v-model="state.showSettings"
    title="轮播设置"
    width="500"
    :close-on-click-modal="false">
    <el-form label-width="auto">
      <el-form-item label="间隔时间" class="form-item">
        <el-input-number v-model="state.data.delay" placeholder="请输入间隔时间" />
      </el-form-item>
    </el-form>
    <div class="list-btns">
      <el-button type="primary" @click="listItemAdd">添加图片</el-button>
      <el-button type="primary" @click="listItemSort">更新排序</el-button>
    </div>
    <el-table :data="state.data.images" border style="width: 100%">
      <el-table-column label="图片" width="125">
        <template #default="scope">
          <img :src="scope.row.url" class="list-img" />
        </template>
      </el-table-column>
      <el-table-column label="排序" width="175">
        <template #default="scope">
          <el-input-number v-model="scope.row.order" />
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="scope">
          <el-button type="danger" @click="listItemRemove(scope.$index)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <template #footer>
      <el-button @click="state.showSettings = false">取消</el-button>
      <el-button type="primary" @click="ok">确定</el-button>
    </template>
  </el-dialog>

  <Swiper
    :autoplay="{ delay: state.data.delay * 1000, pauseOnMouseEnter: false }"
    :loop="true"
    :modules="[Autoplay]">
    <SwiperSlide v-for="item of state.data.images">
      <img :src="item.url" class="img" />
    </SwiperSlide>
  </Swiper>
</template>

<script setup>
  import { reactive } from 'vue'
  import { useEventListener } from '@vueuse/core'
  import { ElMessage } from 'element-plus'
  import { Swiper, SwiperSlide } from 'swiper/vue'
  import { Autoplay } from 'swiper/modules'
  import 'swiper/css'

  const state = reactive({
    showLeft: false,
    showSettings: false,
    data: {
      delay: 1,
      // [{ url: './images/1.jpg', order: 1 }]
      images: [],
    },
  })

  const init = async () => {
    const data = await pywebview.api.getconfig()
    state.data = JSON.parse(data)
  }

  useEventListener('pywebviewready', function () {
    init()
  })

  useEventListener('mousemove', event => {
    if (event.clientX < 200) {
      state.showLeft = true
    } else {
      state.showLeft = false
    }
  })

  const fullscreen = async () => {
    await pywebview.api.fullscreen()
    location.reload()
  }

  const showSettings = () => {
    state.showSettings = true
  }

  const listItemRemove = async index => {
    const filename = state.data.images[index].url.split('/').pop()
    await pywebview.api.removefile(filename)
    state.data.images.splice(index, 1)
  }

  const listItemAdd = async () => {
    const images = await pywebview.api.openfile()
    for (const image of images) {
      state.data.images.push({ url: `./images/${image}`, order: state.data.images.length + 1 })
    }
  }

  const listItemSort = () => {
    state.data.images.sort((a, b) => a.order - b.order)
    state.data.images.forEach((item, index) => {
      item.order = index + 1
    })
    ElMessage.success('排序完成')
  }

  const ok = async () => {
    await pywebview.api.saveconfig(JSON.stringify(state.data))
    ElMessage.success('保存成功')
    state.showSettings = false
    setTimeout(() => {
      location.reload()
    }, 500)
  }
</script>

<style>
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }

  .left {
    width: 200px;
    height: 100vh;
    background-color: #666;
    position: fixed;
    left: 0;
    top: 0;
    z-index: 1000;
    padding: 0 10px;
  }

  .left .item {
    padding: 10px 0;
    font-size: 12px;
    color: #fff;
    cursor: pointer;
    background-color: #444;
    margin-top: 10px;
    text-align: center;
  }

  .left .item:hover {
    background-color: #333;
  }

  .img {
    width: 100%;
    height: 100vh;
    display: block;
  }

  .form-item:last-child {
    margin-bottom: 10px;
  }

  .list-btns {
    margin-bottom: 10px;
  }

  .list-img {
    width: 100px;
    height: 60px;
    object-fit: cover;
    display: block;
  }
</style>
