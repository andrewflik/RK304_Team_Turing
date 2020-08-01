(function($) {
"use strict";


//Venobox
$(document).ready(function(){
    $('.portfolio-icon').venobox(); 
});

//Counter up
$('.counter').counterUp({
    delay: 100,
    time: 2000
});
//Testimonial slider2
$('.testimonial-type2-slider').owlCarousel({
    animateOut: 'slideOutDown',
    animateIn: 'flipInX',
    items: 1,
    loop: true,
    margin: 30,
    nav: false,
    autoplay: false,
    autoplayHoverPause: true,
    autoplayTimeout: 4000,
    autoplaySpeed: 1000,
    smartSpeed: 1000,
    dots: true,
    responsiveClass: true
})
//Banner slider
$('.banner-type1-inner-content').owlCarousel({
    animateOut: 'slideOutDown',
    animateIn: 'flipInX',
    items: 1,
    loop: true,
    margin: 30,
    nav: false,
    autoplay: true,
    autoplayHoverPause: true,
    autoplayTimeout: 3000,
    autoplaySpeed: 1000,
    smartSpeed: 1000,
    dots: false,
    responsiveClass: true
})

//Sticky menu
$(window).scroll(function () {
    if ($(this).scrollTop() > 40) {
        $('.navigation-type2').addClass('sticky');
        $('.inner-page .mean-bar').addClass('sticky');
    } else {
        $('.navigation-type2').removeClass('sticky');
        $('.inner-page .mean-bar').removeClass('sticky');
    }
});

//Testimonial slider
$('.testimonial-slider-typ2').owlCarousel({
    loop:true,
    margin:10,
    autoplay: true,
    dots: false,
    autoplaySpeed:2000,
    nav:false,
    responsive:{
        0:{
            items:1
        },
        300:{
            items:1
        },
        600:{
            items:2
        },
        1000:{
            items:2
        }
    }
})

// Initialize MixITUp
$('#portfolio-item-area').mixItUp({
    load: {
         filter: '.all'
    },
    animation: {
        perspectiveDistance: '1000px'
    }
});

//Product quantit y
function productQuantity(){
        $(".up").on('click',function(){
            var this_select = $(this).siblings("input");
            this_select.val(parseInt(this_select.val())+1,10);
        });

        $(".down").on('click',function(){
            var this_select = $(this).siblings("input");
            this_select.val(parseInt(this_select.val())-1,10);
        });
}
productQuantity();
$('a.venoboxinline').on('click',function(){
    setTimeout(productQuantity, 500);   
});

// Google Map
     var googleMapSelector = $('#contactgoogleMap'),
         myCenter = new google.maps.LatLng(40.789886, -74.056700);

     function initialize() {
         var mapProp = {
             center: myCenter,
             zoom: 15,
             scrollwheel: false,
             mapTypeId: google.maps.MapTypeId.ROADMAP,
             styles: [{
                 "featureType": "administrative",
                 "elementType": "labels.text.fill",
                 "stylers": [{
                     "color": "#444"
                 }]
             }, {
                 "featureType": "landscape",
                 "elementType": "all",
                 "stylers": [{
                     "color": "#eee"
                 }]
             }, {
                 "featureType": "poi",
                 "elementType": "all",
                 "stylers": [{
                     "visibility": "off"
                 }]
             }, {
                 "featureType": "road",
                 "elementType": "all",
                 "stylers": [{
                     "saturation": -100
                 }, {
                     "lightness": 45
                 }]
             }, {
                 "featureType": "road.highway",
                 "elementType": "all",
                 "stylers": [{
                     "visibility": "simplified"
                 }]
             }, {
                 "featureType": "road.arterial",
                 "elementType": "labels.icon",
                 "stylers": [{
                     "visibility": "off"
                 }]
             }, {
                 "featureType": "transit",
                 "elementType": "all",
                 "stylers": [{
                     "visibility": "off"
                 }]
             }, {
                 "featureType": "water",
                 "elementType": "all",
                 "stylers": [{
                     "color": "#444"
                 }, {
                     "visibility": "on"
                 }]
             }]
         };
         var map = new google.maps.Map(document.getElementById("contactgoogleMap"), mapProp);
         var marker = new google.maps.Marker({
             position: myCenter,
             animation: google.maps.Animation.BOUNCE,
             icon: 'img/icon/map-icon.png'
         });
         marker.setMap(map);
     }
     if (googleMapSelector.length) {
         google.maps.event.addDomListener(window, 'load', initialize);
     }

 //Mean menu Installing for Mobile Menu
jQuery('nav.mobile-menu').meanmenu({
    meanScreenWidth: "767"
});
//Preloader
jQuery(window).load(function() {
    $('.preloader').fadeOut('slow');
});

})(jQuery);