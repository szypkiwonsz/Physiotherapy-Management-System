// Wrap every letter in a span
var textWrapper = document.querySelector('.ml13');
textWrapper.innerHTML = textWrapper.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml13 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 300 + 30 * i
    });
// Wrap every letter in a span
var textWrapper2 = document.querySelector('.ml14');
textWrapper2.innerHTML = textWrapper2.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml14 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 1000 + 30 * i
    });
var textWrapper3 = document.querySelector('.ml15');
textWrapper3.innerHTML = textWrapper3.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml15 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 1000 + 30 * i
    });
var textWrapper4 = document.querySelector('.ml16');
textWrapper4.innerHTML = textWrapper4.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml16 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 1700 + 30 * i
    });
var textWrapper5 = document.querySelector('.ml17');
textWrapper5.innerHTML = textWrapper5.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml17 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 1700 + 30 * i
    });
var textWrapper6 = document.querySelector('.ml18');
textWrapper6.innerHTML = textWrapper6.textContent.replace(/\S/g, "<span class='letter'>$&</span>");

anime.timeline({loop: false})
    .add({
        targets: '.ml18 .letter',
        translateY: [100, 0],
        translateZ: 0,
        opacity: [0, 1],
        easing: "easeOutExpo",
        duration: 1400,
        delay: (el, i) => 2400 + 30 * i
    });