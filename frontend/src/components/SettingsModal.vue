<template>
    <div id="modal-settings">
        <div class="modal is-active">
            <div class="modal-background" @click="$emit('exitSettingsModal', true)"></div>
            <div class="modal-card">
                <header class="modal-card-head">
                    <p class="modal-card-title">Paramètres</p>
                    <button class="delete has-background-danger"
                        v-on:click="$emit('exitSettingsModal', true)" aria-label="close"></button>
                </header>
                <section class="modal-card-body">
                  <div class="tabs">
                    <ul>
                      <li :class="currentTab == 0 ? 'is-active' : ''" @click="currentTab = 0">
                        <a>
                          <span class="icon is-small"><i class="fas fa-user-circle" aria-hidden="true"></i></span>
                          <span>Indentification</span>
                        </a>
                      </li>
                      <li :class="currentTab == 1 ? 'is-active' : ''" @click="currentTab = 1">
                        <a>
                          <span class="icon is-small"><i class="fas fa-map-marker-alt" aria-hidden="true"></i></span>
                          <span>Localisation</span>
                        </a>
                      </li>
                    </ul>
                  </div>
                  <div class="tab-content" :class="currentTab == 0 ? 'is-active' : ''">
                    <div class="columns">
                      <div class="column is-one-third">
                        <label class="label">Photo de profil</label>
                        <figure class="image round-shadow has-image-centered is-128x128 mt-4">
                          <img
                            id="profile-image"
                            class="is-rounded"
                            :src="userImageURL" 
							              @error="replaceByDefault"
                          />
                        </figure>
                            <span v-if="!this.isValidPictureProfile" class="icon is-info tooltip">
                            <i class="fas fa-exclamation-circle has-text-danger"></i>
                            <span class="tooltiptext has-background-danger">
                            Type de fichier invalide. Formats acceptés: .jpg, .jpeg, .png.
                            </span>
                          </span>
                        <div class="file is-centered mt-5">
                          <label class="file-label">
                            <input class="file-input" type="file" name="profile_picture" @change="onImageSelected" accept=".jpg, .jpeg, .png"
                            @input="validateImage(this.selectedImageFile)">
                            <span class="file-cta">
                              <span class="file-icon">
                                <i class="fas fa-upload"></i>
                              </span>
                              <span class="file-label">
                                Choisir une photo
                              </span>
                            </span>
                          </label>
                        </div>
                      </div>
                      <div class="column">
                        <div class="columns">
                          <div class="column">
                            <div class="field">
                                <label class="label">Prénom</label>
                                <div class="control">
                                    <input class="input" type="text" :class="!this.validations['isValidFirstName'] ? 'is-danger': ''" :placeholder="this.userInfo.first_name"
                                        v-model="this.updatedUserInfo.first_name"
                                        @input="validateFirstName">
                                        <span v-if="!this.validations['isValidFirstName']" class="icon is-info tooltip">
                                        <i class="fas fa-exclamation-circle has-text-danger"></i>
                                        <span class="tooltiptext has-background-danger">
                                         Le prénom peut être composé de lettres, d'espaces ou du caractère '-'.
                                        </span>
                                      </span>
                                </div>
                            </div>
                          </div>
                          <div class="column">
                            <div class="field">
                                <label class="label">Nom</label>
                                <div class="control">
                                    <input class="input" type="text" :class="!this.validations['isValidLastName'] ? 'is-danger': ''" :placeholder="this.userInfo.last_name"
                                        v-model="this.updatedUserInfo.last_name"
                                        @input="validateLastName">
                                        <span v-if="!this.validations['isValidLastName']"  class="icon is-info tooltip">
                                        <i class="fas fa-exclamation-circle has-text-danger"></i>
                                        <span class="tooltiptext has-background-danger">
                                         Le prénom peut être composé de lettres, d'espaces ou du caractère '-'.
                                        </span>
                                      </span>
                                </div>
                            </div>
                          </div>
                        </div>

                        <div class="field">
                            <label class="label">Courriel</label>
                            <div class="control">
                                <input class="input" type="email" :class="!this.validations['isValidEmail'] ? 'is-danger': ''"  :placeholder="this.userInfo.email"
                                    v-model="this.updatedUserInfo.email"
                                    @input="validateEmail">
                                      <span v-if="!this.validations['isValidEmail']"  class="icon is-info tooltip">
                                      <i class="fas fa-exclamation-circle has-text-danger"></i>
                                      <span class="tooltiptext has-background-danger">
                                        Le format de l'adresse n'est pas valide.
                                      </span>
                                    </span>
                            </div>
                        </div>

                        <div class="field">
                          <label class="label">Biographie</label>
                          <div class="control">
                              <textarea class="textarea" :placeholder="this.userInfo.user_bio" v-model="this.updatedUserInfo.user_bio"></textarea>
                          </div>
                        </div>
                      </div>
                    </div>

                  </div>
                  <div class="tab-content" :class="currentTab == 1 ? 'is-active' : ''">
                    <div class="field">
                        <label class="label">Localisation</label>
                        <div id="map"></div>
                    </div>
                  </div>
                </section>
                <footer class="modal-card-foot is-flex is-justify-content-space-evenly">
                    <button class="button is-success is-rounded w-200" @click="validateUserInfo()">Sauvegarder</button>
                    <button class="button is-danger is-rounded w-200" @click="$emit('exitSettingsModal', true)">Fermer</button>
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
        currentTab: 0,
        selectedImageFile: null,
        fileErrors : [],
        userImageURL : '',
        validations:{
          isValidFirstName:true,
          isValidLastName:true,
          isValidEmail:true
        },
        isValidPictureProfile:true
      };
    },
    beforeCreate() {},
    mounted() {
      this.getUserInfo();
      mapboxgl.accessToken = this.MAPBOX_API_KEY;
      this.map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
      });
      const ro = new ResizeObserver(() => {
        if (this.map) {
          this.map.resize();
        }
      });

      // Observe the map div container.
      ro.observe(document.getElementById('map'));
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
          this.updatedUserInfo.location_lat = response.data['location_lat'];
          this.updatedUserInfo.location_lon = response.data['location_lon'];
          this.userImageURL = this.MEDIA_URL + 'pfp_' + this.userInfo.user_id + '.jpg'
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
      validateFirstName(){
        let regexName = new RegExp(/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð\-\s]{2,15}$/);
        this.updatedUserInfo.first_name
         if (!regexName.test(this.updatedUserInfo.first_name)){
          this.validations['isValidFirstName']=false;
        }else this.validations['isValidFirstName']=true;
      },
      validateLastName(){
        let regexName = new RegExp(/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð\-\s]{2,15}$/);
        this.updatedUserInfo.last_name
        if (!regexName.test(this.updatedUserInfo.last_name)){
          this.validations['isValidLastName']=false;
        }else this.validations['isValidLastName']=true; 
      },
      validateEmail(){
        let regexEmail = RegExp(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/);
        if (!regexEmail.test(this.updatedUserInfo.email)){
           this.validations['isValidEmail']=false;
        }else this.validations['isValidEmail']=true;
      },
      /**
       * Vérifications supplémentaires sur tous les champs.
       */
      validateForm(){
        
       let regexName = new RegExp(/^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð\-\s]{2,15}$/);
       let regexEmail = RegExp(/^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/);

        if (!regexName.test(this.updatedUserInfo.first_name)){
          this.validations['isValidFirstName']=false;
        }else this.validations['isValidFirstName']=true;

        if (!regexName.test(this.updatedUserInfo.last_name)){
          this.validations['isValidLastName']=false;
        }else this.validations['isValidLastName']=true;

         if (!regexEmail.test(this.updatedUserInfo.email)){
           this.validations['isValidEmail']=false;
        }else this.validations['isValidEmail']=true;

        console.log("this.validations['isValidFirstName'] : "+this.validations['isValidFirstName']);
        console.log(" this.validations['isValidLastName'] : "+this.validations['isValidLastName']);
        console.log("this.validations['isValidEmail'] :"+this.validations['isValidEmail'] );

        return this.validations['isValidFirstName'] && this.validations['isValidLastName']  && this.validations['isValidEmail'];
      }
      ,
      async validateUserInfo(){

      if (!this.validateForm()){
        return;
      }
 
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

            //Mise à jour du userInfo dans le store.
            this.$store.dispatch("changeUserInfo", this.userInfo);

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
        if(this.selectedImageFile){
          this.uploadProfileImage();
        }
      },
      updateUserLocation(result){
        this.updatedUserInfo.address = result.place_name;
        this.updatedUserInfo.location_lon = result.center[0].toFixed(6);
        this.updatedUserInfo.location_lat = result.center[1].toFixed(6);
      },
      onImageSelected(event){
        this.selectedImageFile = event.target.files[0];
        var img = document.getElementById('profile-image');
        const reader = new FileReader();
        reader.addEventListener('load', (event) => {
          img.src = event.target.result;
        });
        reader.readAsDataURL(this.selectedImageFile);
      },
      async uploadProfileImage(){        
        if (this.validateImage(this.selectedImageFile)) {
          const fd = new FormData();
          fd.append('image', this.selectedImageFile);
          let config = {
            headers: {
            'Content-Type': 'multipart/form-data'
            }
          }
          await axios
          .post("api/v1/userinfo/me/profile-image/",fd , config)
          .then((response)=>{
            // Set new image 
            this.isValidPictureProfile=true;
          })
          .catch((error) =>{
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
       
          this.isValidPictureProfile=false;
        }
      },
      validateImage(file){
        if (file){
        const fileType = file['type'];
        const validImageTypes = ['image/jpeg', 'image/png'];
        return validImageTypes.includes(fileType) && file.size<1048576;
        }
      },
      replaceByDefault(e){
			  e.target.src = this.MEDIA_URL + 'pfp_default.jpg';
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
  #profile-image{
    height: 128px;
    width: 128px;
    object-fit: cover;
  }
  .tab-content{
    display: none;
  }
  .tab-content.is-active {
    display: block;
  }
  .modal-card-body{
    min-height: 434px!important;
  }
  .tooltip {
	position: relative;
	float: right;
}

.tooltip .tooltiptext {
	visibility: hidden;
	width: 200px;
	color: #fff;
	text-align: center;
	border-radius: 6px;
	padding: 5px 0;
	position: absolute;
	z-index: 10;
	top: 100%;
	right: 0;
	margin-left: -200px;
}

.tooltip:hover .tooltiptext {
  	visibility: visible;
}
</style>