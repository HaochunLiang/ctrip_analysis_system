<template>
  <div class="sight">
    <div class="sight-header">
      <div class="photo-warp">
        <img :src="this.img[0]" class="cp-img">
      </div>
      <div class="cp-name">
        <!-- <img class="wb-logo" src="//www.sinaimg.cn/blog/developer/wiki/LOGO_32x32.png"> -->
        <span class="name">{{this.sightInfo[0].fields.Title}}</span>
      </div>
    </div>
    <el-row :gutter="20">
      <el-col :span="8">
        <div class="grid-content bg-purple">
          <div class="info-left">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>评分 | 评论数</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div class="text item item1">
                {{this.sightInfo[0].fields.CommentScoreReal}}
              </div>
              <div class="text item item1">
                {{this.sightInfo[0].fields.CommentNumberText}}
              </div>
              <div class="text item item1">
                -----
              </div>
              <div class="text item item2">评分</div>
              <div class="text item item2">评论数</div>
            </el-card>

            <el-card class="box-card-detail">
              <div slot="header" class="clearfix">
                <span>基本信息</span>
                <!-- <el-button style="float: right; padding: 3px 0" type="text"></el-button> -->
              </div>

              <div class="text item3 item3-txt">
                地区id
              </div>
              <div class="text item3-detail">
                {{this.sightInfo[0].fields.DistrictId}}
              </div>

              <div class="text item3 item3-txt">
                特点
              </div>
              <div class="text item3-detail">
                {{this.sightInfo[0].fields.Tags}}
              </div>

              <div class="text item3 item3-txt">
                排名
              </div>
              <div class="text item3-detail">
                <span v-if="this.sightInfo[0].fields.Texts">{{this.sightInfo[0].fields.Texts}}</span>
                <span v-else>无</span>
              </div>

              <div class="text item3 item3-txt">
                地点
              </div>
              <div class="text item3-detail">
                <span v-if="this.sightInfo[0].fields.AddressText">{{this.sightInfo[0].fields.AddressText}}</span>
                <span v-else>无</span>
              </div>

              <div class="text item3 item3-txt">
                到达方式
              </div>
              <div class="text item3-detail">
                <span v-if="this.sightInfo[0].fields.AddressWay">{{this.sightInfo[0].fields.AddressWay}}</span>
                <span v-else>无</span>
              </div>

              <div class="text item3 item3-txt">
                携程主页
              </div>
              <div class="text item3-detail">
                <a :href='this.sightInfo[0].fields.BusinessId' target="_blank" class="index">{{this.sightInfo[0].fields.Title}}</a>
              </div>
            </el-card>



          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div id="myChart" :style="{width: '0px', height: '0px'}"></div>
        <div id="id1"  :style="{ height:'300px',width:'500px' }" />
        <div class="grid-content bg-purple">
          <div class="info-right" ref="element">

          </div>
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>


import {
  mapState,
  mapMutations
} from 'vuex'
import axios from 'axios'
import Qs from 'qs'
export default {
  name: 'SightHeader',
  data () {
    this.chartSettings = {
      sizeMin: 20,
      sizeMax: 40
    }
    return {
      textchartData: '',
      chartData: '',
      minganData: '',
      imgObj: {
        sexman: require('@/assets/sex-m.png'),
        sexwoman: require('@/assets/sex-f.png')
      },
      size: 10,
      // pageshow:true,
      // paginationShow:true,
      currentPage: 1,
      mycomments: this.$store.state.sightcomments,
      srcs: this.msrcs(),
      emtionanaly: {
        count0: 0,
        count1: 0,
        len: 1,
        maxdate: 0,
        maxcount: 0,
        smalldate: 0,
        smallcount: 0,
        bigdate: 0,
        bigcount: 0
      }
    }
  },
  computed: {
    ...mapState({
      // user: state => state.user,
      // mytweets:state=>state.usertweets,
      sight: state => state.sight1,
      aspect_word: state=>state.aspect_word
      //mycomments: state => state.sightcomments,
      //total: state => state.total
    }),
    aspectInfo: function()
    {
      return eval('(' + this.aspect_word + ')')
    },
    sightInfo: function ()
    {
      return eval('(' + this.sight + ')')
    },
    sightComments: function ()
    {
      return eval('(' + this.mycomments + ')')
    },
    img: function ()
    {
       return eval('(' +this.sightInfo[0].fields.Img + ')')
      //return eval('(' + '' + ')')
    },
    imglen: function ()
    {
      return this.img.length
    },
    sightId: function ()
    {
      return this.sightInfo[0].pk
    }
  },
  methods: {
    msrcs: function ()
    {
      if (this.imglen > 1) {
        return this.img.splice(1)
      } else {
        return 0
    }
    },
    drawLine () {
          var echarts = require('echarts');
          var myChart = echarts.init(document.getElementById('myChart'));
          myChart.setOption({
            title: {
              text: 'ECharts 入门示例'
            },
            tooltip: {},
            xAxis: {
              data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子']
            },
            yAxis: {},
            series: [{
              name: '销量',
              type: 'bar',
              data: [5, 20, 36, 10, 10, 20]
            }]
          });
    },
     initChart() {
          var echarts = require('echarts');
          this.chart = echarts.init(document.getElementById('id1'));
          const option = {
            title: {
              text: this.title,
              x: "center"
            },
            backgroundColor: "#fff",
            // tooltip: {
            //   pointFormat: "{series.name}: <b>{point.percentage:.1f}%</b>"
            // },
            series: [
              {
                type: "wordCloud",
                //用来调整词之间的距离
                gridSize: 10,
                //用来调整字的大小范围
                // Text size range which the value in data will be mapped to.
                // Default to have minimum 12px and maximum 60px size.
                sizeRange: [14, 60],
                // Text rotation range and step in degree. Text will be rotated randomly in range [-90,                                                                             90] by rotationStep 45
                //用来调整词的旋转方向，，[0,0]--代表着没有角度，也就是词为水平方向，需要设置角度参考注释内容
                // rotationRange: [-45, 0, 45, 90],
                // rotationRange: [ 0,90],
                rotationRange: [0, 0],
                //随机生成字体颜色
                // maskImage: maskImage,
                textStyle: {
                  normal: {
                    color: function() {
                      return (
                        "rgb(" +
                        Math.round(Math.random() * 255) +
                        ", " +
                        Math.round(Math.random() * 255) +
                        ", " +
                        Math.round(Math.random() * 255) +
                        ")"
                      );
                    }
                  }
                },
                //位置相关设置
                // Folllowing left/top/width/height/right/bottom are used for positioning the word cloud
                // Default to be put in the center and has 75% x 80% size.
                left: "center",
                top: "center",
                right: null,
                bottom: null,
                width: "200%",
                height: "200%",
                //数据
                //data:this.aspectInfo[0].fields.AspectWord
                data:eval('(' + this.aspectInfo[0].fields.AspectWord + ')')
                //data:aspect()
              }
            ]
          };
          this.chart.setOption(option);
          //console.log(this.aspectInfo[0].fields.AspectWord)
        },
    open () {
      //console.log(this.sightInfo[0].pk)
      //console.log(this.aspectInfo[0].fields.AspectWord)
      //data1=this.aspectInfo[0].fields.AspectWord
      if (this.sight === '' || this.sight === null ) {
        this.$notify.error({
          title: '信息错误',
          message: '你似乎来到知识的荒原~',
          position: 'bottom-right'
        })
      }
    },
    // search () {
    //       this.paginationShow = false
    //       this.handleCurrentChange(1)
    //       this.$nextTick(function () {
    //         this.paginationShow = true;
    //       })
    //     },
    ...mapMutations(['changeSightComments'])
  },
  mounted () {
    console.log(this.aspectInfo[0].fields.AspectWord)
    data1:this.aspectInfo[0].fields.AspectWord
    this.open()
    //this.drawLine()
    this.initChart()

  }
}

