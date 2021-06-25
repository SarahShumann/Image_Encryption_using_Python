firebase.auth().onAuthStateChanged((user)=>{
if (user) {
    let user = firebase.auth().currentUser;
var storage = firebase.storage();
      var storageRef = storage.ref();
      $('#List').find('tbody').html('');

      var i = 0;
      storageRef.child('users/'+user.uid).listAll().then(function(result){
        result.items.forEach(function(imageRef){
          i++;
          displayImage(i, imageRef);
        });
      });

      function displayImage(row, images){

        images.getDownloadURL().then(function(url){
          console.log(url);

          let new_html = '';
          new_html += '<tr>';
          new_html += '<td>';
          new_html += '<img src=" '+url+' " width="100px" style="float:left"> ';
          new_html += '</td>';
          new_html += '</tr>';
          $('#List').find('tbody').append(new_html);
        })
      }

    }

});