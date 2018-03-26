<template>
  
<div>
<h2>Sending an email via APIs</h2>
  <el-alert v-if="error"
    title="send email error"
    type="error"
    center
    show-icon>
  </el-alert>
<el-form :model="ruleForm2" status-icon :rules="rules2" ref="ruleForm2" label-width="120px" class="demo-ruleForm">
  <el-form-item label="Send mail to" prop="mailto">
    <el-input type="text" v-model="ruleForm2.mailto" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="CC" prop="cc">
    <el-input type="text" v-model="ruleForm2.cc" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="BCC" prop="bcc">
    <el-input type="text" v-model="ruleForm2.bcc" auto-complete="off"></el-input>
  </el-form-item>
  <el-form-item label="Title" prop="title">
    <el-input type="text" v-model="ruleForm2.subject" auto-complete="off"></el-input>
  </el-form-item>

  <el-form-item label="Body" prop="text">
    <el-input type="textarea" v-model="ruleForm2.text" auto-complete="off"></el-input>
  </el-form-item>

  <el-form-item>
    <el-button type="primary" @click="submitForm('ruleForm2')">Submit</el-button>
    <el-button @click="resetForm('ruleForm2')">Reset</el-button>
  </el-form-item>
</el-form>
</div>
</template>
<script>
import axios from 'axios';
const $myreq = axios.create({
  baseURL: '/api/',
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' },
});
export default {
  data() {
    var checkAge = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('Please input the age'));
      }
      setTimeout(() => {
        if (!Number.isInteger(value)) {
          callback(new Error('Please input digits'));
        } else {
          if (value < 18) {
            callback(new Error('Age must be greater than 18'));
          } else {
            callback();
          }
        }
      }, 1000);
    };
    var validateEmail = (rule, value, callback) =>{
      var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      alert(this.ruleForm2.mailto);
      if (this.ruleForm2.mailto === '' && this.ruleForm2.cc ==='' && this.ruleForm2.bcc === ''){
        callback(new Error("Please input an email address"));
      }else{
        var va=value.split(',');
        va.forEach(function(v){
          if (!re.test(v) && v !== ''){
          callback(new Error("Email address "+v+" is wrong format.Please input correct email address"));
        }
        })

        callback();
      }
    };
    return {
      error:"",
      ruleForm2: {
        mailto:'',
        cc:'',
        bcc:'',
        subject:'',
        text:''
      },
      rules2: {
        mailto:[
          {validator: validateEmail, trigger:'blur'}
        ],
        cc:[
          {validator: validateEmail, trigger:'blur'}
        ],
        bcc:[
          {validator: validateEmail, trigger:'blur'}
        ],
        title:[
          {required:true, message:'please input the title', trigger:'blur'}
        ]
      }
    };
  },
  methods: {
    submitForm(formName) {
      var self=this;
      this.$refs[formName].validate((valid) => {
        if (valid) {
          $myreq.post('/sendemail', this.data.ruleForm2).then(
            function(res){
              if(res.data)
                self.$message(res.data["message"])
              else
                self.$message("Email already in sending queue");
            }
          ).catch((error)=>{
            if(res.data)
              self.error=res.data;
            else
              self.error="this is an error";
          })

        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
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
@import url("//unpkg.com/element-ui@2.2.2/lib/theme-chalk/index.css");
</style>