<template>
    <div id="modal-settings">
        <div class="modal is-active">
            <div class="modal-background"></div>
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title">Paramètres</p>
                    <button class="delete has-background-danger"
                        v-on:click="$emit('exitSettingsModal', true)" aria-label="close"></button>
                </header>
                <section class="modal-card-body">
                  <div class="field">
                      <label class="label">Prénom</label>
                      <div class="control">
                          <input class="input" type="text" :placeholder="this.userInfo.first_name"
                              v-model="this.updatedUserInfo.first_name">
                      </div>
                  </div>

                  <div class="field">
                      <label class="label">Nom</label>
                      <div class="control">
                          <input class="input" type="text" :placeholder="this.userInfo.last_name"
                              v-model="this.updatedUserInfo.last_name">
                      </div>
                  </div>
                  <div class="field">
                      <label class="label">Courriel</label>
                      <div class="control">
                          <input class="input" type="email" :placeholder="this.userInfo.email"
                              v-model="this.updatedUserInfo.email">
                      </div>
                  </div>
                  <div class="field">
                      <label class="label">Biographie</label>
                      <div class="control">
                          <textarea class="textarea" :placeholder="this.userInfo.user_bio" v-model="this.updatedUserInfo.user_bio"></textarea>
                      </div>
                  </div>
                  <div class="field">
                      <label class="label">Localisation</label>
                      <div id="map"></div>
                  </div>
                </section>
                <footer class="modal-card-foot is-flex is-justify-content-space-evenly">
                    <button class="button is-success is-rounded w-100" @click="validateUserInfo()">Sauvegarder</button>
                    <button class="button is-danger is-rounded w-100" @click="$emit('exitSettingsModal', true)">Fermer</button>
                </footer>
            </div>
        </div>
    </div>
</template>
<script>
  import axios from "axios";
  import {
    toast
  } from "bulma-toast";
  export default {
    name: "SettingsModal",
    data() {
      return {
        userInfo: {},
        updatedUserInfo: {
          first_name: '',
          last_name: '',
          email: '',
          address: '',
          location_lat: '',
          location_lon: '',
          user_bio:''
        },
      };
    },
    beforeCreate() {
      this.$store.commit("initializeStore");
      const token = this.$store.state.token;
      if (token) {
        axios.defaults.headers.common["Authorization"] = "Token " + token;
      } else {
        axios.defaults.headers.common["Authorization"] = "";
      }
      console.log(token);
    },
    mounted() {
      this.getUserInfo();
      mapboxgl.accessToken = this.MAPBOX_API_KEY;
      this.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11', 
      });

      const geocoder = new MapboxGeocoder({
        accessToken: mapboxgl.accessToken,
        placeholder: 'Chercher une addresse',
        language: 'fr-CA',
        countries: 'ca',
        limit: 3,
        minLength: 3,
        mapboxgl: mapboxgl
      });
      this.map.addControl(geocoder, 'top-left');

      geocoder.on('result', e => {
        this.updateUserLocation(e.result);
      });
    },
    computed: {},
    methods: {
      async getUserInfo(){
        await axios
        .get('api/v1/userinfo/me/')
        .then((response)=>{
          this.userInfo = response.data;
          this.updatedUserInfo.first_name = response.data['first_name'];
          this.updatedUserInfo.last_name = response.data['last_name'];
          this.updatedUserInfo.email = response.data['email'];
          this.updatedUserInfo.address = response.data['address'];
          this.updatedUserInfo.user_bio = response.data['user_bio'];
          if(response.data['location_lat'] && response.data['location_lon']){
            this.homeMarker = new mapboxgl.Marker()
                  .setLngLat([parseFloat(response.data.location_lon), parseFloat(response.data.location_lat)])
                  .addTo(this.map);
            this.map.flyTo({
                center: [parseFloat(response.data.location_lon), parseFloat(response.data.location_lat)],
                essential: true,
                zoom: 13
            });
          }else{
            this.map.flyTo({
                center: [-71.207981, 46.813878],
                essential: true,
                zoom: 9
            });
          }
        })
        .catch((error)=>{
          console.log(error);
        });
      },
      async validateUserInfo(){
        let data = {}
        if(this.updatedUserInfo.first_name != this.userInfo.first_name){
          data.first_name = this.updatedUserInfo.first_name;
        }
        if(this.updatedUserInfo.last_name != this.userInfo.last_name){
          data.last_name = this.updatedUserInfo.last_name;
        }
        if(this.updatedUserInfo.email != this.userInfo.email){
          data.email = this.updatedUserInfo.email;
        }
        if(this.updatedUserInfo.address != this.userInfo.address){
          data.address = this.updatedUserInfo.address;
        }
        if(this.updatedUserInfo.location_lat != this.userInfo.location_lat){
          data.location_lat = this.updatedUserInfo.location_lat;
        }
        if(this.updatedUserInfo.location_lon != this.userInfo.location_lon){
          data.location_lon = this.updatedUserInfo.location_lon;
        }
        if(this.updatedUserInfo.user_bio != this.userInfo.user_bio){
          data.user_bio = this.updatedUserInfo.user_bio;
        }
        if(Object.keys(data).length != 0){
          await axios
          .put('api/v1/userinfo/me/update/', data)
          .then((response)=>{
            this.userInfo = response.data;
            toast({
              message: "Informations sauvegardées avec succès!",
              type: "is-success",
              dismissible: true,
              pauseOnHover: false,
              duration: 3000,
              position: "bottom-right",
              animate: {
                in: "fadeInRightBig",
                out: "fadeOutRightBig",
              },
            });

            if(response.data.location_lon && response.data.location_lon){
              if(this.homeMarker){
                this.homeMarker.remove();
              }
              this.homeMarker = new mapboxgl.Marker()
              .setLngLat([parseFloat(response.data.location_lon), parseFloat(response.data.location_lat)])
              .addTo(this.map);
            }else{
              if(this.homeMarker){
                this.homeMarker.remove();
              }
              this.map.flyTo({
                center: [-71.207981, 46.813878],
                essential: true,
                zoom: 9
              });
            }
          })
          .catch((error)=>{
            console.log(error);
            toast({
              message: "Une erreur est survenue...",
              type: "is-danger",
              dismissible: false,
              pauseOnHover: false,
              duration: 3000,
              position: "bottom-right",
              animate: {
                in: "fadeInRightBig",
                out: "fadeOutRightBig",
              },
            });
          });
        }else{
          toast({
            message: "Informations sauvegardées avec succès!",
            type: "is-success",
            dismissible: true,
            pauseOnHover: false,
            duration: 3000,
            position: "bottom-right",
            animate: {
              in: "fadeInRightBig",
              out: "fadeOutRightBig",
            },
          });
        }
      },
      updateUserLocation(result){
        this.updatedUserInfo.address = result.place_name;
        this.updatedUserInfo.location_lon = result.center[0].toFixed(6);
        this.updatedUserInfo.location_lat = result.center[1].toFixed(6);
      }
    },
  };
</script>
<style scoped>
  #map{
    height: 300px;
    width: 100%;
    border-radius: 5px;
  }
</style>