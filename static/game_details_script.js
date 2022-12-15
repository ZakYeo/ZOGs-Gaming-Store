const firebaseConfig = {
  apiKey: "AIzaSyAopZxjnk3TnQMPg9NUouUvC6aIsvtDCyo",
  authDomain: "ad-2021-03.firebaseapp.com",
  projectId: "ad-2021-03",
  storageBucket: "ad-2021-03.appspot.com",
  messagingSenderId: "243759511961",
  appId: "1:243759511961:web:8e19eab1cbf743c9d27b08",
  measurementId: "G-FKJT5126NC"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.analytics();



const CLOUD_NAME = "dhujezr6s";
const UPLOAD_PRESET = "p0rdbkxh";
let originalTitle = document.querySelector('#gametitle').innerText;
let originalDesc = document.querySelector('#gamedesc').innerText;
let originalPrice = document.querySelector('#gameprice').innerText;
const auth = firebase.auth();


const logoutBtn = document.querySelector('#logout-btn');
logoutBtn.addEventListener('click', e => {
  e.preventDefault();
  auth.signOut();
})


auth.onAuthStateChanged(user => {
  if (user) {
    document.querySelector('#logout-btn').hidden = false;
    document.querySelector('#login-btn').hidden = true;
    document.querySelector('#signup-btn').hidden = true;
    document.querySelector('#profile-section').hidden = false;
    user.getIdToken().then(function (token) {
      // Add the token to the browser's cookies. The server will then be
      // able to verify the token against the API.
      document.cookie = "token=" + token + "; path=/";
      enable_edit();
      document.querySelector('#purchase-game').hidden = false;
    });
  } else {
    document.querySelector('#logout-btn').hidden = true;
    document.querySelector('#login-btn').hidden = false;
    document.querySelector('#signup-btn').hidden = false;
    document.cookie = "token=" + "; path=/";
    document.querySelector('#gametitle').contentEditable = false;
    document.querySelector('#gamedesc').contentEditable = false;
    document.querySelector('#gameprice').contentEditable = false;
    document.querySelector('#upload').hidden = true;
    document.getElementById("remove-game").hidden = true;
    document.querySelector('#purchase-game').hidden = true;
    document.querySelector('#profile-section').hidden = true;
  }
});


const myWidget = cloudinary.createUploadWidget(
  {
    cloudName: CLOUD_NAME,
    uploadPreset: UPLOAD_PRESET,
    multiple: false,  //restrict upload to a single file
  },
  (error, result) => {
    if (!error && result && result.event === "success") {
      document
        .getElementById("uploadedimage")
        .setAttribute("src", result.info.secure_url);

      send_post_request("image", result.info.secure_url);
    }
  }
);

document.getElementById("upload").addEventListener(
  "click",
  function () {
    myWidget.open();
  },
  false
);

document.getElementById("gametitle").addEventListener('blur', (event) => {
  if( event.srcElement.innerText != originalTitle){
    send_post_request("name", event.srcElement.innerText);
  }
});
document.getElementById("gameprice").addEventListener('blur', (event) => {
  if( event.srcElement.innerText != originalPrice){
    send_post_request("price", event.srcElement.innerText);
  }
});
document.getElementById("gamedesc").addEventListener('blur', (event) => {
  if( event.srcElement.innerText != originalDesc){
    send_post_request("desc_long", event.srcElement.innerText);
  }
});

document.getElementById("remove-game").addEventListener('click', () => {
  const url = `${window.location.href}delete/`;
  let xhr = new XMLHttpRequest();
  xhr.open("POST", url );
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
  if (xhr.readyState === 4) {
      alert(xhr.responseText);
      location.reload();
  }};
  xhr.send();
});



function send_post_request(new_key, new_value) {
  let xhr = new XMLHttpRequest();
  let id = window.location.href.split("/")[4];
  const url = `${window.location.href}/update/`;
  xhr.open("POST", url );
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
        alert(xhr.responseText);
    }};
  xhr.send(`
    {"filter_key": "id_",
    "filter_value": ${id}, 
    "new_key": "${new_key}", 
    "new_value": "${new_value}"}`
  );
}

function enable_edit(){
  let xhr = new XMLHttpRequest();
  let url = window.location.href.split("store")[0];
  xhr.open("GET", `${url}/admin` );
  xhr.setRequestHeader("Accept", "application/json");
  xhr.setRequestHeader("Content-Type", "application/json");
  
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      resp = JSON.parse(xhr.responseText);
        if(resp["administrator"] === 1){
          document.querySelector('#gametitle').contentEditable = true;
              document.querySelector('#gamedesc').contentEditable = true;
              document.querySelector('#gameprice').contentEditable = true;
              document.querySelector('#upload').hidden = false;
              document.getElementById("remove-game").hidden = false;
        }
    }};
    xhr.send();
}