</script>

<style lang="scss" scoped>
  .sight {
    padding: 0 100px 0 100px;
    margin-bottom: 20px;
    margin: 0 auto;
    max-width: 1100px;
    min-width: 1000px;

    .sight-header {
      width: 100%;
      text-align: center;
      height: 200px;

      .photo-warp {
        width: 120px;
        height: 120px;
        margin: 0 auto;
        border: 1px solid #fff;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        position: relative;

        .cp-img {
          width: 120px;
          height: 120px;
          border-radius: 50%;
          display: block;
        }

        // .wb-sign{
        //     background-image: url('//img.t.sinajs.cn/t6/style/images/common/icon.png?id=42be5a1688cf4049');
        //     background-repeat: no-repeat;
        //     background-position: -50px 0;
        // }
      }

      .cp-name {
        margin-top: 5px;

        .cp-logo {
          width: 32px;
          height: 32px;
          vertical-align: middle;
        }

        .name {
          vertical-align: middle;
          color: #fff;
          font-size: .35rem;
        }

        .sex {
          width: 30px;
          height: 30px;
          vertical-align: middle;
        }

        .cp-brief {
          margin-top: 10px;
          color: #fff;
          font-size: .2rem;
        }
      }
    }

    .info-left {
      font-size: .2rem;

      .text {
        font-size: 18px;
      }

      .item {
        margin-bottom: 3px;
        width: 33%;
        float: left;
        text-align: center;
      }

      .item3 {
        margin-bottom: 10px;
        width: 30%;
        float: left;
        text-align: center;
      }

      .item3-detail {
        margin-bottom: 10px;
        width: 70%;
        float: left;
        text-align: center;
      }

      .cp-xz {
        width: 22px;
        height: 22px;
      }

      .item3-txt {
        color: #808080;
      }

      .item1 {
        border-right: 1px solid #c2c2c2;
      }

      .item2 {
        color: #808080;
        margin-bottom: 10px;
      }

      .clearfix:before,
      .clearfix:after {
        display: table;
        content: "";
      }

      .clearfix:after {
        clear: both
      }

      .box-card {
        width: 100%;
      }

      .box-card-detail {
        width: 100%;
        margin-top: 30px;
        .avatar {
          width: 100%;
        }
      }
    }

    .info-right {
      margin-left: 3%;
      vertical-align: top;
      font-size: .2rem;

      .comments-header {
        .cp-id {
          font-size: 14px;
          color: #808080;
        }
      }

      .comments-footer {
        background-color: #ecf8ff;
        border-radius: 4px;
        border-left: 5px solid #50bfff;
        height: 105px;
        margin: 10px 0;
        padding: 10px;
        position: relative;

        .footer-left {
          overflow: hidden;
          height: 105px;
          width: 75%;
        }

        .footer-right {
          position: absolute;
          top: -.2rem;
          right: 0;
          width: 25%;

          .progress {
            transform: scale(.7);
          }
        }
      }

      .cp-content {
        margin: 10px 0;
        font-size: 15px;

        .write {
          color: #409EFF;
          width: 22px;
          height: 22px;
        }
      }

      .cp-add {
        text-align: right;
        color: #808080;

        span {
          margin-right: 10px;
        }
      }
    }

    .page {
      text-align: right;
      position: relative;
      bottom: 0;
      z-index: 3;
    }
  }

  .index {
    text-decoration: none;
  }

  .ciyun {
    /deep/ .el-card__body {
      padding: 0;
    }
  }

  .chartsClass {
    padding-left: 1.2rem;
  }

</style>
