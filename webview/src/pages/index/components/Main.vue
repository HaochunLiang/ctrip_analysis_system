<template>
  <div class="home-des">
    <div class="logo">
      <svg class="svg" width="72px" height="72px" viewBox="0 0 64 64" version="1.1">
        <title>Icon</title>
        <defs>
          <linearGradient x1="50%" y1="0%" x2="50%" y2="100%" id="linearGradient-1">
            <stop stop-color="#FFFFFF" offset="0%"></stop>
            <stop stop-color="#F2F2F2" offset="100%"></stop>
          </linearGradient>
          <circle id="path-2" cx="31.9988602" cy="31.9988602" r="2.92886048"></circle>
          <filter x="-85.4%" y="-68.3%" width="270.7%" height="270.7%" filterUnits="objectBoundingBox" id="filter-3">
            <feOffset dx="0" dy="1" in="SourceAlpha" result="shadowOffsetOuter1"></feOffset>
            <feGaussianBlur stdDeviation="1.5" in="shadowOffsetOuter1" result="shadowBlurOuter1"></feGaussianBlur>
            <feColorMatrix values="0 0 0 0 0   0 0 0 0 0   0 0 0 0 0  0 0 0 0.159703351 0" type="matrix"
              in="shadowBlurOuter1"></feColorMatrix>
          </filter>
        </defs>
        <g id="slogo" class="rotation" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
          <g>
            <g id="Icon">
              <circle id="Oval-1" fill="url(#linearGradient-1)" cx="32" cy="32" r="32"></circle>
              <path
                d="M36.7078009,31.8054514 L36.7078009,51.7110548 C36.7078009,54.2844537 34.6258634,56.3695395 32.0579205,56.3695395 C29.4899777,56.3695395 27.4099998,54.0704461 27.4099998,51.7941246 L27.4099998,31.8061972 C27.4099998,29.528395 29.4909575,27.218453 32.0589004,27.230043 C34.6268432,27.241633 36.7078009,29.528395 36.7078009,31.8054514 Z"
                id="blue" fill="#2359F1" fill-rule="nonzero"></path>
              <path
                d="M45.2586091,17.1026914 C45.2586091,17.1026914 45.5657231,34.0524383 45.2345291,37.01141 C44.9033351,39.9703817 43.1767091,41.6667796 40.6088126,41.6667796 C38.040916,41.6667796 35.9609757,39.3676862 35.9609757,37.0913646 L35.9609757,17.1034372 C35.9609757,14.825635 38.0418959,12.515693 40.6097924,12.527283 C43.177689,12.538873 45.2586091,14.825635 45.2586091,17.1026914 Z"
                id="green" fill="#57CF27" fill-rule="nonzero"
                transform="translate(40.674608, 27.097010) rotate(60.000000) translate(-40.674608, -27.097010) "></path>
              <path
                d="M28.0410158,17.0465598 L28.0410158,36.9521632 C28.0410158,39.525562 25.9591158,41.6106479 23.3912193,41.6106479 C20.8233227,41.6106479 18.7433824,39.3115545 18.7433824,37.035233 L18.7433824,17.0473055 C18.7433824,14.7695034 20.8243026,12.4595614 23.3921991,12.4711513 C25.9600956,12.4827413 28.0410158,14.7695034 28.0410158,17.0465598 Z"
                id="red" fill="#FF561B" fill-rule="nonzero"
                transform="translate(23.392199, 27.040878) rotate(-60.000000) translate(-23.392199, -27.040878) ">
              </path>
              <g id="inner-round">
                <use fill="black" fill-opacity="1" filter="url(#filter-3)" xlink:href="#path-2"></use>
                <use fill="#F7F7F7" fill-rule="evenodd" xlink:href="#path-2"></use>
              </g>
            </g>
          </g>
        </g>
      </svg>
      <span class="name">携程旅行情感分析系统</span>
    </div>
    <div class="detail">后台使用django+scrapyd+snownlp 前端vue<br>
      <!-- <span class="desc">实现了requests+etree爬取少量携程旅行信息，<br>
                可独立爬取单条携程旅行m.ctrip.com以及评论，<br>
                后台有scrapyd单账号持续爬虫，日均10W条数据，<br>
                后台使用snownlp实现情感分析，自己训练情感分析模型 <br>
                以此作为本科毕业设计
            </span> -->
    </div>
    <div class="search">
      <!-- <h3>携程旅行爬虫</h3> -->
      <input type="text" class="search-text" placeholder="请输入景点id" ref="sightId">
      <input type="text" class="search-text" placeholder="请输入区域id" ref="districtId">
      <a href="#">
        <button type="button" class="search-scrapy" @click="getInfoId">
          <span>爬虫一下</span>
        </button>
      </a>
    </div>
  </div>
