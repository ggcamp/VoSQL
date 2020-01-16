<template>
  <div class="asr">
    <b-jumbotron>
      <h1>VoSQL: A Database Query Tool via Voice 🤔 🎤 😄</h1>
      <b-modal id="help" title="Manual" size="lg" ok-only>
        <h3>
          What's this?
        </h3>
        <p>
          This is a demo for our Google ML winter camp project.
          We built a simple question answering system based on cutting-edge Text2SQL technique.
        </p>
        <p>
          For more details, please check out <a target=”_blank” href="https://drive.google.com/file/d/18hJWv26f3RktxYWNOuT1r3o7H4Ak9b8N">our poster</a>.
        </p>
        <h3>
          How to ask questions?
        </h3>
        <h5>PC/Android Chrome (RECOMMENDED)</h5>
        <p>
          You can press the <b-icon-mic /> button in the page and ask a question, and (hopefully) the machine will give you some
          useful information. You can check the SQL statement in the output to ensure the answer is correct.
        </p>
        <h5>Other browsers</h5>
        <p>
          Unfortunately, speech recognition API is not available on other browsers yet,
          however you can still enter your question in the text box.
        </p>
        <p>
          You can manually choose a dataset for your question, or you can just let us to detect it for you.
        </p>
        <h3>
          What dataset are available?
        </h3>
        <p>
          We picked out 5 dataset from given data.
          Each of them has several tables which contains some example data.
        </p>
        <ul>
          <li>College dataset: Information about students and their GPA, classes, professors and departments.</li>
          <li>Book dataset: Information about books and their publications.</li>
          <li>Company employee dataset: Information about companies and the employees of the companies.</li>
          <li>Flight dataset: Information about airplanes and flights.</li>
          <li>Concert singer dataset: Information of concerts and singers in the concerts</li>
        </ul>
        <p>
          Try out our example questions to know more about the dataset.
        </p>
        <h3>
          What can't this demo do?
        </h3>
        <p>
          Due to the limitations of the dataset and the currently used technique,
          we can't process questions with specific values.
        </p>
        <h3>
          References
        </h3>
        <div class="references">
          <p>
            [1] Yu, Tao, et al. "Spider: A Large-Scale Human-Labeled Dataset for Complex and Cross-Domain Semantic Parsing and Text-to-SQL Task." Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing. 2018.
          </p>
          <p>
            [2] Guo, Jiaqi, et al. "Towards Complex Text-to-SQL in Cross-Domain Database with Intermediate Representation." arXiv preprint arXiv:1905.08205 (2019).
          </p>
          <p>
            [3] Devlin, Jacob, et al. "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Papers). 2019.
          </p>
        </div>
      </b-modal>
      <b-form @submit.stop.prevent="query">
        <b-form-group
                id="input-group-1"
                label="Ask questions"
                label-for="input-1"
        >
          <b-form-input
                  id="input-1"
                  v-model="msg"
                  type="text"
                  placeholder="Or use your voice!"
          />
        </b-form-group>
        <b-form-group
                id="input-group-2"
                label="Database"
                label-for="input-2"
        >
          <b-form-input
                  id="input-2"
                  v-model="db"
                  type="text"
                  style="display: none;"
          />
          <b-form-select v-model="db" :options="options"/>
        </b-form-group>
        <b-form-group
                id="input-group-3"
                label="Example questions"
                label-for="input-3"
        >
          <ul>
          <li><a href="#" @click="example('What is the title of the most expensive book?')">What is the title of the most expensive book?</a></li>
          <li><a href="#" @click="example('How many books has each writer written?')">How many books has each writer written?</a></li>
          <li><a href="#" @click="example('Show me the student name with highest GPA?')">Show me the student name with highest GPA?</a></li>
          <li><a href="#" @click="example('What\'s the total price of all books?')">What's the total price of all books?</a></li>
          <li><a href="#" @click="example('What\'s the average salary of all workers?')">What's the average salary of all workers?</a></li>
          </ul>
        </b-form-group>
        <b-button-group>
        <b-button @click="startVoice" :variant="voiceStarted ? 'success' : 'secondary'" :disabled="loading">
          <b-icon-mic/>
          <span v-if="voiceStarted">
            Stop
          </span>
        </b-button>
        <b-button type="submit" variant="primary" :disabled="loading"><b-icon-upload /> Submit Text Question</b-button>
        <b-button variant="info" @click="showHelp"><b-icon-question /></b-button>
        </b-button-group>
      </b-form>
      <hr>
      <div v-if="loading">
        <div class="spinner-border" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
      <div v-if="completed && !loading">
        <p style="font-weight: bold">{{reply}}</p>
        <b-card title="Explanation">
          <div class="references">
          <p>SQL: {{sql}}</p>
          <div v-if="db_prediction !== 'No need to predict'">
          <p>Intention: {{db_prediction}}</p>
          <p>Intention Confidence: {{db_confidence}}</p>
          </div>
          </div>
        </b-card>
        <b-table striped hover :items="result"/>
      </div>
    </b-jumbotron>
  </div>
