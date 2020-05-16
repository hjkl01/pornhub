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


function copy(quality,url){
const input = document.createElement('input');
	document.body.appendChild(input);
 	input.setAttribute('value', url);
	input.select();
	if (document.execCommand('copy')) {
		document.execCommand('copy');
		alert(quality + '复制成功');
	}}


var qualites = [
    "quality_1080p",
    "quality_720p",
    "quality_480p",
    "quality_240p",
];

for (var b in window) {
    if (b.includes("flashvars")) {
        for (var i in qualites) {
            if (window[b][qualites[i]]) {
                copy(qualites[i], window[b][qualites[i]]);
                break;
            }
        }
        break;
    }
}

})();
