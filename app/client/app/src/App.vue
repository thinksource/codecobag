<template>

<div>
<h2>Sending an email via APIs</h2>
  <el-alert v-if="error"
    title='send email error'
    type='error'
    center
    show-icon>
  </el-alert>
<el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="120px" class="demo-ruleForm">
  <el-form-item label='Send mail to' prop="to" >
    <el-input type="text" name="emailto" v-model="ruleForm2.to" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="CC" prop="cc">
    <el-input type="text" name="emailcc" v-model="ruleForm2.cc" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="BCC" prop="bcc">
    <el-input type="text" name="emailbcc" v-model="ruleForm2.bcc" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="Title" prop="subject">
    <el-input type="text" name="emailtitle" v-model="ruleForm2.subject" auto-complete="off"></el-input>
  </el-form-item>

  <el-form-item label="Body" prop="text">
    <el-input type="textarea" name="emailtext" v-model="ruleForm2.text" auto-complete="off"></el-input>
  </el-form-item>

  <el-form-item>
    <el-button type="primary" name="submit" @click="submitForm('ruleForm2')">Submit</el-button>
    <el-button @click="resetForm('ruleForm2')">Reset</el-button>
  </el-form-item>
</el-form>
</div>
</template>
<script>
import axios from 'axios'
const $myreq = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' }
})
export default {
  // name: "Form component",
  data () {
    // var checkAge = (rule, value, callback) => {
    //   if (!value) {
    //     return callback(new Error('Please input the age'))
    //   }
    //   setTimeout(() => {
    //     if (!Number.isInteger(value)) {
    //       callback(new Error('Please input digits'))
    //     } else {
    //       if (value < 18) {
    //         callback(new Error('Age must be greater than 18'))
    //       } else {
    //         callback()
    //       }
    //     }
    //   }, 1000)
    // }
    var validateEmail = (rule, value, callback) => {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      // alert(this.ruleForm2.mailto);
      if (this.ruleForm2.to === '' && this.ruleForm2.cc === '' && this.ruleForm2.bcc === '') {
        callback(new Error('Please input an email address'))
      } else {
        var va = value.split(',')
        va.forEach(function (v) {
          if (!re.test(v.trim()) && v !== '') {
            callback(new Error('Email address ' + v + ' is wrong format.Please input correct email address'))
          }
        })

        callback()
      }
    }
    return {
      error: '',
      ruleForm2: {
        to: '',
        cc: '',
        bcc: '',
        subject: '',
        text: ''
      },
      rules2: {
        to: [
          { validator: validateEmail, trigger: 'blur' }
        ],
        cc: [
          { validator: validateEmail, trigger: 'blur' }
        ],
        bcc: [
          { validator: validateEmail, trigger: 'blur' }
        ],
        subject: [
          { required: true, message: 'please input the title', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm (formName) {
      var self = this
      this.error = ''
      console.log(this.$refs[formName])
      this.$refs[formName].validate((valid) => {
        if (valid) {
          $myreq.post('/sendmail', this.ruleForm2).then(
            function (res) {
              if (res.data) { self.$message(res.data['message']) } else { self.$message('Email already in sending queue') }
            }
          ).catch((error) => {
            if (error.data) { self.error = error.data } else { self.error = 'this is an error' }
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    resetForm (formName) {
      this.$refs[formName].resetFields()
      this.error = ''
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
<style lang="scss">
@import url("//unpkg.com/element-ui/lib/theme-chalk/index.css");
// @import 'assets/css/index.css';
</style>
