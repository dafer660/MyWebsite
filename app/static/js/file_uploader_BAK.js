// $('#image-toggle').popover({
//   trigger: 'focus'
// })
//
// $(function () {
//     $('.image-toggle').popover({
//         container: 'body'
//     })
// })

function filesize(elem){
    document.cookie = `filesize=${elem.files[0].size}`
}

$(document).ready(function () {
    $('form').on('submit', function(event) {

		event.preventDefault();

		var formData = new FormData($('form')[0]);

        $.ajax({
            xhr : function (){
              let xhr = new window.XMLHttpRequest() ;

              xhr.upload.addEventListener('progress', function (ev){
                  if (ev.lengthComputable) {
                      console.log('Bytes: ' + ev.loaded);
                      console.log('Total Size: ' + ev.total);
                      console.log('Percentage Uploaded: ' + (ev.loaded / ev.total))

                      let percent = Math.round((ev.loaded / ev.total) * 100);

                      $('#progressBar').attr('aria-valuenow', percent).css('width', percent + '%').text(percent + '%');
                  }
              });
              return xhr;
            },
            type : 'POST',
            url : '/upload_files',
            data: formData,
            processData: false,
            contentType: false,
            success : function (response) {
                if(response != 0){
                    // console.log(response)
                    $('#image-div').html(response)
                    // $("#img").attr('src', response['image_resp']);
                }else{
                    alert('file not uploaded');
                }
            }
        });
    });
});

