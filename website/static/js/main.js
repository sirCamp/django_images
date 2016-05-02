/**
 * Created by stefano on 02/05/16.
 */

    window.fbAsyncInit = function() {
        FB.init({
          appId      : '855735074546415',
          xfbml      : true,
          version    : 'v2.5'
        });
      };

      (function(d, s, id){
         var js, fjs = d.getElementsByTagName(s)[0];
         if (d.getElementById(id)) {return;}
         js = d.createElement(s); js.id = id;
         js.src = "//connect.facebook.net/en_US/sdk.js";
         fjs.parentNode.insertBefore(js, fjs);
       }(document, 'script', 'facebook-jssdk'));

jQuery(document).ready(function(){
    
      jQuery('#share').on('click',function() {

          jQuery('#loader').show();
          jQuery('#share').hide();
          jQuery.ajax({

              url: '/post/',
              dataType: "json",
              method: 'GET',

              success: function (data) {

                  jQuery('#loader').hide();
                  jQuery('#share').show();
                  FB.ui({
                    method: 'share_open_graph',
                    action_type: 'og.shares',
                    action_properties: JSON.stringify({
                        object : {
                           'og:url': data.server,
                           'og:title': data.title,
                           'og:description': data.message,
                           'og:og:image:width': '400',
                           'og:image:height': '300',
                           'og:image': data.url
                        }
                    })
                  });

              },
              error: function(){

                  jQuery('#loader').hide();
                  jQuery('#share').show();
                  alert('Something wrong')
              }
      });

      });


})
