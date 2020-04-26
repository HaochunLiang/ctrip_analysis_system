<template>
  <div class="sight">
<!--            {{this.sightInfo[0].pk}}
            <br><br>
            {{this.sightInfo[0].fields.Img}}
            <br><br>
            {{this.img[0]}}
            <br><br>
            {{this.imglen}} -->
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

            <el-card class="box-card-detail ciyun">
              <div slot="header" class="clearfix">
                <span>词云展示</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-if="this.chartData ==='' " style="padding: 0.3125rem;">词云加载中...</div>
              <div v-else>
                <ve-wordcloud :data="chartData" :settings="chartSettings"></ve-wordcloud>
                <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                  景点@<strong>{{this.sightInfo[0].fields.Title}}</strong>的评论内容中，词云分析结果如上图所示，其中
                  <strong>{{this.chartData.rows[0].word}}</strong>的频率最高，达到
                  <strong>{{this.chartData.rows[0].count}}</strong>次，其次是
                  <strong>{{this.chartData.rows[1].word}}</strong>、
                  <strong>{{this.chartData.rows[2].word}}</strong>、
                  <strong>{{this.chartData.rows[3].word}}</strong>分别达到
                  <strong>{{this.chartData.rows[1].count}}</strong>、
                  <strong>{{this.chartData.rows[2].count}}</strong>、
                  <strong>{{this.chartData.rows[3].count}}</strong>次。
                </div>
              </div>
            </el-card>
            <el-card class="box-card-detail ciyun">
              <div slot="header" class="clearfix">
                <span>敏感率</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-if="this.chartData ==='' " style="padding: 0.3125rem;">敏感率加载中...</div>
              <div v-else>
                <ve-bar :data="this.minganData" height="3.4rem" style="margin-top: .3125rem;"></ve-bar>
                <div class="well fz14" style="padding: 0.3125rem;font-size: 13px;margin-bottom: 0;background-color:#f7f9fa !important">
                  景点@<strong>{{this.sightInfo[0].fields.Title}}</strong>的评论内容中，敏感占比（当前敏感率只检测暴恐、反动、民生、色情等词汇）
                  <strong>{{this.minganData.rows[0].敏感*100}}%</strong>,
                  在<strong>
                    <span v-if="this.minganData.rows[0].敏感 < 0.25">极低</span>
                    <span v-else-if="this.minganData.rows[0].敏感 >= 0.25 && this.minganData.rows[0].敏感 < 0.5">低</span>
                    <span v-else-if="this.minganData.rows[0].敏感 >= 0.5  && this.minganData.rows[0].敏感 < 0.75">高</span>
                    <span v-else>极高</span>
                  </strong>敏感范围内。
                </div>
              </div>
              <!-- <img v-else :src="'data:image/png;base64,'+ico" class="avatar"> -->
            </el-card>
   
          </div>
        </div>
      </el-col>
      <el-col :span="16">
        <div class="grid-content bg-purple">
          <div class="info-right" ref="element">
            <el-card class="box-card">
              <div slot="header" class="clearfix">
                <span>评论内容情感分析</span>
                <el-button style="float: right; padding: 3px 0" type="text"></el-button>
              </div>
              <div v-for="(comment, index) in this.sightComments" :key="index" style="height:auto">
                <div class="comments-header">
                  <div class="cp-id">
                    <span>评论ID：{{comment.pk}}</span>
                    <el-button style="float: right; padding: 3px 0" type="text">{{comment.fields.AuditTime}} </el-button>
                  </div>
                  <div class="cp-content">
                    <i class="el-icon-edit write"></i>{{comment.fields.Content}}
                  </div>
                  <div class="cp-add">
                    <span>
                      景色：{{comment.fields.Score1}}
                      趣味：{{comment.fields.Score2}}
                      性价比：{{comment.fields.Score3}}
                    </span>
                  </div>
                </div>
                <div class="tweets-footer clearfix">
                  <div class="footer-left">
                    关键字：
                    <span v-if="comment.fields.sentiments>0.5" style="background:#c2e7b0">
                      {{comment.fields.tags}}
                    </span>
                    <span v-else style="background:#fbc4c4">
                      {{comment.fields.tags}}
                    </span>
                    <br>
                    情感数值：{{comment.fields.sentiments}}
                    <br>
                    词性：{{comment.fields.pinyin}}
                  </div>
                  <div class="footer-right">
                    <el-progress class="progress" v-if="comment.fields.sentiments>0.5" type="circle"
                      :percentage="comment.fields.sentiments*100" color="#13ce66" status="text">情感积极</el-progress>
                    <el-progress class="progress" v-else type="circle" :percentage="comment.fields.sentiments*100"
                      color="#ff4949" status="text">情感消极</el-progress>
                  </div>
                </div>
                <hr style="background-color:#50bfff;height:1px;border:none;">
              </div>
            </el-card>
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="page" ref="page" >
      <el-pagination  @current-change="handleCurrentChange" :current-page.sync="currentPage" :page-size="this.size"
        layout="prev, pager, next" :total='this.total'>
      </el-pagination>
    </div>
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
      sight: state => state.sight,
      mycomments: state => state.sightcomments,
      total: state => state.total
    }),
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
    open () {
      console.log(this.sightInfo[0].pk)

      if (this.sight === '' || this.sight === null || this.mycomments === '' || this.mycomments === null) {
        this.$notify.error({
          title: '信息错误',
          message: '你似乎来到知识的荒原~',
          position: 'bottom-right'
        })
      } else {
        this.$notify.info({
          title: '消息',
          message: '后台抓取用户所有信息开始生成词云',
          position: 'bottom-right'
        })
        axios.get('http://127.0.0.1:8000/wordcloudapi?&sightId=' + this.sightId)
          .then((response) => {
            let res = []
            for (let i = 0; i < response.data.cipin.length; i++) {
              res.push({
                'word': response.data.cipin[i].word,
                'count': response.data.cipin[i].count
              })
            }
            let chartData = {
              columns: ['word', 'count'],
              rows: res
            }
            this.chartData = chartData
            let mingan = {
              columns: ['敏感率', '敏感', '非敏感'],
              rows: [
                { '敏感率': '敏感率', '敏感': response.data.mingan.toFixed(2), '非敏感': 1 - response.data.mingan.toFixed(2) }
              ]
            }
            this.minganData = mingan
            let tu = eval('(' + response.data.tu + ')')
            this.emtionanaly.len = tu.length
            this.emtionanaly.smalldate = tu[0][0]
            this.emtionanaly.smallcount = tu[0][1]
            this.emtionanaly.bigdate = tu[tu.length - 1][0]
            this.emtionanaly.bigcount = tu[tu.length - 1][1]
            let tures = []
            for (let i = 0; i < tu.length; i++) {
              if (tu[i][1] > this.emtionanaly.maxcount) {
                this.emtionanaly.maxcount = tu[i][1]
                this.emtionanaly.maxdate = tu[i][0]
              }
              tures.push({
                '情感值': tu[i][0].substring(0, 4),
                '次数': tu[i][1]
              })
              if (tu[i][0] < 0.5) {
                this.emtionanaly.count0++
              } else {
                this.emtionanaly.count1++
              }
            }
            let textchartData = {
              columns: ['情感值', '次数'],
              rows: tures
            }
            this.textchartData = textchartData
            let pl = '消极偏多😭'
            if (this.emtionanaly.count0 > this.emtionanaly.count1) {
              pl = '消极偏多😭'
            } else {
              pl = '积极偏多😁'
            }
            this.$notify({
              message: '整体情感评定：' + pl,
              type: 'success',
              position: 'bottom-right'
            })
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
    handleCurrentChange (val) {
      console.log(val)
      console.log(this.sightId)
      console.log(this.currentPage)
      // this.pageshow = true//让分页隐藏
      axios.post('http://127.0.0.1:8000/commentsapi/',
        Qs.stringify({
          sightId: this.sightId,
          page: val
        })
      ).then((response) => {
        this.$store.state.sightcomments = null
        this.$store.state.sightcomments = response.data.data
        this.sightcomments = response.data.data
        // this.getData();//获取数据
        // this.pageshow = false//让分页隐藏
        // this.$nextTick(() => {//重新渲染分页
        //     this.pageshow = true
        // })
        // this.currentPage=1
        // this.currentPage=val
        // console.log(this.$store.state.sightcomments)
        // console.log("----------------------")
        this.mycomments = this.sightcomments
        // console.log(this.mycomments)
        // this.sightComments=this.sightcomments
      })
    },
    ...mapMutations(['changeSightComments'])
  },
  mounted () {
    this.open()
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

</style>
