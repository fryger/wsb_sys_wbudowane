<template>
  <div class="mt-12">
    <v-row>
      <v-col cols="12" lg="8">
        <v-card class="rounded-lg">
          <v-card-title style="background-color: orange">
            Parking configuration
            <v-btn color="success" rounded :right="true" :absolute="true" large @click="sendSpotConfig"
              >Send</v-btn
            >
          </v-card-title>
          <v-card-content>
            <v-form class="ma-3" ref="configForm" v-model="valid" lazy-validation>
            <v-row class="mt-2">
              
              <v-col cols="12" lg="6">
                <v-text-field
                  v-model="name"
                  label="Spot name"
                  :rules='nameRules'
                  class="pa-2"
                  filled
                  outlined
                  dense
                ></v-text-field>
                <v-text-field
                  v-model="urls"
                  label="Stream URL"
                  :rules='urlRules'
                  class="pa-2"
                  filled
                  outlined
                  dense
                ></v-text-field>
              </v-col>
              <v-col cols="12" lg="6">
                <v-text-field
                  v-model="spots"
                  label="Spots count"
                  :rules="spotRules"
                  class="pa-2"
                  filled
                  outlined
                  dense
                ></v-text-field>
                <v-text-field
                  v-model="time"
                  label="Send report time"
                  :rules="timeRules"
                  class="pa-2"
                  filled
                  outlined
                  dense
                ></v-text-field>
              </v-col>
              
            </v-row>
            </v-form>
            <v-row class="justify-center">
              <v-cols cols="12" lg="3"
                ><v-card-text
                  >Area width: {{ coordinates.width }}</v-card-text
                ></v-cols
              >
              <v-cols cols="12" lg="3"
                ><v-card-text
                  >Area height: {{ coordinates.height }}</v-card-text
                ></v-cols
              >
              <v-cols cols="12" lg="3"
                ><v-card-text
                  >Offset top: {{ coordinates.top }}</v-card-text
                ></v-cols
              >
              <v-cols cols="12" lg="3"
                ><v-card-text
                  >Offset left: {{ coordinates.left }}</v-card-text
                ></v-cols
              >
            </v-row>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-card height="100%">
                    <video
                      id="video"
                      controls="controls"
                      crossorigin="anonymous"
                      style="width:100%"
                      :key="urls"
                    >
                      <source :src="urls" />
                    </video>
                    <v-card-action>
                      <v-btn block @click="captureByVideo">Select area</v-btn>
                    </v-card-action>
                  </v-card>
                </v-col>
              </v-row>
            </v-container>
          </v-card-content>
          <v-dialog v-model="dialog" max-width="1200px">
            <v-container fluid class="pa-6">
              <v-row>
                <v-col cols="12" md="8"
                  ><cropper
                    class="cropper pa-12"
                    :src="frame"
                    @change="change"
                    style="width:100%;"
                /></v-col>
                <v-col cols="12" md="4" class="pa-4">
                  <v-text-field
                    filled
                    outlined
                    label="Width"
                    v-model="coordinates.width"
                  ></v-text-field
                  ><v-text-field
                    filled
                    outlined
                    label="Height"
                    v-model="coordinates.height"
                  ></v-text-field>

                  <v-text-field
                    filled
                    outlined
                    label="Top"
                    v-model="coordinates.top"
                  ></v-text-field>
                  <v-text-field
                    filled
                    outlined
                    label="Left"
                    v-model="coordinates.left"
                  ></v-text-field>
                  <v-btn block @click="dialog = false">SET</v-btn>
                </v-col>
              </v-row>
            </v-container>
          </v-dialog>
        </v-card>
      </v-col>
      <v-col cols="12" lg="4">
        <v-expansion-panels focusable>
          <Email />
        </v-expansion-panels>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";

import Panel from "../components/Panel.vue";
import Email from "../components/Email.vue";
export default {
  components: {
    Cropper,
    Panel,
    Email
  },
  data() {
    return {
      dialog: false,
      name: "",
      urls: "",
      spots: "",
      time: "",
      frame: "",
      coordinates: {
        width: "0",
        height: "0",
        top: "0",
        left: "0"
      },
      nameRules: [
        v => !!v || 'Name is required',
        v => (v && v.length >= 2) || 'Name must be more than 2 characters',
      ],
      urlRules: [
        v => !!v || 'Url is required',
        v => /[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/.test(v) || 'Invalid Url'
      ],
      spotRules: [
        v => !!v || 'Spot count is required',
        v => !isNaN(v) || 'Spot count must be number'
      ],
      timeRules: [
        v => !!v || 'Time is required',
        v => /\d\d:\d\d/.test(v) || 'Time must be in format hh:mm'
      ]
    };
  },
  async mounted() {
    await this.$axios
      .get("http://localhost:5000/")
      .then(
        response => (
          (this.name = response.data.name),
          (this.urls = response.data.urls),
          (this.spots = response.data.spots),
          (this.time = response.data.time),
          (this.coordinates.width = response.data.width),
          (this.coordinates.height = response.data.height),
          (this.coordinates.top = response.data.top),
          (this.coordinates.left = response.data.left)
        )
      )
      .catch(error => console.log(error));
  },
  methods: {
    async sendSpotConfig() {
      if (this.$refs.configForm.validate()) {
     let data = {
        name: this.name,
        url: this.urls,
        spots: this.spots,
        time: this.time,
        width: this.coordinates.width,
        height: this.coordinates.height,
        top: this.coordinates.top,
        left: this.coordinates.left
      };
      await this.$axios
        .post("http://localhost:5000/", data)
        .then(response => console.log(response))
        .catch(error => console.log(error));
      }
    },
    captureByVideo() {
      this.dialog = true;
      const video = document.getElementById("video");
      console.log(video);
      const canvas = document.createElement("canvas");
      // scale the canvas accordingly
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      // draw the video at that frame
      canvas
        .getContext("2d")
        .drawImage(video, 0, 0, canvas.width, canvas.height);
      // convert it to a usable data URL
      const dataURL = canvas.toDataURL();
      this.frame = dataURL;
    },
    change({ coordinates, canvas }) {
      console.log(coordinates);
      this.coordinates.width = coordinates.width;
      this.coordinates.height = coordinates.height;
      this.coordinates.top = coordinates.top;
      this.coordinates.left = coordinates.left;
    }
  }
};
</script>
