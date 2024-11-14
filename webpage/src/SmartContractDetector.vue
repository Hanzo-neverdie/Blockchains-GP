<template>
    <div class="background  background-image">
      <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">
        <div class="container">
          <a class="navbar-brand" href="#">
            BlockChains Group Project
          </a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarsExampleDefault" aria-controls="navbarsExampleDefault" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
        </div>
      </nav>

      <main role="main" class="container">
        <div class="starter-template">
          <h1 class="font-white">Smart Contract Vulnerability Detection</h1>         
        </div>
        <div>
          <p class="lead font-white" style="text-align: left" >This project joins hands with <a href="https://github.com/crytic/slither" class="underline-link"style="color:yellow">Slither</a> to help you diagnose smart contract vulnerabilities.
          <br>Upload your smart contract code to detect potential vulnerabilities!</p>
        </div>
  
        <div class="row">
          <div class="col-md-12">
            <form @submit.prevent="handleSubmit">
              <div class="form-group">
                <label for="contractCode" class="font-size font-white">Smart Contract Code</label>
                <textarea class="form-control" id="contractCode" v-model="contractCode" rows="10"></textarea>
              </div>
              <button @click="submitContractCode" class="btn btn-primary">Detect Vulnerabilities</button>
            </form>
          </div>
        </div>
        
        <div>
          <div v-for="(title, index) in result" :key="index" class="high-impact-vulnerability">
            <h2 class="font-white">High Impact Vulnerability </h2>
            <div class="border p-3">
              <pre style="color: red;">{{ index + 1 }}.{{ title }}</pre>
            </div>
          </div>
        </div>
      </main>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const contractCode = ref('');
const result = ref([]);

const submitContractCode = async () => {
  try {
    // 使用 fetch API 发送 AJAX 请求
    const response = await fetch('http://127.0.0.1:5173/api/submit-contract', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ code: contractCode.value })
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    const data = await response.json(); // 先获取整个响应数据
    // 遍历 data 数组，并将每个 Title 值存储到 result 数组中
    data.forEach(item => {
      result.value.push(item.Title); // 假设每个 item 都有一个 Title 属性
    });
   
    alert('Contract code submitted successfully!');
  } catch (error) {
    console.error('Error submitting contract code:', error);
    alert('Failed to submit contract code');
  }
};

</script>
<!-- <script>
import { ref } from 'vue';

export default {
  setup() {
    const contractCode = ref('');
    const results = ref(null);

    function analyzeContract() {
      // 调用后端API进行分析，并获取结果
      // 假设我们有一个API端点 '/api/analyze'
      fetch('http://127.0.0.1:5173/api/submit-contract', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code: contractCode.value }),
      })
      .then(response => response.json())
      .then(data => {
        results.value = data.result;
      })
      .catch(error => console.error('Error:', error));
    }

    return {
      contractCode,
      results,
      analyzeContract,
    };
  },
};
</script> -->
  
  <style scoped>
  body {
    padding-top: 5rem;
  }
  .starter-template {
    padding: 5rem 14rem;
    text-align: center;
  }
  .lead{
    padding: 2rem 0rem;
  }
  .background {
      background-color: #276595;
  } 
  .background-image {
    background-image: url('./assets/logo-bg.png');
    background-position: center center;
    background-size: cover;
  }
  .underline-link {
      text-decoration: underline;
  }
  .font-white {
    color: aliceblue
  }
  .font-size {
    font-size: 30px;
  }
    
  </style>