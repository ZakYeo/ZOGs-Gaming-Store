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
        document.querySelector('#profile-section').hidden = false;
        document.querySelector('#signup-btn').hidden = true;
        document.querySelector('#profile-btn').hidden = false;
        user.getIdToken().then(function (token) {
            // Add the token to the browser's cookies. The server will then be
            // able to verify the token against the API.
            document.cookie = "token=" + token + "; path=/";
            let xhr = new XMLHttpRequest();
            let url = window.location.href.split("store")[0];
            xhr.open("GET", `${url}/admin` );
            xhr.setRequestHeader("Accept", "application/json");
            xhr.setRequestHeader("Content-Type", "application/json");
            
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4) {
                resp = JSON.parse(xhr.responseText);
                    if(resp["administrator"] === 1){
                        document.querySelector('#admin').hidden = false;
                        document.querySelector('#add-game').href = `${window.location.href.split("store")[0]}add`;
                        render_analytics();
                    }
                }};
            xhr.send();
        });

    } else {
        document.querySelector('#logout-btn').hidden = true;
        document.querySelector('#login-btn').hidden = false;
        document.querySelector('#admin').hidden = true;
        document.querySelector('#profile-section').hidden = true;
        document.querySelector('#signup-btn').hidden = false;
        document.querySelector('#profile-btn').hidden = true;
        document.cookie = "token=" + "; path=/";
    }
});

function render_analytics() {
    let xhr = new XMLHttpRequest();
    let url = window.location.href.split("store")[0];
    xhr.open("GET", `${url}/times/10` );
    xhr.setRequestHeader("Accept", "application/json");
    xhr.setRequestHeader("Content-Type", "application/json");
    
    xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
        resp = JSON.parse(xhr.responseText);
        str = "";
        for(let i=0; i< Object.keys(resp).length; i++){
        str += `${resp[i].timestamp}: ${resp[i].email}\n`
        }
        document.querySelector('#logininfo').innerText = str;
        
    }};
    xhr.send();                 
}