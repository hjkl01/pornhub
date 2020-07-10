// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       github.com/formateddd/pornhub
// @include      *.pornhub.com/view_video.php?viewkey=*
// @grant        none
// ==/UserScript==



(function() {
    'use strict';

    // Your code here...


    var qualites = [
        "quality_1080p",
        "quality_720p",
        "quality_480p",
        "quality_240p",
    ];

    for (var i in qualites) {
        if (window[qualites[i]]){
            document.querySelector("h1").innerHTML += '<a href=' + window[qualites[i]] + '>' + qualites[i] + '</a>'
            console.info(window.qualites[i]);
            break
        }
    }


})();