</template>

<script>
const axios = require('axios');

export default {
  name: 'HelloWorld',
  data() {
    return {
      msg: '',
      db: 'detect',
      options: [
        { value: 'detect', text: 'Auto detect'},
        { value: 'college_1', text: 'College dataset' },
        { value: 'book_2', text: 'Book dataset' },
        { value: 'company_employee', text: 'Company employee dataset' },
        { value: 'flight_1', text: 'Flight dataset' },
        { value: 'concert_singer', text: 'Concert singer dataset' },
      ],
      result: [],
      reply: '',
      lastResult: '',
      loading: false,
      completed: false,
      voiceStarted: false,
      db_prediction: '',
      db_confidence: 0.0,
      recognition: ''
    }
  },
  mounted() {
    this.$bvModal.show('help')
  },
  methods: {
    example (x) {
      this.msg = x;
      this.query();
    },
    showHelp () {
      this.$bvModal.show('help')
    },
    query () {
      this.loading = true;
      if(this.db === 'detect') {
        axios.get('/detect', {'params': {'q': this.msg}}).then(
                (response) => {
                  // eslint-disable-next-line no-console
                  console.log(response.data);
                  this.db_prediction = response.data.data;
                  this.db_confidence = response.data.confidence;
                }
        ).then(
                () => {
                  return axios.get('/text2sql', {'params': {'q': this.msg, 'db': this.db_prediction, 'last': this.lastResult}}).then(
                          (response) => {
                            // eslint-disable-next-line no-console
                            console.log(response.data);
                            this.result = response.data.data;
                            this.sql = response.data.sql;
                            this.completed = true;
                            this.getReply();
                          }
                  )
                }
        ).finally(() => {
          this.loading = false
        })
      } else {
        this.db_prediction = 'No need to predict';
        this.db_confidence = 'No need to predict';
        axios.get('/text2sql', {'params': {'q': this.msg, 'db': this.db, 'last': this.lastResult}}).then(
                (response) => {
                  // eslint-disable-next-line no-console
                  console.log(response.data);
                  this.result = response.data.data;
                  this.sql = response.data.sql;
                  this.completed = true;
                  this.getReply();
                }
        ).finally(() => {
          this.loading = false
        })
      }
    },
    getReply() {
      this.lastResult = '';
      if(this.result.length === 0) {
        this.reply = "Sorry, no results are found"
      } else if(this.result.length === 1) {
        let count = 0;
        let value = '';
        let result = this.result[0];
        for (let key in result) {
          if (result.hasOwnProperty(key)) {
            count++;
            value = result[key];
          }
        }
        if (count === 1) {
          this.reply = "The result is " + value;
          this.lastResult = value;
        } else {
          this.reply = "I've found 1 result for you";
        }
      } else if (this.result.length > 10) {
        this.reply = "I've found " + this.result.length + " results for you";
      } else {
        this.reply = "The result is ";
        for (let i = 0; i < this.result.length; i++) {
          let count = 0;
          let value = '';
          let result = this.result[i];
          for (let key in result){
            if(result.hasOwnProperty(key)){
              count++;
              value = result[key];
            }
          }
          if(count === 1) {
            this.reply += value;
            if (i !== this.result.length - 1) {
              this.reply += ', ';
            }
          } else {
            this.reply = "I've found " + this.result.length + " results for you";
          }
        }
      }
      this.reply += '.';
      var utterance = new SpeechSynthesisUtterance(this.reply);
      utterance.lang = 'en-US';
      speechSynthesis.speak(utterance);
    },
    startVoice() {
      if (this.voiceStarted) {
        this.voiceStarted = false;
        this.recognition.abort();
      } else {
        this.voiceStarted = true;
        let SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.lang = 'en-US';
        this.recognition.start();
        this.recognition.onresult = (event) => {
          this.voiceStarted = false;
          // eslint-disable-next-line no-console
          console.log(event.results[0][0].transcript);
          this.msg = event.results[0][0].transcript;
          this.recognition.stop();
          this.query();
        };
        this.recognition.onnomatch = () => {
          this.voiceStarted = false;
        }
        this.recognition.onerror = () => {
          this.voiceStarted = false;
        }
      }

    }
  }
}
</script>

<style scoped>
.references {
  font-size: small;
}
</style>
