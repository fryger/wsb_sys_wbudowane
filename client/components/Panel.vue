<template>
  <v-expansion-panel>
    <v-expansion-panel-header>ADD Spot</v-expansion-panel-header>
    <v-expansion-panel-content>
      <v-row>
        <v-col cols="12" lg="6">
          <video
            v-if="!captureSwitch"
            id="video"
            controls="controls"
            crossorigin="anonymous"
            style="width:100%"
            :key="urls"
          >
            <source :src="urls" />
          </video>
          <v-container fluid>
          <img id="pic" crossorigin="anonymous" :src="urls">
          </v-container>
          <v-switch v-model="captureSwitch"></v-switch>
        </v-col>

        <v-col cols="12" lg="6">
          <v-text-field v-model="url" label="Stream URL"></v-text-field>
          <v-dialog v-model="dialog" max-width="800px">
            <v-container fluid class="pa-12">
              <cropper
                class="cropper"
                :src="frame"
                @change="change"
                style="width:100%;"
              />
            </v-container>
            <v-row>
              <v-col cols="12" lg="2"
                ><v-text-field
                  label="Width"
                  v-model="coordinates.width"
                ></v-text-field
              ></v-col>
              <v-col cols="12" lg="2"
                ><v-text-field
                  label="Height"
                  v-model="coordinates.height"
                ></v-text-field
              ></v-col>
              <v-col cols="12" lg="2">
                <v-text-field
                  label="Top"
                  v-model="coordinates.top"
                ></v-text-field
              ></v-col>
              <v-col cols="12" lg="2"
                ><v-text-field
                  label="Left"
                  v-model="coordinates.left"
                ></v-text-field
              ></v-col>
            </v-row>

            <v-btn @click="dialog = false">SET</v-btn>
          </v-dialog>
          <v-btn @click="changeImg">Change img</v-btn>
          <v-btn  @click="captureImg">Capture area</v-btn>
          <v-btn  @click="captureImgs">Capture area img</v-btn>
          <v-text-field
            v-model="spots"
            label="Number of parking spots"
          ></v-text-field>
          <v-btn @click="sendData" block color="success">Send</v-btn>
        </v-col>
      </v-row>
    </v-expansion-panel-content>
  </v-expansion-panel>
</template>

<script>
import { Cropper } from "vue-advanced-cropper";
import "vue-advanced-cropper/dist/style.css";

export default {
  components: {
    Cropper
  },
  name: "Panel",
  props: [],
  data() {
    return {
      dialog: false,
      captureSwitch: false,
      coordinates: {
        width: "",
        height: "",
        top: "",
        left: ""
      },
      urls: "https://imageserver.webcamera.pl/rec/lanckorona/latest.mp4",
      url: "",
      frame: "",
      spots: ""
    };
  },
  methods: {
    captureImgs() {
      this.dialog = true;
      const img = document.getElementById("pic");
      const cvs = document.createElement("canvas");
      cvs.width = img.width;
      cvs.height = img.height;
      cvs.getContext("2d").drawImage(img, 0,0);

      
      const dataUri = cvs.toDataURL();
      console.log(dataUri)
      this.frame = dataUri;
    },
    captureImg() {
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
      console.log(dataURL);
    },
    changeImg() {
      this.urls = this.url;
    },
    change({ coordinates, canvas }) {
      console.log(coordinates);
      this.coordinates.width = coordinates.width;
      this.coordinates.height = coordinates.height;
      this.coordinates.top = coordinates.top;
      this.coordinates.left = coordinates.left;
    },
    async sendData() {
      let data = {
        name: "Reda - przód",
        time: "10:30",
        url: this.urls,
        width: this.coordinates.width,
        height: this.coordinates.height,
        left: this.coordinates.left,
        top: this.coordinates.top,
        spots: this.spots
      };
      await this.$axios
        .post("http://localhost:5000/", data)
        .then(res => console.log(res))
        .catch(error => {
          console.log(error.response);
        });
    }
  }
};
</script>


<style scoped>

</style>