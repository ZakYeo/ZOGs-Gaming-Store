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
        user.getIdToken().then(function (token) {
            // Add the token to the browser's cookies. The server will then be
            // able to verify the token against the API.
            document.cookie = "token=" + token + "; path=/";
        });

    } else {
        document.querySelector('#logout-btn').hidden = true;
        document.querySelector('#login-btn').hidden = false;
        document.querySelector('#profile-section').hidden = true;
        document.cookie = "token=" + "; path=/";
    }
});
