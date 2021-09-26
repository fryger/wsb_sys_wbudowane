<template>
  <v-expansion-panel @change="getConfig">
    <v-expansion-panel-header color="orange"
      >Email configuration</v-expansion-panel-header
    >
    <v-expansion-panel-content>
      <v-form class="ma-3" ref="form" v-model="valid" lazy-validation>
        <v-text-field
          label="Sender"
          outlined
          v-model="sender"
          :rules="emailRules"
        ></v-text-field>
        <v-text-field
          label="Sender password"
          outlined
          v-model="pass"
          :type="showPassword ? 'text' : 'password'"
          prepend-icon="mdi-lock"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          @click:append="showPassword = !showPassword"
          :rules="passwordRules"
        ></v-text-field>
        <v-text-field
          class="mt-3"
          label="Receiver"
          outlined
          v-model="receiver"
          :rules="emailRules"
        ></v-text-field>
        <v-btn
          large
          block
          color="secondary"
          @click="updateConfig"
          :loading="btnLoading"
          >Update config</v-btn
        >
      </v-form>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
export default {
  data() {
    return {
      btnLoading: false,
      showPassword: false,
      sender: "",
      pass: "",
      receiver: "",
      emailRules: [
        v => !!v || "E-mail is required",
        v => /.+@.+\..+/.test(v) || "E-mail must be valid"
      ],
      passwordRules: [v => !!v || "Password is required"]
    };
  },
  methods: {
    async getConfig() {
      await this.$axios
        .get("http://localhost:5000/email")
        .then(
          response => (
            (this.sender = response.data.sender),
            (this.receiver = response.data.receiver)
          )
        )
        .catch(error => {
          console.log(error.response);
        });
    },
    async updateConfig() {
      if (this.$refs.form.validate()) {
        const data = {
          sender: this.sender,
          password: this.pass,
          receiver: this.receiver
        };
        this.btnLoading = true;
        await this.$axios
          .post("http://localhost:5000/email", data)
          .then(response => console.log(response))
          .catch(error => console.log(error))
          .then((this.btnLoading = false));
      }
    }
  }
};
</script>