</template>

<script>
// import {mapState} from 'vuex'
import axios from 'axios'
import Qs from 'qs'

export default {
  name: 'IndexMain',
  data () {
    return {
      sightId: '',
      districtId: '',
      wordcloundId: '',
      loading: ''
    }
  },
  methods: {
    getInfoId: function () {
      // this.weiboId = this.$refs.wbId.value
      this.sightId = this.$refs.sightId.value
      this.districtId = this.$refs.districtId.value
      // this.wordcloundId = this.$refs.wordcloundId.value
      console.log(this.sightId)
      console.log(this.districtId)
      if (this.sightId && this.districtId) {
        this.openFullScreen2()
        console.log('zq')
        axios.post('http://127.0.0.1:8000/spiderapi/',
          Qs.stringify({
            sightId: this.sightId,
            districtId: this.districtId
          }))
          .then((response) => {
            console.log(response.data.data)
            console.log(response.data.comments)
            console.log(response.data.total)
            // console.log(response.data.sentiments)
            this.$store.state.sight = response.data.data
            this.$store.state.sightcomments = response.data.comments
            this.$store.state.total = response.data.total
            this.loading.close()
            this.$router.push({
              path: '/sight'
            })
          })
          .catch((error) => {
            this.loading.close()
            this.$message.error('请求失败，请检查后台是否正常运行！！', error)
          })
      } else {
        this.$message.error('景点id和区域id不得为空，请检查后重新输入！')
      }
    },
    openFullScreen2 () {
      this.loading = this.$loading({
        lock: true,
        text: '后台疯狂进行爬虫计算中',
        spinner: 'el-icon-loading',
        background: 'rgba(0, 0, 0, 0.7)'
      })
    }
  }
}

</script>

<style lang="scss" scoped>
  .home-des {
    text-align: center;
    margin-top: 130px;
  }

  .svg {
    vertical-align: middle;
  }

  .detail {
    vertical-align: middle;
    font-size: .28rem;
    margin-left: .24rem;
    font-weight: 200;
    color: #fff;
    margin-top: 20px;

    .desc {
      font-size: .25rem;
    }
  }

  .search {
    margin-top: 30px;
    -webkit-text-size-adjust: none;

    h3 {
      color: #abc;
      display: inline-block;
      font-size: 1.4em;
    }

    .search-text {
      display: inline-block;
      width: 500px;
      margin: 0 auto;
      font-size: 1.4em;
      height: 2.7em;
    }

    a {
      display: inline-block;
      text-decoration: none;

      .search-scrapy {
        width: 120px;
        font-size: 1.4em;
        height: 2.7em;
        position: relative;
        left: -10px;
        top: 1px;
        cursor: pointer;
      }
    }

  }

  .name {
    vertical-align: middle;
    font-size: .48rem;
    margin-left: .24rem;
    font-weight: 200;
    color: #fff;
  }

  @-webkit-keyframes rotation {
    from {
      -webkit-transform: rotate(0deg);
    }

    to {
      -webkit-transform: rotate(360deg);
    }
  }

  .rotation {
    -webkit-transform: rotate(360deg);
    animation: rotation 3s linear infinite;
    -moz-animation: rotation 3s linear infinite;
    -webkit-animation: rotation 3s linear infinite;
    -o-animation: rotation 3s linear infinite;
    transform-origin: center center;
  }

  input[type="text"],
  button {
    box-sizing: border-box;
    text-align: center;
    font-size: 1.4em;
    height: 2.7em;
    // border-radius:4px;
    border: 1px solid #c8cccf;
    color: #6a6f77;
    -web-kit-appearance: none;
    -moz-appearance: none;
    display: block;
    outline: 0;
    padding: 0 1em;
    text-decoration: none;
    width: 100%;
  }

  input[type="text"] {
    border-top-left-radius: 4px;
    border-bottom-left-radius: 4px;
  }

  button {
    background-color: #32325d;
    border-top-right-radius: 4px;
    border-bottom-right-radius: 4px;
    border: none;
    color: #fff;
  }

</style>
